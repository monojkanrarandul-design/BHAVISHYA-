# intel_feed.py

def get_map_html(lat, lon):
    """Generates an interactive tactical map. Clicking the map sends coordinates to Streamlit."""
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
        <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
        <style>
            body {{ margin: 0; padding: 0; background-color: #030a04; overflow: hidden; }}
            #map {{ width: 100%; height: 280px; border: 1px solid #00ff41; box-shadow: inset 0 0 10px #00ff41; background: #030a04; cursor: crosshair; }}
            /* CSS Inversion for Dark Tactical Mode */
            .leaflet-layer, .leaflet-control-zoom-in, .leaflet-control-zoom-out, .leaflet-control-attribution {{
                filter: invert(100%) hue-rotate(180deg) brightness(95%) contrast(90%);
            }}
            .leaflet-container {{ font-family: monospace; }}
            /* Targeting Reticle */
            .crosshair {{ position: absolute; top: 50%; left: 50%; width: 30px; height: 30px; border: 2px solid rgba(0, 255, 65, 0.8); transform: translate(-50%, -50%); z-index: 1000; pointer-events: none; border-radius: 50%; box-shadow: 0 0 10px #00ff41; }}
            .crosshair::before, .crosshair::after {{ content: ''; position: absolute; background: rgba(0, 255, 65, 0.8); }}
            .crosshair::before {{ top: 50%; left: -15px; right: -15px; height: 2px; }}
            .crosshair::after {{ left: 50%; top: -15px; bottom: -15px; width: 2px; }}
        </style>
    </head>
    <body>
        <div style="position: relative;">
            <div id="map"></div>
            <div class="crosshair"></div>
        </div>
        <script>
            var map = L.map('map', {{ zoomControl: false, attributionControl: false }}).setView([{lat}, {lon}], 14);
            
            // Base Map Layer
            L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{ maxZoom: 19 }}).addTo(map);
            
            // Synthetic Radar Pulse
            var circle = L.circle([{lat}, {lon}], {{
                color: '#ff003c',
                fillColor: '#ff003c',
                fillOpacity: 0.1,
                radius: 800
            }}).addTo(map);

            // Communication back to Streamlit when the map is clicked
            map.on('click', function(e) {{
                const newLat = e.latlng.lat;
                const newLon = e.latlng.lng;
                // Send data to Streamlit via parent window
                window.parent.postMessage({{
                    type: 'streamlit:setComponentValue',
                    value: {{ lat: newLat, lon: newLon }}
                }}, '*');
            }});
        </script>
    </body>
    </html>
    """

def get_news_summary(risk_score, traffic_density, target_name):
    """Generates an AI-style localized news briefing."""
    if risk_score > 75:
        color = "#ff003c"; status = "CRITICAL INCIDENT"
        intel = f"SEVERE BOTTLENECK DETECTED NEAR {target_name.upper()}. Traffic density at {traffic_density}%. Multiple civic reports of infrastructure stress. Automated emergency routing engaged. High probability of cascading failure."
    elif risk_score > 50:
        color = "#f0a500"; status = "ELEVATED ALERT"
        intel = f"TRAFFIC BUILDUP NEAR {target_name.upper()}. Density at {traffic_density}%. Drainage capacity nearing limits due to precipitation. Monitoring critical junctions for localized flooding."
    else:
        color = "#00ff41"; status = "NOMINAL OPERATIONS"
        intel = f"Target zone {target_name.upper()} flowing at standard efficiency ({traffic_density}% capacity). No major incidents reported on primary arterials. Infrastructure integrity holding."

    return f"""
    <div style="border: 1px solid {color}; padding: 12px; background: rgba(0, 20, 0, 0.6); height: 280px; overflow-y: hidden; box-shadow: inset 0 0 10px {color}33;">
        <h4 style="color: {color}; margin-top: 0; text-transform: uppercase; font-family: 'Share Tech Mono', monospace; border-bottom: 1px solid {color}; padding-bottom: 5px; font-size: 1.1rem;">
            > COMMS INTEL: {status}
        </h4>
        <p style="color: #a3a3a3; font-size: 0.85rem; font-family: 'Share Tech Mono', monospace; line-height: 1.4;">
            <span style="color: #00f0ff;">[AUTO-TRANSCRIPT]</span> {intel}
        </p>
        <p style="color: #00ff41; font-size: 0.75rem; font-family: 'Share Tech Mono', monospace; margin-top: 15px;">
            > INTERCEPTING RADIO...<br>
            > SCANNING LOCAL SENSORS... OK<br>
            > NLP SUMMARY GENERATED.
        </p>
    </div>
    """