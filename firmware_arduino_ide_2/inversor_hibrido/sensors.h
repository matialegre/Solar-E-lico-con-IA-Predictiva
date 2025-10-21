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
};

SensorData sensores;

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
}

// ===== LECTURA VOLTAJES =====
float leerVoltaje(int pin) {
  int raw = analogRead(pin);
  float voltaje = raw * VOLTAJE_FACTOR;
  
  #ifdef DEBUG_SENSORS
  // Serial.printf("ADC[%d]: %d → %.2fV\n", pin, raw, voltaje);
  #endif
  
  return voltaje;
}

// ===== LECTURA CORRIENTES =====
float leerCorriente(int pin) {
  // Leer múltiples muestras para estabilidad
  const int muestras = 10;
  long suma = 0;
  
  for (int i = 0; i < muestras; i++) {
    suma += analogRead(pin);
    delayMicroseconds(100);
  }
  
  int raw = suma / muestras;
  
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
float leerIrradiancia(int pin) {
  int raw = analogRead(pin);
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
  // Voltajes
  sensores.voltaje_bat1 = leerVoltaje(PIN_VOLTAJE_BAT1);
  sensores.voltaje_bat2 = leerVoltaje(PIN_VOLTAJE_BAT2);
  sensores.voltaje_bat3 = leerVoltaje(PIN_VOLTAJE_BAT3);
  sensores.voltaje_promedio = (sensores.voltaje_bat1 + sensores.voltaje_bat2 + sensores.voltaje_bat3) / 3.0;
  
  // Corrientes
  sensores.corriente_solar = leerCorriente(PIN_CORRIENTE_SOLAR);
  sensores.corriente_eolica = leerCorriente(PIN_CORRIENTE_EOLICA);
  sensores.corriente_consumo = leerCorriente(PIN_CORRIENTE_CONSUMO);
  
  // Potencias
  sensores.potencia_solar = sensores.voltaje_promedio * sensores.corriente_solar;
  sensores.potencia_eolica = sensores.voltaje_promedio * sensores.corriente_eolica;
  sensores.potencia_consumo = sensores.voltaje_promedio * sensores.corriente_consumo;
  
  // Ambiente
  sensores.irradiancia = leerIrradiancia(PIN_IRRADIANCIA);
  sensores.velocidad_viento = leerVelocidadViento();
  
  // Estado batería
  sensores.soc = calcularSOC(sensores.voltaje_promedio);
  sensores.temperatura = 25.0;  // Simulado (agregar DS18B20 si querés)
  
  #ifdef DEBUG_SENSORS
  static unsigned long lastDebug = 0;
  if (millis() - lastDebug >= 5000) {
    float rpm = calcularRPM();
    Serial.println("\n📊 SENSORES:");
    Serial.printf("   Voltaje: %.2fV | SOC: %.1f%% | Temp: %.1f°C\n", 
                  sensores.voltaje_promedio, sensores.soc, sensores.temperatura);
    Serial.printf("   Solar:   %.2fA / %.0fW\n", sensores.corriente_solar, sensores.potencia_solar);
    Serial.printf("   Eólica:  %.2fA / %.0fW\n", sensores.corriente_eolica, sensores.potencia_eolica);
    Serial.printf("   Consumo: %.2fA / %.0fW\n", sensores.corriente_consumo, sensores.potencia_consumo);
    Serial.printf("   Viento:  %.1f m/s (%.0f RPM) | Luz: %.0f W/m²\n\n", 
                  sensores.velocidad_viento, rpm, sensores.irradiancia);
    lastDebug = millis();
  }
  #endif
}

#endif // SENSORS_H
