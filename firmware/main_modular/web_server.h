/**
 * @file web_server.h
 * @brief Servidor web para configuración y monitoreo
 */

#ifndef WEB_SERVER_H
#define WEB_SERVER_H

#include <Arduino.h>
#include <ESPAsyncWebServer.h>
#include <ArduinoJson.h>
#include "config.h"
#include "sensors.h"

#define WEB_SERVER_PORT 80

class WebServerManager {
private:
    AsyncWebServer server;
    SensorsManager* sensors;
    
    void setupRoutes();
    void handleRoot(AsyncWebServerRequest *request);
    void handleSensorData(AsyncWebServerRequest *request);
    void handleConfig(AsyncWebServerRequest *request);
    void handleConfigPost(AsyncWebServerRequest *request);
    void handleNotFound(AsyncWebServerRequest *request);

public:
    WebServerManager();
    
    bool begin(SensorsManager* sensors_ptr);
    void handle();
};

#endif // WEB_SERVER_H
