/**
 * ╔════════════════════════════════════════════════════════════╗
 * ║   SISTEMA INVERSOR HÍBRIDO INTELIGENTE - ESP32            ║
 * ║   Firmware 2.0 - Solo ADC Interno + OpAmps                ║
 * ╚════════════════════════════════════════════════════════════╝
 * 
 * Hardware:
 * - ESP32 Dev Kit / WROOM-32
 * - ADC interno 12-bit (0-3.3V)
 * - Amplificadores operacionales (LM358, TL072, etc.)
 * - Divisores resistivos para voltajes
 * 
 * Autor: Tu equipo
 * Versión: 2.0
 * Fecha: 2025
 */

#include "config.h"
#include "sensors.h"
#include "wifi_manager.h"
#include "relays.h"
#include "protection.h"
#include "http_client.h"

// ===== VARIABLES GLOBALES =====
unsigned long lastSendTime = 0;
unsigned long lastCommandCheck = 0;
unsigned long lastConfigCheck = 0;
bool systemReady = false;
bool estrategiaAutoActiva = true;  // Estrategia automática por defecto

// ===== SETUP =====
void setup() {
  // Iniciar serial
  Serial.begin(115200);
  delay(1000);
  
  printHeader();
  
  // Inicializar sensores
  Serial.println("⚩️  Inicializando sensores ADC...");
  initSensors();
  Serial.println("✅ Sensores inicializados");
  
  // Inicializar relés
  Serial.println("⚩️  Inicializando relés...");
  initRelays();
  Serial.println("✅ Relés inicializados");
  
  // Inicializar protección
  Serial.println("⚩️  Inicializando sistema de protección...");
  initProtection();
  Serial.println("✅ Protección inicializada");
  
  // Conectar WiFi
  Serial.println("📡 Conectando WiFi...");
  if (connectWiFi()) {
    Serial.println("✅ WiFi conectado");
    Serial.print("   IP: ");
    Serial.println(WiFi.localIP());
    Serial.print("   RSSI: ");
    Serial.print(WiFi.RSSI());
    Serial.println(" dBm");
  } else {
    Serial.println("❌ Error WiFi - reiniciando...");
    ESP.restart();
  }
  
  // Configurar HTTP
  Serial.println("🌐 Configurando cliente HTTP...");
  initHTTP();
  Serial.println("✅ Cliente HTTP listo");
  
  // Registrar dispositivo en servidor
  Serial.println("📝 Registrando dispositivo en servidor...");
  if (registerDevice()) {
    Serial.println("✅ Dispositivo registrado");
  } else {
    Serial.println("⚠️  Error al registrar (continuando de todas formas)");
  }
  
  // Obtener configuración inicial del servidor
  Serial.println("📥 Obteniendo configuración del servidor...");
  getConfiguracion();
  Serial.printf("✅ Ubicación: %.4f, %.4f\n", config_dinamica.latitude, config_dinamica.longitude);
  
  Serial.println("\n╔════════════════════════════════════════╗");
  Serial.println("║   ✅ SISTEMA INICIADO CORRECTAMENTE   ║");
  Serial.println("╚════════════════════════════════════════╝");
  Serial.println();
  Serial.println("📊 ESTADO INICIAL:");
  Serial.printf("   Device ID: %s\n", DEVICE_ID);
  Serial.printf("   IP Local: %s\n", WiFi.localIP().toString().c_str());
  Serial.printf("   MAC: %s\n", WiFi.macAddress().c_str());
  Serial.printf("   Backend: %s\n", SERVER_URL);
  Serial.printf("   Lat/Lon: %.4f, %.4f\n", config_dinamica.latitude, config_dinamica.longitude);
  Serial.printf("   Batería: %.0f Wh\n", config_dinamica.battery_capacity_wh);
  Serial.printf("   Protección: %s\n", config_dinamica.proteccion_activa ? "ACTIVA" : "INACTIVA");
  Serial.printf("   Estrategia auto: %s\n", estrategiaAutoActiva ? "SI" : "NO");
  Serial.println("\n⏰ Intervalo telemetría: 5 seg");
  Serial.println("⏰ Intervalo comandos: 10 seg");
  Serial.println("⏰ Heartbeat: 30 seg");
  Serial.println();
  
  systemReady = true;
}

// ===== LOOP PRINCIPAL =====
void loop() {
  // Verificar WiFi
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("⚠️  WiFi desconectado - reconectando...");
    connectWiFi();
  }
  
  // Leer sensores constantemente
  readAllSensors();
  
  // Monitorear protección contra embalamiento
  if (config_dinamica.proteccion_activa) {
    monitorearProteccion();
  }
  
  // Aplicar estrategia automática si está activa
  if (estrategiaAutoActiva) {
    static unsigned long lastEstrategia = 0;
    if (millis() - lastEstrategia >= 5000) {  // Cada 5 segundos
      aplicarEstrategia(sensores.soc, sensores.potencia_solar, 
                       sensores.potencia_eolica, sensores.potencia_consumo);
      lastEstrategia = millis();
    }
  }
  
  // Enviar telemetría cada SEND_INTERVAL
  if (millis() - lastSendTime >= SEND_INTERVAL) {
    sendTelemetry();
    lastSendTime = millis();
  }
  
  // Verificar comandos cada COMMAND_CHECK_INTERVAL
  if (millis() - lastCommandCheck >= COMMAND_CHECK_INTERVAL) {
    checkCommands();
    lastCommandCheck = millis();
  }
  
  // Heartbeat cada 30 segundos
  static unsigned long lastHeartbeat = 0;
  if (millis() - lastHeartbeat >= 30000) {
    sendHeartbeat();
    lastHeartbeat = millis();
  }
  
  // Actualizar configuración cada 5 minutos
  if (millis() - lastConfigCheck >= 300000) {  // 5 minutos
    getConfiguracion();
    lastConfigCheck = millis();
  }
  
  // Delay corto para no saturar
  delay(100);
}

// ===== FUNCIONES AUXILIARES =====

void printHeader() {
  Serial.println("\n\n");
  Serial.println("╔════════════════════════════════════════════════════════════╗");
  Serial.println("║   🔋 SISTEMA INVERSOR HÍBRIDO INTELIGENTE - ESP32 🔋     ║");
  Serial.println("║                    Firmware 2.0                           ║");
  Serial.println("╚════════════════════════════════════════════════════════════╝");
  Serial.println();
  Serial.print("   Device ID: ");
  Serial.println(DEVICE_ID);
  Serial.print("   Backend:   ");
  Serial.println(SERVER_URL);
  Serial.println();
}
