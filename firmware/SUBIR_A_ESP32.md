# 🔧 Subir Firmware al ESP32

Guía para subir el firmware al ESP32 Dev Kit o ESP32-WROOM.

---

## ✅ Compatibilidad

| Módulo | Compatible | Notas |
|--------|-----------|-------|
| **ESP32 Dev Kit** | ✅ | Totalmente compatible |
| **ESP32-WROOM-32** | ✅ | Mismo chip, funciona igual |
| **ESP32-WROVER** | ✅ | También compatible |
| **ESP32-S2/S3/C3** | ⚠️ | Requiere ajustes de pines |

**Conclusión:** ESP32 Dev Kit y ESP32-WROOM son **IGUALES** para este proyecto.

---

## 📋 Métodos de Subida

### **Opción A: PlatformIO (Recomendado)**
✅ Más fácil  
✅ Maneja librerías automáticamente  
✅ Soporte VS Code  

### **Opción B: Arduino IDE**
✅ Más conocido  
⚠️ Instalar librerías manualmente  

---

## 🚀 Método 1: PlatformIO (Recomendado)

### **1. Instalar PlatformIO**
```bash
pip install platformio
```

O desde VS Code:
- Instalar extensión "PlatformIO IDE"

### **2. Configurar WiFi y Backend**
```bash
cd firmware
copy include\config.h.example include\config.h
notepad include\config.h
```

**Editar:**
```cpp
// WiFi
#define WIFI_SSID "TU_RED_WIFI"
#define WIFI_PASSWORD "TU_PASSWORD"

// Backend (IP pública)
#define SERVER_URL "http://190.211.201.217:11113"

// O Ngrok
// #define SERVER_URL "https://argentina.ngrok.pro"

// ID único del dispositivo
#define DEVICE_ID "ESP32_INVERSOR_001"
```

### **3. Conectar ESP32**
- Conectar ESP32 al puerto USB
- Verificar puerto COM en Administrador de Dispositivos (ej: COM3)

### **4. Compilar y Subir**
```bash
cd firmware
pio run --target upload
```

### **5. Monitor Serial**
```bash
pio device monitor
```

Deberías ver:
```
✅ WiFi conectado: 192.168.0.X
✅ Backend: http://190.211.201.217:11113
✅ Sensores inicializados
✅ Sistema iniciado
```

---

## 🔧 Método 2: Arduino IDE

### **1. Instalar Arduino IDE**
Descargar de: https://www.arduino.cc/en/software

### **2. Agregar Soporte ESP32**

**File → Preferences → Additional Board Manager URLs:**
```
https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json
```

**Tools → Board → Boards Manager:**
- Buscar "ESP32"
- Instalar "esp32 by Espressif Systems"

### **3. Instalar Librerías**

**Sketch → Include Library → Manage Libraries:**

Instalar:
- `ArduinoJson` (by Benoit Blanchon)
- `Adafruit INA219` (by Adafruit)
- `Adafruit BusIO` (by Adafruit)
- `OneWire` (by Paul Stoffregen)
- `DallasTemperature` (by Miles Burton)
- `ESPAsyncWebServer` (buscar en GitHub)
- `ESPAsyncTCP` (buscar en GitHub)

### **4. Configurar Board**

**Tools → Board:** ESP32 Dev Module  
**Tools → Upload Speed:** 921600  
**Tools → Flash Frequency:** 80MHz  
**Tools → Flash Mode:** QIO  
**Tools → Flash Size:** 4MB  
**Tools → Port:** (tu puerto COM)

### **5. Copiar Configuración**
```bash
cd firmware
copy include\config.h.example include\config.h
```

Editar `config.h` como en el paso 2 de PlatformIO.

### **6. Abrir en Arduino IDE**

**File → Open:**
- Seleccionar `firmware/src/main_modular.cpp`

**Cambiar extensión a `.ino`** (Arduino IDE lo requiere):
```bash
rename src\main_modular.cpp main_modular.ino
```

### **7. Compilar y Subir**

**Sketch → Upload** (o Ctrl+U)

### **8. Monitor Serial**

**Tools → Serial Monitor**

Baud rate: 115200

---

## 🔌 Conexión Hardware

```
ESP32 Dev Kit / WROOM
┌─────────────────────┐
│  EN        VIN      │ ← 5V USB
│  GPIO36    GND      │ ← GND
│  GPIO39    GPIO13   │
│  GPIO34    GPIO12   │ ← LDR (ADC interno)
│  GPIO35    GPIO14   │
│  GPIO32    GPIO27   │
│  GPIO33    GPIO26   │ ← Anemómetro
│  GPIO25    GPIO25   │ ← DS18B20
│  GPIO26    GPIO32   │
│  GPIO27    GPIO33   │
│  GPIO14    GPIO34   │
│  GPIO12    GPIO35   │
│  GPIO13    GPIO36   │
│  GND       GPIO39   │
│  VIN       EN       │
│  3V3       GPIO22   │ ← I2C SCL
│  GPIO21    TXD0     │ ← I2C SDA
│  RXD0      RXD0     │
└─────────────────────┘
```

**Pines usados:**
- **GPIO34:** LDR (ADC interno, irradiancia solar)
- **GPIO25:** DS18B20 (temperatura)
- **GPIO26:** Anemómetro (Hall sensor)
- **GPIO21:** I2C SDA (INA219 x3)
- **GPIO22:** I2C SCL (INA219 x3)

---

## 🧪 Probar Sin Hardware

Si NO tenés los sensores conectados, el firmware funciona igual pero con valores simulados.

**Para desarrollo:**
1. Subir firmware solo con WiFi conectado
2. Verificar que envía datos al backend
3. Ver en http://localhost:11113/docs los datos recibidos

---

## 🆘 Solución de Problemas

### **Error: "esptool.py not found"**
```bash
pip install esptool
```

### **Error: "A fatal error occurred: Failed to connect"**
1. Mantener presionado botón **BOOT** del ESP32
2. Presionar botón **RESET**
3. Soltar **RESET**, luego soltar **BOOT**
4. Reintentar upload

### **Error: "Port COM3 busy"**
1. Cerrar Arduino IDE / PlatformIO
2. Desconectar y reconectar USB
3. Verificar que no haya otro programa usando el puerto

### **ESP32 no responde después de subir**
1. Presionar botón **RESET** del ESP32
2. Verificar alimentación (5V por USB o VIN)
3. Abrir monitor serial para ver errores

### **No aparece en puertos COM**
1. Instalar drivers CH340 o CP2102 según tu placa
2. Probar otro cable USB (algunos son solo carga)
3. Verificar en Administrador de Dispositivos

---

## ✅ Verificación Post-Upload

### **1. Monitor Serial**
Deberías ver:
```
╔═══════════════════════════════════════════════════════════╗
║   🔋 SISTEMA INVERSOR INTELIGENTE HÍBRIDO - ESP32 🔋    ║
╚═══════════════════════════════════════════════════════════╝

✅ Sensores inicializados
📡 Conectando WiFi...
✅ WiFi conectado: 192.168.0.150
   RSSI: -45 dBm
📡 Configurando cliente HTTP...
✅ Cliente HTTP configurado
   Servidor: http://190.211.201.217:11113
   Device ID: ESP32_INVERSOR_001
🌐 Iniciando servidor web...
✅ Servidor web en http://192.168.0.150
⚙️  Creando tareas...
✅ Tarea Sensores iniciada (Core 0)
✅ Tarea Comunicación iniciada (Core 1)
✅ Tarea Monitor iniciada (Core 1)

🚀 Sistema iniciado correctamente
```

### **2. Backend Recibiendo Datos**
Ir a: http://localhost:11113/docs

Ejecutar: `GET /api/energy/history?hours=1`

Deberías ver datos del ESP32.

### **3. Dashboard Mostrando Datos**
Ir a: http://localhost:3002

El dashboard debería mostrar datos en tiempo real del ESP32.

---

## 📊 Frecuencia de Envío

- **Lectura sensores:** Cada 1 segundo
- **Envío telemetría:** Cada 5 segundos
- **Verificar comandos:** Cada 10 segundos

Configurable en `config.h`:
```cpp
#define HTTP_SEND_INTERVAL 5000
#define HTTP_COMMAND_CHECK_INTERVAL 10000
```

---

## 🔐 Seguridad

⚠️ **IMPORTANTE:** No subas `config.h` a Git  
✅ Usa `config.h.example` como plantilla  
✅ Cada usuario crea su propio `config.h`

---

## 📝 Personalización

### **Cambiar Device ID**
```cpp
#define DEVICE_ID "ESP32_CASA_JUAN"
```

### **Cambiar URLs**
```cpp
// Producción
#define SERVER_URL "http://190.211.201.217:11113"

// Desarrollo local
// #define SERVER_URL "http://192.168.0.100:11113"

// Desarrollo con ngrok
// #define SERVER_URL "https://argentina.ngrok.pro"
```

### **Ajustar Intervalos**
```cpp
// Enviar más frecuente (cada 2 segundos)
#define HTTP_SEND_INTERVAL 2000

// Verificar comandos más seguido (cada 5 segundos)
#define HTTP_COMMAND_CHECK_INTERVAL 5000
```

---

**¡Listo para programar tu ESP32!** 🚀

**PlatformIO es más fácil, pero Arduino IDE también funciona bien.**
