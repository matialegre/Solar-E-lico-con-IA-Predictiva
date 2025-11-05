/**
 * @file config.h
 * @brief Configuración del sistema
 * 
 * ⚠️ EDITA ESTE ARCHIVO CON TUS DATOS
 */

#ifndef CONFIG_H
#define CONFIG_H

// ===== WiFi =====
#define WIFI_SSID "PANDEMONIUM"
#define WIFI_PASSWORD "PANDEMONIUM"
#define WIFI_TIMEOUT_MS 20000                 // 20 segundos

// ===== BACKEND (HTTP - SIN MQTT) =====
// Opción A: IP Pública (✅ CONFIGURADO)
#define SERVER_URL "http://190.211.201.217:11113"

// Opción B: Ngrok (para desarrollo/pruebas)
// #define SERVER_URL "https://argentina.ngrok.pro"

// Opción C: IP Local (solo si está en la misma red)
// #define SERVER_URL "http://localhost:11113"

#define DEVICE_ID "ESP32_INVERSOR_001"
#define SEND_INTERVAL 500                     // ⚡ Enviar datos cada 0.5 seg (TIEMPO REAL)
#define COMMAND_CHECK_INTERVAL 10000          // Verificar comandos cada 10 seg

// ===== STAGE 1: Intervals =====
#define STAGE1_INTERVAL 1000                  // Stage 1: Send every 1 second

// ===== PINES ADC (GPIO solo input) =====
#define PIN_VOLTAJE_BAT1    34  // ADC1_CH6 - Voltaje batería (único canal activo)
#define PIN_VOLTAJE_BAT2    34  // Reutilizado para evitar GPIO32/33 (no cableado)
#define PIN_VOLTAJE_BAT3    34  // Reutilizado para evitar GPIO32/33 (no cableado)
#define PIN_CORRIENTE_SOLAR 36  // ADC1_CH0 - Corriente solar (0–3.3V)
#define PIN_CORRIENTE_EOLICA 35 // ADC1_CH7 - Eólica (DC filtrado 0–3.3V)
#define PIN_CORRIENTE_CONSUMO 39 // ADC1_CH3 - Corriente consumo (shunt + OpAmp)
#define PIN_IRRADIANCIA     27  // GPIO27 - LDR (radiación solar) - MOVIDO de 25
#define PIN_VELOCIDAD_VIENTO 14 // GPIO14 - Anemómetro (pulsos) - MOVIDO de 26

// ===== PINES RELÉS (GPIO output) ===== 
// ⚠️ HARDWARE REAL: const uint8_t relays[] = {26, 25, 32, 33}
#define PIN_RELE_SOLAR      26  // GPIO26 - Relé panel solar (HARDWARE REAL)
#define PIN_RELE_EOLICA     25  // GPIO25 - Relé turbina eólica (HARDWARE REAL)
#define PIN_RELE_RED        32  // GPIO32 - Relé red backup (HARDWARE REAL)
#define PIN_RELE_CARGA      33  // GPIO33 - Relé carga (HARDWARE REAL)
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

// ===== RPM (frecuencia eléctrica -> RPM turbina) =====
// Señal 0–3 V: HIGH en semiciclo positivo, LOW en negativo.
// Contaremos flanco ascendente (RISING) => 1 flanco por ciclo eléctrico.
#define PIN_RPM_INPUT                  13      // GPIO para RPM (ajustar según hardware)
#define RPM_EDGES_PER_ELECTRICAL_CYCLE 1       // flancos útiles por ciclo eléctrico
#define RPM_MEASURE_WINDOW_MS          500     // ventana de integración (ms)
#define RPM_DEBOUNCE_US                500     // anti-rebote por ruido (µs)

// Conversión frecuencia eléctrica -> RPM mecánica:
//   RPM = (freq_electrica_Hz * 60) / POLE_PAIRS / GEAR_RATIO
#define TURBINE_POLE_PAIRS             10      // pares de polos del generador
#define TURBINE_GEAR_RATIO             1.0f    // 1.0 = acople directo

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
