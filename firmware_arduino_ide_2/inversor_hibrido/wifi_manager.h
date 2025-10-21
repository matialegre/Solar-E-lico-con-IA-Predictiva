/**
 * @file wifi_manager.h
 * @brief Gestión de conexión WiFi
 */

#ifndef WIFI_MANAGER_H
#define WIFI_MANAGER_H

#include <WiFi.h>
#include "config.h"

bool connectWiFi() {
  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  
  #ifdef DEBUG_WIFI
  Serial.print("   Conectando");
  #endif
  
  unsigned long startTime = millis();
  while (WiFi.status() != WL_CONNECTED) {
    if (millis() - startTime > WIFI_TIMEOUT_MS) {
      #ifdef DEBUG_WIFI
      Serial.println(" ❌ Timeout");
      #endif
      return false;
    }
    
    delay(500);
    #ifdef DEBUG_WIFI
    Serial.print(".");
    #endif
  }
  
  #ifdef DEBUG_WIFI
  Serial.println(" ✅");
  #endif
  
  return true;
}

void checkWiFi() {
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("⚠️  WiFi perdido - reconectando...");
    connectWiFi();
  }
}

#endif // WIFI_MANAGER_H
