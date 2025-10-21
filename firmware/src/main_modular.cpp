/**
 * @file main.cpp
 * @brief Sistema Inversor Inteligente Híbrido - Firmware ESP32
 * 
 * ARQUITECTURA MODULAR:
 * - sensors.cpp: Lectura de todos los sensores
 * - wifi_manager.cpp: Gestión WiFi y AP
 * - mqtt_client.cpp: Comunicación con backend
 * - web_server.cpp: Servidor web para configuración
 * - data_logger.cpp: Respaldo en SPIFFS
 */

#include <Arduino.h>
#include "config.h"
#include "sensors.h"
#include "wifi_manager.h"
#include "mqtt_client.h"
#include "web_server.h"
#include "data_logger.h"

// ===== OBJETOS GLOBALES =====
SensorsManager sensors;
WiFiManager wifiMgr;
MQTTClientManager mqttClient;
WebServerManager webServer;
DataLogger dataLogger;

// ===== CONFIGURACIÓN DE TAREAS =====
TaskHandle_t taskSensorsHandle;
TaskHandle_t taskCommunicationHandle;
TaskHandle_t taskMonitorHandle;

// ===== VARIABLES DE TIEMPO =====
unsigned long lastSensorRead = 0;
unsigned long lastMQTTSend = 0;
unsigned long lastWebUpdate = 0;
unsigned long lastLogSave = 0;

// ===== CONSTANTES =====
#define SENSOR_READ_INTERVAL 1000    // 1 segundo
#define MQTT_SEND_INTERVAL 5000      // 5 segundos
#define WEB_UPDATE_INTERVAL 2000     // 2 segundos
#define LOG_SAVE_INTERVAL 60000      // 1 minuto

// ===== PROTOTIPOS =====
void taskSensors(void *parameter);
void taskCommunication(void *parameter);
void taskMonitor(void *parameter);
void onMQTTMessage(String topic, String payload);
void printStartupInfo();

void setup() {
    Serial.begin(115200);
    delay(1000);
    
    Serial.println("\n\n");
    Serial.println("╔═══════════════════════════════════════════════════════════╗");
    Serial.println("║   🔋 SISTEMA INVERSOR INTELIGENTE HÍBRIDO - ESP32 🔋    ║");
    Serial.println("╚═══════════════════════════════════════════════════════════╝");
    Serial.println();
    
    // 1. Inicializar SPIFFS para logs
    Serial.println("📂 Inicializando SPIFFS...");
    if (!SPIFFS.begin(true)) {
        Serial.println("❌ Error montando SPIFFS");
    } else {
        Serial.println("✅ SPIFFS OK");
    }
    
    // 2. Inicializar sensores
    if (!sensors.begin()) {
        Serial.println("❌ Error crítico inicializando sensores");
        Serial.println("   Sistema en modo degradado");
    }
    
    // 3. Inicializar WiFi
    Serial.println("\n📡 Conectando WiFi...");
    if (!wifiMgr.begin(WIFI_SSID, WIFI_PASSWORD)) {
        Serial.println("⚠️  WiFi no conectado, iniciando modo AP");
    } else {
        Serial.printf("✅ WiFi conectado: %s\n", wifiMgr.getIPAddress().c_str());
        Serial.printf("   RSSI: %d dBm\n", wifiMgr.getRSSI());
    }
    
    // 4. Inicializar MQTT
    if (wifiMgr.isConnected()) {
        Serial.println("\n📤 Conectando MQTT...");
        if (mqttClient.begin(MQTT_SERVER, MQTT_PORT, DEVICE_ID)) {
            Serial.println("✅ MQTT conectado");
            mqttClient.onMessage(onMQTTMessage);
        } else {
            Serial.println("⚠️  MQTT no disponible");
        }
    }
    
    // 5. Inicializar servidor web
    Serial.println("\n🌐 Iniciando servidor web...");
    if (webServer.begin(&sensors)) {
        Serial.printf("✅ Servidor web en http://%s\n", wifiMgr.getIPAddress().c_str());
    }
    
    // 6. Inicializar data logger
    Serial.println("\n💾 Inicializando logger...");
    if (dataLogger.begin()) {
        Serial.println("✅ Logger OK");
    }
    
    // 7. Crear tareas FreeRTOS
    Serial.println("\n⚙️  Creando tareas...");
    
    xTaskCreatePinnedToCore(
        taskSensors,           // Función
        "Sensors",             // Nombre
        4096,                  // Stack size
        NULL,                  // Parámetros
        2,                     // Prioridad (alta)
        &taskSensorsHandle,    // Handle
        0                      // Core 0
    );
    
    xTaskCreatePinnedToCore(
        taskCommunication,
        "Communication",
        8192,
        NULL,
        1,                     // Prioridad media
        &taskCommunicationHandle,
        1                      // Core 1
    );
    
    xTaskCreatePinnedToCore(
        taskMonitor,
        "Monitor",
        2048,
        NULL,
        0,                     // Prioridad baja
        &taskMonitorHandle,
        1                      // Core 1
    );
    
    Serial.println("✅ Tareas creadas");
    
    // Información del sistema
    printStartupInfo();
    
    Serial.println("\n🚀 Sistema iniciado correctamente\n");
}

void loop() {
    // Loop vacío - todo en tareas FreeRTOS
    vTaskDelay(pdMS_TO_TICKS(1000));
}

// ===== TAREA 1: LECTURA DE SENSORES =====
void taskSensors(void *parameter) {
    Serial.println("✅ Tarea Sensores iniciada (Core 0)");
    
    for (;;) {
        unsigned long currentMillis = millis();
        
        if (currentMillis - lastSensorRead >= SENSOR_READ_INTERVAL) {
            // Leer todos los sensores
            SensorData data = sensors.readAll();
            lastSensorRead = currentMillis;
            
            // Guardar en log cada minuto
            if (currentMillis - lastLogSave >= LOG_SAVE_INTERVAL) {
                dataLogger.logData(data);
                lastLogSave = currentMillis;
            }
        }
        
        vTaskDelay(pdMS_TO_TICKS(100));
    }
}

// ===== TAREA 2: COMUNICACIÓN =====
void taskCommunication(void *parameter) {
    Serial.println("✅ Tarea Comunicación iniciada (Core 1)");
    
    for (;;) {
        unsigned long currentMillis = millis();
        
        // Mantener WiFi conectado
        wifiMgr.handle();
        
        // Manejar MQTT
        if (wifiMgr.isConnected()) {
            mqttClient.handle();
            
            // Publicar datos cada 5 segundos
            if (currentMillis - lastMQTTSend >= MQTT_SEND_INTERVAL) {
                if (mqttClient.isConnected()) {
                    SensorData data = sensors.getLastData();
                    mqttClient.publishSensorData(data);
                    lastMQTTSend = currentMillis;
                }
            }
        }
        
        // Servidor web
        webServer.handle();
        
        vTaskDelay(pdMS_TO_TICKS(100));
    }
}

// ===== TAREA 3: MONITOR DEL SISTEMA =====
void taskMonitor(void *parameter) {
    Serial.println("✅ Tarea Monitor iniciada (Core 1)");
    
    for (;;) {
        // Imprimir datos cada 10 segundos
        static unsigned long lastPrint = 0;
        unsigned long currentMillis = millis();
        
        if (currentMillis - lastPrint >= 10000) {
            sensors.printData();
            
            Serial.printf("\n📊 ESTADO DEL SISTEMA:\n");
            Serial.printf("   WiFi: %s (RSSI: %d dBm)\n", 
                wifiMgr.isConnected() ? "Conectado" : "Desconectado",
                wifiMgr.getRSSI());
            Serial.printf("   MQTT: %s\n", 
                mqttClient.isConnected() ? "Conectado" : "Desconectado");
            Serial.printf("   Logs: %lu registros\n", dataLogger.getLogCount());
            Serial.printf("   Uptime: %lu segundos\n", millis() / 1000);
            Serial.printf("   Free Heap: %u bytes\n", ESP.getFreeHeap());
            Serial.println();
            
            lastPrint = currentMillis;
        }
        
        vTaskDelay(pdMS_TO_TICKS(1000));
    }
}

// ===== CALLBACK MQTT =====
void onMQTTMessage(String topic, String payload) {
    Serial.printf("📩 MQTT recibido: %s\n", topic.c_str());
    Serial.printf("   Payload: %s\n", payload.c_str());
    
    // Parsear comandos
    StaticJsonDocument<512> doc;
    DeserializationError error = deserializeJson(doc, payload);
    
    if (error) {
        Serial.println("❌ Error parseando JSON");
        return;
    }
    
    // Procesar comandos
    if (topic.endsWith("/command")) {
        String cmd = doc["command"].as<String>();
        
        if (cmd == "calibrate_ldr") {
            sensors.calibrateLDR();
            mqttClient.publishStatus("LDR calibrado");
        }
        else if (cmd == "reset_wind") {
            sensors.resetWindCounter();
            mqttClient.publishStatus("Anemómetro reseteado");
        }
        else if (cmd == "clear_logs") {
            dataLogger.clearLog();
            mqttClient.publishStatus("Logs eliminados");
        }
        else if (cmd == "reboot") {
            mqttClient.publishStatus("Reiniciando...");
            delay(1000);
            ESP.restart();
        }
    }
}

// ===== INFO DEL SISTEMA =====
void printStartupInfo() {
    Serial.println("\n╔═══════════════════════════════════════════════════════════╗");
    Serial.println("║                   INFORMACIÓN DEL SISTEMA                  ║");
    Serial.println("╠═══════════════════════════════════════════════════════════╣");
    Serial.printf("║ Chip: %s                                        ║\n", ESP.getChipModel());
    Serial.printf("║ Cores: %d                                              ║\n", ESP.getChipCores());
    Serial.printf("║ Frecuencia: %d MHz                                   ║\n", ESP.getCpuFreqMHz());
    Serial.printf("║ Flash: %u bytes                                 ║\n", ESP.getFlashChipSize());
    Serial.printf("║ RAM: %u bytes                                   ║\n", ESP.getHeapSize());
    Serial.printf("║ RAM libre: %u bytes                             ║\n", ESP.getFreeHeap());
    Serial.printf("║ MAC: %s                        ║\n", WiFi.macAddress().c_str());
    Serial.println("╠═══════════════════════════════════════════════════════════╣");
    Serial.printf("║ Device ID: %-47s║\n", DEVICE_ID);
    Serial.printf("║ WiFi SSID: %-47s║\n", WIFI_SSID);
    if (wifiMgr.isConnected()) {
        Serial.printf("║ IP: %-54s║\n", wifiMgr.getIPAddress().c_str());
    }
    Serial.printf("║ MQTT Server: %-44s║\n", MQTT_SERVER);
    Serial.println("╚═══════════════════════════════════════════════════════════╝");
}
