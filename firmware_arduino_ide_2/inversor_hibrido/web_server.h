/**
 * @file web_server.h
 * @brief Servidor web local del ESP32
 * Muestra ADCs, relés, estado de conexión en tiempo real
 */

#ifndef WEB_SERVER_H
#define WEB_SERVER_H

#ifdef ENABLE_WEB_SERVER
#include <ESPAsyncWebServer.h>
#include "config.h"
#include "sensors.h"
#include "relays.h"

// Servidor web en puerto 80
AsyncWebServer server(80);

// HTML de la página
const char index_html[] PROGMEM = R"rawliteral(
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ESP32 Inversor - Dashboard Local</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }
        h1 {
            color: #667eea;
            text-align: center;
            margin-bottom: 30px;
            font-size: 2em;
        }
        .status-bar {
            background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
            color: white;
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .status-bar.offline {
            background: linear-gradient(135deg, #eb3349 0%, #f45c43 100%);
        }
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }
        .card {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 15px;
            border-left: 5px solid #667eea;
        }
        .card h3 {
            color: #667eea;
            margin-bottom: 15px;
            font-size: 1.2em;
        }
        .metric {
            display: flex;
            justify-content: space-between;
            padding: 10px 0;
            border-bottom: 1px solid #ddd;
        }
        .metric:last-child { border-bottom: none; }
        .metric-label { color: #666; }
        .metric-value {
            font-weight: bold;
            color: #333;
            font-size: 1.1em;
        }
        .relay {
            display: inline-block;
            padding: 8px 16px;
            border-radius: 20px;
            margin: 5px;
            font-weight: bold;
            color: white;
        }
        .relay.on { background: #38ef7d; }
        .relay.off { background: #eb3349; }
        .badge {
            display: inline-block;
            padding: 5px 15px;
            border-radius: 20px;
            font-weight: bold;
            font-size: 0.9em;
        }
        .badge.online {
            background: #38ef7d;
            color: white;
            animation: pulse 2s infinite;
        }
        .badge.offline {
            background: #eb3349;
            color: white;
        }
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.6; }
        }
        .refresh-btn {
            background: #667eea;
            color: white;
            border: none;
            padding: 12px 30px;
            border-radius: 25px;
            cursor: pointer;
            font-size: 1em;
            margin-top: 20px;
            display: block;
            margin-left: auto;
            margin-right: auto;
        }
        .refresh-btn:hover {
            background: #5568d3;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔌 ESP32 Inversor Híbrido</h1>
        
        <!-- Estado de conexión -->
        <div class="status-bar" id="statusBar">
            <div>
                <span class="badge online" id="statusBadge">● ONLINE</span>
                <strong id="deviceId">ESP32_INVERSOR_001</strong>
            </div>
            <div>
                <span id="serverStatus">🌐 Conectado al servidor</span>
            </div>
        </div>

        <!-- ADCs y Sensores -->
        <div class="grid">
            <div class="card">
                <h3>🔋 Batería</h3>
                <div class="metric">
                    <span class="metric-label">Voltaje:</span>
                    <span class="metric-value" id="voltage">--V</span>
                </div>
                <div class="metric">
                    <span class="metric-label">SOC:</span>
                    <span class="metric-value" id="soc">--%</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Temperatura:</span>
                    <span class="metric-value" id="temp">--°C</span>
                </div>
            </div>

            <div class="card">
                <h3>☀️ Solar</h3>
                <div class="metric">
                    <span class="metric-label">Corriente:</span>
                    <span class="metric-value" id="solarCurrent">--A</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Potencia:</span>
                    <span class="metric-value" id="solarPower">--W</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Irradiancia:</span>
                    <span class="metric-value" id="irradiance">-- W/m²</span>
                </div>
            </div>

            <div class="card">
                <h3>💨 Eólica</h3>
                <div class="metric">
                    <span class="metric-label">Corriente:</span>
                    <span class="metric-value" id="windCurrent">--A</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Potencia:</span>
                    <span class="metric-value" id="windPower">--W</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Velocidad viento:</span>
                    <span class="metric-value" id="windSpeed">-- m/s</span>
                </div>
            </div>

            <div class="card">
                <h3>⚡ Consumo</h3>
                <div class="metric">
                    <span class="metric-label">Corriente:</span>
                    <span class="metric-value" id="loadCurrent">--A</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Potencia:</span>
                    <span class="metric-value" id="loadPower">--W</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Balance:</span>
                    <span class="metric-value" id="balance">--W</span>
                </div>
            </div>
        </div>

        <!-- Estado de Relés -->
        <div class="card">
            <h3>🔌 Estado de Relés</h3>
            <div style="text-align: center; padding: 10px;">
                <span class="relay on" id="relaySolar">☀️ SOLAR: ON</span>
                <span class="relay on" id="relayWind">💨 EÓLICA: ON</span>
                <span class="relay off" id="relayGrid">🔌 RED: OFF</span>
                <span class="relay on" id="relayLoad">⚡ CARGA: ON</span>
            </div>
        </div>

        <button class="refresh-btn" onclick="loadData()">🔄 Actualizar Datos</button>
        
        <div style="text-align: center; margin-top: 20px; color: #666; font-size: 0.9em;">
            <p>Última actualización: <span id="lastUpdate">--</span></p>
            <p>IP Local: <span id="ipAddress">--</span></p>
        </div>
    </div>

    <script>
        function loadData() {
            fetch('/api/data')
                .then(res => res.json())
                .then(data => {
                    // Batería
                    document.getElementById('voltage').textContent = data.voltage.toFixed(2) + 'V';
                    document.getElementById('soc').textContent = data.soc.toFixed(1) + '%';
                    document.getElementById('temp').textContent = data.temperature.toFixed(1) + '°C';
                    
                    // Solar
                    document.getElementById('solarCurrent').textContent = data.solar_current.toFixed(2) + 'A';
                    document.getElementById('solarPower').textContent = Math.round(data.solar_power) + 'W';
                    document.getElementById('irradiance').textContent = Math.round(data.irradiance) + ' W/m²';
                    
                    // Eólica
                    document.getElementById('windCurrent').textContent = data.wind_current.toFixed(2) + 'A';
                    document.getElementById('windPower').textContent = Math.round(data.wind_power) + 'W';
                    document.getElementById('windSpeed').textContent = data.wind_speed.toFixed(1) + ' m/s';
                    
                    // Consumo
                    document.getElementById('loadCurrent').textContent = data.load_current.toFixed(2) + 'A';
                    document.getElementById('loadPower').textContent = Math.round(data.load_power) + 'W';
                    
                    let balance = data.solar_power + data.wind_power - data.load_power;
                    document.getElementById('balance').textContent = Math.round(balance) + 'W';
                    
                    // Relés
                    updateRelay('relaySolar', '☀️ SOLAR', data.relay_solar);
                    updateRelay('relayWind', '💨 EÓLICA', data.relay_wind);
                    updateRelay('relayGrid', '🔌 RED', data.relay_grid);
                    updateRelay('relayLoad', '⚡ CARGA', data.relay_load);
                    
                    // Estado conexión
                    document.getElementById('serverStatus').textContent = 
                        data.server_connected ? '🌐 Conectado al servidor' : '⚠️ Desconectado del servidor';
                    
                    // Info
                    document.getElementById('lastUpdate').textContent = new Date().toLocaleTimeString();
                    document.getElementById('ipAddress').textContent = data.ip_address;
                })
                .catch(err => {
                    console.error('Error:', err);
                    document.getElementById('statusBar').classList.add('offline');
                    document.getElementById('statusBadge').textContent = '● OFFLINE';
                    document.getElementById('statusBadge').classList.remove('online');
                    document.getElementById('statusBadge').classList.add('offline');
                });
        }

        function updateRelay(id, label, state) {
            let elem = document.getElementById(id);
            elem.textContent = label + ': ' + (state ? 'ON' : 'OFF');
            elem.className = 'relay ' + (state ? 'on' : 'off');
        }

        // Actualizar cada 2 segundos
        loadData();
        setInterval(loadData, 2000);
    </script>
</body>
</html>
)rawliteral";

// ===== INICIALIZAR SERVIDOR WEB =====
void initWebServer() {
  // Ruta principal
  server.on("/", HTTP_GET, [](AsyncWebServerRequest *request){
    request->send_P(200, "text/html", index_html);
  });
  
  // API de datos JSON
  server.on("/api/data", HTTP_GET, [](AsyncWebServerRequest *request){
    // Crear JSON con datos actuales
    String json = "{";
    json += "\"voltage\":" + String(sensores.voltaje_promedio, 2) + ",";
    json += "\"soc\":" + String(sensores.soc, 1) + ",";
    json += "\"temperature\":" + String(sensores.temperatura, 1) + ",";
    json += "\"solar_current\":" + String(sensores.corriente_solar, 2) + ",";
    json += "\"solar_power\":" + String(sensores.potencia_solar, 0) + ",";
    json += "\"wind_current\":" + String(sensores.corriente_eolica, 2) + ",";
    json += "\"wind_power\":" + String(sensores.potencia_eolica, 0) + ",";
    json += "\"load_current\":" + String(sensores.corriente_consumo, 2) + ",";
    json += "\"load_power\":" + String(sensores.potencia_consumo, 0) + ",";
    json += "\"irradiance\":" + String(sensores.irradiancia, 0) + ",";
    json += "\"wind_speed\":" + String(sensores.velocidad_viento, 1) + ",";
    json += "\"relay_solar\":" + String(relay_state.solar_conectado ? "true" : "false") + ",";
    json += "\"relay_wind\":" + String(relay_state.eolica_conectada ? "true" : "false") + ",";
    json += "\"relay_grid\":" + String(relay_state.red_conectada ? "true" : "false") + ",";
    json += "\"relay_load\":" + String(relay_state.carga_conectada ? "true" : "false") + ",";
    json += "\"server_connected\":" + String((WiFi.status() == WL_CONNECTED) ? "true" : "false") + ",";
    json += "\"ip_address\":\"" + WiFi.localIP().toString() + "\"";
    json += "}";
    
    request->send(200, "application/json", json);
  });
  
  // Iniciar servidor
  server.begin();
  
  Serial.println("\n🌐 Servidor web iniciado");
  Serial.print("   Acceso local: http://");
  Serial.println(WiFi.localIP());
  Serial.println("   Dashboard en tiempo real disponible\n");
}

#else  // ENABLE_WEB_SERVER not defined

// Stub para compilar sin servidor web ni dependencias Async
inline void initWebServer() {
  // Web server deshabilitado en esta build
}

#endif // ENABLE_WEB_SERVER

#endif // WEB_SERVER_H
