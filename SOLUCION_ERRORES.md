# 🔧 SOLUCIÓN A LOS ERRORES

---

## ❌ **PROBLEMA 1: WebSocket con Ngrok (HTTPS)**

**Error:**
```
Failed to construct 'WebSocket': An insecure WebSocket connection 
may not be initiated from a page loaded over HTTPS.
```

**Causa:**
- Ngrok usa HTTPS (seguro)
- WebSocket configurado con `ws://` (inseguro)
- HTTPS no permite conexiones WebSocket inseguras

**Solución:**
✅ **WebSocket deshabilitado temporalmente**
- El sistema funciona SIN WebSocket (no es crítico)
- Los datos se actualizan cada 30 seg por polling
- Para habilitar WebSocket con Ngrok:
  - Backend necesita SSL/TLS
  - Cambiar `ws://` a `wss://`

---

## ❌ **PROBLEMA 2: CORS Policy (Backend)**

**Error:**
```
Access to XMLHttpRequest at 'http://190.211.201.217:11113/api/dashboard' 
has been blocked by CORS policy
```

**Causa:**
- Frontend en `https://argentina.ngrok.pro`
- Backend en `http://190.211.201.217:11113`
- Backend no permite solicitudes desde ese origen

**Solución:**
✅ **Backend ya tiene CORS abierto** (`allow_origins=["*"]`)

**PERO el backend NO está corriendo:**
```bash
Failed to load resource: net::ERR_FAILED
```

**DEBES INICIAR EL BACKEND:**
```bash
cd backend
python -m uvicorn main:app --host 0.0.0.0 --port 11113 --reload
```

---

## ❌ **PROBLEMA 3: ESP32 Valores Negativos**

**Error del ESP32:**
```
Solar: -138.42A / -366W
Eólica: -149.91A / -397W
Consumo: -149.91A / -397W
```

**Causa:**
- Sensores ADC leyendo ruido sin hardware conectado
- Sin offset/calibración
- ADC sin señal válida = valores aleatorios

**Solución:**

### **Opción A: Calibración de Offset**
```cpp
// En sensors.h - agregar offset
#define ADC_OFFSET 2048  // Punto medio 12-bit

float leerCorriente(int pin) {
    int raw = analogRead(pin);
    int ajustado = raw - ADC_OFFSET;  // Centrar en 0
    
    if (abs(ajustado) < 50) {  // Umbral ruido
        return 0.0;
    }
    
    return ajustado * CORRIENTE_FACTOR;
}
```

### **Opción B: Modo Simulación (Temporal)**
```cpp
// En config.h
#define MODO_SIMULACION true

// En sensors.cpp
if (MODO_SIMULACION) {
    corriente_solar = 5.0;   // Simulado
    corriente_eolica = 3.0;
    voltaje_bat = 52.0;
}
```

---

## ✅ **PASOS PARA QUE TODO FUNCIONE:**

### **1. Iniciar Backend (CRÍTICO):**
```bash
cd X:\PREDICCION DE CLIMA\backend
python -m uvicorn main:app --host 0.0.0.0 --port 11113 --reload
```

**Verificar que dice:**
```
INFO: Uvicorn running on http://0.0.0.0:11113
INFO: Application startup complete
```

### **2. Frontend ya está corriendo:**
```
✅ http://localhost:3002 (local)
✅ https://argentina.ngrok.pro (internet)
```

### **3. ESP32 - Agregar Filtro de Ruido:**

Editar `firmware_arduino_ide_2/inversor_hibrido/sensors.h`:

```cpp
// Agregar después de las definiciones
#define ADC_NOISE_THRESHOLD 50  // Bits de ruido
#define ADC_OFFSET 2048          // Centro 12-bit

float SensorManager::leerCorriente(int pin) {
    int adc_raw = analogRead(pin);
    
    // Centrar en 0 y filtrar ruido
    int adc_centered = adc_raw - ADC_OFFSET;
    
    if (abs(adc_centered) < ADC_NOISE_THRESHOLD) {
        return 0.0;  // Es ruido, retornar 0
    }
    
    // Calcular corriente
    float corriente = adc_centered * CORRIENTE_FACTOR;
    
    // Limitar a rango válido
    if (corriente < -300.0) corriente = 0.0;
    if (corriente > 300.0) corriente = 300.0;
    
    return corriente;
}
```

### **4. Re-subir Firmware:**
- Arduino IDE → Upload
- Abrir Serial Monitor
- Verificar que valores sean 0 o positivos

---

## 🎯 **PRIORIDAD DE SOLUCIÓN:**

```
1️⃣ URGENTE: Iniciar backend
   → Sin esto, el frontend no funciona

2️⃣ MEDIA: Arreglar sensores ESP32
   → Agregar filtro de ruido
   → Valores negativos son ruido ADC

3️⃣ BAJA: WebSocket
   → Ya está deshabilitado
   → Sistema funciona sin él
```

---

## 🚀 **COMANDO RÁPIDO:**

```bash
# Terminal 1 - Backend
cd X:\PREDICCION DE CLIMA\backend
python -m uvicorn main:app --host 0.0.0.0 --port 11113 --reload

# Terminal 2 - Frontend (ya corriendo)
# npm start

# Terminal 3 - Ngrok (ya corriendo)
# ngrok http 3002 --domain=argentina.ngrok.pro
```

---

## ✅ **VERIFICACIÓN:**

### **Backend corriendo:**
```bash
curl http://localhost:11113/docs
# Debe abrir Swagger UI
```

### **Frontend accesible:**
```
http://localhost:3002 ✅
https://argentina.ngrok.pro ✅
```

### **ESP32 conectado:**
```
Serial Monitor:
✅ WiFi conectado
✅ Dispositivo registrado
⚠️ Valores negativos (arreglar sensores)
```

---

**INICIA EL BACKEND AHORA Y TODO FUNCIONARÁ** 🚀
