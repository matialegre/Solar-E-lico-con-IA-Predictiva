# 🔋 SISTEMA INVERSOR HÍBRIDO INTELIGENTE - CONTEXTO COMPLETO

**Para: Nueva IA que va a ayudar con este proyecto**  
**Fecha: Octubre 2025**  
**Estado: 95% funcional - Solo faltan 2 bugs críticos**

---

## 📊 QUÉ ES ESTE PROYECTO

Sistema COMPLETO de gestión energética híbrida (Solar + Eólico + Batería) con:
- **IA Predictiva** (Random Forest) usando datos meteorológicos reales
- **ESP32** con firmware complejo (FreeRTOS, sensores, relés, HTTP, JSON)
- **Backend FastAPI** (Puerto 11113) con ML, base de datos, APIs
- **Frontend React** (Puerto 11112) con dashboard, gráficos, control en tiempo real
- **Protección inteligente** contra embalamiento eólico
- **Estrategia automática** de priorización de fuentes
- **4 Relés** controlables remotamente (Solar, Eólica, Red, Carga)
- **6 ADCs** (4 voltajes + LDR + Anemómetro)

---

## 🚨 PROBLEMAS ACTUALES (LO QUE HAY QUE ARREGLAR)

### **PROBLEMA 1: GET -7 (Intermitente)**
**Síntoma:**
```
[12] POST:200 GET:-7 | R:---C | D34:0.000V D36:0.000V D35:0.000V D39:0.000V
```

**Causa raíz:** 
- Timeout de 15s no es suficiente para WiFi lento del usuario
- ESP pierde comandos cuando GET -7 ocurre

**Impacto:**
- Comandos se encolan en backend pero ESP no los recibe
- De 6 comandos enviados, solo 1 llega

**¿Qué NO funciona como workaround:**
- ❌ Aumentar timeout a 15s (ya probado, sigue fallando)
- ❌ Reintentos automáticos (no implementado)
- ❌ Cola persistente (se borra en cada GET)

**Solución ideal:**
- WebSocket bidireccional ESP ↔ Backend
- O sistema de ACK: ESP confirma comando ejecutado en siguiente telemetría


### **PROBLEMA 2: Sin confirmación real de comandos**
**Síntoma:**
Usuario envía comando → Backend dice "success" → No hay forma de saber si ESP lo ejecutó

**Qué pasa ahora:**
```bash
$ send_esp32_command.bat eolica on
{"status":"success",...}  # ← Backend dice OK, pero ESP quizás nunca lo recibió
```

**Solución ideal:**
- ESP incluye en telemetría: `{"last_command_executed": "eolica on", "timestamp": "..."}`
- Backend trackea: comandos_enviados vs comandos_ejecutados
- Script espera confirmación antes de decir "Listo"

---

## 🏗️ ARQUITECTURA ACTUAL (LO QUE YA FUNCIONA)

### **Estructura de carpetas:**
```
X:\PREDICCION DE CLIMA\
├── backend/                    # FastAPI (Puerto 11113)
│   ├── main.py                # Endpoints, ML, lógica principal
│   ├── requirements.txt       # fastapi, uvicorn, scikit-learn, etc
│   └── configuracion_usuario.json
├── frontend/                   # React (Puerto 11112)
│   ├── src/
│   │   ├── components/
│   │   │   ├── ESP32Control.jsx    # Control relés + ADCs
│   │   │   ├── ESP32Status.jsx
│   │   │   └── ...
│   │   └── api/
│   │       └── api.js         # axios, baseURL=11113
│   └── package.json
├── firmware_arduino_ide_2/
│   └── inversor_hibrido/
│       ├── inversor_hibrido.ino    # Main loop
│       ├── config.h                 # WiFi, SERVER_URL, pines
│       ├── sensors.h                # Lectura ADCs
│       ├── relays.h                 # Control relés
│       └── http_client.h            # POST/GET, JSON, comandos
├── send_esp32_command.bat     # Script para enviar comandos
├── test_reles.bat             # Menú interactivo relés
├── INICIAR_SISTEMA.bat        # Inicia backend + frontend
└── 📘 SISTEMA INVERSOR HÍBRIDO - MANUAL TÉCNICO COMPLETO.pdf (x4)
```

### **Puertos y URLs:**
- Backend: `http://190.211.201.217:11113` o `http://localhost:11113`
- Frontend: `http://localhost:11112`
- ESP32 IP: Dinámica (DHCP), ej: `192.168.1.105`

### **Endpoints Backend (los que importan):**
```
POST /api/esp32/telemetry         ← ESP envía datos cada 1s
GET  /api/esp32/commands/{id}     ← ESP consulta comandos cada 1s
POST /api/esp32/command/{id}      ← Frontend/script envía comando
GET  /api/esp32/estado/{id}       ← Frontend consulta estado ESP
```

### **Flujo de comandos (actual):**
```
1. Usuario presiona botón frontend o ejecuta .bat
2. POST /api/esp32/command → Backend encola comando
3. ESP hace GET /api/esp32/commands (polling cada 1s)
4. Backend retorna lista de comandos y vacía cola
5. ESP ejecuta comando, muestra en Serial
6. (NO HAY ACK - este es el problema)
```

---

## 💻 FIRMWARE ESP32 - DETALLES TÉCNICOS

### **Hardware:**
- Placa: ESP32 Dev Module
- Serial: 115200 baud
- WiFi: 2.4GHz

### **Pines configurados:**

#### ADC (0-3.3V, 12-bit):
- GPIO34 → Batería (v_bat_v)
- GPIO35 → Eólica DC filtrado (v_wind_v_dc) con filtro Biquad IIR
- GPIO36 → Solar (v_solar_v)
- GPIO39 → Carga (v_load_v)
- GPIO27 → LDR (irradiancia)
- GPIO14 → Anemómetro (pulsos)

#### Relés (OUTPUT, activo HIGH):
- GPIO26 → Panel Solar
- GPIO25 → Eólica
- GPIO32 → Red Backup
- GPIO33 → Carga
- GPIO23 → Freno embalamiento

### **Archivos del firmware:**

**config.h** - Configuración:
```cpp
#define WIFI_SSID "..."
#define WIFI_PASSWORD "..."
#define SERVER_URL "http://190.211.201.217:11113"
#define DEVICE_ID "ESP32_INVERSOR_001"

#define PIN_RELE_SOLAR  26
#define PIN_RELE_EOLICA 25
#define PIN_RELE_RED    32
#define PIN_RELE_CARGA  33
// ... etc
```

**http_client.h** - Comunicación:
- `sendStage1Telemetry()` - POST cada 1s con JSON {seq, v_bat_v, ...}
- `checkStage1Commands()` - GET cada 1s, parsea JSON, ejecuta comandos
- Timeout actual: 15000ms (15s)
- Serial output: `[seq] POST:code GET:code | R:xxxx | D34:x.xxx...`

**sensors.h** - Sensores:
- Filtro Biquad 2nd order Butterworth para extraer DC de señal AC eólica
- `readAllSensors()` lee todos los ADCs
- struct SensorData con todos los valores

**relays.h** - Relés:
- `setRelaySolar(bool)`, `setRelayEolica(bool)`, etc
- `aplicarEstrategia()` - Lógica automática de priorización
- Protección: no conectar eólica con freno activo

### **Loop principal (simplificado):**
```cpp
void loop() {
  readAllSensors();           // Leer ADCs
  sendStage1Telemetry();      // POST a /telemetry
  checkStage1Commands();      // GET /commands
  printStage1UART();          // Serial: 1 línea compacta
  
  delay(1000);  // 1 segundo entre iteraciones
}
```

### **Salida Serial (formato actual):**
```
[12] POST:200 GET:200 | R:---C | D34:0.000V D36:0.000V D35:0.000V D39:0.000V
```
Donde:
- `[12]` = secuencia
- `POST:200` = telemetría OK
- `GET:200` = comandos consultados OK (-7 = timeout)
- `R:---C` = Relés (S=Solar, E=Eólica, R=Red, C=Carga, -=OFF)
- `D34:0.000V` = GPIO34 voltaje con 3 decimales

**Cuando llega comando:**
```
***************************************
>>> PRENDER RELE EOLICO <<<
***************************************
⚡ Relé Eólica: CONECTADO
[13] POST:200 GET:200 | R:-E-C | D34:0.000V...
```

---

## 🐍 BACKEND - DETALLES TÉCNICOS

### **Stack:**
- FastAPI (Python)
- Uvicorn (ASGI server)
- SQLite (base de datos)
- scikit-learn (ML Random Forest)
- OpenWeatherMap API (datos meteorológicos)

### **main.py - Estructura:**

#### Variables globales:
```python
command_queue = {}  # {device_id: [commands]}
telemetry = {}      # {device_id: {last_telemetry, last_seen, relays}}
```

#### Endpoint recibir telemetría:
```python
@app.post("/api/esp32/telemetry")
async def recibir_telemetria_esp32(data: dict):
    device_id = data.get('device_id')
    
    # Guardar telemetría
    telemetry[device_id] = {
        'v_bat_v': data.get('v_bat_v'),
        'v_wind_v_dc': data.get('v_wind_v_dc'),
        # ...
        'last_seen': datetime.now()
    }
    
    print(f"[TELEM] {device_id} seq={data.get('seq')}")
    return {"status": "received"}
```

#### Endpoint encolar comando:
```python
@app.post("/api/esp32/command/{device_id}")
async def enviar_comando_esp32(device_id: str, command: dict):
    if device_id not in command_queue:
        command_queue[device_id] = []
    
    command_queue[device_id].append({
        'command': command.get('command'),
        'parameter': command.get('parameter'),
        'timestamp': datetime.now().isoformat()
    })
    
    print(f"📤 Comando encolado: {command}")
    return {"status": "success"}
```

#### Endpoint consultar comandos (ESP polling):
```python
@app.get("/api/esp32/commands/{device_id}")
async def obtener_comandos_esp32(device_id: str):
    commands = command_queue.get(device_id, [])
    command_queue[device_id] = []  # ← VACÍA LA COLA (problema si GET -7)
    
    if commands:
        print(f"[CMD] {device_id} → Sent: ...")
        return {"status": "CMD", "commands": commands}
    else:
        return {"status": "OK", "commands": []}
```

### **ML (Predicción):**
- Random Forest Regressor entrenado con históricos
- Predice generación solar/eólica 24h adelante
- Usa datos de OpenWeatherMap API
- Archivos: `modelo_solar.pkl`, `modelo_eolico.pkl`

### **Otros endpoints (funcionan bien):**
- `/api/dashboard` - Resumen general
- `/api/energy/history` - Histórico
- `/api/predictions/24h` - Predicciones ML
- `/api/wind/protection/status` - Estado protección embalamiento

---

## ⚛️ FRONTEND - DETALLES TÉCNICOS

### **Stack:**
- React 18
- React Router
- Axios (HTTP client)
- Recharts (gráficos)
- Lucide React (iconos)
- Tailwind CSS

### **Componentes relevantes:**

**ESP32Control.jsx** - Control de relés:
```jsx
const DEVICE_ID = 'ESP32_INVERSOR_001';
const API_BASE = 'http://190.211.201.217:11113';

// Fetch estado cada 2s
useEffect(() => {
  const interval = setInterval(async () => {
    const res = await axios.get(`${API_BASE}/api/esp32/estado/${DEVICE_ID}`);
    setEspData(res.data);
  }, 2000);
  return () => clearInterval(interval);
}, []);

// Enviar comando
const sendCommand = async (command, parameter) => {
  await axios.post(`${API_BASE}/api/esp32/command/${DEVICE_ID}`, {
    command,
    parameter
  });
};
```

**Problemas actuales en frontend:**
- ❌ Botones no confirman si comando fue ejecutado
- ❌ Estado de relés se actualiza cada 2s (si telemetría llega)
- ❌ Si GET -7, estado queda desactualizado

---

## 📄 DOCUMENTACIÓN EXISTENTE

El usuario YA TIENE 4 manuales PDF completos:
- `📘 SISTEMA INVERSOR HÍBRIDO - MANUAL TÉCNICO COMPLETO.pdf`
- `📘 SISTEMA INVERSOR HÍBRIDO - MANUAL TÉCNICO COMPLETO (1).pdf`
- `📘 SISTEMA INVERSOR HÍBRIDO - MANUAL TÉCNICO COMPLETO (2).pdf`
- `📘 SISTEMA INVERSOR HÍBRIDO - MANUAL TÉCNICO COMPLETO (3).pdf`

**Contienen:**
- Arquitectura completa del sistema
- Diagramas de flujo
- Explicación de ML
- Protección embalamiento
- Estrategia automática
- Instalación paso a paso
- Troubleshooting

---

## 🎯 QUÉ HAY QUE HACER (ALCANCE)

### ✅ LO QUE YA FUNCIONA (NO TOCAR):
- ✅ Backend FastAPI completo
- ✅ Frontend React completo
- ✅ Firmware compila sin errores
- ✅ ESP conecta WiFi
- ✅ Telemetría llega cada 1s
- ✅ ML predictions
- ✅ Dashboard completo
- ✅ Scripts .bat funcionan
- ✅ Relés se controlan (cuando GET 200)

### ❌ LO QUE HAY QUE ARREGLAR (SOLO ESTO):

#### TAREA 1: Eliminar GET -7
**Opciones:**
1. WebSocket bidireccional (mejor solución)
2. Aumentar más el timeout (parcial)
3. Reintentos automáticos en ESP (workaround)
4. Cola persistente en backend (no se borra si GET falla)

#### TAREA 2: Sistema de ACK
**Implementar:**
1. ESP incluye en telemetría: `last_command_executed`
2. Backend trackea: comandos_pendientes vs comandos_ejecutados
3. `send_esp32_command.bat` espera confirmación (polling hasta ver ACK)
4. Frontend muestra "Ejecutando..." → "Ejecutado ✓"

### 📏 ALCANCE MÁXIMO: 50 PROMPTS (150 CRÉDITOS)

Cada prompt debe:
- Ser específico y accionable
- Modificar SOLO lo necesario
- Mantener todo lo que ya funciona
- Verificar que funciona antes de continuar

---

## 🛠️ COMANDOS ÚTILES

### Iniciar sistema completo:
```cmd
cd X:\PREDICCION DE CLIMA
INICIAR_SISTEMA.bat
```

### Iniciar backend solo:
```cmd
cd X:\PREDICCION DE CLIMA\backend
python main.py
```

### Iniciar frontend solo:
```cmd
cd X:\PREDICCION DE CLIMA\frontend
npm start
```

### Probar relés:
```cmd
cd X:\PREDICCION DE CLIMA
test_reles.bat
```

### Enviar comando individual:
```cmd
send_esp32_command.bat eolica on
send_esp32_command.bat eolica off
```

### Verificar estado ESP:
```cmd
curl http://190.211.201.217:11113/api/esp32/estado/ESP32_INVERSOR_001
```

---

## 🔍 DEBUGGING

### Ver logs backend:
La consola de Python muestra:
```
[TELEM] ESP32_INVERSOR_001 seq=123 ...
📤 Comando encolado: ...
[CMD] ESP32_INVERSOR_001 → Sent: eolica(on)
```

### Ver logs ESP (Serial Monitor 115200):
```
[12] POST:200 GET:200 | R:---C | D34:0.000V...
***************************************
>>> PRENDER RELE EOLICO <<<
***************************************
```

### Ver logs frontend (consola navegador F12):
```
Error loading ESP32 devices: Network Error
```

---

## 📊 MÉTRICAS ACTUALES

- **Telemetría**: 1 mensaje/segundo ✅
- **Latencia comando** (cuando funciona): < 2 segundos ✅
- **Pérdida comandos**: ~83% (5 de 6 se pierden por GET -7) ❌
- **GET -7 frecuencia**: ~50% de los requests ❌
- **Frontend actualización**: 2 segundos ✅
- **Uptime ESP**: > 24 horas ✅

---

## 🎓 CONCEPTOS CLAVE

### HTTP Polling (actual):
- ESP pregunta cada 1s si hay comandos
- Simple, pero pierde comandos si GET falla
- No es tiempo real

### WebSocket (ideal):
- Backend empuja comandos al ESP
- Bidireccional
- Tiempo real
- Requiere cambiar firmware y backend

### Sistema de ACK:
- ESP confirma comando ejecutado
- Backend sabe si llegó o no
- Frontend puede mostrar estado real

---

## ⚠️ RESTRICCIONES

1. **NO CAMBIAR** la arquitectura general (ESP32 + Backend + Frontend)
2. **NO ELIMINAR** funcionalidades que ya funcionan (ML, protección, etc)
3. **MANTENER** los puertos 11113 y 11112
4. **MANTENER** la estructura de archivos
5. **PRIORIZAR** soluciones simples sobre complejas

---

## 📞 SI ALGO NO ESTÁ CLARO

Preguntar al usuario:
- ¿Qué componente específico falla?
- ¿Qué dice el Serial Monitor del ESP?
- ¿Qué dice la consola del backend?
- ¿Qué errores muestra el frontend?

NUNCA asumir. SIEMPRE verificar.

---

## 🎯 OBJETIVO FINAL

**Sistema 100% funcional donde:**
- ✅ Comandos llegan SIEMPRE (GET 200 siempre, nunca -7)
- ✅ Usuario sabe SI el comando fue ejecutado (ACK visible)
- ✅ Frontend actualiza estado en tiempo real
- ✅ Todo lo demás sigue funcionando (ML, gráficos, protección, etc)

**Tiempo estimado:** 3-4 horas con IA eficiente (50 prompts máximo)

---

FIN DEL CONTEXTO COMPLETO
