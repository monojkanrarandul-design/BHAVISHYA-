# intel_feed.py

def get_map_html(lat, lon):
    """Generates a dark-mode tactical map using CSS inversion on free OSM tiles."""
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
        <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
        <style>
            body {{ margin: 0; padding: 0; background-color: #030a04; overflow: hidden; }}
            #map {{ width: 100%; height: 280px; border: 1px solid #00ff41; box-shadow: inset 0 0 10px #00ff41; background: #030a04; }}
            .leaflet-layer, .leaflet-control-zoom-in, .leaflet-control-zoom-out, .leaflet-control-attribution {{
                filter: invert(100%) hue-rotate(180deg) brightness(95%) contrast(90%);
            }}
            .leaflet-container {{ font-family: monospace; }}
            .crosshair {{ position: absolute; top: 50%; left: 50%; width: 20px; height: 20px; border: 1px solid rgba(0, 255, 65, 0.5); transform: translate(-50%, -50%); z-index: 1000; pointer-events: none; border-radius: 50%; }}
            .crosshair::before, .crosshair::after {{ content: ''; position: absolute; background: rgba(0, 255, 65, 0.5); }}
            .crosshair::before {{ top: 50%; left: -10px; right: -10px; height: 1px; }}
            .crosshair::after {{ left: 50%; top: -10px; bottom: -10px; width: 1px; }}
        </style>
    </head>
    <body>
        <div style="position: relative;">
            <div id="map"></div>
            <div class="crosshair"></div>
        </div>
        <script>
            var map = L.map('map', {{ zoomControl: false, attributionControl: false }}).setView([{lat}, {lon}], 13);
            L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{ maxZoom: 19 }}).addTo(map);
            var circle = L.circle([{lat}, {lon}], {{ color: '#00ff41', fillColor: '#00ff41', fillOpacity: 0.15, radius: 1200 }}).addTo(map);
        </script>
    </body>
    </html>
    """

def get_cctv_html(youtube_id):
    """Embeds a live video feed styled as a hacked CCTV camera with audio."""
    return f"""
    <div style="border: 1px solid #00ff41; padding: 2px; background: #030a04; position: relative; height: 280px; box-shadow: inset 0 0 10px rgba(0,255,65,0.2);">
        <style>
            @keyframes blink {{ 50% {{ opacity: 0; }} }}
            .rec-indicator {{ position: absolute; top: 10px; left: 15px; color: #ff003c; font-family: 'Courier New', monospace; z-index: 999; animation: blink 1s step-end infinite; text-shadow: 0 0 5px #ff003c; font-weight: bold; font-size: 1.1rem; pointer-events: none; }}
        </style>
        <div class="rec-indicator">● REC_LIVE</div>
        <!-- Note: autoplay=1 and mute=0 are set. Browsers may require user to click the video once to enable sound! -->
        <iframe width="100%" height="274" src="https://www.youtube-nocookie.com/embed/{youtube_id}?autoplay=1&mute=0&controls=1&modestbranding=1&live=1" title="CCTV FEED" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
    </div>
    """

def get_news_summary(risk_score, traffic_density, city_name):
    """Generates an AI-style localized news briefing."""
    if risk_score > 75:
        color = "#ff003c"; status = "CRITICAL INCIDENT"
        intel = f"SEVERE BOTTLENECK DETECTED IN {city_name.upper()}. Traffic density at {traffic_density}%. Multiple civic reports of infrastructure stress. Automated emergency routing engaged."
    elif risk_score > 50:
        color = "#f0a500"; status = "ELEVATED ALERT"
        intel = f"TRAFFIC BUILDUP IN {city_name.upper()}. Density at {traffic_density}%. Drainage capacity nearing limits due to precipitation. Monitoring critical junctions."
    else:
        color = "#00ff41"; status = "NOMINAL OPERATIONS"
        intel = f"{city_name.upper()} traffic flowing at standard efficiency ({traffic_density}% capacity). No major incidents reported. Infrastructure integrity holding."

    return f"""
    <div style="border: 1px solid {color}; padding: 12px; background: rgba(0, 20, 0, 0.6); height: 280px; overflow-y: hidden;">
        <h4 style="color: {color}; margin-top: 0; text-transform: uppercase; font-family: 'Share Tech Mono', monospace; border-bottom: 1px solid {color}; padding-bottom: 5px; font-size: 1.1rem;">
            > COMMS INTEL: {status}
        </h4>
        <p style="color: #a3a3a3; font-size: 0.85rem; font-family: 'Share Tech Mono', monospace; line-height: 1.4;">
            <span style="color: #00f0ff;">[AUTO-TRANSCRIPT]</span> {intel}
        </p>
        <p style="color: #00ff41; font-size: 0.75rem; font-family: 'Share Tech Mono', monospace; margin-top: 15px;">
            > INTERCEPTING RADIO...<br>
            > SCANNING CCTV... OK<br>
            > NLP SUMMARY GENERATED.
        </p>
    </div>
    """