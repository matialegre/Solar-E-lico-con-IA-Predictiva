# ⚡ Cambios en Firmware - Velocidad y Logs

## 🎯 Cambios Realizados

### 1. ⚡ Velocidad de Envío: 5s → 0.5s

**Archivo**: `config.h`

**ANTES** (lento):
```cpp
#define SEND_INTERVAL 5000  // 5 segundos
```

**AHORA** (rápido):
```cpp
#define SEND_INTERVAL 500   // ⚡ 0.5 segundos (TIEMPO REAL)
```

**Resultado**: El ESP32 ahora envía datos **10 veces más rápido** ✅

---

### 2. 📊 Logs Serial Monitor - SÚPER CLAROS

**Archivo**: `http_client.h` → Función `printStage1UART()`

#### Modo DETALLADO (cada 5 segundos)

```
╔════════════════════════════════════════════════════════════════╗
║  📊 TELEMETRÍA #123 | Uptime: 456s                             ║
╠════════════════════════════════════════════════════════════════╣
║  📍 ADCs RAW (0-3.3V REALES):                                  ║
║    GPIO34 (Batería):  0.563V  [raw: 698/4095]                  ║
║    GPIO35 (Eólica):   0.551V  [raw: 683/4095]                  ║
║    GPIO36 (Solar):    0.012V  [raw: 14/4095]                   ║
║    GPIO39 (Carga):    0.003V  [raw: 3/4095]                    ║
╠════════════════════════════════════════════════════════════════╣
║  🎯 RPM TURBINA:                                               ║
║    RPM: 287.3 RPM  |  Frecuencia: 47.89 Hz                     ║
╠════════════════════════════════════════════════════════════════╣
║  🔌 RELÉS: [✓] Solar  [✗] Eólica  [✓] Red  [✗] Carga          ║
╠════════════════════════════════════════════════════════════════╣
║  🌐 HTTP: POST 200  GET 200  |  WiFi RSSI: -45 dBm            ║
╚════════════════════════════════════════════════════════════════╝
```

#### Modo COMPACTO (cada 0.5 segundos)

```
⚡[1] 0.563V 0.551V 0.012V 0.003V | RPM:287 | POST:200
⚡[2] 0.564V 0.552V 0.013V 0.003V | RPM:289 | POST:200
⚡[3] 0.562V 0.550V 0.011V 0.004V | RPM:285 | POST:200
⚡[4] 0.565V 0.553V 0.014V 0.003V | RPM:291 | POST:200
```

**Características**:
- ✅ **Tabla clara** cada 5 segundos con TODOS los detalles
- ✅ **Línea compacta** cada 0.5 segundos para seguimiento rápido
- ✅ **Valores RAW** (0-4095) para debugging
- ✅ **Voltajes 0-3.3V** precisos
- ✅ **RPM y frecuencia** visibles
- ✅ **Estado de relés** con checkmarks
- ✅ **RSSI WiFi** para diagnóstico

---

## 🔄 Sistema Completo Ahora

### Flujo de Datos

```
ESP32 (cada 0.5s)
    ↓
  Lee ADCs con filtrado (50 muestras batería)
    ↓
  Calcula RPM (ISR cada 500ms)
    ↓
  Imprime en Serial Monitor
    • Detallado cada 5s
    • Compacto cada 0.5s
    ↓
  Envía JSON al backend (HTTP POST)
    ↓
Backend recibe (cada 0.5s)
    ↓
Frontend polling (cada 0.5s)
    ↓
Usuario ve actualización CASI EN TIEMPO REAL
```

---

## 🧪 Cómo Probar

### Paso 1: Compilar y Subir Firmware

```
1. Abre Arduino IDE
2. Abre inversor_hibrido.ino
3. Compila (Ctrl+R)
4. Sube al ESP32 (Ctrl+U)
```

### Paso 2: Abrir Serial Monitor

```
1. Tools → Serial Monitor
2. Baud rate: 115200
3. Observa los logs
```

### Paso 3: Qué Verás

**Primeros 5 segundos** (líneas compactas):
```
⚡[1] 0.563V 0.551V 0.012V 0.003V | RPM:287 | POST:200
⚡[2] 0.564V 0.552V 0.013V 0.003V | RPM:289 | POST:200
⚡[3] 0.562V 0.550V 0.011V 0.004V | RPM:285 | POST:200
⚡[4] 0.565V 0.553V 0.014V 0.003V | RPM:291 | POST:200
⚡[5] 0.563V 0.551V 0.012V 0.003V | RPM:288 | POST:200
⚡[6] 0.564V 0.552V 0.013V 0.003V | RPM:290 | POST:200
⚡[7] 0.562V 0.550V 0.011V 0.004V | RPM:286 | POST:200
⚡[8] 0.565V 0.553V 0.014V 0.003V | RPM:292 | POST:200
⚡[9] 0.563V 0.551V 0.012V 0.003V | RPM:289 | POST:200
⚡[10] 0.564V 0.552V 0.013V 0.003V | RPM:291 | POST:200
```

**Después de 5 segundos** (tabla detallada):
```
╔════════════════════════════════════════════════════════════════╗
║  📊 TELEMETRÍA #10 | Uptime: 5s                                ║
╠════════════════════════════════════════════════════════════════╣
║  📍 ADCs RAW (0-3.3V REALES):                                  ║
║    GPIO34 (Batería):  0.564V  [raw: 699/4095]                  ║
║    GPIO35 (Eólica):   0.552V  [raw: 684/4095]                  ║
║    GPIO36 (Solar):    0.013V  [raw: 15/4095]                   ║
║    GPIO39 (Carga):    0.003V  [raw: 3/4095]                    ║
╠════════════════════════════════════════════════════════════════╣
║  🎯 RPM TURBINA:                                               ║
║    RPM: 291.0 RPM  |  Frecuencia: 48.50 Hz                     ║
╠════════════════════════════════════════════════════════════════╣
║  🔌 RELÉS: [✓] Solar  [✗] Eólica  [✓] Red  [✗] Carga          ║
╠════════════════════════════════════════════════════════════════╣
║  🌐 HTTP: POST 200  GET 200  |  WiFi RSSI: -45 dBm            ║
╚════════════════════════════════════════════════════════════════╝

⚡[11] 0.563V 0.551V 0.012V 0.003V | RPM:288 | POST:200
⚡[12] 0.564V 0.552V 0.013V 0.003V | RPM:290 | POST:200
...
```

---

## 📊 Comparación Antes/Después

| Aspecto | ANTES | AHORA |
|---------|-------|-------|
| **Velocidad envío** | 5 segundos | 0.5 segundos |
| **Updates/minuto** | 12 | 120 |
| **Latencia visual** | 2-5s | 0.5-1s |
| **Logs Serial** | 1 línea básica | Tabla detallada + compacto |
| **Info visible** | Voltajes | Voltajes + RAW + RPM + Relés + WiFi |
| **Debugging** | Difícil | Muy fácil |

---

## 🎯 Ventajas de los Nuevos Logs

### 1. **Debugging Fácil** ✅
- Ves valores RAW (0-4095) → Detectas problemas hardware
- Ves voltajes 0-3.3V → Verificas divisores
- Ves POST status → Confirmas conexión backend

### 2. **Monitoreo en Tiempo Real** ✅
- Líneas compactas cada 0.5s → Sigues los cambios
- Tabla cada 5s → Checkeo completo

### 3. **Validación de Sensores** ✅
```
Si ves:
  GPIO34: 0.000V [raw: 0/4095]
  ↓
  Problema: Sensor desconectado o pin flotante
  
Si ves:
  GPIO34: 0.563V [raw: 698/4095]
  ↓
  OK: Sensor funcionando correctamente
```

### 4. **RPM Visual** ✅
```
RPM: 0.0 RPM  |  Frecuencia: 0.00 Hz
↓
Sin señal en GPIO13 (normal si no hay generador)

RPM: 287.3 RPM  |  Frecuencia: 47.89 Hz
↓
Señal funcionando correctamente
```

---

## ⚠️ Notas Importantes

### Consumo de Red
**Antes**: 12 requests/minuto → ~96 KB/min → 5.7 MB/hora
**Ahora**: 120 requests/minuto → ~960 KB/min → 57 MB/hora

**Impacto**: Para 1 dispositivo es NADA. Para 100 dispositivos considera optimizar.

### Serial Monitor Performance
Los logs detallados cada 5s NO afectan performance porque:
- Solo se imprimen cada 5 segundos
- Las líneas compactas son muy rápidas
- Serial.print() es non-blocking

### WiFi Estabilidad
A 0.5s el ESP32 puede estar más ocupado con WiFi. Si ves problemas:
```cpp
// Cambiar a 1 segundo en config.h
#define SEND_INTERVAL 1000  // Más conservador
```

---

## 🚀 Próximos Pasos

### 1. Prueba con Hardware Real
- Conecta voltaje fijo a GPIO34 (ej: 2.5V)
- Verifica que se ve estable en Serial Monitor
- Confirma que backend recibe los datos

### 2. Validar RPM
- Si tienes señal de frecuencia → Conecta a GPIO13
- Deberías ver valores en la tabla detallada
- Frecuencia debería coincidir con tu señal

### 3. Optimizar Si Es Necesario
- Si hay lag → Aumenta SEND_INTERVAL a 1000ms
- Si faltan datos → Reduce a 250ms (experimental)

---

## 📁 Archivos Modificados

1. ✅ `config.h` - SEND_INTERVAL: 5000 → 500
2. ✅ `http_client.h` - printStage1UART() completamente reescrita

**No se tocó**:
- `inversor_hibrido.ino` (no requiere cambios)
- `sensors.h` (ya tiene el filtrado)
- `relays.h`, `wifi_manager.h` (no relacionados)

---

## ✅ Estado Final

- ✅ **Firmware**: Envía cada 0.5s
- ✅ **Simulador**: Envía cada 0.5s
- ✅ **Frontend**: Polling cada 0.5s
- ✅ **Logs**: Súper claros y visuales
- ✅ **Todo sincronizado**: Sistema en tiempo real

**¡Compila y sube el firmware para ver los cambios! 🚀**
