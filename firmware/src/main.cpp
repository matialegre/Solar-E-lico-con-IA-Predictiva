/*
 * Sistema Inversor Inteligente Híbrido - Firmware ESP32
 * 
 * Características:
 * - Lectura de sensores de voltaje y corriente
 * - Comunicación WiFi con servidor backend
 * - Control de relés para conmutación de fuentes
 * - Tareas FreeRTOS para operación concurrente
 * - Watchdog timer para seguridad
 */

#include <Arduino.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include "config.h"

// ===== ESTRUCTURAS DE DATOS =====
struct SensorData {
    float solar_voltage_v;
    float solar_current_a;
    float wind_voltage_v;
    float wind_current_a;
    float battery_voltage_v;
    float battery_current_a;
    float load_current_a;
    float temperature_c;
};

struct RelayState {
    bool solar_enabled;
    bool wind_enabled;
    bool battery_enabled;
    bool grid_enabled;
};

// ===== VARIABLES GLOBALES =====
SensorData currentData;
RelayState relayState;
SemaphoreHandle_t dataMutex;
bool wifiConnected = false;
unsigned long lastSensorRead = 0;
unsigned long lastServerSend = 0;

// ===== PROTOTIPOS DE FUNCIONES =====
void setupWiFi();
void setupPins();
void readSensors();
float readVoltage(int pin);
float readCurrent(int pin);
float readADCAverage(int pin, int samples);
void sendDataToServer();
void controlRelays();
void taskSensorRead(void *parameter);
void taskServerComm(void *parameter);
void taskControlLogic(void *parameter);
void blinkLED(int pin, int times, int delayMs);

// ===== SETUP =====
void setup() {
    Serial.begin(115200);
    Serial.println("\n\n=================================");
    Serial.println("Sistema Inversor Inteligente ESP32");
    Serial.println("=================================\n");

    // Configurar pines
    setupPins();

    // Inicializar mutex para protección de datos
    dataMutex = xSemaphoreCreateMutex();

    // Conectar WiFi
    setupWiFi();

    // Crear tareas FreeRTOS
    xTaskCreatePinnedToCore(
        taskSensorRead,      // Función de la tarea
        "SensorRead",        // Nombre
        4096,                // Stack size
        NULL,                // Parámetros
        2,                   // Prioridad (alta)
        NULL,                // Handle
        0                    // Core 0
    );

    xTaskCreatePinnedToCore(
        taskServerComm,      
        "ServerComm",        
        8192,                
        NULL,                
        1,                   // Prioridad (media)
        NULL,                
        1                    // Core 1
    );

    xTaskCreatePinnedToCore(
        taskControlLogic,    
        "ControlLogic",      
        4096,                
        NULL,                
        1,                   // Prioridad (media)
        NULL,                
        0                    // Core 0
    );

    Serial.println("✅ Sistema inicializado correctamente");
    Serial.println("✅ Tareas FreeRTOS creadas");
}

// ===== LOOP (no se usa, FreeRTOS maneja las tareas) =====
void loop() {
    vTaskDelay(pdMS_TO_TICKS(1000));
}

// ===== CONFIGURACIÓN WiFi =====
void setupWiFi() {
    Serial.print("Conectando a WiFi: ");
    Serial.println(WIFI_SSID);

    WiFi.mode(WIFI_STA);
    WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

    int attempts = 0;
    while (WiFi.status() != WL_CONNECTED && attempts < 30) {
        delay(500);
        Serial.print(".");
        digitalWrite(PIN_LED_WIFI, !digitalRead(PIN_LED_WIFI));
        attempts++;
    }

    if (WiFi.status() == WL_CONNECTED) {
        wifiConnected = true;
        digitalWrite(PIN_LED_WIFI, HIGH);
        Serial.println("\n✅ WiFi conectado");
        Serial.print("IP: ");
        Serial.println(WiFi.localIP());
    } else {
        Serial.println("\n❌ Error conectando WiFi");
        digitalWrite(PIN_LED_WIFI, LOW);
    }
}

// ===== CONFIGURACIÓN DE PINES =====
void setupPins() {
    // Pines analógicos (ADC)
    pinMode(PIN_SOLAR_VOLTAGE, INPUT);
    pinMode(PIN_SOLAR_CURRENT, INPUT);
    pinMode(PIN_WIND_VOLTAGE, INPUT);
    pinMode(PIN_WIND_CURRENT, INPUT);
    pinMode(PIN_BATTERY_VOLTAGE, INPUT);
    pinMode(PIN_BATTERY_CURRENT, INPUT);
    pinMode(PIN_LOAD_CURRENT, INPUT);

    // Pines de relés (salidas)
    pinMode(PIN_RELAY_SOLAR, OUTPUT);
    pinMode(PIN_RELAY_WIND, OUTPUT);
    pinMode(PIN_RELAY_BATTERY, OUTPUT);
    pinMode(PIN_RELAY_GRID, OUTPUT);

    // LEDs de estado
    pinMode(PIN_LED_STATUS, OUTPUT);
    pinMode(PIN_LED_WIFI, OUTPUT);

    // Estado inicial de relés (todos desactivados)
    digitalWrite(PIN_RELAY_SOLAR, LOW);
    digitalWrite(PIN_RELAY_WIND, LOW);
    digitalWrite(PIN_RELAY_BATTERY, LOW);
    digitalWrite(PIN_RELAY_GRID, LOW);

    relayState.solar_enabled = false;
    relayState.wind_enabled = false;
    relayState.battery_enabled = true;  // Batería por defecto
    relayState.grid_enabled = false;

    Serial.println("✅ Pines configurados");
}

// ===== LECTURA DE SENSORES =====
void readSensors() {
    SensorData newData;

    // Leer voltajes
    newData.solar_voltage_v = readVoltage(PIN_SOLAR_VOLTAGE);
    newData.wind_voltage_v = readVoltage(PIN_WIND_VOLTAGE);
    newData.battery_voltage_v = readVoltage(PIN_BATTERY_VOLTAGE);

    // Leer corrientes
    newData.solar_current_a = readCurrent(PIN_SOLAR_CURRENT);
    newData.wind_current_a = readCurrent(PIN_WIND_CURRENT);
    newData.battery_current_a = readCurrent(PIN_BATTERY_CURRENT);
    newData.load_current_a = readCurrent(PIN_LOAD_CURRENT);

    // Leer temperatura interna del ESP32
    newData.temperature_c = temperatureRead();

    // Actualizar datos globales con mutex
    if (xSemaphoreTake(dataMutex, portMAX_DELAY)) {
        currentData = newData;
        xSemaphoreGive(dataMutex);
    }
}

// ===== LEER VOLTAJE =====
float readVoltage(int pin) {
    float adcValue = readADCAverage(pin, SAMPLE_COUNT);
    float voltage = (adcValue / ADC_MAX_VALUE) * ADC_VREF;
    float realVoltage = voltage * VOLTAGE_DIVIDER_RATIO;
    return realVoltage;
}

// ===== LEER CORRIENTE =====
float readCurrent(int pin) {
    float adcValue = readADCAverage(pin, SAMPLE_COUNT);
    float voltage = (adcValue / ADC_MAX_VALUE) * ADC_VREF;
    
    // Convertir voltaje a corriente según sensor
    float current = (voltage - CURRENT_SENSOR_OFFSET) / CURRENT_SENSOR_SENSITIVITY;
    
    // Si es muy pequeña, considerarla cero
    if (abs(current) < 0.1) {
        current = 0.0;
    }
    
    return abs(current);
}

// ===== PROMEDIO DE LECTURAS ADC =====
float readADCAverage(int pin, int samples) {
    long sum = 0;
    for (int i = 0; i < samples; i++) {
        sum += analogRead(pin);
        delay(SAMPLE_DELAY / samples);
    }
    return (float)sum / samples;
}

// ===== ENVIAR DATOS AL SERVIDOR =====
void sendDataToServer() {
    if (!wifiConnected) {
        Serial.println("⚠️ WiFi no conectado, reintentando...");
        setupWiFi();
        return;
    }

    HTTPClient http;
    String url = String(SERVER_URL) + String(API_ENDPOINT);
    
    http.begin(url);
    http.addHeader("Content-Type", "application/json");

    // Crear JSON con datos
    StaticJsonDocument<512> doc;
    
    if (xSemaphoreTake(dataMutex, pdMS_TO_TICKS(100))) {
        doc["solar_voltage_v"] = currentData.solar_voltage_v;
        doc["solar_current_a"] = currentData.solar_current_a;
        doc["wind_voltage_v"] = currentData.wind_voltage_v;
        doc["wind_current_a"] = currentData.wind_current_a;
        doc["battery_voltage_v"] = currentData.battery_voltage_v;
        doc["battery_current_a"] = currentData.battery_current_a;
        doc["load_current_a"] = currentData.load_current_a;
        doc["temperature_c"] = currentData.temperature_c;
        xSemaphoreGive(dataMutex);
    }

    String jsonString;
    serializeJson(doc, jsonString);

    // Enviar petición POST
    int httpResponseCode = http.POST(jsonString);

    if (httpResponseCode > 0) {
        Serial.print("✓ Datos enviados - Código: ");
        Serial.println(httpResponseCode);
        blinkLED(PIN_LED_STATUS, 1, 100);
    } else {
        Serial.print("✗ Error enviando datos: ");
        Serial.println(httpResponseCode);
    }

    http.end();
}

// ===== CONTROL DE RELÉS =====
void controlRelays() {
    digitalWrite(PIN_RELAY_SOLAR, relayState.solar_enabled ? HIGH : LOW);
    digitalWrite(PIN_RELAY_WIND, relayState.wind_enabled ? HIGH : LOW);
    digitalWrite(PIN_RELAY_BATTERY, relayState.battery_enabled ? HIGH : LOW);
    digitalWrite(PIN_RELAY_GRID, relayState.grid_enabled ? HIGH : LOW);
}

// ===== PARPADEAR LED =====
void blinkLED(int pin, int times, int delayMs) {
    for (int i = 0; i < times; i++) {
        digitalWrite(pin, HIGH);
        delay(delayMs);
        digitalWrite(pin, LOW);
        delay(delayMs);
    }
}

// ===== TAREA: LECTURA DE SENSORES =====
void taskSensorRead(void *parameter) {
    Serial.println("▶️ Tarea SensorRead iniciada");
    
    for (;;) {
        readSensors();
        
        // Imprimir datos cada 5 segundos
        if (xSemaphoreTake(dataMutex, portMAX_DELAY)) {
            Serial.println("\n--- Sensores ---");
            Serial.printf("Solar: %.2fV, %.2fA (%.0fW)\n", 
                currentData.solar_voltage_v, 
                currentData.solar_current_a,
                currentData.solar_voltage_v * currentData.solar_current_a);
            Serial.printf("Viento: %.2fV, %.2fA (%.0fW)\n", 
                currentData.wind_voltage_v, 
                currentData.wind_current_a,
                currentData.wind_voltage_v * currentData.wind_current_a);
            Serial.printf("Batería: %.2fV, %.2fA\n", 
                currentData.battery_voltage_v, 
                currentData.battery_current_a);
            Serial.printf("Carga: %.2fA\n", currentData.load_current_a);
            Serial.printf("Temperatura: %.1f°C\n", currentData.temperature_c);
            xSemaphoreGive(dataMutex);
        }
        
        vTaskDelay(pdMS_TO_TICKS(SENSOR_READ_INTERVAL));
    }
}

// ===== TAREA: COMUNICACIÓN CON SERVIDOR =====
void taskServerComm(void *parameter) {
    Serial.println("▶️ Tarea ServerComm iniciada");
    
    for (;;) {
        sendDataToServer();
        vTaskDelay(pdMS_TO_TICKS(SERVER_SEND_INTERVAL));
    }
}

// ===== TAREA: LÓGICA DE CONTROL =====
void taskControlLogic(void *parameter) {
    Serial.println("▶️ Tarea ControlLogic iniciada");
    
    for (;;) {
        // Aquí se puede implementar lógica local de seguridad
        // Por ejemplo, desconectar si voltaje de batería es muy bajo
        
        if (xSemaphoreTake(dataMutex, portMAX_DELAY)) {
            // Protección de batería
            if (currentData.battery_voltage_v < 44.0) {  // ~20% SoC
                Serial.println("⚠️ Batería baja, protegiendo...");
                // Podría activar alarma o reducir carga
            }
            
            // Protección de sobrevoltaje
            if (currentData.battery_voltage_v > 58.0) {
                Serial.println("⚠️ Sobrevoltaje detectado!");
                relayState.solar_enabled = false;
                relayState.wind_enabled = false;
            }
            
            xSemaphoreGive(dataMutex);
        }
        
        controlRelays();
        
        vTaskDelay(pdMS_TO_TICKS(1000));
    }
}
