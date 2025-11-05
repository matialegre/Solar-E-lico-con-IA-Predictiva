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
  // Configurar timeout (15s para evitar GET -7)
  http.setTimeout(15000);
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
  
  // Crear JSON Stage 1 (con raw_adc para depuración de GPIOs)
  StaticJsonDocument<768> doc;
  doc["device_id"] = DEVICE_ID;
  doc["seq"] = stage1_seq;
  doc["ts"] = millis() / 1000;  // epoch en segundos
  doc["v_bat_v"] = sensores.v_bat_v;
  doc["v_wind_v_dc"] = sensores.v_wind_v_dc;
  doc["v_solar_v"] = sensores.v_solar_v;
  doc["v_load_v"] = sensores.v_load_v;

  // Añadir raw_adc (0–3.3V y raw) igual que en sendTelemetry()
  JsonObject raw_adc = doc.createNestedObject("raw_adc");
  raw_adc["adc1_bat1"] = (sensores.adc_bat1 * 3.3) / 4095.0;
  raw_adc["adc1_bat1_raw"] = sensores.adc_bat1;
  raw_adc["adc2_bat2"] = (sensores.adc_bat2 * 3.3) / 4095.0;
  raw_adc["adc2_bat2_raw"] = sensores.adc_bat2;
  raw_adc["adc3_bat3"] = (sensores.adc_bat3 * 3.3) / 4095.0;
  raw_adc["adc3_bat3_raw"] = sensores.adc_bat3;
  raw_adc["adc4_solar"] = (sensores.adc_solar * 3.3) / 4095.0;
  raw_adc["adc4_solar_raw"] = sensores.adc_solar;
  raw_adc["adc5_wind"] = (sensores.adc_eolica * 3.3) / 4095.0;
  raw_adc["adc5_wind_raw"] = sensores.adc_eolica;
  raw_adc["adc6_load"] = (sensores.adc_consumo * 3.3) / 4095.0;
  raw_adc["adc6_load_raw"] = sensores.adc_consumo;
  
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
    String payload = http.getString();
    
    // Parsear primero el payload completo (sin truncar) para no romper JSON
    StaticJsonDocument<512> doc;
    DeserializationError error = deserializeJson(doc, payload);
    
    if (!error) {
      // Mensaje simple cuando no hay comandos
      if (doc.containsKey("status")) {
        String st = doc["status"].as<String>();
        if (st == "OK") {
          last_get_resp = "{\"status\":\"OK\",\"commands\":[]}";
          Serial.println("MENSAJE DE SERVIDOR: OK");
        }
      }
      
      // Ejecutar comandos si existen
      if (doc.containsKey("commands")) {
        JsonArray commands = doc["commands"];
        if (commands.size() > 0) {
          // Construir una respuesta corta para el log UART
          last_get_resp = "{\\\"status\\\":\\\"CMD\\\",\\\"count\\\":" + String(commands.size()) + "}";
          
          for (JsonVariant cmdObj : commands) {
            String command = cmdObj["command"].as<String>();
            String param = cmdObj.containsKey("parameter") ? cmdObj["parameter"].as<String>() : "";
            
            // Mensaje humano en serie (SUPER VISIBLE)
            Serial.println();
            Serial.println("***************************************");
            if (command == "eolica") {
              Serial.printf(">>> %s RELE EOLICO <<<\n", (param == "on" || param == "1") ? "PRENDER" : "APAGAR");
            } else if (command == "solar") {
              Serial.printf(">>> %s RELE SOLAR <<<\n", (param == "on" || param == "1") ? "PRENDER" : "APAGAR");
            } else if (command == "red") {
              Serial.printf(">>> %s RELE RED <<<\n", (param == "on" || param == "1") ? "PRENDER" : "APAGAR");
            } else if (command == "carga") {
              Serial.printf(">>> %s RELE CARGA <<<\n", (param == "on" || param == "1") ? "PRENDER" : "APAGAR");
            } else if (command == "freno") {
              Serial.printf(">>> %s FRENO <<<\n", (param == "on" || param == "1") ? "ACTIVAR" : "DESACTIVAR");
            } else if (command == "reboot") {
              Serial.println(">>> REINICIAR ESP (3s) <<<");
            } else {
              Serial.printf(">>> COMANDO: %s (%s) <<<\n", command.c_str(), param.c_str());
            }
            Serial.println("***************************************");
            Serial.println();
            
            // Ejecutar comandos (reusa lógica existente)
            if (!ejecutarComandoRele(command, param)) {
              if (command == "reboot") {
                delay(3000);
                ESP.restart();
              }
            }
          }
        }
      }
    } else {
      last_get_resp = "{\"status\":\"ERROR\",\"parse\":1}";
    }
    
    // Truncar SOLO para la impresión UART (no para parseo)
    if (last_get_resp.length() > 80) {
      last_get_resp = last_get_resp.substring(0, 77) + "...";
    }
  } else {
    last_get_resp = "{\"status\":\"ERROR\",\"code\":" + String(httpCode) + "}";
  }
  
  http.end();
}

// ===== STAGE 1: UART print VISUAL MUY CLARO =====
void printStage1UART() {
  static unsigned long lastDetailPrint = 0;
  unsigned long now = millis();
  
  // Cada 5 segundos: Imprimir detalle COMPLETO
  if (now - lastDetailPrint >= 5000) {
    Serial.println();
    Serial.println("╔════════════════════════════════════════════════════════════════╗");
    Serial.print("║  📊 TELEMETRÍA #");
    Serial.print(stage1_seq);
    Serial.print(" | Uptime: ");
    Serial.print(millis()/1000);
    Serial.println("s                             ║");
    Serial.println("╠════════════════════════════════════════════════════════════════╣");
    
    // ADCs RAW (0-3.3V)
    Serial.println("║  📍 ADCs RAW (0-3.3V REALES):                                  ║");
    Serial.print("║    GPIO34 (Batería):  ");
    Serial.print(sensores.v_bat_v, 3);
    Serial.print("V  [raw: ");
    Serial.print(sensores.adc_bat1);
    Serial.println("/4095]              ║");
    
    Serial.print("║    GPIO35 (Eólica):   ");
    Serial.print(sensores.v_wind_v_dc, 3);
    Serial.print("V  [raw: ");
    Serial.print(sensores.adc_eolica);
    Serial.println("/4095]              ║");
    
    Serial.print("║    GPIO36 (Solar):    ");
    Serial.print(sensores.v_solar_v, 3);
    Serial.print("V  [raw: ");
    Serial.print(sensores.adc_solar);
    Serial.println("/4095]              ║");
    
    Serial.print("║    GPIO39 (Carga):    ");
    Serial.print(sensores.v_load_v, 3);
    Serial.print("V  [raw: ");
    Serial.print(sensores.adc_consumo);
    Serial.println("/4095]              ║");
    
    Serial.println("╠════════════════════════════════════════════════════════════════╣");
    
    // RPM y Frecuencia
    Serial.println("║  🎯 RPM TURBINA:                                               ║");
    Serial.print("║    RPM: ");
    Serial.print(sensores.turbine_rpm, 1);
    Serial.print(" RPM  |  Frecuencia: ");
    Serial.print(sensores.frequency_hz, 2);
    Serial.println(" Hz               ║");
    
    Serial.println("╠════════════════════════════════════════════════════════════════╣");
    
    // Relés
    Serial.print("║  🔌 RELÉS: [");
    Serial.print(relay_state.solar_conectado ? "✓" : "✗");
    Serial.print("] Solar  [");
    Serial.print(relay_state.eolica_conectada ? "✓" : "✗");
    Serial.print("] Eólica  [");
    Serial.print(relay_state.red_conectada ? "✓" : "✗");
    Serial.print("] Red  [");
    Serial.print(relay_state.carga_conectada ? "✓" : "✗");
    Serial.println("] Carga  ║");
    
    Serial.println("╠════════════════════════════════════════════════════════════════╣");
    
    // Estado HTTP
    Serial.print("║  🌐 HTTP: POST ");
    Serial.print(last_post_code);
    Serial.print("  GET ");
    Serial.print(last_get_code);
    Serial.print("  |  WiFi RSSI: ");
    Serial.print(WiFi.RSSI());
    Serial.println(" dBm          ║");
    
    Serial.println("╚════════════════════════════════════════════════════════════════╝");
    Serial.println();
    
    lastDetailPrint = now;
  } else {
    // Modo COMPACTO cada envío (0.5s)
    Serial.print("⚡[");
    Serial.print(stage1_seq);
    Serial.print("] ");
    Serial.print(sensores.v_bat_v, 3);
    Serial.print("V ");
    Serial.print(sensores.v_wind_v_dc, 3);
    Serial.print("V ");
    Serial.print(sensores.v_solar_v, 3);
    Serial.print("V ");
    Serial.print(sensores.v_load_v, 3);
    Serial.print("V | RPM:");
    Serial.print(sensores.turbine_rpm, 0);
    Serial.print(" | POST:");
    Serial.println(last_post_code);
  }
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
  
  // RPM turbina eólica
  doc["turbine_rpm"] = sensores.turbine_rpm;
  doc["rpm"] = sensores.turbine_rpm;  // Legacy compatibility
  doc["frequency_hz"] = sensores.frequency_hz;
  
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
  
  // GPIO34 - Batería (ADC1_CH6)
  raw_adc["adc1_bat1"] = (sensores.adc_bat1 * 3.3) / 4095.0;
  raw_adc["adc1_bat1_raw"] = sensores.adc_bat1;
  
  // GPIO35 - Eólica DC (ADC1_CH7)
  raw_adc["adc2_eolica"] = (sensores.adc_eolica * 3.3) / 4095.0;
  raw_adc["adc2_eolica_raw"] = sensores.adc_eolica;
  
  // GPIO36 - Solar (ADC1_CH0)
  raw_adc["adc5_solar"] = (sensores.adc_solar * 3.3) / 4095.0;
  raw_adc["adc5_solar_raw"] = sensores.adc_solar;
  
  // GPIO39 - Carga/Load (ADC1_CH3)
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
  
  // Debug desactivado para no bombardear serial
  // #ifdef DEBUG_HTTP
  // if (httpCode > 0) {
  //   Serial.printf("📤 Telemetría enviada: %d\n", httpCode);
  // } else {
  //   Serial.printf("❌ Error HTTP: %s\n", http.errorToString(httpCode).c_str());
  // }
  // #endif
  
  http.end();
}

// ===== OBTENER CONFIGURACIÓN DEL SERVIDOR =====
void getConfiguracion() {
  if (WiFi.status() != WL_CONNECTED) return;
  
  String url = String(SERVER_URL) + "/api/esp32/config/" + String(DEVICE_ID);
  http.begin(url);
  
  int httpCode = http.GET();
  last_get_code = httpCode;
  
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
        last_get_resp = "{\\\"status\\\":\\\"CMD\\\",\\\"count\\\":" + String(commands.size()) + "}";
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
      else {
        // Sin comandos
        last_get_resp = "{\\\"status\\\":\\\"OK\\\",\\\"commands\\\":[]}";
      }
    }
  } else if (httpCode != 404) {  // 404 = no hay comandos (normal)
#ifdef DEBUG_HTTP
    Serial.printf("❌ Error comandos: %d\n", httpCode);
#endif
    last_get_resp = "{\"status\":\"ERROR\",\"code\":" + String(httpCode) + "}";
  }
  
  http.end();
}

#endif // HTTP_CLIENT_H
