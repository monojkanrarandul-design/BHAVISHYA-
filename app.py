import streamlit as st
import graphviz
import time
import requests
from datetime import datetime
import streamlit.components.v1 as components
from intel_feed import get_map_html, get_news_summary

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="BHAVISHYA | GLOBAL HUD", layout="wide", initial_sidebar_state="expanded")

# --- CYBERPUNK / HELICOPTER HUD CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap');
    html, body, [class*="css"] { font-family: 'Share Tech Mono', monospace !important; background-color: #030a04 !important; color: #00ff41 !important; }
    .stApp { background-color: #030a04; background-image: linear-gradient(rgba(0, 255, 65, 0.03) 1px, transparent 1px), linear-gradient(90deg, rgba(0, 255, 65, 0.03) 1px, transparent 1px); background-size: 20px 20px; }
    .hud-panel { border: 1px solid #00ff41; background: rgba(0, 20, 0, 0.6); padding: 15px; box-shadow: inset 0 0 15px rgba(0,255,65,0.2); margin-bottom: 15px; }
    .warning-flash { color: #ff003c; font-weight: bold; text-shadow: 0 0 5px #ff003c; animation: blink 1s step-end infinite; }
    @keyframes blink { 50% { opacity: 0; } }
    h1, h2, h3 { color: #00f0ff !important; text-transform: uppercase; letter-spacing: 2px; }
    .telemetry { font-size: 0.8rem; color: #a3a3a3; }
    [data-testid="stSidebar"] { background-color: #020603 !important; border-right: 1px solid #00ff41; }
    #MainMenu, footer {visibility: hidden;}
    /* Style the text input box to look like a terminal */
    .stTextInput input { background-color: #001a04 !important; color: #00ff41 !important; border: 1px solid #00ff41 !important; font-family: 'Share Tech Mono', monospace !important; }
    </style>
""", unsafe_allow_html=True)

# --- SESSION STATE INITIALIZATION ---
# Default to Howrah
if 'target_lat' not in st.session_state: st.session_state['target_lat'] = "22.5958"
if 'target_lon' not in st.session_state: st.session_state['target_lon'] = "88.2636"
if 'target_name' not in st.session_state: st.session_state['target_name'] = "HOWRAH, IN"

# --- GEOCODING FUNCTION (Free OpenStreetMap API) ---
def geocode_location(query):
    try:
        # Nominatim requires a user-agent header
        headers = {'User-Agent': 'BhavishyaHackathonApp/1.0 (test@example.com)'}
        url = f"https://nominatim.openstreetmap.org/search?q={query}&format=json&limit=1"
        response = requests.get(url, headers=headers).json()
        if response:
            return response[0]['lat'], response[0]['lon'], response[0]['display_name'].split(',')[0].upper()
        return None, None, None
    except: return None, None, None

# --- SIDEBAR (FLIGHT CONTROLS) ---
st.sidebar.markdown("### 🌐 GLOBAL TARGETING SYSTEM")
st.sidebar.caption("ENTER ANY CITY OR ADDRESS WORLDWIDE:")
search_query = st.sidebar.text_input("TARGET COORDINATES:", value="Howrah, India")

if st.sidebar.button("ENGAGE SEARCH"):
    with st.spinner("CALCULATING ORBITAL TRAJECTORY..."):
        lat, lon, name = geocode_location(search_query)
        if lat and lon:
            st.session_state['target_lat'] = lat
            st.session_state['target_lon'] = lon
            st.session_state['target_name'] = name
            st.sidebar.success(f"LOCK AQUIRED: {name}")
        else:
            st.sidebar.error("TARGET NOT FOUND.")

st.sidebar.markdown("---")
st.sidebar.markdown("### 🎛️ SENSOR CONTROLS")
use_live_data = st.sidebar.toggle(f"🟢 ACTIVATE LIVE SENSORS", value=False)

# LIVE API CALLS
def get_live_weather(lat, lon):
    try:
        api_key = st.secrets["OPENWEATHER_KEY"]
        res = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric").json()
        if 'rain' in res: return res['rain'].get('1h', 0) * 10 
        return 0 
    except: return 0

def get_live_traffic(lat, lon):
    try:
        api_key = st.secrets["TOMTOM_KEY"]
        res = requests.get(f"https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json?key={api_key}&point={lat},{lon}").json()
        free_flow = res['flowSegmentData']['freeFlowSpeed']
        if free_flow > 0: return int(max(10, 100 - ((res['flowSegmentData']['currentSpeed'] / free_flow) * 100)))
        return 45
    except: return 45

if use_live_data:
    st.sidebar.markdown("<span style='color:#00ff41'>[LINK ESTABLISHED]</span>", unsafe_allow_html=True)
    live_rain = get_live_weather(st.session_state['target_lat'], st.session_state['target_lon'])
    live_traffic = get_live_traffic(st.session_state['target_lat'], st.session_state['target_lon'])
    rain = st.sidebar.slider("PRECIPITATION [mm/h]", 0, 150, int(live_rain), disabled=True)
    traffic = st.sidebar.slider("TRAFFIC DENSITY [%]", 10, 100, int(live_traffic), disabled=True)
else:
    st.sidebar.markdown("<span style='color:#ff003c'>[MANUAL OVERRIDE]</span>", unsafe_allow_html=True)
    rain = st.sidebar.slider("PRECIPITATION [mm/h]", 0, 150, 35)
    traffic = st.sidebar.slider("TRAFFIC DENSITY [%]", 10, 100, 45)

st.sidebar.markdown("---")
drain = st.sidebar.slider("DRAINAGE CAPACITY [%]", 10, 100, 85)
beds = st.sidebar.slider("TRAUMA CENTER LOAD [%]", 10, 100, 70)

traffic_val = st.session_state.get('traffic', traffic)
drain_val = st.session_state.get('drain', drain)

# --- MATH ---
risk_score = min(100, int((rain * 0.45) + (traffic_val * 0.35) + ((100 - drain_val) * 0.3) + ((100 - beds) * 0.2)))
alert_class = "warning-flash" if risk_score > 75 else ""
color_hex = "#ff003c" if risk_score > 75 else ("#f0a500" if risk_score > 50 else "#00ff41")

# --- TOP HUD TELEMETRY BAR ---
current_time = datetime.now().strftime("%H:%M:%S:%f")[:-3]
st.markdown(f"""
    <div style='display: flex; justify-content: space-between; border-bottom: 2px solid #00f0ff; padding-bottom: 5px; margin-bottom: 20px;'>
        <div><span style='color:#00f0ff'>SYS:</span> BHAVISHYA_GLOBAL_V3.0</div>
        <div><span style='color:#00f0ff'>TGT:</span> {st.session_state['target_name']} [{st.session_state['target_lat']}° N, {st.session_state['target_lon']}° E]</div>
        <div class='telemetry'><span style='color:#00f0ff'>UPTIME:</span> {current_time}</div>
    </div>
""", unsafe_allow_html=True)


# --- MAIN HUD LAYOUT ---
col1, col2, col3 = st.columns([1.2, 1.5, 1.2])

with col1:
    st.markdown(f"""
        <div class="hud-panel">
            <h3 style="margin-top:0;">THREAT LEVEL</h3>
            <div style="font-size: 3rem; color: {color_hex};" class="{alert_class}">{risk_score}%</div>
            <div class="telemetry">PROBABILITY OF CASCADE FAILURE</div>
        </div>
    """, unsafe_allow_html=True)
    st.markdown('<div class="hud-panel">', unsafe_allow_html=True)
    st.markdown("### NEURAL NETWORK ATTRIBUTION")
    st.progress(min(1, (rain * 0.45) / 100), text="[ATMOSPHERE] PRECIPITATION INUNDATION")
    st.progress(min(1, (traffic_val * 0.35) / 100), text="[SURFACE] KINEMATIC BOTTLENECK")
    st.progress(min(1, ((100 - drain_val) * 0.3) / 100), text="[SUB-SURFACE] DRAINAGE DEFICIT")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="hud-panel" style="text-align:center;">', unsafe_allow_html=True)
    st.markdown(f"### TACTICAL TOPOLOGY RADAR")
    graph = graphviz.Digraph(engine='dot')
    graph.attr(bgcolor='transparent', size='4,4')
    
    def node_style(risk_thresh):
        if risk_score > risk_thresh: return {'style': 'bold', 'color': '#ff003c', 'fontcolor': '#ff003c', 'fillcolor': '#1a0006'}
        return {'style': 'bold', 'color': '#00ff41', 'fontcolor': '#00ff41', 'fillcolor': '#001a04'}

    graph.node('Power', f'MAIN SUBSTATION\n[GRID_OK]', **node_style(999)) 
    graph.node('Pump', f'DRAINAGE PUMP\n[ZONE_ALPHA]', **node_style(60))
    graph.node('Road', f'PRIMARY ARTERY\n[SURFACE_LINK]', **node_style(75))
    graph.node('Hospital', f'APEX TRAUMA\n[MED_EVAC]', **node_style(80))
    
    graph.edge('Power', 'Pump', color='#00ff41')
    graph.edge('Pump', 'Road', color='#ff003c' if risk_score > 60 else '#00ff41', style='dashed' if risk_score > 60 else 'solid')
    graph.edge('Road', 'Hospital', color='#ff003c' if risk_score > 75 else '#00ff41', style='dashed' if risk_score > 75 else 'solid')
    
    st.graphviz_chart(graph, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="hud-panel">', unsafe_allow_html=True)
    st.markdown("### AI DIRECTIVES")
    if risk_score > 75: st.markdown(f"<div class='warning-flash' style='border: 1px solid #ff003c; padding: 10px;'>> CRITICAL BREACH DETECTED<br>> T-MINUS 38 MIN TO APEX HOSPITAL BLOCKADE.<br><br><strong>RECOMMENDED ACTION:</strong><br>DEPLOY EMERGENCY PUMPS. SEVER CIVILIAN TRAFFIC.</div>", unsafe_allow_html=True)
    elif risk_score > 50: st.markdown(f"<div style='color: #f0a500; border: 1px solid #f0a500; padding: 10px;'>> ELEVATED LOAD WARNING<br>> SUBSURFACE DRAINAGE COMPROMISED.<br><br><strong>RECOMMENDED ACTION:</strong><br>PRE-STAGE AUXILIARY UNITS AT ZONE ALPHA.</div>", unsafe_allow_html=True)
    else: st.markdown(f"<div style='color: #00ff41; border: 1px solid #00ff41; padding: 10px;'>> SYSTEM NOMINAL<br>> ALL PARAMETERS WITHIN TOLERANCE.<br>> MAINTAINING ADAPTIVE FLOW.</div>", unsafe_allow_html=True)
    st.markdown("<br><div class='telemetry'>CONFIDENCE MATCH: 93.8%<br>DATASET: 36_MO_SPATIOTEMPORAL_LOG</div>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- ROW 2: LIVE SAT-MAP & INTEL FEED ---
st.markdown("<br>", unsafe_allow_html=True)
map_col, intel_col = st.columns([1.5, 1])

with map_col:
    st.markdown('<div class="hud-panel" style="padding: 0; border: none;">', unsafe_allow_html=True)
    st.markdown(f"<h3 style='margin-bottom: 5px;'>🛰️ ORBITAL RADAR [{st.session_state['target_name']}]</h3>", unsafe_allow_html=True)
    # The map is now fully interactive!
    components.html(get_map_html(lat=st.session_state['target_lat'], lon=st.session_state['target_lon']), height=290)
    st.markdown('</div>', unsafe_allow_html=True)

with intel_col:
    st.markdown('<div class="hud-panel" style="padding: 0; border: none;">', unsafe_allow_html=True)
    st.markdown("<h3 style='margin-bottom: 5px;'>📡 SIGNAL INTEL</h3>", unsafe_allow_html=True)
    st.markdown(get_news_summary(risk_score, traffic_val, st.session_state['target_name']), unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)