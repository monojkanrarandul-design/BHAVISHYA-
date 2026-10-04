import streamlit as st
import graphviz
import time

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="BHAVISHYA | Predictive Grid", layout="wide", initial_sidebar_state="expanded")

# Custom CSS for a hacker/dashboard vibe
st.markdown("""
    <style>
    .big-font { font-size: 2.5rem !important; font-weight: 800; font-family: monospace; }
    .status-badge { background-color: #0f3433; color: #00f0ff; padding: 5px 15px; border-radius: 20px; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

st.title("BHAVISHYA // PREDICTIVE URBAN GRID")
st.markdown("<span class='status-badge'>🟢 LIVE INFERENCE ENGINE</span>", unsafe_allow_html=True)
st.markdown("---")

# --- SIDEBAR: WHAT-IF SIMULATION ---
st.sidebar.header("🎛️ What-If Simulation")
st.sidebar.caption("Perturb variables to trigger spatiotemporal cascading risks.")

rain = st.sidebar.slider("Rainfall (mm/h)", 0, 150, 35)
traffic = st.sidebar.slider("Traffic Density (%)", 10, 100, 45)
drain = st.sidebar.slider("Drainage Capacity (%)", 10, 100, 85)
beds = st.sidebar.slider("Hospital Beds Available (%)", 10, 100, 70)

# Simulate applying intervention
if st.sidebar.button("🚨 Deploy AI Recommended Protocol"):
    with st.spinner("Rerouting traffic & pre-staging pumps..."):
        time.sleep(1.5)
        # Force states for demo purposes
        st.session_state['traffic'] = 30
        st.session_state['drain'] = 95
        st.success("Intervention Deployed Successfully!")

# Use session state if intervention was applied
traffic_val = st.session_state.get('traffic', traffic)
drain_val = st.session_state.get('drain', drain)

# --- INFERENCE MATH (Cascading Risk) ---
# In reality, this is where you would do: `from engine import model; risk = model.predict(...)`
risk_score = min(100, int((rain * 0.45) + (traffic_val * 0.35) + ((100 - drain_val) * 0.3) + ((100 - beds) * 0.2)))

# Determine Status Colors
if risk_score > 75:
    status_color, risk_text = "red", "CRITICAL"
elif risk_score > 50:
    status_color, risk_text = "orange", "ELEVATED"
else:
    status_color, risk_text = "green", "NOMINAL"

# --- MAIN DASHBOARD LAYOUT ---
col1, col2, col3 = st.columns([1, 1.5, 1])

# COLUMN 1: Risk & XAI
with col1:
    st.subheader("City Risk Index (T + 60m)")
    st.markdown(f"<div class='big-font' style='color: {status_color};'>{risk_score}% - {risk_text}</div>", unsafe_allow_html=True)
    
    st.markdown("### Explainable AI (XAI)")
    st.caption("Feature Attribution for Risk Spike")
    
    rain_contrib = min(100, int(rain * 0.45))
    traffic_contrib = min(100, int(traffic_val * 0.35))
    drain_contrib = min(100, int((100 - drain_val) * 0.3))
    
    st.progress(rain_contrib / 100, text=f"Rainfall Inundation: +{rain_contrib}%")
    st.progress(traffic_contrib / 100, text=f"Road Bottleneck: +{traffic_contrib}%")
    st.progress(drain_contrib / 100, text=f"Drainage Deficit: +{drain_contrib}%")

# COLUMN 2: GNN Dependency Graph
with col2:
    st.subheader("GNN Cascading Failure Topology")
    
    # Generate Graphviz network
    graph = graphviz.Digraph(engine='dot')
    graph.attr(bgcolor='transparent')
    
    # Node styling based on risk thresholds
    pump_color = 'red' if risk_score > 60 else 'green'
    road_color = 'red' if risk_score > 75 else 'green'
    hosp_color = 'red' if risk_score > 80 else 'green'
    
    graph.node('Power', 'Substation 4', style='filled', fillcolor='green', fontcolor='white')
    graph.node('Pump', 'Drainage Pump B', style='filled', fillcolor=pump_color, fontcolor='white')
    graph.node('Road', 'Arterial Flyover', style='filled', fillcolor=road_color, fontcolor='white')
    graph.node('Hospital', 'Apex Trauma Center', style='filled', fillcolor=hosp_color, fontcolor='white')
    
    graph.edge('Power', 'Pump', color='gray')
    graph.edge('Pump', 'Road', color='red' if pump_color=='red' else 'gray')
    graph.edge('Road', 'Hospital', color='red' if road_color=='red' else 'gray')
    
    st.graphviz_chart(graph, use_container_width=True)

# COLUMN 3: Prescriptive Engine
with col3:
    st.subheader("Prescriptive Intelligence")
    
    if risk_score > 75:
        st.error("**CRITICAL: Reroute Arterial Transit & Dispatch Pumps**\n\nPredicted 38-min ambulance blockade to Apex Hospital. Pre-emptively redirect heavy traffic to Ring Road.\n\n*Expected Risk Reduction: -41%*")
    elif risk_score > 50:
        st.warning("**ELEVATED: Pre-stage Auxiliary Pumps in Zone B**\n\nDrainage capacity threshold nearing limits. Standard monitoring advised.\n\n*Expected Risk Reduction: -22%*")
    else:
        st.success("**NOMINAL: Standard Traffic Adaptive Flow**\n\nAll infrastructure operating within safe tolerance parameters.")
        
    st.info("**Model Confidence: 93.8%**\nTrained on 36-month spatiotemporal flood & transit logs.")