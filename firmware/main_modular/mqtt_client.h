/**
 * @file mqtt_client.h
 * @brief Cliente MQTT para comunicación con el backend
 */

#ifndef MQTT_CLIENT_H
#define MQTT_CLIENT_H

#include <Arduino.h>
#include <PubSubClient.h>
#include <WiFi.h>
#include <ArduinoJson.h>
#include "config.h"
#include "sensors.h"

#define MQTT_RECONNECT_INTERVAL 5000  // 5 segundos
#define MQTT_QOS 1
#define MQTT_RETAIN false

class MQTTClientManager {
private:
    WiFiClient wifi_client;
    PubSubClient mqtt_client;
    String device_id;
    unsigned long last_reconnect_attempt;
    
    // Topics
    String topic_telemetry;
    String topic_command;
    String topic_status;
    String topic_config;
    
    // Callbacks
    void (*message_callback)(String topic, String payload);
    
    bool reconnect();
    static void mqttCallback(char* topic, byte* payload, unsigned int length);
    static MQTTClientManager* instance;

public:
    MQTTClientManager();
    
    bool begin(const char* server, int port, const char* device_id);
    void handle();
    bool isConnected();
    
    // Publicar
    bool publishSensorData(const SensorData& data);
    bool publishStatus(const String& status);
    bool publishAlert(const String& message);
    
    // Suscribirse
    void onMessage(void (*callback)(String topic, String payload));
    
    // Reconexión
    void setReconnectInterval(unsigned long interval);
};

#endif // MQTT_CLIENT_H
