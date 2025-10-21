# 🔌 Firmware ESP32 - Sistema Inversor Híbrido

## 📋 Descripción

Firmware modular para ESP32 que gestiona:
- **Sensores:** INA219 (corriente/voltaje), ADS1115 (LDR), DS18B20 (temperatura), Hall (anemómetro)
- **Comunicación:** WiFi, MQTT, HTTP REST API
- **Almacenamiento:** SPIFFS para logs
- **Servidor Web:** Configuración y monitoreo local
- **FreeRTOS:** Tareas concurrentes en ambos cores

---

## 🗂️ Estructura Modular

```
firmware/
├── platformio.ini          # Configuración del proyecto
├── include/                # Headers (.h)
│   ├── config.h           # Configuración general
│   ├── sensors.h          # Gestión de sensores
│   ├── wifi_manager.h     # WiFi y modo AP
│   ├── mqtt_client.h      # Cliente MQTT
│   ├── web_server.h       # Servidor web
│   └── data_logger.h      # Logger SPIFFS
└── src/                    # Implementaciones (.cpp)
    ├── main_modular.cpp   # Main con arquitectura modular
    ├── sensors.cpp        # Implementación sensores
    ├── wifi_manager.cpp   # Implementación WiFi
    ├── mqtt_client.cpp    # Implementación MQTT
    ├── web_server.cpp     # Implementación web
    └── data_logger.cpp    # Implementación logger
```

---

## 🔧 Hardware Requerido

### **Microcontrolador:**
- ESP32 DevKit (dual-core, WiFi, Bluetooth)

### **Sensores:**

| Sensor | Función | Dirección I2C | Pines |
|--------|---------|---------------|-------|
| **INA219 #1** | Corriente/voltaje solar | 0x40 | SDA(21), SCL(22) |
| **INA219 #2** | Corriente/voltaje eólico | 0x41 | SDA(21), SCL(22) |
| **INA219 #3** | Corriente/voltaje batería | 0x44 | SDA(21), SCL(22) |
| **ADS1115** | ADC 16-bit (LDR) | 0x48 | SDA(21), SCL(22) |
| **DS18B20** | Temperatura ambiente | - | GPIO 25 |
| **Hall Effect** | Anemómetro (pulsos) | - | GPIO 26 |

### **Conexiones:**

```
ESP32 Pinout:
┌─────────────────────────────────┐
│  [3V3]  ━━━━━━━━━━━━━━  VCC    │ → Alimentación sensores
│  [GND]  ━━━━━━━━━━━━━━  GND    │ → Tierra común
│  [21]   ━━━━━━━━━━━━━━  SDA    │ → I2C Data
│  [22]   ━━━━━━━━━━━━━━  SCL    │ → I2C Clock
│  [25]   ━━━━━━━━━━━━━━  DS18B20│ → Temperatura
│  [26]   ━━━━━━━━━━━━━━  Hall   │ → Anemómetro
│  [34]   ━━━━━━━━━━━━━━  LDR    │ → Irradiancia (ADC interno)
└─────────────────────────────────┘
```

---

## ⚙️ Configuración

### **1. Editar `include/config.h`:**

```cpp
// WiFi
#define WIFI_SSID "TU_RED_WIFI"
#define WIFI_PASSWORD "TU_PASSWORD"

// MQTT
#define MQTT_SERVER "192.168.1.100"  // IP del backend
#define MQTT_PORT 1883
#define DEVICE_ID "ESP32_INVERSOR_001"

// Sistema
#define BATTERY_CAPACITY_WH 5000.0   // Capacidad batería (Wh)
#define SOLAR_PANEL_AREA_M2 16.0     // Área paneles (m²)
#define WIND_TURBINE_POWER_W 2000.0  // Potencia turbina (W)
```

---

## 🚀 Compilación y Carga

### **Opción 1: PlatformIO (Recomendado)**

```bash
# Instalar PlatformIO
pip install platformio

# Compilar
cd firmware
pio run

# Cargar al ESP32
pio run --target upload

# Monitor serial
pio device monitor
```

### **Opción 2: Arduino IDE**

1. Instalar ESP32 boards: `https://dl.espressif.com/dl/package_esp32_index.json`
2. Instalar librerías (ver `platformio.ini`)
3. Abrir `src/main_modular.cpp`
4. Seleccionar placa: **ESP32 Dev Module**
5. Compilar y cargar

---

## 📡 Comunicación con Backend

### **Protocolo: HTTP POST**

El ESP32 envía telemetría cada 5 segundos:

```http
POST http://BACKEND_IP:8801/api/esp32/telemetry
Content-Type: application/json

{
  "device_id": "ESP32_001",
  "timestamp": "2025-10-21T08:15:30",
  "solar": {
    "voltage": 48.2,
    "current": 12.5,
    "power": 602.5,
    "irradiance": 850.0
  },
  "wind": {
    "voltage": 47.8,
    "current": 5.2,
    "power": 248.5,
    "wind_speed": 8.5
  },
  "battery": {
    "voltage": 50.1,
    "current": 8.3,
    "power": 415.8,
    "soc": 65.5
  },
  "load_power_w": 435.0,
  "temperature_c": 22.5
}
```

---

## 🧪 Pruebas sin Hardware (Simulador)

### **Usar el simulador Python:**

```bash
# Iniciar backend
python start_system.py

# En otra terminal, ejecutar simulador
python simulador_esp32.py

# Opciones del simulador
python simulador_esp32.py --mode solar      # Solo solar
python simulador_esp32.py --mode wind       # Solo eólico
python simulador_esp32.py --interval 2      # Enviar cada 2 seg
python simulador_esp32.py --backend http://IP:8801
```

**Salida del simulador:**

```
╔═══════════════════════════════════════════════════════════╗
║         🔬 SIMULADOR ESP32 - SENSORES HÍBRIDOS 🔬        ║
╚═══════════════════════════════════════════════════════════╝

⏰ 2025-10-21T08:15:30
────────────────────────────────────────────────────────────
☀️  SOLAR:
    48.20 V  │  12.50 A  │   602.50 W
   Irradiancia:  850.00 W/m²

💨 EÓLICO:
    47.80 V  │   5.20 A  │   248.50 W
   Viento:   8.50 m/s

🔋 BATERÍA:
    50.10 V  │   8.30 A  │   415.80 W
   SOC:  65.5 %

🏠 CONSUMO:  435.00 W
🌡️  TEMP:  22.5 °C

⚡ BALANCE: +416.00 W
✅ Enviado al backend (1)
```

---

## 📊 Monitoreo Serial

Al conectar por USB, el ESP32 muestra:

```
╔═══════════════════════════════════════════════════════════╗
║   🔋 SISTEMA INVERSOR INTELIGENTE HÍBRIDO - ESP32 🔋    ║
╚═══════════════════════════════════════════════════════════╝

🔧 Inicializando sensores...
✅ INA219 Solar OK
✅ INA219 Wind OK
✅ INA219 Battery OK
✅ ADS1115 OK
✅ DS18B20 OK
✅ Anemómetro OK

📡 Conectando WiFi...
✅ WiFi conectado: 192.168.1.50
   RSSI: -45 dBm

📤 Conectando MQTT...
✅ MQTT conectado

🌐 Iniciando servidor web...
✅ Servidor web en http://192.168.1.50

⚙️  Creando tareas...
✅ Tareas creadas

╔═══════════════════════════════════════════════════════════╗
║                   INFORMACIÓN DEL SISTEMA                  ║
╠═══════════════════════════════════════════════════════════╣
║ Chip: ESP32                                               ║
║ Cores: 2                                                  ║
║ Frecuencia: 240 MHz                                       ║
║ Device ID: ESP32_INVERSOR_001                             ║
╚═══════════════════════════════════════════════════════════╝

🚀 Sistema iniciado correctamente

╔════════════════════════════════════════════════╗
║         DATOS DE SENSORES                      ║
╠════════════════════════════════════════════════╣
║ ☀️  SOLAR:                                     ║
║    Voltaje:      48.20 V                       ║
║    Corriente:    12.50 A                       ║
║    Potencia:    602.50 W                       ║
║    Irradiancia:  850.00 W/m²                   ║
║                                                ║
║ 💨 EÓLICO:                                     ║
║    Voltaje:      47.80 V                       ║
║    Corriente:     5.20 A                       ║
║    Potencia:    248.50 W                       ║
║    Viento:        8.50 m/s                     ║
║                                                ║
║ 🔋 BATERÍA:                                    ║
║    Voltaje:      50.10 V                       ║
║    Corriente:     8.30 A                       ║
║    Potencia:    415.80 W                       ║
║    SOC:          65.50 %                       ║
║                                                ║
║ 🌡️  Temperatura:  22.5 °C                     ║
╚════════════════════════════════════════════════╝
```

---

## 🌐 Servidor Web Integrado

Acceder a `http://IP_ESP32` para:

- **Ver datos en tiempo real**
- **Configurar WiFi/MQTT**
- **Descargar logs**
- **Ejecutar calibraciones**
- **Reiniciar sistema**

---

## 🔒 Seguridad

- **Watchdog timer:** Reinicia si el sistema se cuelga
- **Protección de sobretensión:** Detecta voltajes anómalos
- **Protección de sobrecorriente:** Limita lecturas máximas
- **Logs de respaldo:** SPIFFS mantiene datos ante pérdida de WiFi

---

## 🐛 Troubleshooting

### **Error: No se detectan sensores I2C**
```bash
# Escanear bus I2C
pio device monitor --filter=esp32_exception_decoder

# Verificar conexiones SDA/SCL
# Verificar alimentación 3.3V
```

### **Error: WiFi no conecta**
```cpp
// Cambiar a modo AP temporal
#define WIFI_AP_MODE_ON_FAIL true
```

### **Error: MQTT desconectado**
```cpp
// Verificar IP del servidor
// Verificar firewall
// Verificar puerto 1883
```

---

## 📦 Envío a Amigo Remoto

### **Para enviar el firmware completo:**

```bash
# Comprimir directorio firmware
tar -czf firmware_esp32_inversor.tar.gz firmware/

# O usar Git
git add firmware/
git commit -m "Firmware ESP32 completo y probado"
git push
```

**Tu amigo necesitará:**
1. Instalar PlatformIO: `pip install platformio`
2. Descomprimir o clonar repo
3. Editar `include/config.h` con sus credenciales
4. Compilar: `pio run`
5. Cargar: `pio run --target upload`

---

## 📖 Documentación de Módulos

### **sensors.h/cpp**
- `begin()`: Inicializa todos los sensores
- `readAll()`: Lee todos los sensores una vez
- `getLastData()`: Obtiene última lectura
- `printData()`: Imprime datos formateados

### **wifi_manager.h/cpp**
- `begin()`: Conecta WiFi o inicia AP
- `handle()`: Mantiene conexión
- `isConnected()`: Estado WiFi
- `reconnect()`: Reintenta conexión

### **mqtt_client.h/cpp**
- `begin()`: Conecta MQTT broker
- `publishSensorData()`: Publica telemetría
- `onMessage()`: Callback mensajes
- `handle()`: Mantiene conexión

---

## 📝 Notas para Desarrollo

- **Core 0:** Sensores (alta prioridad)
- **Core 1:** Comunicación y web (media/baja prioridad)
- **Stack sizes:** Ajustar según uso de memoria
- **Interval de lectura:** 1 segundo (configurable)
- **Logs SPIFFS:** Rotación automática a 1MB

---

## ✅ Checklist Pre-Deploy

- [ ] Configurar WiFi SSID/Password
- [ ] Configurar IP backend
- [ ] Verificar conexiones I2C
- [ ] Calibrar LDR con luz solar
- [ ] Probar anemómetro
- [ ] Verificar polaridad INA219
- [ ] Probar comunicación HTTP
- [ ] Verificar logs SPIFFS
- [ ] Probar servidor web local
- [ ] Documentar instalación específica

---

**¡Firmware listo para producción!** 🚀
