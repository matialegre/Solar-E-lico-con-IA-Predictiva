/**
 * @file sensors.h
 * @brief Lectura de sensores con ADC interno ESP32
 * 
 * Hardware:
 * - ADC interno 12-bit (0-4095) → 0-3.3V
 * - Divisores resistivos para voltajes altos
 * - Shunts + OpAmps para corriente
 */

#ifndef SENSORS_H
#define SENSORS_H

#include <Arduino.h>
#include "config.h"

// ===== BIQUAD IIR FILTER (2nd order low-pass for wind DC extraction) =====
struct Biquad {
  float a1 = 0, a2 = 0;
  float b0 = 0, b1 = 0, b2 = 0;
  float z1 = 0, z2 = 0;
};

// Create 2nd-order Butterworth low-pass filter (TPT bilinear)
Biquad make_lp(float fs, float fc, float Q = 0.707f) {
  float K = tanf(PI * fc / fs);
  float norm = 1.0f / (1.0f + K / Q + K * K);
  Biquad b;
  b.b0 = (K * K) * norm;
  b.b1 = 2.0f * b.b0;
  b.b2 = b.b0;
  b.a1 = 2.0f * (K * K - 1.0f) * norm;
  b.a2 = (1.0f - K / Q + K * K) * norm;
  return b;
}

// Process one sample through biquad filter
inline float biquad_process(Biquad &f, float x) {
  float y = f.b0 * x + f.b1 * f.z1 + f.b2 * f.z2 - f.a1 * f.z1 - f.a2 * f.z2;
  f.z2 = f.z1;
  f.z1 = y;
  return y;
}

// ===== VARIABLES GLOBALES =====
struct SensorData {
  // Voltajes (V)
  float voltaje_bat1;
  float voltaje_bat2;
  float voltaje_bat3;
  float voltaje_promedio;
  
  // Corrientes (A)
  float corriente_solar;
  float corriente_eolica;
  float corriente_consumo;
  
  // Potencias (W)
  float potencia_solar;
  float potencia_eolica;
  float potencia_consumo;
  
  // Ambiente
  float irradiancia;        // W/m²
  float velocidad_viento;   // m/s
  
  // Estado batería
  float soc;                // % (0-100)
  float temperatura;        // °C (simulado si no hay sensor)
  
  // ===== VALORES RAW DE ADCs (para debug y calibración) =====
  int adc_bat1;             // Valor raw ADC batería 1 (0-4095)
  int adc_bat2;             // Valor raw ADC batería 2 (0-4095)
  int adc_bat3;             // Valor raw ADC batería 3 (0-4095)
  int adc_solar;            // Valor raw ADC corriente solar (0-4095)
  int adc_eolica;           // Valor raw ADC corriente eólica (0-4095)
  int adc_consumo;          // Valor raw ADC corriente consumo (0-4095)
  int adc_ldr;              // Valor raw ADC LDR irradiancia (0-4095)
  
  // ===== STAGE 1: Voltajes 0-3.3V sin calibración =====
  float v_bat_v;            // Voltaje batería raw (0-3.3V)
  float v_wind_v_dc;        // Voltaje eólica DC filtrado (0-3.3V)
  float v_solar_v;          // Voltaje solar raw (0-3.3V)
  float v_load_v;           // Voltaje consumo raw (0-3.3V)
};

SensorData sensores;

// Biquad filter for wind channel (fs=1000Hz, fc=10Hz, Q=0.707)
Biquad wind_lp;

// ===== CONTADORES PARA ANEMÓMETRO =====
volatile unsigned long windPulseCount = 0;
unsigned long lastWindTime = 0;

// ===== ISR ANEMÓMETRO =====
void IRAM_ATTR windPulseISR() {
  windPulseCount++;
}

// ===== INICIALIZACIÓN =====
void initSensors() {
  // Configurar ADC
  analogReadResolution(12);  // 12-bit (0-4095)
  analogSetAttenuation(ADC_11db);  // 0-3.3V
  
  // Configurar pin anemómetro
  pinMode(PIN_VELOCIDAD_VIENTO, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(PIN_VELOCIDAD_VIENTO), windPulseISR, FALLING);
  
  // Inicializar datos
  memset(&sensores, 0, sizeof(sensores));
  lastWindTime = millis();
  
  // Inicializar filtro biquad para viento (fs=1000Hz, fc=10Hz, Q=0.707)
  wind_lp = make_lp(1000.0f, 10.0f, 0.707f);
}

// ===== LECTURA VOLTAJES =====
float leerVoltaje(int pin, int* raw_out = nullptr) {
  int raw = analogRead(pin);
  
  // Guardar valor RAW si se proporciona puntero
  if (raw_out != nullptr) {
    *raw_out = raw;
  }
  
  // Detectar sensor no conectado (pin flotante genera valores muy bajos)
  if (raw < 100) {  // Menos de ~0.08V indica sensor desconectado
    return 0.0;
  }
  
  float voltaje = raw * VOLTAJE_FACTOR;
  
  // Validar rango realista para batería 48V (40V - 60V)
  if (voltaje < 10.0 || voltaje > 65.0) {
    return 0.0;  // Fuera de rango = no conectado
  }
  
  #ifdef DEBUG_SENSORS
  // Serial.printf("ADC[%d]: %d → %.2fV\n", pin, raw, voltaje);
  #endif
  
  return voltaje;
}

// ===== LECTURA CORRIENTES =====
float leerCorriente(int pin, int* raw_out = nullptr) {
  // Leer múltiples muestras para estabilidad
  const int muestras = 10;
  long suma = 0;
  
  for (int i = 0; i < muestras; i++) {
    suma += analogRead(pin);
    delayMicroseconds(100);
  }
  
  int raw = suma / muestras;
  
  // Guardar valor RAW si se proporciona puntero
  if (raw_out != nullptr) {
    *raw_out = raw;
  }
  
  // Eliminar offset (0A está en CORRIENTE_OFFSET ~2048)
  int raw_offset = raw - CORRIENTE_OFFSET;
  
  // Convertir a corriente (shunt 300A)
  float corriente = abs(raw_offset) * CORRIENTE_FACTOR;
  
  // Determinar dirección (positivo = generando, negativo = consumiendo)
  if (raw_offset < -10) corriente = -corriente;  // Threshold para evitar ruido
  
  // Filtrar ruido bajo
  if (abs(corriente) < 0.5) corriente = 0;
  
  return corriente;
}

// ===== LECTURA IRRADIANCIA =====
float leerIrradiancia(int pin, int* raw_out = nullptr) {
  int raw = analogRead(pin);
  
  // Guardar valor RAW si se proporciona puntero
  if (raw_out != nullptr) {
    *raw_out = raw;
  }
  
  float irradiancia = raw * IRRADIANCIA_FACTOR;
  return irradiancia;
}

// ===== CALCULAR RPM =====
float calcularRPM() {
  unsigned long now = millis();
  unsigned long elapsed = now - lastWindTime;
  
  if (elapsed >= 1000) {
    float rps = (float)windPulseCount / (elapsed / 1000.0);
    float rpm = rps * 60.0;
    return rpm;
  }
  
  return 0;
}

// ===== LECTURA VELOCIDAD VIENTO =====
float leerVelocidadViento() {
  unsigned long now = millis();
  unsigned long elapsed = now - lastWindTime;
  
  if (elapsed >= 1000) {  // Calcular cada 1 segundo
    float rps = (float)windPulseCount / (elapsed / 1000.0);  // Rev por segundo
    float velocidad = (2.0 * PI * VIENTO_RADIO_M * rps * VIENTO_FACTOR_CORRECCION);  // m/s
    
    windPulseCount = 0;
    lastWindTime = now;
    
    return velocidad;
  }
  
  return sensores.velocidad_viento;  // Mantener último valor
}

// ===== CALCULAR SOC =====
float calcularSOC(float voltaje) {
  if (voltaje <= BATTERY_VOLTAGE_MIN) return 0.0;
  if (voltaje >= BATTERY_VOLTAGE_MAX) return 100.0;
  
  float soc = ((voltaje - BATTERY_VOLTAGE_MIN) / (BATTERY_VOLTAGE_MAX - BATTERY_VOLTAGE_MIN)) * 100.0;
  return constrain(soc, 0.0, 100.0);
}

// ===== LEER TODOS LOS SENSORES =====
void readAllSensors() {
  // Voltajes (guardar valores RAW también)
  sensores.voltaje_bat1 = leerVoltaje(PIN_VOLTAJE_BAT1, &sensores.adc_bat1);
  sensores.voltaje_bat2 = leerVoltaje(PIN_VOLTAJE_BAT2, &sensores.adc_bat2);
  sensores.voltaje_bat3 = leerVoltaje(PIN_VOLTAJE_BAT3, &sensores.adc_bat3);
  
  // Calcular promedio solo de sensores conectados
  int sensores_activos = 0;
  float suma_voltajes = 0;
  if (sensores.voltaje_bat1 > 0) { suma_voltajes += sensores.voltaje_bat1; sensores_activos++; }
  if (sensores.voltaje_bat2 > 0) { suma_voltajes += sensores.voltaje_bat2; sensores_activos++; }
  if (sensores.voltaje_bat3 > 0) { suma_voltajes += sensores.voltaje_bat3; sensores_activos++; }
  
  sensores.voltaje_promedio = (sensores_activos > 0) ? (suma_voltajes / sensores_activos) : 0.0;
  
  // Corrientes (guardar valores RAW también)
  sensores.corriente_solar = leerCorriente(PIN_CORRIENTE_SOLAR, &sensores.adc_solar);
  sensores.corriente_eolica = leerCorriente(PIN_CORRIENTE_EOLICA, &sensores.adc_eolica);
  sensores.corriente_consumo = leerCorriente(PIN_CORRIENTE_CONSUMO, &sensores.adc_consumo);
  
  // Potencias
  sensores.potencia_solar = sensores.voltaje_promedio * sensores.corriente_solar;
  sensores.potencia_eolica = sensores.voltaje_promedio * sensores.corriente_eolica;
  sensores.potencia_consumo = sensores.voltaje_promedio * sensores.corriente_consumo;
  
  // Ambiente (guardar valor RAW del LDR también)
  sensores.irradiancia = leerIrradiancia(PIN_IRRADIANCIA, &sensores.adc_ldr);
  sensores.velocidad_viento = leerVelocidadViento();
  
  // Estado batería
  sensores.soc = calcularSOC(sensores.voltaje_promedio);
  sensores.temperatura = 25.0;  // Simulado (agregar DS18B20 si querés)
  
  // ===== STAGE 1: Leer voltajes raw 0-3.3V (sin calibración) =====
  // Batería: promedio de los 3 canales convertidos a 0-3.3V
  sensores.v_bat_v = ((sensores.adc_bat1 + sensores.adc_bat2 + sensores.adc_bat3) / 3.0f) * 3.3f / 4095.0f;
  
  // Eólica: aplicar filtro biquad para extraer DC (cada llamada a readAllSensors)
  float v_wind_raw = sensores.adc_eolica * 3.3f / 4095.0f;
  sensores.v_wind_v_dc = biquad_process(wind_lp, v_wind_raw);
  
  // Solar: directo
  sensores.v_solar_v = sensores.adc_solar * 3.3f / 4095.0f;
  
  // Consumo: directo
  sensores.v_load_v = sensores.adc_consumo * 3.3f / 4095.0f;
  
  // Debug de sensores desactivado para no bombardear serial
  // #ifdef DEBUG_SENSORS
  // static unsigned long lastDebug = 0;
  // if (millis() - lastDebug >= 5000) {
  //   float rpm = calcularRPM();
  //   Serial.println("\n📊 SENSORES:");
  //   Serial.printf("   Voltaje: %.2fV | SOC: %.1f%% | Temp: %.1f°C\n", 
  //                 sensores.voltaje_promedio, sensores.soc, sensores.temperatura);
  //   Serial.printf("   Solar:   %.2fA / %.0fW\n", sensores.corriente_solar, sensores.potencia_solar);
  //   Serial.printf("   Eólica:  %.2fA / %.0fW\n", sensores.corriente_eolica, sensores.potencia_eolica);
  //   Serial.printf("   Consumo: %.2fA / %.0fW\n", sensores.corriente_consumo, sensores.potencia_consumo);
  //   Serial.printf("   Viento:  %.1f m/s (%.0f RPM) | Luz: %.0f W/m²\n\n", 
  //                 sensores.velocidad_viento, rpm, sensores.irradiancia);
  //   lastDebug = millis();
  // }
  // #endif
}

#endif // SENSORS_H
