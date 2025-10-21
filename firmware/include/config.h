#ifndef CONFIG_H
#define CONFIG_H

// ===== CONFIGURACIÓN WiFi =====
#define WIFI_SSID "TU_WIFI_SSID"
#define WIFI_PASSWORD "TU_WIFI_PASSWORD"

// ===== CONFIGURACIÓN DEL SERVIDOR =====
#define SERVER_URL "http://192.168.1.100:8000"
#define API_ENDPOINT "/api/energy/record"

// ===== PINES ANALÓGICOS (ADC) =====
#define PIN_SOLAR_VOLTAGE 34      // ADC1_CH6
#define PIN_SOLAR_CURRENT 35      // ADC1_CH7
#define PIN_WIND_VOLTAGE 32       // ADC1_CH4
#define PIN_WIND_CURRENT 33       // ADC1_CH5
#define PIN_BATTERY_VOLTAGE 25    // ADC2_CH8
#define PIN_BATTERY_CURRENT 26    // ADC2_CH9
#define PIN_LOAD_CURRENT 27       // ADC2_CH7

// ===== PINES DIGITALES (CONTROL) =====
#define PIN_RELAY_SOLAR 12
#define PIN_RELAY_WIND 13
#define PIN_RELAY_BATTERY 14
#define PIN_RELAY_GRID 15

// ===== PINES DE ESTADO =====
#define PIN_LED_STATUS 2
#define PIN_LED_WIFI 4

// ===== CALIBRACIÓN DE SENSORES =====
// Sensores de voltaje (divisor resistivo)
#define VOLTAGE_DIVIDER_RATIO 11.0  // Ej: 100k/10k = 11
#define ADC_MAX_VALUE 4095.0
#define ADC_VREF 3.3

// Sensores de corriente (ACS712 o similar)
#define CURRENT_SENSOR_SENSITIVITY 0.066  // 66mV/A para ACS712-30A
#define CURRENT_SENSOR_OFFSET 2.5         // Offset de 2.5V (sin corriente)

// ===== CONFIGURACIÓN DEL SISTEMA =====
#define SENSOR_READ_INTERVAL 5000    // Leer sensores cada 5s
#define SERVER_SEND_INTERVAL 10000   // Enviar al servidor cada 10s
#define WATCHDOG_TIMEOUT 30          // Timeout del watchdog en segundos

// ===== FILTRADO Y PROMEDIADO =====
#define SAMPLE_COUNT 10              // Muestras para promediar
#define SAMPLE_DELAY 50              // ms entre muestras

// ===== CONFIGURACIÓN MQTT (OPCIONAL) =====
#define USE_MQTT false
#define MQTT_BROKER "192.168.1.100"
#define MQTT_PORT 1883
#define MQTT_TOPIC_DATA "inversor/data"
#define MQTT_TOPIC_CONTROL "inversor/control"

#endif
