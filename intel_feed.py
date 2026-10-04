## intel_feed.py

def get_map_html(lat, lon):
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
        <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
        <style>
            body {{ margin: 0; padding: 0; background-color: #030a04; overflow: hidden; }}
            #map {{ width: 100%; height: 280px; border: 1px solid #00ff41; background: #030a04; }}
            .leaflet-layer, .leaflet-control-zoom-in, .leaflet-control-zoom-out, .leaflet-control-attribution {{
                filter: invert(100%) hue-rotate(180deg) brightness(95%) contrast(90%);
            }}
            .leaflet-container {{ font-family: monospace; }}
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
            L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{ maxZoom: 19 }}).addTo(map);
            var circle = L.circle([{lat}, {lon}], {{ color: '#ff003c', fillColor: '#ff003c', fillOpacity: 0.1, radius: 800 }}).addTo(map);
        </script>
    </body>
    </html>
    """

def get_cctv_html(youtube_id=None):
    """Generates a Synthetic AI Computer Vision feed using HTML5 Canvas (100% reliable)."""
    return f"""
    <div style="border: 1px solid #00ff41; padding: 2px; background: #030a04; position: relative; height: 280px; box-shadow: inset 0 0 10px rgba(0,255,65,0.2); overflow: hidden;">
        <style>
            @keyframes blink {{ 50% {{ opacity: 0; }} }}
            .rec-indicator {{ position: absolute; top: 10px; left: 15px; color: #ff003c; font-family: 'Courier New', monospace; z-index: 999; animation: blink 1s step-end infinite; text-shadow: 0 0 5px #ff003c; font-weight: bold; font-size: 1.1rem; pointer-events: none; }}
            .overlay-text {{ position: absolute; bottom: 10px; left: 15px; color: #00ff41; font-family: 'Share Tech Mono', monospace; font-size: 0.8rem; z-index: 999; pointer-events: none; text-shadow: 0 0 3px #00ff41; }}
            /* CRT Scanline effect */
            .scanlines {{ position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.25) 50%), linear-gradient(90deg, rgba(255, 0, 0, 0.06), rgba(0, 255, 0, 0.02), rgba(0, 0, 255, 0.06)); background-size: 100% 4px, 3px 100%; z-index: 100; pointer-events: none; }}
        </style>
        
        <div class="rec-indicator">● AI_VISION_ACTIVE</div>
        <div class="scanlines"></div>
        <div class="overlay-text">
            > MODEL: YOLOV8_URBAN<br>
            > LATENCY: 12ms<br>
            > DETECTIONS: MULTIPLE
        </div>
        
        <canvas id="ai-feed" width="400" height="280" style="width: 100%; height: 100%; display: block; filter: contrast(1.2) brightness(0.9); opacity: 0.8;"></canvas>
        
        <script>
            const canvas = document.getElementById('ai-feed');
            const ctx = canvas.getContext('2d');
            
            // Simulated vehicles
            let objects = [
                {{ x: 150, y: -50, w: 40, h: 60, speed: 1.5, type: 'VEHICLE', conf: 98 }},
                {{ x: 220, y: -150, w: 45, h: 70, speed: 1.2, type: 'TRANSIT', conf: 94 }},
                {{ x: 130, y: -250, w: 35, h: 55, speed: 1.8, type: 'VEHICLE', conf: 99 }},
                {{ x: 250, y: -350, w: 40, h: 60, speed: 1.4, type: 'VEHICLE', conf: 91 }}
            ];

            function draw() {{
                // Clear background with radar-like dark green fade
                ctx.fillStyle = 'rgba(3, 10, 4, 0.3)';
                ctx.fillRect(0, 0, canvas.width, canvas.height);
                
                // Draw perspective road lines
                ctx.strokeStyle = 'rgba(0, 255, 65, 0.2)';
                ctx.lineWidth = 2;
                ctx.beginPath(); ctx.moveTo(180, 0); ctx.lineTo(100, 280); ctx.stroke();
                ctx.beginPath(); ctx.moveTo(220, 0); ctx.lineTo(300, 280); ctx.stroke();
                
                // Draw crosshairs
                ctx.beginPath(); ctx.moveTo(200, 0); ctx.lineTo(200, 280); ctx.setLineDash([5, 15]); ctx.stroke(); ctx.setLineDash([]);
                
                // Animate and draw bounding boxes
                objects.forEach(obj => {{
                    obj.y += obj.speed;
                    
                    // Reset to top when off screen to create infinite loop
                    if (obj.y > 300) {{
                        obj.y = -Math.random() * 200 - 50;
                        obj.conf = Math.floor(Math.random() * 10) + 90;
                    }}
                    
                    // Draw bounding box
                    ctx.strokeStyle = '#00ff41';
                    ctx.lineWidth = 1.5;
                    ctx.strokeRect(obj.x, obj.y, obj.w, obj.h);
                    
                    // Draw corner brackets for tactical feel
                    ctx.beginPath(); ctx.moveTo(obj.x, obj.y+10); ctx.lineTo(obj.x, obj.y); ctx.lineTo(obj.x+10, obj.y); ctx.stroke();
                    ctx.beginPath(); ctx.moveTo(obj.x+obj.w-10, obj.y); ctx.lineTo(obj.x+obj.w, obj.y); ctx.lineTo(obj.x+obj.w, obj.y+10); ctx.stroke();
                    
                    // Draw label background
                    ctx.fillStyle = 'rgba(0, 255, 65, 0.2)';
                    ctx.fillRect(obj.x, obj.y - 15, obj.w + 30, 15);
                    
                    // Draw text
                    ctx.fillStyle = '#00ff41';
                    ctx.font = '10px monospace';
                    ctx.fillText(`${{obj.type}} [${{obj.conf}}%]`, obj.x + 2, obj.y - 4);
                }});
                
                requestAnimationFrame(draw);
            }}
            draw();
        </script>
    </div>
    """

def get_news_summary(risk_score, traffic_density, target_name):
    if risk_score > 75:
        color = "#ff003c"; status = "CRITICAL INCIDENT"
        intel = f"SEVERE BOTTLENECK DETECTED NEAR {target_name.upper()}. Traffic density at {traffic_density}%. Multiple civic reports of infrastructure stress. Automated emergency routing engaged."
    elif risk_score > 50:
        color = "#f0a500"; status = "ELEVATED ALERT"
        intel = f"TRAFFIC BUILDUP NEAR {target_name.upper()}. Density at {traffic_density}%. Drainage capacity nearing limits due to precipitation. Monitoring critical junctions."
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