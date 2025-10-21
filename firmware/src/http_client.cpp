/**
 * @file http_client.cpp
 * @brief Implementación del cliente HTTP
 */

#include "../include/http_client.h"

HTTPClientManager::HTTPClientManager() {
    last_send_time = 0;
    last_command_check = 0;
    successful_sends = 0;
    failed_sends = 0;
}

bool HTTPClientManager::begin(const char* url, const char* id) {
    server_url = String(url);
    device_id = String(id);
    
    Serial.println("📡 Cliente HTTP configurado");
    Serial.printf("   Servidor: %s\n", server_url.c_str());
    Serial.printf("   Device ID: %s\n", device_id.c_str());
    
    return true;
}

void HTTPClientManager::handle() {
    unsigned long current_time = millis();
    
    // Verificar comandos pendientes cada 10 segundos
    if (current_time - last_command_check >= 10000) {
        String commands = checkForCommands();
        if (commands.length() > 0) {
            Serial.printf("📩 Comandos recibidos: %s\n", commands.c_str());
            // Aquí procesarías los comandos
        }
        last_command_check = current_time;
    }
}

bool HTTPClientManager::sendTelemetry(const SensorData& data) {
    // Crear JSON con datos de sensores
    StaticJsonDocument<1024> doc;
    
    doc["device_id"] = device_id;
    doc["timestamp"] = millis();
    
    // Solar
    JsonObject solar = doc.createNestedObject("solar");
    solar["voltage"] = data.solar_voltage_v;
    solar["current"] = data.solar_current_a;
    solar["power"] = data.solar_power_w;
    solar["irradiance"] = data.irradiance_w_m2;
    
    // Eólico
    JsonObject wind = doc.createNestedObject("wind");
    wind["voltage"] = data.wind_voltage_v;
    wind["current"] = data.wind_current_a;
    wind["power"] = data.wind_power_w;
    wind["wind_speed"] = data.wind_speed_ms;
    
    // Batería
    JsonObject battery = doc.createNestedObject("battery");
    battery["voltage"] = data.battery_voltage_v;
    battery["current"] = data.battery_current_a;
    battery["power"] = data.battery_power_w;
    battery["soc"] = data.battery_soc_percent;
    
    // Otros
    doc["temperature_c"] = data.temperature_c;
    
    // Serializar
    String payload;
    serializeJson(doc, payload);
    
    // Enviar POST
    bool success = sendPOST("/api/esp32/telemetry", payload);
    
    if (success) {
        successful_sends++;
        Serial.println("✅ Telemetría enviada");
    } else {
        failed_sends++;
        Serial.println("❌ Error enviando telemetría");
    }
    
    last_send_time = millis();
    return success;
}

bool HTTPClientManager::sendStatus(const String& status) {
    StaticJsonDocument<256> doc;
    doc["device_id"] = device_id;
    doc["status"] = status;
    doc["timestamp"] = millis();
    
    String payload;
    serializeJson(doc, payload);
    
    return sendPOST("/api/esp32/status", payload);
}

bool HTTPClientManager::sendAlert(const String& message) {
    StaticJsonDocument<256> doc;
    doc["device_id"] = device_id;
    doc["alert"] = message;
    doc["timestamp"] = millis();
    
    String payload;
    serializeJson(doc, payload);
    
    return sendPOST("/api/esp32/alert", payload);
}

String HTTPClientManager::checkForCommands() {
    String endpoint = "/api/esp32/commands/" + device_id;
    return sendGET(endpoint);
}

bool HTTPClientManager::sendPOST(const String& endpoint, const String& payload) {
    String url = server_url + endpoint;
    
    http.begin(url);
    http.addHeader("Content-Type", "application/json");
    http.setTimeout(HTTP_TIMEOUT);
    
    int httpCode = http.POST(payload);
    
    bool success = (httpCode == 200 || httpCode == 201);
    
    if (!success) {
        Serial.printf("❌ HTTP POST error: %d\n", httpCode);
    }
    
    http.end();
    return success;
}

String HTTPClientManager::sendGET(const String& endpoint) {
    String url = server_url + endpoint;
    
    http.begin(url);
    http.setTimeout(HTTP_TIMEOUT);
    
    int httpCode = http.GET();
    
    String response = "";
    if (httpCode == 200) {
        response = http.getString();
    } else {
        Serial.printf("❌ HTTP GET error: %d\n", httpCode);
    }
    
    http.end();
    return response;
}

void HTTPClientManager::getStats(unsigned long& sent, unsigned long& failed) {
    sent = successful_sends;
    failed = failed_sends;
}
