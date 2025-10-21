/**
 * @file http_client.h
 * @brief Cliente HTTP para comunicación con backend
 */

#ifndef HTTP_CLIENT_H
#define HTTP_CLIENT_H

#include <HTTPClient.h>
#include <ArduinoJson.h>
#include "config.h"
#include "sensors.h"
#include "relays.h"
#include "protection.h"

HTTPClient http;

// Configuración dinámica (recibida del servidor)
ConfigDinamica config_dinamica = {
  .latitude = -38.7183,
  .longitude = -62.2663,
  .battery_capacity_wh = BATTERY_CAPACITY_WH,
  .solar_area_m2 = SOLAR_PANEL_AREA_M2,
  .wind_power_w = WIND_TURBINE_POWER_W,
  .proteccion_activa = true,
  .aprendizaje_activo = false
};

// ===== INICIALIZACIÓN =====
void initHTTP() {
  // Configurar timeout
  http.setTimeout(5000);
}

// ===== REGISTRAR DISPOSITIVO =====
bool registerDevice() {
  if (WiFi.status() != WL_CONNECTED) return false;
  
  StaticJsonDocument<256> doc;
  doc["device_id"] = DEVICE_ID;
  doc["ip_local"] = WiFi.localIP().toString();
  doc["mac_address"] = WiFi.macAddress();
  doc["firmware_version"] = "2.0";
  doc["latitude"] = config_dinamica.latitude;
  doc["longitude"] = config_dinamica.longitude;
  
  String jsonString;
  serializeJson(doc, jsonString);
  
  String url = String(SERVER_URL) + "/api/esp32/register";
  http.begin(url);
  http.addHeader("Content-Type", "application/json");
  
  int httpCode = http.POST(jsonString);
  
  bool success = (httpCode == 200 || httpCode == 201);
  
  #ifdef DEBUG_HTTP
  if (success) {
    Serial.printf("✅ Registro exitoso: %d\n", httpCode);
  } else {
    Serial.printf("❌ Error registro: %d\n", httpCode);
  }
  #endif
  
  http.end();
  return success;
}

// ===== HEARTBEAT =====
void sendHeartbeat() {
  if (WiFi.status() != WL_CONNECTED) return;
  
  StaticJsonDocument<128> doc;
  doc["device_id"] = DEVICE_ID;
  doc["uptime"] = millis() / 1000;  // Segundos
  doc["free_heap"] = ESP.getFreeHeap();
  doc["rssi"] = WiFi.RSSI();
  
  String jsonString;
  serializeJson(doc, jsonString);
  
  String url = String(SERVER_URL) + "/api/esp32/heartbeat";
  http.begin(url);
  http.addHeader("Content-Type", "application/json");
  
  int httpCode = http.POST(jsonString);
  
  #ifdef DEBUG_HTTP
  if (httpCode == 200) {
    Serial.println("❤️  Heartbeat OK");
  }
  #endif
  
  http.end();
}

// ===== ENVIAR TELEMETRÍA =====
void sendTelemetry() {
  if (WiFi.status() != WL_CONNECTED) return;
  
  // Crear JSON
  StaticJsonDocument<768> doc;
  doc["device_id"] = DEVICE_ID;
  doc["timestamp"] = millis();
  
  // Ubicación (de config dinámica)
  doc["latitude"] = config_dinamica.latitude;
  doc["longitude"] = config_dinamica.longitude;
  
  // Voltajes
  doc["voltaje_bat1"] = sensores.voltaje_bat1;
  doc["voltaje_bat2"] = sensores.voltaje_bat2;
  doc["voltaje_bat3"] = sensores.voltaje_bat3;
  doc["voltaje_promedio"] = sensores.voltaje_promedio;
  
  // Corrientes
  doc["corriente_solar"] = sensores.corriente_solar;
  doc["corriente_eolica"] = sensores.corriente_eolica;
  doc["corriente_consumo"] = sensores.corriente_consumo;
  
  // Potencias
  doc["potencia_solar"] = sensores.potencia_solar;
  doc["potencia_eolica"] = sensores.potencia_eolica;
  doc["potencia_consumo"] = sensores.potencia_consumo;
  
  // Ambiente
  doc["irradiancia"] = sensores.irradiancia;
  doc["velocidad_viento"] = sensores.velocidad_viento;
  
  // Estado batería
  doc["soc"] = sensores.soc;
  doc["temperatura"] = sensores.temperatura;
  
  // Estado de relés
  JsonObject relays = doc.createNestedObject("relays");
  relays["solar"] = relay_state.solar_conectado;
  relays["eolica"] = relay_state.eolica_conectada;
  relays["red"] = relay_state.red_conectada;
  relays["carga"] = relay_state.carga_conectada;
  relays["freno"] = relay_state.freno_activo;
  
  // Estado de protección
  doc["proteccion_estado"] = getProtectionStatus();
  doc["embalamiento_detectado"] = protection_state.embalamiento_detectado;
  
  // Serializar
  String jsonString;
  serializeJson(doc, jsonString);
  
  // Enviar POST
  String url = String(SERVER_URL) + "/api/esp32/telemetry";
  http.begin(url);
  http.addHeader("Content-Type", "application/json");
  
  int httpCode = http.POST(jsonString);
  
  #ifdef DEBUG_HTTP
  if (httpCode > 0) {
    Serial.printf("📤 Telemetría enviada: %d\n", httpCode);
  } else {
    Serial.printf("❌ Error HTTP: %s\n", http.errorToString(httpCode).c_str());
  }
  #endif
  
  http.end();
}

// ===== OBTENER CONFIGURACIÓN DEL SERVIDOR =====
void getConfiguracion() {
  if (WiFi.status() != WL_CONNECTED) return;
  
  String url = String(SERVER_URL) + "/api/esp32/config/" + String(DEVICE_ID);
  http.begin(url);
  
  int httpCode = http.GET();
  
  if (httpCode == 200) {
    String payload = http.getString();
    
    StaticJsonDocument<512> doc;
    DeserializationError error = deserializeJson(doc, payload);
    
    if (!error) {
      // Actualizar configuración dinámica
      if (doc.containsKey("latitude")) {
        config_dinamica.latitude = doc["latitude"];
        config_dinamica.longitude = doc["longitude"];
        
        #ifdef DEBUG_HTTP
        Serial.printf("📍 Ubicación actualizada: %.4f, %.4f\n", 
                      config_dinamica.latitude, config_dinamica.longitude);
        #endif
      }
      
      if (doc.containsKey("battery_capacity_wh")) {
        config_dinamica.battery_capacity_wh = doc["battery_capacity_wh"];
      }
      
      if (doc.containsKey("solar_area_m2")) {
        config_dinamica.solar_area_m2 = doc["solar_area_m2"];
      }
      
      if (doc.containsKey("wind_power_w")) {
        config_dinamica.wind_power_w = doc["wind_power_w"];
      }
      
      if (doc.containsKey("proteccion_activa")) {
        config_dinamica.proteccion_activa = doc["proteccion_activa"];
      }
    }
  }
  
  http.end();
}

// ===== VERIFICAR COMANDOS =====
void checkCommands() {
  if (WiFi.status() != WL_CONNECTED) return;
  
  // GET comandos
  String url = String(SERVER_URL) + "/api/esp32/commands/" + String(DEVICE_ID);
  http.begin(url);
  
  int httpCode = http.GET();
  
  if (httpCode == 200) {
    String payload = http.getString();
    
    // Parsear JSON
    StaticJsonDocument<512> doc;
    DeserializationError error = deserializeJson(doc, payload);
    
    if (!error) {
      JsonArray commands = doc["commands"];
      
      if (commands.size() > 0) {
        Serial.println("📥 Comandos recibidos:");
        
        for (JsonVariant cmdObj : commands) {
          String command = cmdObj["command"].as<String>();
          String param = cmdObj.containsKey("parameter") ? cmdObj["parameter"].as<String>() : "";
          
          Serial.printf("   - %s", command.c_str());
          if (param != "") Serial.printf(" (%s)", param.c_str());
          Serial.println();
          
          // Ejecutar comandos de relés
          if (ejecutarComandoRele(command, param)) {
            Serial.println("     ✅ Ejecutado");
          }
          // Comandos de sistema
          else if (command == "reboot") {
            Serial.println("🔄 Reiniciando en 3 segundos...");
            delay(3000);
            ESP.restart();
          }
          else if (command == "calibrate") {
            Serial.println("🔧 Calibrando sensores...");
            // TODO: Implementar calibración
          }
          else if (command == "get_config") {
            Serial.println("📥 Solicitando configuración...");
            getConfiguracion();
          }
          else if (command == "apagar_todo") {
            Serial.println("🚨 Apagando todo...");
            apagarTodo();
          }
          else if (command == "activar_freno") {
            Serial.println("🔥 Activando freno manual...");
            setRelayFreno(true);
          }
          else if (command == "desactivar_freno") {
            Serial.println("✅ Desactivando freno...");
            setRelayFreno(false);
          }
          else if (command == "estrategia_auto") {
            Serial.println("🤖 Aplicando estrategia automática...");
            aplicarEstrategia(sensores.soc, sensores.potencia_solar, 
                            sensores.potencia_eolica, sensores.potencia_consumo);
          }
          else {
            Serial.printf("     ⚠️  Comando desconocido\n");
          }
        }
      }
    }
  } else if (httpCode != 404) {  // 404 = no hay comandos (normal)
    #ifdef DEBUG_HTTP
    Serial.printf("❌ Error comandos: %d\n", httpCode);
    #endif
  }
  
  http.end();
}

#endif // HTTP_CLIENT_H
