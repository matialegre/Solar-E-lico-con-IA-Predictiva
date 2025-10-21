/**
 * @file sensors.h
 * @brief Módulo de sensores para el sistema inversor híbrido
 * 
 * Sensores implementados:
 * - INA219: Medición de corriente/voltaje solar y eólico
 * - ADS1115: ADC de 16 bits para LDR (irradiancia)
 * - DS18B20: Temperatura ambiente
 * - Hall Effect: Anemómetro (velocidad viento)
 */

#ifndef SENSORS_H
#define SENSORS_H

#include <Arduino.h>
#include <Wire.h>
#include <Adafruit_INA219.h>
#include <Adafruit_ADS1X15.h>
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
    // Objetos de sensores
    Adafruit_INA219 ina219_solar;
    Adafruit_INA219 ina219_wind;
    Adafruit_INA219 ina219_battery;
    Adafruit_ADS1115 ads1115;
    OneWire oneWire;
    DallasTemperature ds18b20;
    
    // Variables para anemómetro
    volatile unsigned int wind_pulse_count;
    unsigned long wind_last_calc_time;
    float wind_speed_ms;
    
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
    void calibrateLDR();
    void resetWindCounter();
    
    // Debug
    void printData();
};

#endif // SENSORS_H
