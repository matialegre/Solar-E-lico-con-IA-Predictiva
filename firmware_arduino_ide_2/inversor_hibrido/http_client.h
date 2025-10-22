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

// ===== STAGE 1: Variables globales =====
static uint32_t stage1_seq = 0;           // Sequence number
static uint32_t stage1_uplink_lost = 0;   // Total packets lost
static int last_post_code = 0;            // Last POST HTTP code
static int last_get_code = 0;             // Last GET HTTP code
static String last_get_resp = "";         // Last GET response

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
  
  // SIEMPRE mostrar resultado (sin #ifdef DEBUG_HTTP)
  Serial.println("\n================================================");
  if (success) {
    Serial.println("✅ ¡CONEXIÓN EXITOSA CON EL SERVIDOR!");
    Serial.println("================================================");
    Serial.printf("   📡 Dispositivo: %s\n", DEVICE_ID);
    Serial.printf("   🌐 Servidor: %s\n", SERVER_URL);
    Serial.printf("   ✅ Código HTTP: %d (OK)\n", httpCode);
    Serial.println("   🔗 El servidor confirmó el registro");
    Serial.println("================================================\n");
  } else {
    Serial.println("❌ ERROR AL CONECTAR CON EL SERVIDOR");
    Serial.println("================================================");
    Serial.printf("   📡 Dispositivo: %s\n", DEVICE_ID);
    Serial.printf("   🌐 Servidor: %s\n", SERVER_URL);
    Serial.printf("   ❌ Código HTTP: %d\n", httpCode);
    Serial.println("   ⚠️  Verifica que el servidor esté corriendo");
    Serial.println("================================================\n");
  }
  
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

// ===== STAGE 1: Enviar telemetría simplificada =====
void sendStage1Telemetry() {
  if (WiFi.status() != WL_CONNECTED) {
    last_post_code = -1;
    return;
  }
  
  // Crear JSON Stage 1 (minimal)
  StaticJsonDocument<256> doc;
  doc["device_id"] = DEVICE_ID;
  doc["seq"] = stage1_seq;
  doc["ts"] = millis() / 1000;  // epoch en segundos
  doc["v_bat_v"] = sensores.v_bat_v;
  doc["v_wind_v_dc"] = sensores.v_wind_v_dc;
  doc["v_solar_v"] = sensores.v_solar_v;
  doc["v_load_v"] = sensores.v_load_v;
  
  String jsonString;
  serializeJson(doc, jsonString);
  
  String url = String(SERVER_URL) + "/api/esp32/telemetry";
  http.begin(url);
  http.addHeader("Content-Type", "application/json");
  
  int httpCode = http.POST(jsonString);
  last_post_code = httpCode;
  
  // Si éxito (2xx), incrementar seq. Si error, mantener seq para retry
  if (httpCode >= 200 && httpCode < 300) {
    stage1_seq++;
  }
  
  http.end();
}

// ===== STAGE 1: Verificar comandos =====
void checkStage1Commands() {
  if (WiFi.status() != WL_CONNECTED) {
    last_get_code = -1;
    last_get_resp = "{\"status\":\"ERROR\"}";
    return;
  }
  
  String url = String(SERVER_URL) + "/api/esp32/commands/" + String(DEVICE_ID);
  http.begin(url);
  
  int httpCode = http.GET();
  last_get_code = httpCode;
  
  if (httpCode == 200) {
    last_get_resp = http.getString();
    
    // Truncar respuesta si es muy larga
    if (last_get_resp.length() > 80) {
      last_get_resp = last_get_resp.substring(0, 77) + "...";
    }
    
    // Parsear y ejecutar comandos si existen
    StaticJsonDocument<512> doc;
    DeserializationError error = deserializeJson(doc, last_get_resp);
    
    if (!error && doc.containsKey("commands")) {
      JsonArray commands = doc["commands"];
      for (JsonVariant cmdObj : commands) {
        String command = cmdObj["command"].as<String>();
        String param = cmdObj.containsKey("parameter") ? cmdObj["parameter"].as<String>() : "";
        
        // Ejecutar comandos (reusa lógica existente)
        if (command == "reboot") {
          delay(3000);
          ESP.restart();
        }
      }
    }
  } else {
    last_get_resp = "{\"status\":\"ERROR\",\"code\":" + String(httpCode) + "}";
  }
  
  http.end();
}

// ===== STAGE 1: UART print =====
void printStage1UART() {
  // Línea 1: Datos de sensores
  Serial.print("[ESP32] seq=");
  Serial.print(stage1_seq);
  Serial.print("  Vbat=");
  Serial.print(sensores.v_bat_v, 3);
  Serial.print("V  Vwind_DC=");
  Serial.print(sensores.v_wind_v_dc, 3);
  Serial.print("V  Vsolar=");
  Serial.print(sensores.v_solar_v, 3);
  Serial.print("V  Vload=");
  Serial.print(sensores.v_load_v, 3);
  Serial.println("V");
  
  // Línea 2: Estado HTTP
  Serial.print("POST ");
  Serial.print(last_post_code);
  Serial.print(" | GET ");
  Serial.print(last_get_code);
  Serial.print(" | Resp=");
  Serial.print(last_get_resp);
  Serial.print(" | Lost=");
  Serial.println(stage1_uplink_lost);
}

// ===== ENVIAR TELEMETRÍA ORIGINAL (mantener para compatibilidad) =====
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
  
  // ===== VALORES RAW DE ADCs (0-3.3V REALES) =====
  JsonObject raw_adc = doc.createNestedObject("raw_adc");
  
  // ADC1 - Batería 1 (GPIO34)
  raw_adc["adc1_bat1"] = (sensores.adc_bat1 * 3.3) / 4095.0;
  raw_adc["adc1_bat1_raw"] = sensores.adc_bat1;
  
  // ADC2 - Batería 2 (GPIO35)
  raw_adc["adc2_bat2"] = (sensores.adc_bat2 * 3.3) / 4095.0;
  raw_adc["adc2_bat2_raw"] = sensores.adc_bat2;
  
  // ADC3 - Batería 3 (GPIO32)
  raw_adc["adc3_bat3"] = (sensores.adc_bat3 * 3.3) / 4095.0;
  raw_adc["adc3_bat3_raw"] = sensores.adc_bat3;
  
  // ADC4 - Corriente Solar (GPIO33)
  raw_adc["adc4_solar"] = (sensores.adc_solar * 3.3) / 4095.0;
  raw_adc["adc4_solar_raw"] = sensores.adc_solar;
  
  // ADC5 - Corriente Eólica (GPIO36)
  raw_adc["adc5_wind"] = (sensores.adc_eolica * 3.3) / 4095.0;
  raw_adc["adc5_wind_raw"] = sensores.adc_eolica;
  
  // ADC6 - Corriente Consumo (GPIO39)
  raw_adc["adc6_load"] = (sensores.adc_consumo * 3.3) / 4095.0;
  raw_adc["adc6_load_raw"] = sensores.adc_consumo;
  
  // ADC7 - LDR Irradiancia (GPIO25)
  raw_adc["adc7_ldr"] = (sensores.adc_ldr * 3.3) / 4095.0;
  raw_adc["adc7_ldr_raw"] = sensores.adc_ldr;
  
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
