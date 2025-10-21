# Firmware ESP32 - Inversor Inteligente

## 📋 Descripción

Firmware para ESP32 que controla y monitorea un sistema inversor híbrido solar-eólico-batería.

## 🔧 Hardware Requerido

### Componente Principal
- **ESP32 DevKit** (recomendado: ESP32-WROOM-32)

### Sensores
- **Voltaje**: Módulos divisores de voltaje (0-60V → 0-3.3V)
- **Corriente**: Sensores ACS712 (5A, 20A o 30A según capacidad)
- **Alternativa**: Módulos INA219 (I2C, mayor precisión)

### Actuadores
- **Relés**: Módulo de 4 relés 5V/10A
- **Alternativa**: MOSFETs (IRF540N para alta corriente)

### Conexiones

```
ESP32 Pin  →  Función
=============================
GPIO 34    →  Voltaje Solar (ADC)
GPIO 35    →  Corriente Solar (ADC)
GPIO 32    →  Voltaje Viento (ADC)
GPIO 33    →  Corriente Viento (ADC)
GPIO 25    →  Voltaje Batería (ADC)
GPIO 26    →  Corriente Batería (ADC)
GPIO 27    →  Corriente Carga (ADC)

GPIO 12    →  Relé Solar
GPIO 13    →  Relé Viento
GPIO 14    →  Relé Batería
GPIO 15    →  Relé Red

GPIO 2     →  LED Status
GPIO 4     →  LED WiFi
```

## ⚙️ Configuración

1. **Copiar archivo de configuración**:
   ```bash
   cp include/config.h include/config_local.h
   ```

2. **Editar `config_local.h`**:
   ```cpp
   #define WIFI_SSID "TU_RED_WIFI"
   #define WIFI_PASSWORD "TU_PASSWORD"
   #define SERVER_URL "http://IP_SERVIDOR:8000"
   ```

3. **Calibrar sensores** según tu hardware:
   ```cpp
   #define VOLTAGE_DIVIDER_RATIO 11.0
   #define CURRENT_SENSOR_SENSITIVITY 0.066
   ```

## 📦 Instalación

### Usando PlatformIO (Recomendado)

1. **Instalar PlatformIO**:
   ```bash
   pip install platformio
   ```

2. **Compilar**:
   ```bash
   cd firmware
   pio run
   ```

3. **Subir al ESP32**:
   ```bash
   pio run --target upload
   ```

4. **Monitor serial**:
   ```bash
   pio device monitor
   ```

### Usando Arduino IDE

1. Instalar soporte para ESP32
2. Instalar librerías:
   - ArduinoJson
   - PubSubClient (si usas MQTT)
3. Abrir `src/main.cpp`
4. Compilar y subir

## 🚀 Uso

1. **Conectar hardware** según el diagrama
2. **Alimentar ESP32** (5V USB o regulador)
3. **El ESP32 automáticamente**:
   - Se conecta al WiFi
   - Lee sensores cada 5 segundos
   - Envía datos al servidor cada 10 segundos
   - Ejecuta lógica de protección local

## 📊 Salida Serial

```
=================================
Sistema Inversor Inteligente ESP32
=================================

✅ Pines configurados
Conectando a WiFi: MiRed
✅ WiFi conectado
IP: 192.168.1.50
✅ Sistema inicializado correctamente
✅ Tareas FreeRTOS creadas

--- Sensores ---
Solar: 45.20V, 5.30A (240W)
Viento: 38.50V, 3.20A (123W)
Batería: 48.10V, -2.50A
Carga: 6.80A
Temperatura: 35.2°C

✓ Datos enviados - Código: 200
```

## 🔒 Seguridad

El firmware incluye protecciones:
- **Bajo voltaje de batería**: Alerta si <44V
- **Sobrevoltaje**: Desconecta fuentes si >58V
- **Watchdog**: Reinicia si el sistema se congela
- **Timeout de WiFi**: Reintenta conexión

## 🐛 Troubleshooting

### ESP32 no conecta a WiFi
- Verificar SSID y contraseña
- Verificar señal WiFi
- Probar con hotspot móvil

### Lecturas erróneas de sensores
- Verificar conexiones físicas
- Calibrar constantes en `config.h`
- Verificar GND común

### No envía datos al servidor
- Verificar que el servidor esté corriendo
- Verificar URL y puerto en config
- Revisar firewall

## 📝 Notas

- El ESP32 usa **Core 0** para sensores y control
- El ESP32 usa **Core 1** para comunicaciones
- FreeRTOS gestiona multitarea automáticamente
- Todos los relés inician **desactivados** por seguridad

## 🔗 Referencias

- [ESP32 Datasheet](https://www.espressif.com/sites/default/files/documentation/esp32_datasheet_en.pdf)
- [FreeRTOS Docs](https://www.freertos.org/Documentation/RTOS_book.html)
- [PlatformIO Docs](https://docs.platformio.org/)
