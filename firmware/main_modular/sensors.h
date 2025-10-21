/**
 * @file sensors.h
 * @brief Gestor de sensores del sistema híbrido
 * 
 * Sensores:
 * - 3x INA219 (Solar, Wind, Battery) - I2C
 * - ADC INTERNO ESP32 (LDR para irradiancia) - GPIO34 
 * - 1x DS18B20 (Temperatura) - OneWire
 * - Hall Effect (Anemómetro) - GPIO
 * 
 * NOTA: Usa ADC interno ESP32 (12-bit) con amplificador operacional MCP
 */

#ifndef SENSORS_H
#define SENSORS_H

#include <Arduino.h>
#include <Wire.h>
#include <Adafruit_INA219.h>
#include <OneWire.h>
#include <DallasTemperature.h>

// ===== PINES =====
#define PIN_LDR 34              // ADC1_CH6 - LDR para irradiancia
#define PIN_DS18B20 25          // DS18B20 temperatura
#define PIN_ANEMOMETRO 26       // Sensor Hall anemómetro
#define PIN_SDA 21              // I2C SDA
#define PIN_SCL 22              // I2C SCL

// ===== DIRECCIONES I2C =====
#define INA219_SOLAR_ADDR 0x40   // INA219 panel solar
#define INA219_WIND_ADDR 0x41    // INA219 turbina eólica
#define INA219_BATTERY_ADDR 0x44 // INA219 batería
#define ADS1115_ADDR 0x48        // ADS1115 ADC externo

// ===== CONSTANTES =====
#define LDR_SAMPLES 10           // Muestras para promedio LDR
#define TEMP_PRECISION 12        // Bits de precisión DS18B20
#define WIND_PULSES_PER_REV 2    // Pulsos por revolución anemómetro
#define WIND_RADIUS_M 0.1        // Radio anemómetro (metros)

// ===== ESTRUCTURA DE DATOS =====
struct SensorData {
    // Solar
    float solar_voltage_v;
    float solar_current_a;
    float solar_power_w;
    float irradiance_w_m2;
    
    // Eólico
    float wind_voltage_v;
    float wind_current_a;
    float wind_power_w;
    float wind_speed_ms;
    
    // Batería
    float battery_voltage_v;
    float battery_current_a;
    float battery_power_w;
    float battery_soc_percent;
    
    // Ambiente
    float temperature_c;
    
    // Timestamp
    unsigned long timestamp_ms;
};

class SensorsManager {
private:
    // Sensores I2C
    Adafruit_INA219 ina219_solar;
    Adafruit_INA219 ina219_wind;
    Adafruit_INA219 ina219_battery;
    
    // Temperatura
    OneWire oneWire;
    DallasTemperature dallas;
    
    // Anemómetro
    volatile unsigned long wind_pulse_count;
    unsigned long last_wind_measurement;
    
    // ADC interno ESP32 para LDR
    float ldr_calibration_factor;
    int ldr_raw_min = 0;      // Calibración mínimo (noche)
    int ldr_raw_max = 4095;    // Calibración máximo (sol pleno)
    
    // Última lectura
    SensorData last_data;
    
    // Métodos privados
    float readIrradiance();
    float readTemperature();
    float readWindSpeed();
    float calculateSOC(float voltage);
    static void IRAM_ATTR windPulseISR();
    static SensorsManager* instance;

public:
    SensorsManager();
    
    bool begin();
    SensorData readAll();
    SensorData getLastData();
    
    // Lecturas individuales
    float readSolarVoltage();
    float readSolarCurrent();
    float readSolarPower();
    float readWindVoltage();
    float readWindCurrent();
    float readWindPower();
    float readBatteryVoltage();
    float readBatteryCurrent();
    float readBatteryPower();
    float readBatterySOC();
    
    // Calibración
    void setCalibrationFactor(float factor);
    float getCalibrationFactor();
    void calibrateLDR(int raw_min, int raw_max);
    void resetWindCounter();
    
    // Debug
    void printData();
};

#endif // SENSORS_H
