/**
 * @file wifi_manager.h
 * @brief Gestión de conexión WiFi y modo AP
 */

#ifndef WIFI_MANAGER_H
#define WIFI_MANAGER_H

#include <Arduino.h>
#include <WiFi.h>
#include <DNSServer.h>
#include "config.h"

#define WIFI_CONNECT_TIMEOUT 20000  // 20 segundos
#define WIFI_CHECK_INTERVAL 30000   // 30 segundos

class WiFiManager {
private:
    String ssid;
    String password;
    bool ap_mode;
    DNSServer dns_server;
    unsigned long last_check_time;
    
    void startAPMode();
    void connectToWiFi();

public:
    WiFiManager();
    
    bool begin(const char* ssid, const char* password);
    void handle();
    bool isConnected();
    bool isAPMode();
    String getIPAddress();
    int getRSSI();
    void disconnect();
    void reconnect();
    
    // Configuración
    void setCredentials(const char* ssid, const char* password);
};

#endif // WIFI_MANAGER_H
