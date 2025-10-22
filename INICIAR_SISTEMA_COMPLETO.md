# 🚀 INICIAR SISTEMA COMPLETO - GUÍA PASO A PASO

---

## ✅ **CHECKLIST PRE-INICIO:**

- [ ] Node.js instalado (v16+)
- [ ] Python 3.8+ instalado
- [ ] Arduino IDE 2.0 instalado (para ESP32)
- [ ] Puerto COM disponible para ESP32
- [ ] Red WiFi funcionando
- [ ] Puerto 11113 libre (backend)
- [ ] Puerto 3002 libre (frontend)

---

## 🔌 **PASO 1: PROGRAMAR ESP32**

### **1.1 Preparar Firmware:**

```bash
cd firmware_arduino_ide_2\inversor_hibrido
```

### **1.2 Editar Configuración:**

Abrir `config.h` y configurar:

```cpp
// WiFi
#define WIFI_SSID "TU_WIFI"
#define WIFI_PASSWORD "TU_PASSWORD"

// Backend
#define SERVER_URL "http://192.168.0.XXX:11113"  // Tu IP local
// O usar: "http://localhost:11113" si está en la misma PC

// Device ID (único para cada ESP32)
#define DEVICE_ID "ESP32_INVERSOR_001"
```

### **1.3 Abrir en Arduino IDE:**

1. Abrir `inversor_hibrido.ino` en Arduino IDE 2.0
2. Seleccionar placa: **ESP32 Dev Module**
3. Seleccionar puerto COM
4. Click **Upload** (→)

### **1.4 Verificar en Monitor Serie:**

```
Abrir Tools → Serial Monitor
Baudrate: 115200

Esperarás ver:
✅ WiFi conectado
✅ IP: 192.168.0.150
✅ Registrando dispositivo...
✅ Dispositivo registrado
✅ Sistema iniciado correctamente
```

---

## 🖥️ **PASO 2: INICIAR BACKEND**

### **2.1 Instalar Dependencias:**

```bash
cd backend
pip install -r requirements.txt
pip install httpx==0.25.2
```

### **2.2 Configurar `.env`:**

Crear/editar `backend/.env`:

```env
# Ubicación por defecto
LATITUDE=-38.7183
LONGITUDE=-62.2663

# OpenWeather API (obtener gratis en openweathermap.org)
OPENWEATHER_API_KEY=tu_api_key_aqui

# Base de datos
DATABASE_URL=sqlite:///./energy.db

# Puerto
PORT=11113
```

### **2.3 Iniciar Backend:**

**Opción A - Con script:**
```bash
PROBAR_BACKEND_NUEVO.bat
```

**Opción B - Manual:**
```bash
cd backend
python -m uvicorn main:app --host 0.0.0.0 --port 11113 --reload
```

### **2.4 Verificar:**

Abrir navegador:
```
http://localhost:11113/docs
```

Deberías ver Swagger UI con todos los endpoints.

---

## 🎨 **PASO 3: INICIAR FRONTEND**

### **3.1 Instalar Dependencias:**

```bash
cd frontend
npm install
npm install react-router-dom
```

### **3.2 Configurar `.env`:**

Crear/editar `frontend/.env`:

```env
# Backend URL
REACT_APP_API_URL=http://localhost:11113

# O si usas IP pública:
# REACT_APP_API_URL=http://190.211.201.217:11113
```

### **3.3 Iniciar Frontend:**

```bash
npm start
```

O usar el script:
```bash
INICIAR.bat
```

### **3.4 Verificar:**

El navegador debería abrir automáticamente:
```
http://localhost:3002
```

---

## 🌐 **PASO 4: CONFIGURAR NGROK (Opcional - Acceso Remoto)**

### **4.1 Iniciar Ngrok:**

```bash
ngrok http 3002
```

### **4.2 Obtener URL:**

```
Ngrok te dará una URL como:
https://argentina.ngrok.pro
```

### **4.3 Acceder remotamente:**

Desde cualquier dispositivo:
```
https://argentina.ngrok.pro
```

---

## ✅ **PASO 5: VERIFICAR TODO FUNCIONA**

### **5.1 Verificar Backend:**

```bash
curl http://localhost:11113/api/status/health
```

Deberías ver:
```json
{
  "services": {
    "backend": {"status": "online"},
    "openweather": {"status": "online"},
    "nasa_power": {"status": "online"},
    "esp32": {"status": "online", "online": 1},
    "machine_learning": {"status": "not_trained"}
  }
}
```

### **5.2 Verificar ESP32 Registrado:**

```bash
curl http://localhost:11113/api/esp32/devices
```

Deberías ver tu ESP32:
```json
{
  "devices": [{
    "device_id": "ESP32_INVERSOR_001",
    "status": "online",
    "ip_local": "192.168.0.150"
  }],
  "online": 1
}
```

### **5.3 Verificar Frontend:**

Abrir `http://localhost:3002` y verificar:

- [ ] **Panel de Estado** muestra servicios online
- [ ] **ESP32** aparece como conectado
- [ ] **Datos reales** (no simulados)
- [ ] **Gráficos** actualizándose
- [ ] **Tabs** funcionando (Dashboard, Monitoreo, Config, Info)

---

## 📊 **LO QUE VERÁS EN EL DASHBOARD:**

### **Al Inicio (Sin ESP32):**

```
⚠️ ESTADO DEL SISTEMA: 80% (4/5 servicios)

✅ Backend: online
✅ OpenWeather: online
✅ NASA: online
⚠️ ESP32: No hay dispositivos registrados
⚠️ ML: Modelos no entrenados

📊 Datos: Simulados
```

### **Con ESP32 Conectado:**

```
✅ ESTADO DEL SISTEMA: 100% (5/5 servicios)

✅ Backend: online
✅ OpenWeather: online (245ms)
✅ NASA: online (1,234ms)
✅ ESP32: 1 online (192.168.0.150)
⚠️ ML: Modelos no entrenados

📊 Datos: REALES desde ESP32 ✅
```

### **Con ML Entrenado:**

```
✅ ESTADO DEL SISTEMA: 100% (5/5 servicios)

✅ Backend: online
✅ OpenWeather: online (245ms)
✅ NASA: online (1,234ms)
✅ ESP32: 1 online
✅ ML: Ready (Solar: 87%, Eólico: 81%)

📊 Sistema completamente operativo ✅
```

---

## 🤖 **PASO 6: ENTRENAR MACHINE LEARNING (Opcional)**

### **6.1 Desde Frontend:**

1. Ir a tab **Configuración**
2. Click en **Dimensionamiento**
3. Ingresar datos de ubicación
4. El sistema entrenará ML automáticamente

### **6.2 Desde API:**

```bash
curl -X POST http://localhost:11113/api/ml/train \
  -H "Content-Type: application/json" \
  -d '{
    "latitude": -38.7183,
    "longitude": -62.2663,
    "years_back": 10
  }'
```

**Tiempo estimado:** 10-15 segundos

---

## 🔧 **TROUBLESHOOTING:**

### **❌ ESP32 no se conecta:**

```
1. Verificar WiFi SSID y password en config.h
2. Verificar que backend está corriendo
3. Verificar IP del backend en config.h
4. Ver Monitor Serie (115200 baud) para errores
```

### **❌ Backend da error al iniciar:**

```
1. Verificar puerto 11113 libre:
   netstat -ano | findstr :11113
   
2. Matar proceso si está ocupado:
   taskkill /F /PID <pid>
   
3. Verificar Python 3.8+:
   python --version
   
4. Reinstalar dependencias:
   pip install -r requirements.txt --force-reinstall
```

### **❌ Frontend no conecta con backend:**

```
1. Verificar REACT_APP_API_URL en frontend/.env
2. Verificar CORS habilitado en backend
3. Abrir consola del navegador (F12) y ver errores
4. Probar backend directamente:
   http://localhost:11113/docs
```

### **❌ APIs no responden:**

```
1. OpenWeather:
   - Verificar API key válida
   - Verificar límite de requests (60/min gratis)
   
2. NASA POWER:
   - Verificar conexión internet
   - API es gratis sin límite
```

---

## 📋 **ORDEN RECOMENDADO DE INICIO:**

```
1️⃣ Backend     (primero - ESP32 lo necesita)
2️⃣ ESP32       (se registra en backend)
3️⃣ Frontend    (consume backend y muestra datos)
4️⃣ Ngrok       (opcional - acceso remoto)
```

---

## 🎯 **RESULTADO ESPERADO:**

```
✅ Backend corriendo en puerto 11113
✅ Frontend corriendo en puerto 3002
✅ ESP32 registrado y enviando telemetría
✅ Dashboard mostrando datos reales
✅ Todas las APIs respondiendo
✅ Sistema 100% operativo

Todo funcionando correctamente 🚀
```

---

## 🔄 **SCRIPTS ÚTILES:**

### **Iniciar Todo:**
```bash
# 1. Backend
PROBAR_BACKEND_NUEVO.bat

# 2. Frontend (en otra terminal)
cd frontend
npm start

# 3. ESP32
# Programar con Arduino IDE
```

### **Detener Todo:**
```bash
DETENER.bat
```

### **Ver Estado:**
```bash
curl http://localhost:11113/api/status/health
```

### **Ver Dispositivos ESP32:**
```bash
curl http://localhost:11113/api/esp32/devices
```

---

## 📱 **ACCESO DESDE OTROS DISPOSITIVOS:**

### **En la misma red local:**
```
http://192.168.0.XXX:3002
(Reemplazar XXX con IP de tu PC)
```

### **Desde internet (con Ngrok):**
```
https://argentina.ngrok.pro
```

---

## ✅ **CHECKLIST FINAL:**

- [ ] ✅ Backend online (puerto 11113)
- [ ] ✅ Frontend online (puerto 3002)
- [ ] ✅ ESP32 registrado y online
- [ ] ✅ OpenWeather API funcionando
- [ ] ✅ NASA POWER API funcionando
- [ ] ✅ Panel de estado muestra 100%
- [ ] ✅ Datos reales desde ESP32
- [ ] ✅ Gráficos actualizándose
- [ ] ✅ Tabs funcionando
- [ ] ✅ Todo operativo

---

# 🎉 **¡SISTEMA COMPLETAMENTE FUNCIONAL!**

**Ahora podés:**
- ✅ Monitorear generación solar y eólica en tiempo real
- ✅ Ver pronósticos con IA
- ✅ Controlar relés automáticamente
- ✅ Proteger batería y turbina
- ✅ Dimensionar sistemas nuevos
- ✅ Gestionar múltiples ESP32
- ✅ Acceder remotamente

**Disfrutá tu sistema híbrido inteligente** 🔋⚡💨
