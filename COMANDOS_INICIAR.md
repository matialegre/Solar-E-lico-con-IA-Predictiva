# 🚀 COMANDOS PARA INICIAR EL SISTEMA

## 1️⃣ BACKEND (FastAPI + Python)

### Iniciar servidor backend
```cmd
cd X:\PREDICCION DE CLIMA\backend
python main.py
```

**Esperado en consola:**
```
✅ Modelos cargados desde disco
✅ Modelos ML cargados desde disco
✅ Base de datos inicializada
✅ Sistema Inversor Inteligente iniciado
📍 Ubicación: -38.7183, -62.2663
🔋 Capacidad batería: 5000.0 Wh
INFO:     Uvicorn running on http://0.0.0.0:11113
```

**URL Backend:** `http://localhost:11113`

---

## 2️⃣ FRONTEND (React + Vite)

### Iniciar servidor de desarrollo
```cmd
cd X:\PREDICCION DE CLIMA\frontend
npm start
```

**Esperado en consola:**
```
Compiled successfully!

You can now view inversor-inteligente-frontend in the browser.

  Local:            http://localhost:3000
  On Your Network:  http://192.168.x.x:3000
```

**URL Frontend:** `http://localhost:3000`
**Nota:** Se abrirá automáticamente en el navegador

---

## 3️⃣ ESP32 (Firmware Arduino)

### Subir firmware al ESP32
1. Abrir **Arduino IDE**
2. Abrir archivo: `X:\PREDICCION DE CLIMA\firmware_arduino_ide_2\inversor_hibrido\inversor_hibrido.ino`
3. Seleccionar placa: **ESP32 Dev Module**
4. Seleccionar puerto: **COMx** (el puerto donde está conectado tu ESP32)
5. Click en **Subir** (Upload)

**Esperado en Serial Monitor (115200 baud):**
```
╔════════════════════════════════════════════════════════════╗
║   🔋 SISTEMA INVERSOR HÍBRIDO INTELIGENTE - ESP32 🔋     ║
║                    Firmware 2.0                           ║
╚════════════════════════════════════════════════════════════╝

✅ Sensores inicializados
✅ Relés inicializados
✅ WiFi conectado
   IP: 192.168.x.x
✅ Cliente HTTP listo
✅ Dispositivo registrado

╔════════════════════════════════════════╗
║   ✅ SISTEMA INICIADO CORRECTAMENTE   ║
╚════════════════════════════════════════╝
```

---

## 4️⃣ PRUEBAS DE CONTROL DE RELÉS

### Usar script .bat (Windows)

**Opción A - Script con menú interactivo:**
```cmd
cd X:\PREDICCION DE CLIMA
test_reles.bat
```
Este script muestra un menú con opciones 1-9 para controlar cada relé.

**Opción B - Comandos directos:**
```cmd
cd X:\PREDICCION DE CLIMA

# === PANEL SOLAR ===
send_esp32_command.bat solar on
send_esp32_command.bat solar off

# === EOLICA ===
send_esp32_command.bat eolica on
send_esp32_command.bat eolica off

# === RED BACKUP ===
send_esp32_command.bat red on
send_esp32_command.bat red off

# === CARGA ===
send_esp32_command.bat carga on
send_esp32_command.bat carga off

# === EMERGENCIA ===
send_esp32_command.bat apagar_todo
```

### Usar PowerShell (alternativa)
```powershell
$u = "http://190.211.201.217:11113/api/esp32/command/ESP32_INVERSOR_001"
$h = @{ "Content-Type" = "application/json" }

# Encender eólica
$b = '{"command":"eolica","parameter":"on"}'
Invoke-WebRequest -Uri $u -Headers $h -Method POST -Body $b

# Apagar eólica
$b = '{"command":"eolica","parameter":"off"}'
Invoke-WebRequest -Uri $u -Headers $h -Method POST -Body $b
```

---

## 5️⃣ ENDPOINTS API ÚTILES

### Obtener estado del ESP32
```
GET http://190.211.201.217:11113/api/esp32/estado/ESP32_INVERSOR_001
```

**Respuesta:**
```json
{
  "status": "success",
  "device_id": "ESP32_INVERSOR_001",
  "last_seen": "2025-10-22T12:00:00",
  "telemetry": {
    "v_bat_v": 0.153,
    "v_wind_v_dc": 0.002,
    "v_solar_v": 0.176,
    "v_load_v": 0.000
  },
  "relays": {
    "solar": false,
    "wind": false,
    "grid": false,
    "load": true
  },
  "raw_adc": {
    "adc1_bat1": 0.000,
    "adc4_solar": 0.000,
    "adc5_wind": 0.000,
    "adc6_load": 0.000
  }
}
```

### Enviar comando
```
POST http://190.211.201.217:11113/api/esp32/command/ESP32_INVERSOR_001
Content-Type: application/json

{
  "command": "eolica",
  "parameter": "on"
}
```

### Ver comandos pendientes
```
GET http://190.211.201.217:11113/api/esp32/commands/ESP32_INVERSOR_001
```

---

## 6️⃣ FRONTEND: CONTROL DE RELÉS

Una vez que tanto **backend** como **frontend** estén corriendo:

1. Abrir navegador: `http://localhost:5173`
2. Buscar el panel **"🔌 Control ESP32"**
3. Usar botones **ON/OFF** para cada relé:
   - Panel Solar
   - Eólica
   - Red Backup
   - Carga
4. Ver lecturas ADC en tiempo real (0–3.3V)
5. Ver voltajes procesados Stage 1

---

## 7️⃣ VERIFICACIÓN DE FUNCIONAMIENTO

### En el ESP32 (Serial Monitor)
Al enviar un comando desde frontend o .bat, deberías ver:

```
MENSAJE DE SERVIDOR: PRENDER RELE EOLICO
⚡ Relé Eólica: CONECTADO
POST 200 | GET 200 | Resp={"status":"CMD","count":1}
GPIO34 → Batería1 (0–3.3V): 0.000V
GPIO35 → Batería2 (0–3.3V): 0.000V
GPIO36 → Corriente Eólica RAW (0–3.3V): 0.000V | Filtrada DC: 0.000V
GPIO39 → Corriente Carga (0–3.3V): 0.000V
```

### En el Backend (consola Python)
```
📤 Comando encolado para ESP32_INVERSOR_001: {'command': 'eolica', 'parameter': 'on'}
INFO: "POST /api/esp32/command/ESP32_INVERSOR_001" 200 OK
[CMD] ESP32_INVERSOR_001 → Sent: eolica(on)
INFO: "GET /api/esp32/commands/ESP32_INVERSOR_001" 200 OK
```

### En el Frontend
- Los estados de los relés se actualizan en tiempo real
- Las lecturas ADC se refrescan cada 2 segundos
- El botón cambia de color según el estado

---

## 8️⃣ TROUBLESHOOTING

### Problema: Comandos no llegan al ESP
**Solución:**
1. Verificar que el backend esté corriendo y escuchando en puerto 11113
2. Verificar que el ESP tenga WiFi conectado (ver Serial Monitor)
3. Verificar que `SERVER_URL` en `config.h` apunte a la IP correcta

### Problema: Frontend no se conecta al backend
**Solución:**
1. Verificar que backend esté en `http://190.211.201.217:11113`
2. Si estás en la misma máquina, también puedes usar `http://localhost:11113`
3. Verificar firewall de Windows permita el puerto 11113

### Problema: ADC siempre en 0V
**Solución:**
1. Los pines ADC están sin cablear (esperado si no hay hardware conectado)
2. Para probar: conecta un divisor resistivo simple (3.3V → R1 → ADC → R2 → GND)

---

## 9️⃣ PINES DE HARDWARE CONFIGURADOS

### ADC (Entradas analógicas 0–3.3V)
- **GPIO34** → Batería (voltaje)
- **GPIO35** → Corriente Eólica (DC filtrado)
- **GPIO36** → Corriente Solar
- **GPIO39** → Corriente Carga
- **GPIO27** → LDR (irradiancia)
- **GPIO14** → Anemómetro (pulsos)

### Relés (Salidas digitales)
- **GPIO26** → Relé Panel Solar
- **GPIO25** → Relé Eólica
- **GPIO32** → Relé Red Backup
- **GPIO33** → Relé Carga
- **GPIO23** → Relé Freno (embalamiento)

---

## 🎯 RESUMEN RÁPIDO

**Opción A - Script automático (inicia todo):**
```cmd
cd X:\PREDICCION DE CLIMA
INICIAR_SISTEMA.bat
```
Esto abre 2 ventanas: Backend y Frontend

**Opción B - Manual:**
```cmd
# Terminal 1 - Backend
cd X:\PREDICCION DE CLIMA\backend
python main.py

# Terminal 2 - Frontend
cd X:\PREDICCION DE CLIMA\frontend
npm start

# Terminal 3 - Pruebas
cd X:\PREDICCION DE CLIMA
test_reles.bat
```

**Frontend:** http://localhost:3000  
**Backend:** http://localhost:11113  
**ESP32:** Ver Serial Monitor (115200 baud)
