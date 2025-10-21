/**
 * @file data_logger.h
 * @brief Logger de datos en SPIFFS/SD para respaldo
 */

#ifndef DATA_LOGGER_H
#define DATA_LOGGER_H

#include <Arduino.h>
#include <FS.h>
#include <SPIFFS.h>
#include <ArduinoJson.h>
#include "sensors.h"

#define LOG_FILE "/sensor_log.csv"
#define MAX_LOG_SIZE 1048576  // 1 MB
#define LOG_INTERVAL 60000    // 1 minuto

class DataLogger {
private:
    File log_file;
    unsigned long last_log_time;
    unsigned long log_count;
    
    bool openLogFile();
    void closeLogFile();
    bool rotateLog();

public:
    DataLogger();
    
    bool begin();
    bool logData(const SensorData& data);
    String getLog();
    void clearLog();
    unsigned long getLogCount();
};

#endif // DATA_LOGGER_H
