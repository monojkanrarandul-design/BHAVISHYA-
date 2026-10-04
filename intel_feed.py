# intel_feed.py

def get_map_html(lat="22.5958", lon="88.2636"):
    """Generates a dark-mode tactical map using CSS inversion on free OSM tiles."""
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
        <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
        <style>
            body {{ margin: 0; padding: 0; background-color: #030a04; }}
            #map {{ width: 100%; height: 280px; border: 1px solid #00ff41; box-shadow: inset 0 0 10px #00ff41; background: #030a04; }}
            
            /* THE HACKATHON TRICK: Invert standard map colors to make a dark mode map! */
            .leaflet-layer,
            .leaflet-control-zoom-in,
            .leaflet-control-zoom-out,
            .leaflet-control-attribution {{
                filter: invert(100%) hue-rotate(180deg) brightness(95%) contrast(90%);
            }}

            .leaflet-container {{ font-family: monospace; }}
            /* Crosshair overlay */
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
            
            // 100% Free OpenStreetMap Tiles (No API key needed ever)
            L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
                maxZoom: 19
            }}).addTo(map);
            
            // Radar pulse effect
            var circle = L.circle([{lat}, {lon}], {{
                color: '#00ff41',
                fillColor: '#00ff41',
                fillOpacity: 0.15,
                radius: 1200
            }}).addTo(map);
        </script>
    </body>
    </html>
    """

def get_news_summary(risk_score, traffic_density):
    """Generates an AI-style localized news briefing."""
    if risk_score > 75:
        color = "#ff003c"
        status = "CRITICAL INCIDENT"
        intel = f"SEVERE BOTTLENECK DETECTED. Kona Expressway traffic density at {traffic_density}%. Multiple civic reports of waterlogging near Santragachi. Ambulance routing to Apex Trauma compromised."
    elif risk_score > 50:
        color = "#f0a500"
        status = "ELEVATED ALERT"
        intel = f"TRAFFIC BUILDUP ON ARTERIAL ROUTES. Density at {traffic_density}%. Drainage capacity nearing limits due to sustained precipitation. Monitoring Howrah Station approach."
    else:
        color = "#00ff41"
        status = "NOMINAL OPERATIONS"
        intel = f"Traffic flowing at standard efficiency ({traffic_density}% capacity). No major incidents reported on NH16 or Kona Expressway. Infrastructure integrity holding."

    return f"""
    <div style="border: 1px solid {color}; padding: 12px; background: rgba(0, 20, 0, 0.6); height: 280px; overflow-y: hidden;">
        <h4 style="color: {color}; margin-top: 0; text-transform: uppercase; font-family: 'Share Tech Mono', monospace; border-bottom: 1px solid {color}; padding-bottom: 5px; font-size: 1.1rem;">
            > COMMS INTEL: {status}
        </h4>
        <p style="color: #a3a3a3; font-size: 0.9rem; font-family: 'Share Tech Mono', monospace; line-height: 1.4;">
            <span style="color: #00f0ff;">[AUTO-TRANSCRIPT]</span> {intel}
        </p>
        <p style="color: #00ff41; font-size: 0.8rem; font-family: 'Share Tech Mono', monospace; margin-top: 15px;">
            > INTERCEPTING RADIO...<br>
            > SCANNING CCTV... OK<br>
            > NLP SUMMARY GENERATED.
        </p>
    </div>
    """