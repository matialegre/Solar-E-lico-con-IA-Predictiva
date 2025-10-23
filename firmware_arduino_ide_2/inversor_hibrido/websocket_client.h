/**
 * @file websocket_client.h
 * @brief Cliente WebSocket para comunicación bidireccional ESP32 ↔ Backend
 * 
 * ELIMINA EL PROBLEMA DE GET -7 usando conexión permanente
 * Incluye sistema de ACK para confirmar comandos ejecutados
 */

#ifndef WEBSOCKET_CLIENT_H
#define WEBSOCKET_CLIENT_H

#include <WebSocketsClient.h>
#include <ArduinoJson.h>
#include "config.h"
#include "relays.h"

WebSocketsClient webSocket;

// ===== ESTADO WEBSOCKET =====
bool ws_connected = false;
unsigned long ws_last_connect_attempt = 0;
#define WS_RECONNECT_INTERVAL 5000  // Reintentar cada 5 segundos

// ===== CALLBACKS =====
void webSocketEvent(WStype_t type, uint8_t * payload, size_t length) {
    switch(type) {
        case WStype_DISCONNECTED:
            Serial.println("❌ WebSocket desconectado");
            ws_connected = false;
            break;
            
        case WStype_CONNECTED:
            Serial.println("✅ WebSocket conectado!");
            Serial.printf("   URL: %s\n", payload);
            ws_connected = true;
            
            // Enviar mensaje inicial de bienvenida
            webSocket.sendTXT("{\"type\":\"hello\",\"device_id\":\"" + String(DEVICE_ID) + "\"}");
            break;
            
        case WStype_TEXT:
            {
                Serial.printf("📥 [WS] Mensaje recibido: %s\n", payload);
                
                // Parsear JSON
                StaticJsonDocument<512> doc;
                DeserializationError error = deserializeJson(doc, payload, length);
                
                if (error) {
                    Serial.println("❌ Error parseando JSON WebSocket");
                    return;
                }
                
                // Procesar comando
                String msg_type = doc["type"].as<String>();
                
                if (msg_type == "command") {
                    String command_id = doc["id"].as<String>();
                    String command = doc["command"].as<String>();
                    String parameter = doc.containsKey("parameter") ? doc["parameter"].as<String>() : "";
                    
                    // Mensaje SUPER VISIBLE en Serial
                    Serial.println();
                    Serial.println("***************************************");
                    Serial.println(">>> COMANDO POR WEBSOCKET <<<");
                    if (command == "eolica") {
                        Serial.printf(">>> %s RELE EOLICO <<<\n", (parameter == "on" || parameter == "1") ? "PRENDER" : "APAGAR");
                    } else if (command == "solar") {
                        Serial.printf(">>> %s RELE SOLAR <<<\n", (parameter == "on" || parameter == "1") ? "PRENDER" : "APAGAR");
                    } else if (command == "red") {
                        Serial.printf(">>> %s RELE RED <<<\n", (parameter == "on" || parameter == "1") ? "PRENDER" : "APAGAR");
                    } else if (command == "carga") {
                        Serial.printf(">>> %s RELE CARGA <<<\n", (parameter == "on" || parameter == "1") ? "PRENDER" : "APAGAR");
                    } else if (command == "freno") {
                        Serial.printf(">>> %s FRENO <<<\n", (parameter == "on" || parameter == "1") ? "ACTIVAR" : "DESACTIVAR");
                    } else if (command == "reboot") {
                        Serial.println(">>> REINICIAR ESP (3s) <<<");
                    } else {
                        Serial.printf(">>> COMANDO: %s (%s) <<<\n", command.c_str(), parameter.c_str());
                    }
                    Serial.printf(">>> ID: %s <<<\n", command_id.c_str());
                    Serial.println("***************************************");
                    Serial.println();
                    
                    // Ejecutar comando
                    bool success = false;
                    if (ejecutarComandoRele(command, parameter)) {
                        success = true;
                    } else if (command == "reboot") {
                        // Enviar ACK antes de reiniciar
                        StaticJsonDocument<128> ack;
                        ack["type"] = "ack";
                        ack["command_id"] = command_id;
                        ack["status"] = "success";
                        String ackJson;
                        serializeJson(ack, ackJson);
                        webSocket.sendTXT(ackJson);
                        
                        Serial.println("🔄 Reiniciando en 3 segundos...");
                        delay(3000);
                        ESP.restart();
                        return;
                    } else {
                        Serial.printf("⚠️  Comando desconocido: %s\n", command.c_str());
                    }
                    
                    // Enviar ACK al backend
                    StaticJsonDocument<128> ack;
                    ack["type"] = "ack";
                    ack["command_id"] = command_id;
                    ack["status"] = success ? "success" : "error";
                    ack["timestamp"] = millis();
                    
                    String ackJson;
                    serializeJson(ack, ackJson);
                    webSocket.sendTXT(ackJson);
                    
                    Serial.printf("✅ ACK enviado para comando [%s]\n", command_id.substring(0, 8).c_str());
                }
                else if (msg_type == "ping") {
                    // Responder a ping con pong
                    webSocket.sendTXT("{\"type\":\"pong\"}");
                }
            }
            break;
            
        case WStype_BIN:
            Serial.printf("📦 [WS] Binario recibido (%u bytes)\n", length);
            break;
            
        case WStype_ERROR:
            Serial.println("❌ [WS] Error!");
            break;
            
        case WStype_FRAGMENT_TEXT_START:
        case WStype_FRAGMENT_BIN_START:
        case WStype_FRAGMENT:
        case WStype_FRAGMENT_FIN:
            // Fragmentos no soportados en este caso
            break;
    }
}

// ===== INICIALIZAR WEBSOCKET =====
void initWebSocket() {
    Serial.println("🔌 Inicializando WebSocket Client...");
    
    // Extraer host y puerto de SERVER_URL
    String url = String(SERVER_URL);
    
    // Formato esperado: "http://IP:PUERTO" o "https://DOMAIN"
    // Ejemplo: "http://190.211.201.217:11113"
    
    String host = "";
    uint16_t port = 80;
    String path = "/api/ws/esp32/" + String(DEVICE_ID);
    
    // Parsear URL
    if (url.startsWith("http://")) {
        url = url.substring(7);  // Quitar "http://"
        
        int colonPos = url.indexOf(':');
        if (colonPos > 0) {
            host = url.substring(0, colonPos);
            int slashPos = url.indexOf('/', colonPos);
            if (slashPos > 0) {
                port = url.substring(colonPos + 1, slashPos).toInt();
            } else {
                port = url.substring(colonPos + 1).toInt();
            }
        } else {
            int slashPos = url.indexOf('/');
            if (slashPos > 0) {
                host = url.substring(0, slashPos);
            } else {
                host = url;
            }
            port = 80;
        }
    } else if (url.startsWith("https://")) {
        url = url.substring(8);  // Quitar "https://"
        
        int slashPos = url.indexOf('/');
        if (slashPos > 0) {
            host = url.substring(0, slashPos);
        } else {
            host = url;
        }
        port = 443;
    }
    
    Serial.printf("   Host: %s\n", host.c_str());
    Serial.printf("   Port: %d\n", port);
    Serial.printf("   Path: %s\n", path.c_str());
    
    // Configurar WebSocket
    webSocket.begin(host, port, path);
    webSocket.onEvent(webSocketEvent);
    webSocket.setReconnectInterval(WS_RECONNECT_INTERVAL);
    
    // Configurar timeouts más largos para WiFi lento
    webSocket.enableHeartbeat(15000, 3000, 2);  // ping cada 15s, timeout 3s, 2 intentos
    
    Serial.println("✅ WebSocket configurado");
    
    ws_last_connect_attempt = millis();
}

// ===== LOOP WEBSOCKET =====
void loopWebSocket() {
    // Mantener WebSocket vivo
    webSocket.loop();
    
    // Si no está conectado y pasó el intervalo, reintentar
    if (!ws_connected && (millis() - ws_last_connect_attempt > WS_RECONNECT_INTERVAL)) {
        Serial.println("🔄 Reintentando conexión WebSocket...");
        ws_last_connect_attempt = millis();
    }
}

// ===== ENVIAR HEARTBEAT POR WEBSOCKET =====
void sendWebSocketHeartbeat() {
    if (!ws_connected) return;
    
    StaticJsonDocument<128> doc;
    doc["type"] = "heartbeat";
    doc["device_id"] = DEVICE_ID;
    doc["uptime"] = millis() / 1000;
    doc["free_heap"] = ESP.getFreeHeap();
    doc["rssi"] = WiFi.RSSI();
    
    String json;
    serializeJson(doc, json);
    webSocket.sendTXT(json);
}

// ===== VERIFICAR SI WEBSOCKET ESTÁ CONECTADO =====
bool isWebSocketConnected() {
    return ws_connected;
}

#endif // WEBSOCKET_CLIENT_H
