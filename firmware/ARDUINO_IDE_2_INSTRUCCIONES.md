# 🎯 Arduino IDE 2.0 - Guía Completa

Cómo usar Arduino IDE 2.0 con el firmware del inversor.

---

## 📥 Instalación Arduino IDE 2.0

1. Descargar de: https://www.arduino.cc/en/software
2. Instalar (Next, Next, Install)
3. Abrir Arduino IDE 2.0

---

## 🔧 Configuración Inicial (Solo Primera Vez)

### **Paso 1: Agregar Soporte ESP32**

En Arduino IDE 2.0:

1. **File → Preferences** (o `Ctrl+,`)
2. En **"Additional Boards Manager URLs"** pegar:
   ```
   https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json
   ```
3. Click **OK**

4. **Boards Manager** (icono de tablero en la barra izquierda)
5. Buscar: `ESP32`
6. Instalar: **"esp32" by Espressif Systems** (versión más reciente)
7. Esperar a que termine (puede tardar 5-10 minutos)

---

### **Paso 2: Instalar Librerías**

En Arduino IDE 2.0:

1. **Library Manager** (icono de libros en barra izquierda)
2. Buscar e instalar **UNO POR UNO**:

```
ArduinoJson          (by Benoit Blanchon)
Adafruit INA219      (by Adafruit)
Adafruit BusIO       (by Adafruit)
OneWire              (by Paul Stoffregen)
DallasTemperature    (by Miles Burton)
```

3. Para **ESPAsyncWebServer** y **ESPAsyncTCP** (no están en el Library Manager):

   **Opción A: Descarga manual**
   - Ir a: https://github.com/me-no-dev/ESPAsyncWebServer
   - Download ZIP
   - Sketch → Include Library → Add .ZIP Library
   - Seleccionar el ZIP descargado
   
   - Repetir con: https://github.com/me-no-dev/ESPAsyncTCP

   **Opción B: Ignorar** (solo necesarias si usas el servidor web local del ESP32)

---

## 🚀 Preparar el Proyecto

### **Ejecutar Script Automático:**

```bash
cd firmware
ARDUINO_IDE_2_SETUP.bat
```

Esto crea:
- `main_modular/main_modular.ino` (archivo principal)
- Copia todos los `.h` necesarios
- Crea `config.h` si no existe

---

### **O Manual:**

1. Copiar `include/config.h.example` a `include/config.h`
2. Crear carpeta `firmware/main_modular/`
3. Copiar `src/main_modular.cpp` a `main_modular/main_modular.ino`
4. Copiar todos los `.h` de `include/` a `main_modular/`

---

## 📝 Configurar WiFi y Backend

### **1. Abrir el proyecto:**

Arduino IDE 2.0:
- **File → Open**
- Navegar a: `X:\PREDICCION DE CLIMA\firmware\main_modular\`
- Seleccionar: `main_modular.ino`

### **2. Editar config.h:**

En Arduino IDE verás varias pestañas arriba:
- `main_modular`
- `config.h` ← Click aquí
- Otros `.h`

En la pestaña `config.h`, editar:

```cpp
// ===== WiFi =====
#define WIFI_SSID "MI_RED_WIFI"        // ← TU WiFi
#define WIFI_PASSWORD "mipassword123"   // ← TU Password

// ===== BACKEND =====
#define SERVER_URL "http://190.211.201.217:11113"  // ← IP pública del backend

#define DEVICE_ID "ESP32_INVERSOR_001"
```

**Guardar:** `Ctrl+S`

---

## ⚙️ Configurar Placa y Puerto

### **1. Conectar ESP32 al USB**

### **2. Seleccionar Board:**

En Arduino IDE 2.0:
- **Select Board** (menú desplegable arriba)
- **Select other board and port...**
- Buscar: `ESP32 Dev Module`
- Seleccionar tu puerto COM (ej: COM3)
- Click **OK**

### **3. Configurar opciones de la placa:**

**Tools → Board: "ESP32 Dev Module"**

Configurar:
```
Upload Speed:        921600
CPU Frequency:       240MHz
Flash Frequency:     80MHz
Flash Mode:          QIO
Flash Size:          4MB (32Mb)
Partition Scheme:    Default 4MB with spiffs
Core Debug Level:    None
PSRAM:               Disabled
```

---

## 🔨 Compilar y Subir

### **1. Verificar (Compilar sin subir):**

- Click en ✅ (Verify)
- Esperar a que compile
- Debe decir: `Done compiling`

**Si hay errores:**
- Verificar que todas las librerías estén instaladas
- Verificar que `config.h` exista y esté bien configurado

### **2. Subir al ESP32:**

- Click en → (Upload)
- Esperar...

**Si falla "Failed to connect":**
1. Mantener presionado **BOOT** en el ESP32
2. Click Upload
3. Cuando diga "Connecting...", soltar **BOOT**

### **3. Monitor Serial:**

- Click en **Serial Monitor** (icono de lupa arriba a la derecha)
- Seleccionar baud rate: `115200`

Deberías ver:
```
╔═══════════════════════════════════════════╗
║   🔋 SISTEMA INVERSOR INTELIGENTE 🔋    ║
╚═══════════════════════════════════════════╝

✅ Sensores inicializados
📡 Conectando WiFi...
✅ WiFi conectado: 192.168.0.150
✅ Cliente HTTP configurado
   Servidor: http://190.211.201.217:11113
✅ Sistema iniciado
```

---

## 🎨 Interfaz Arduino IDE 2.0

```
┌─────────────────────────────────────────────────────────┐
│ File Edit Sketch Tools Help          ✅ → Serial Monitor│
├─────────────────────────────────────────────────────────┤
│ Select Board: ESP32 Dev Module (COM3)        Select Port│
├─────────────────────────────────────────────────────────┤
│ main_modular | config.h | sensors.h | ...              │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  1  #include <Arduino.h>                                │
│  2  #include "config.h"                                 │
│  3  #include "sensors.h"                                │
│  4  ...                                                 │
│                                                         │
│                    [TU CÓDIGO AQUÍ]                     │
│                                                         │
├─────────────────────────────────────────────────────────┤
│ Output / Console                                        │
│ Compiling sketch...                                     │
│ Done compiling                                          │
└─────────────────────────────────────────────────────────┘
```

**Barra izquierda:**
- 📋 Board Manager
- 📚 Library Manager
- 🔍 Search

**Barra superior:**
- ✅ Verify (Compilar)
- → Upload (Subir)
- 🐛 Serial Monitor

---

## 🆘 Solución de Problemas

### **"config.h: No such file or directory"**

```bash
cd firmware
copy include\config.h.example include\config.h
```

O ejecutar: `ARDUINO_IDE_2_SETUP.bat`

### **"ESP32 not found"**

1. Cerrar Arduino IDE
2. Desconectar ESP32
3. Reconectar ESP32
4. Abrir Arduino IDE
5. Seleccionar puerto de nuevo

### **"Compilation error: ..."**

Verificar librerías instaladas:
- ArduinoJson
- Adafruit INA219
- Adafruit BusIO
- OneWire
- DallasTemperature

### **"A fatal error occurred: Failed to connect"**

**Método 1:** Modo boot manual
1. Mantener **BOOT** presionado
2. Click Upload
3. Cuando diga "Connecting...", soltar **BOOT**

**Método 2:** Reset
1. Presionar **RESET** en el ESP32
2. Inmediatamente click Upload

**Método 3:** Drivers
- Instalar drivers CH340 o CP2102 según tu placa

### **Puerto COM no aparece**

1. Verificar cable USB (algunos son solo carga)
2. Instalar drivers:
   - CH340: https://sparks.gogo.co.nz/ch340.html
   - CP2102: https://www.silabs.com/developers/usb-to-uart-bridge-vcp-drivers
3. Verificar en Administrador de Dispositivos (Windows)

---

## 📊 Verificar que Funciona

### **1. Monitor Serial:**

```
✅ WiFi conectado
✅ HTTP configurado
📤 Enviando datos... OK
📥 Comandos: []
```

### **2. Backend recibiendo:**

Ir a: http://localhost:11113/docs

Ejecutar: `GET /api/energy/history?hours=1`

Deberías ver datos del ESP32.

### **3. Dashboard:**

Ir a: http://localhost:3002

Deberías ver datos en tiempo real.

---

## 🔄 Actualizar Firmware

Para actualizar el código después de cambios:

1. Hacer cambios en el código
2. **Guardar** (`Ctrl+S`)
3. **Upload** (→)

No es necesario cerrar Arduino IDE.

---

## 📝 Estructura del Proyecto en Arduino IDE

Cuando abres `main_modular.ino`, verás estas pestañas:

```
┌────────────┬───────────┬──────────────┬────────────┬─────────┐
│main_modular│  config.h │  sensors.h   │  relays.h  │  wifi.h │
└────────────┴───────────┴──────────────┴────────────┴─────────┘
```

**Editar cada pestaña** según necesites:
- `config.h` → WiFi, backend URL
- `sensors.h` → Configuración de sensores
- `relays.h` → Control de relés
- `wifi.h` → Gestión WiFi

---

## ⚡ Atajos de Arduino IDE 2.0

| Atajo | Acción |
|-------|--------|
| `Ctrl+U` | Upload |
| `Ctrl+R` | Verify (compilar) |
| `Ctrl+Shift+M` | Serial Monitor |
| `Ctrl+Shift+L` | Serial Plotter |
| `Ctrl+T` | Auto Format |
| `Ctrl+/` | Comentar línea |
| `Ctrl+F` | Buscar |

---

## 🎯 Resumen Rápido

```bash
# 1. Preparar
cd firmware
ARDUINO_IDE_2_SETUP.bat

# 2. Abrir Arduino IDE 2.0
# File → Open → main_modular/main_modular.ino

# 3. Editar config.h (pestaña)
# Poner WiFi y backend URL

# 4. Conectar ESP32 por USB

# 5. Tools → Board → ESP32 Dev Module

# 6. Upload (→)

# 7. Serial Monitor para ver logs
```

---

**¡Listo para programar con Arduino IDE 2.0!** 🚀

**Cualquier error, avísame.**
