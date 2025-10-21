/**
 * @file sensors.cpp
 * @brief Implementación del módulo de sensores
 */

#include "../include/sensors.h"

// Instancia estática para ISR
SensorsManager* SensorsManager::instance = nullptr;

SensorsManager::SensorsManager() 
    : ina219_solar(INA219_SOLAR_ADDR),
      ina219_wind(INA219_WIND_ADDR),
      ina219_battery(INA219_BATTERY_ADDR),
      oneWire(PIN_DS18B20),
      ds18b20(&oneWire) {
    
    wind_pulse_count = 0;
    wind_last_calc_time = 0;
    wind_speed_ms = 0.0;
    instance = this;
}

bool SensorsManager::begin() {
    Serial.println("🔧 Inicializando sensores...");
    
    // Inicializar I2C
    Wire.begin(PIN_SDA, PIN_SCL);
    
    // INA219 Solar
    if (!ina219_solar.begin()) {
        Serial.println("❌ Error inicializando INA219 Solar");
        return false;
    }
    ina219_solar.setCalibration_32V_2A();
    Serial.println("✅ INA219 Solar OK");
    
    // INA219 Wind
    if (!ina219_wind.begin(&Wire, INA219_WIND_ADDR)) {
        Serial.println("❌ Error inicializando INA219 Wind");
        return false;
    }
    ina219_wind.setCalibration_32V_2A();
    Serial.println("✅ INA219 Wind OK");
    
    // INA219 Battery
    if (!ina219_battery.begin(&Wire, INA219_BATTERY_ADDR)) {
        Serial.println("❌ Error inicializando INA219 Battery");
        return false;
    }
    ina219_battery.setCalibration_32V_2A();
    Serial.println("✅ INA219 Battery OK");
    
    // ADS1115
    if (!ads1115.begin(ADS1115_ADDR)) {
        Serial.println("❌ Error inicializando ADS1115");
        return false;
    }
    ads1115.setGain(GAIN_ONE);  // +/- 4.096V
    Serial.println("✅ ADS1115 OK");
    
    // DS18B20
    ds18b20.begin();
    ds18b20.setResolution(TEMP_PRECISION);
    Serial.println("✅ DS18B20 OK");
    
    // Anemómetro (Sensor Hall)
    pinMode(PIN_ANEMOMETRO, INPUT_PULLUP);
    attachInterrupt(digitalPinToInterrupt(PIN_ANEMOMETRO), windPulseISR, FALLING);
    Serial.println("✅ Anemómetro OK");
    
    Serial.println("✅ Todos los sensores inicializados");
    return true;
}

SensorData SensorsManager::readAll() {
    SensorData data;
    
    // Solar
    data.solar_voltage_v = ina219_solar.getBusVoltage_V();
    data.solar_current_a = ina219_solar.getCurrent_mA() / 1000.0;
    data.solar_power_w = data.solar_voltage_v * data.solar_current_a;
    data.irradiance_w_m2 = readIrradiance();
    
    // Eólico
    data.wind_voltage_v = ina219_wind.getBusVoltage_V();
    data.wind_current_a = ina219_wind.getCurrent_mA() / 1000.0;
    data.wind_power_w = data.wind_voltage_v * data.wind_current_a;
    data.wind_speed_ms = readWindSpeed();
    
    // Batería
    data.battery_voltage_v = ina219_battery.getBusVoltage_V();
    data.battery_current_a = ina219_battery.getCurrent_mA() / 1000.0;
    data.battery_power_w = data.battery_voltage_v * data.battery_current_a;
    data.battery_soc_percent = calculateSOC(data.battery_voltage_v);
    
    // Temperatura
    data.temperature_c = readTemperature();
    
    // Timestamp
    data.timestamp_ms = millis();
    
    last_data = data;
    return data;
}

SensorData SensorsManager::getLastData() {
    return last_data;
}

float SensorsManager::readIrradiance() {
    // Leer LDR a través del ADS1115
    int16_t adc_value = ads1115.readADC_SingleEnded(0);
    
    // Convertir a voltaje (0-4.096V)
    float voltage = adc_value * 0.125 / 1000.0;
    
    // Convertir a irradiancia (calibración específica del LDR)
    // Asumiendo: 0V = 0 W/m², 4V = 1000 W/m²
    float irradiance = (voltage / 4.096) * 1000.0;
    
    return irradiance;
}

float SensorsManager::readTemperature() {
    ds18b20.requestTemperatures();
    float temp = ds18b20.getTempCByIndex(0);
    
    // Verificar lectura válida
    if (temp == DEVICE_DISCONNECTED_C) {
        Serial.println("⚠️  DS18B20 desconectado");
        return 25.0;  // Valor por defecto
    }
    
    return temp;
}

float SensorsManager::readWindSpeed() {
    unsigned long current_time = millis();
    unsigned long time_diff = current_time - wind_last_calc_time;
    
    // Calcular cada segundo
    if (time_diff >= 1000) {
        // Velocidad = (Pulsos / Pulsos_por_rev) * (2 * PI * radio) * (60 / tiempo_seg)
        // Simplificado: v = pulsos * k
        float k = (2.0 * PI * WIND_RADIUS_M * 60.0) / (WIND_PULSES_PER_REV * 60.0);
        wind_speed_ms = wind_pulse_count * k;
        
        // Reset contador
        wind_pulse_count = 0;
        wind_last_calc_time = current_time;
    }
    
    return wind_speed_ms;
}

float SensorsManager::calculateSOC(float voltage) {
    // Batería de plomo-ácido 48V (4x12V en serie)
    // Rango: 44V (0%) a 52V (100%)
    const float V_MIN = 44.0;
    const float V_MAX = 52.0;
    
    if (voltage <= V_MIN) return 0.0;
    if (voltage >= V_MAX) return 100.0;
    
    float soc = ((voltage - V_MIN) / (V_MAX - V_MIN)) * 100.0;
    return soc;
}

void IRAM_ATTR SensorsManager::windPulseISR() {
    if (instance) {
        instance->wind_pulse_count++;
    }
}

// Lecturas individuales
float SensorsManager::readSolarVoltage() {
    return ina219_solar.getBusVoltage_V();
}

float SensorsManager::readSolarCurrent() {
    return ina219_solar.getCurrent_mA() / 1000.0;
}

float SensorsManager::readSolarPower() {
    return readSolarVoltage() * readSolarCurrent();
}

float SensorsManager::readWindVoltage() {
    return ina219_wind.getBusVoltage_V();
}

float SensorsManager::readWindCurrent() {
    return ina219_wind.getCurrent_mA() / 1000.0;
}

float SensorsManager::readWindPower() {
    return readWindVoltage() * readWindCurrent();
}

float SensorsManager::readBatteryVoltage() {
    return ina219_battery.getBusVoltage_V();
}

float SensorsManager::readBatteryCurrent() {
    return ina219_battery.getCurrent_mA() / 1000.0;
}

float SensorsManager::readBatteryPower() {
    return readBatteryVoltage() * readBatteryCurrent();
}

float SensorsManager::readBatterySOC() {
    return calculateSOC(readBatteryVoltage());
}

void SensorsManager::calibrateLDR() {
    Serial.println("🔧 Calibrando LDR...");
    Serial.println("   Exponer a luz solar plena durante 5 segundos...");
    
    float max_value = 0;
    for (int i = 0; i < 50; i++) {
        int16_t adc = ads1115.readADC_SingleEnded(0);
        if (adc > max_value) max_value = adc;
        delay(100);
    }
    
    Serial.printf("   Valor máximo: %.2f\n", max_value);
    Serial.println("✅ Calibración completada");
}

void SensorsManager::resetWindCounter() {
    wind_pulse_count = 0;
    wind_speed_ms = 0.0;
}

void SensorsManager::printData() {
    SensorData data = last_data;
    
    Serial.println("\n╔════════════════════════════════════════════════╗");
    Serial.println("║         DATOS DE SENSORES                      ║");
    Serial.println("╠════════════════════════════════════════════════╣");
    Serial.printf("║ ☀️  SOLAR:                                     ║\n");
    Serial.printf("║    Voltaje:     %6.2f V                      ║\n", data.solar_voltage_v);
    Serial.printf("║    Corriente:   %6.2f A                      ║\n", data.solar_current_a);
    Serial.printf("║    Potencia:    %6.2f W                      ║\n", data.solar_power_w);
    Serial.printf("║    Irradiancia: %6.2f W/m²                   ║\n", data.irradiance_w_m2);
    Serial.println("║                                                ║");
    Serial.printf("║ 💨 EÓLICO:                                     ║\n");
    Serial.printf("║    Voltaje:     %6.2f V                      ║\n", data.wind_voltage_v);
    Serial.printf("║    Corriente:   %6.2f A                      ║\n", data.wind_current_a);
    Serial.printf("║    Potencia:    %6.2f W                      ║\n", data.wind_power_w);
    Serial.printf("║    Viento:      %6.2f m/s                    ║\n", data.wind_speed_ms);
    Serial.println("║                                                ║");
    Serial.printf("║ 🔋 BATERÍA:                                    ║\n");
    Serial.printf("║    Voltaje:     %6.2f V                      ║\n", data.battery_voltage_v);
    Serial.printf("║    Corriente:   %6.2f A                      ║\n", data.battery_current_a);
    Serial.printf("║    Potencia:    %6.2f W                      ║\n", data.battery_power_w);
    Serial.printf("║    SOC:         %6.2f %%                     ║\n", data.battery_soc_percent);
    Serial.println("║                                                ║");
    Serial.printf("║ 🌡️  Temperatura: %5.1f °C                     ║\n", data.temperature_c);
    Serial.println("╚════════════════════════════════════════════════╝\n");
}
