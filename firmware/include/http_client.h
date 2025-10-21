/**
 * @file http_client.h
 * @brief Cliente HTTP/HTTPS para enviar telemetría al servidor
 * 
 * SIN MQTT - Solo protocolo IP (HTTP/WebSocket)
 */

#ifndef HTTP_CLIENT_H
#define HTTP_CLIENT_H

#include <Arduino.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include "config.h"
#include "sensors.h"

#define HTTP_TIMEOUT 10000  // 10 segundos
#define HTTP_SEND_INTERVAL 5000  // 5 segundos

class HTTPClientManager {
private:
    HTTPClient http;
    String server_url;
    String device_id;
    unsigned long last_send_time;
    unsigned long last_command_check;
    
    // Contadores
    unsigned long successful_sends;
    unsigned long failed_sends;
    
    bool sendPOST(const String& endpoint, const String& payload);
    String sendGET(const String& endpoint);

public:
    HTTPClientManager();
    
    bool begin(const char* server_url, const char* device_id);
    void handle();
    
    // Enviar datos
    bool sendTelemetry(const SensorData& data);
    bool sendStatus(const String& status);
    bool sendAlert(const String& message);
    
    // Recibir comandos (polling)
    String checkForCommands();
    
    // Estadísticas
    void getStats(unsigned long& sent, unsigned long& failed);
};

#endif // HTTP_CLIENT_H
