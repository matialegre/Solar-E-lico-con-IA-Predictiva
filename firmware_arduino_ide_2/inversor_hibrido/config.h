/**
 * @file config.h
 * @brief Configuración del sistema
 * 
 * ⚠️ EDITA ESTE ARCHIVO CON TUS DATOS
 */

#ifndef CONFIG_H
#define CONFIG_H

// ===== WiFi =====
#define WIFI_SSID "TU_RED_WIFI"              // ← CAMBIAR
#define WIFI_PASSWORD "TU_PASSWORD"           // ← CAMBIAR
#define WIFI_TIMEOUT_MS 20000                 // 20 segundos

// ===== BACKEND (HTTP - SIN MQTT) =====
// Opción A: IP Pública (recomendado)
#define SERVER_URL "http://190.211.201.217:11113"

// Opción B: Ngrok (desarrollo)
// #define SERVER_URL "https://argentina.ngrok.pro"

// Opción C: IP Local (misma red)
// #define SERVER_URL "http://192.168.0.100:11113"

#define DEVICE_ID "ESP32_INVERSOR_001"
#define SEND_INTERVAL 5000                    // Enviar datos cada 5 seg
#define COMMAND_CHECK_INTERVAL 10000          // Verificar comandos cada 10 seg

// ===== PINES ADC (GPIO solo input) =====
#define PIN_VOLTAJE_BAT1    34  // ADC1_CH6 - Voltaje batería 1
#define PIN_VOLTAJE_BAT2    35  // ADC1_CH7 - Voltaje batería 2  
#define PIN_VOLTAJE_BAT3    32  // ADC1_CH4 - Voltaje batería 3
#define PIN_CORRIENTE_SOLAR 33  // ADC1_CH5 - Corriente solar (shunt + OpAmp)
#define PIN_CORRIENTE_EOLICA 36 // ADC1_CH0 - Corriente eólica (shunt + OpAmp)
#define PIN_CORRIENTE_CONSUMO 39 // ADC1_CH3 - Corriente consumo (shunt + OpAmp)
#define PIN_IRRADIANCIA     25  // ADC2_CH8 - LDR (radiación solar)
#define PIN_VELOCIDAD_VIENTO 26 // GPIO - Anemómetro (pulsos)

// ===== PINES RELÉS (GPIO output) =====
#define PIN_RELE_SOLAR      16  // GPIO16 - Relé panel solar
#define PIN_RELE_EOLICA     17  // GPIO17 - Relé turbina eólica
#define PIN_RELE_RED        18  // GPIO18 - Relé red backup
#define PIN_RELE_CARGA      19  // GPIO19 - Relé carga
#define PIN_RELE_FRENO      23  // GPIO23 - Relé resistencia frenado (embalamiento)

// ===== CALIBRACIÓN ADC =====
// ADC ESP32: 12-bit (0-4095) → 0-3.3V

// Voltaje batería (0-60V con divisor 100k/10k)
#define VOLTAJE_FACTOR 0.01465  // (3.3V / 4095) * 11

// Corriente con SHUNT 300A (75mV @ 300A + OpAmp ganancia 44x)
// 75mV * 44 = 3.3V → 300A
#define CORRIENTE_FACTOR 0.0732  // 300A / 4095
#define CORRIENTE_OFFSET 2048     // ADC en 0A está en ~2048

// Irradiancia (LDR 0-3.3V → 0-1200 W/m²)
#define IRRADIANCIA_FACTOR 0.293  // 1200 / 4095

// Velocidad viento (Reed switch + imán)
#define VIENTO_PULSOS_POR_REV 1
#define VIENTO_RADIO_M 0.1  // 10cm
#define VIENTO_FACTOR_CORRECCION 1.18  // Factor para viento real

// ===== SISTEMA =====
#define BATTERY_CAPACITY_WH 5000.0
#define SOLAR_PANEL_AREA_M2 16.0
#define WIND_TURBINE_POWER_W 2000.0
#define BATTERY_VOLTAGE_MIN 44.0
#define BATTERY_VOLTAGE_MAX 54.0
#define BATTERY_VOLTAGE_NOMINAL 48.0

// ===== PROTECCIÓN EMBALAMIENTO =====
#define MAX_VIENTO_MS 25.0        // Máx velocidad viento segura (m/s)
#define MAX_VOLTAJE_V 65.0        // Máx voltaje turbina (V)
#define MAX_RPM 500               // Máx RPM turbina
#define FRENO_ACTIVACION_DELAY 2000  // Delay antes de activar freno (ms)
#define RESISTENCIA_FRENADO_OHM 10.0 // Resistencia frenado (Ω)
#define RESISTENCIA_MAX_W 2000.0     // Potencia máx resistencia (W)

// ===== ESTRATEGIA BATERÍA =====
#define SOC_MIN_DESCARGA 25.0     // No descargar bajo 25%
#define SOC_MAX_CARGA 80.0        // No cargar sobre 80%
#define SOC_CRITICO 10.0          // Nivel crítico

// ===== DEBUG =====
#define DEBUG_SENSORS true
#define DEBUG_WIFI true
#define DEBUG_HTTP true
#define DEBUG_RELAYS true
#define DEBUG_PROTECTION true

// ===== CONFIGURACIÓN DINÁMICA =====
// Estos valores se pueden actualizar desde el servidor
struct ConfigDinamica {
  float latitude;
  float longitude;
  float battery_capacity_wh;
  float solar_area_m2;
  float wind_power_w;
  bool proteccion_activa;
  bool aprendizaje_activo;
};

extern ConfigDinamica config_dinamica;

#endif // CONFIG_H
