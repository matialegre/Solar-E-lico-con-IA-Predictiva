# 🔋 Sistema Inversor Híbrido Inteligente

Sistema de gestión energética con IA para instalaciones solar + eólico.

---

## 🚀 Inicio Rápido

### **Iniciar Todo:**
```bash
INICIAR.bat
```

### **Detener Todo:**
```bash
DETENER.bat
```

---

## 📋 URLs del Sistema

| Servicio | URL | Descripción |
|----------|-----|-------------|
| **Dashboard** | http://localhost:3002 | Interfaz principal |
| **API Backend** | http://localhost:8801/docs | Documentación API |
| **Ngrok Público** | https://argentina.ngrok.pro | Acceso público |
| **Panel Ngrok** | http://localhost:4040 | Monitor ngrok |

---

## 📁 Estructura

```
PREDICCION DE CLIMA/
├── backend/          # API Python (FastAPI)
├── frontend/         # Dashboard React
├── firmware/         # Código ESP32
├── INICIAR.bat       # ⭐ Iniciar sistema
├── DETENER.bat       # ⭐ Detener sistema
└── README.md         # Este archivo
```

---

## ⚙️ Configuración

### **Backend (.env):**
```bash
cd backend
notepad .env
```

Configurar:
- `OPENWEATHER_API_KEY` - Tu API key (gratis en openweathermap.org)
- `LATITUDE` / `LONGITUDE` - Coordenadas de tu ubicación

### **Frontend (.env):**
```bash
cd frontend
notepad .env
```

Configurar:
- `REACT_APP_API_URL` - URL del backend

---

## 🔧 Instalación Primera Vez

### **Backend:**
```bash
cd backend
pip install -r requirements.txt
```

### **Frontend:**
```bash
cd frontend
npm install
```

### **Firmware ESP32:**
```bash
cd firmware
pip install platformio
pio run --target upload
```

---

## 📡 Arquitectura HTTP (Sin MQTT)

```
[ESP32] ──HTTP POST──> [Backend] ──WebSocket──> [Dashboard]
        ◄──HTTP GET───           ◄────────────
```

**Protocolo IP puro:** No necesita MQTT ni puertos abiertos en el router.

---

## 🧪 Simulador ESP32

Para probar sin hardware:
```bash
python simulador_esp32.py
```

---

## 🆘 Solución de Problemas

### **Backend no inicia:**
- Verifica `backend/.env` tenga API key válida
- Revisa `backend/main.py` para errores

### **Frontend en blanco:**
- Verifica que backend esté corriendo primero
- Abre http://localhost:8801/docs para confirmar

### **Ngrok falla:**
- Verifica que tengas cuenta en ngrok.com
- Configura: `ngrok config add-authtoken TU_TOKEN`

---

## 📊 Características

- ✅ Predicción meteorológica con IA
- ✅ Gestión inteligente solar + eólico
- ✅ Protección batería LiFePO4
- ✅ Dashboard en tiempo real
- ✅ Simulador para desarrollo
- ✅ API REST completa

---

## 📝 Licencia

MIT License - Ver LICENSE

---

## 🤝 Soporte

Para dudas o problemas, revisar:
- Documentación API: http://localhost:8801/docs
- Código fuente: Carpetas backend/, frontend/, firmware/

---

**Desarrollado con FastAPI + React + ESP32**
