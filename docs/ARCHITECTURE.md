# 🏗️ Arquitectura del Sistema

## Visión General

El Sistema Inversor Inteligente Híbrido es una solución completa de gestión energética que combina:
- **Hardware IoT** (ESP32)
- **Backend inteligente** (Python FastAPI)
- **Frontend moderno** (React)
- **IA predictiva** (Machine Learning)

```
┌──────────────────────────────────────────────────────────────┐
│                    Sistema Completo                           │
├──────────────────────────────────────────────────────────────┤
│                                                                │
│  ┌─────────────┐      ┌──────────────┐      ┌─────────────┐ │
│  │             │      │              │      │             │ │
│  │   ESP32     │─────▶│   Backend    │◀─────│  Frontend   │ │
│  │  Hardware   │ WiFi │   FastAPI    │ HTTP │   React     │ │
│  │             │      │              │      │             │ │
│  └─────────────┘      └──────────────┘      └─────────────┘ │
│       │                      │                                │
│       │                      │                                │
│   ┌───▼────┐           ┌────▼─────┐                         │
│   │Sensores│           │   IA     │                         │
│   │ V/A/T  │           │Predictiva│                         │
│   └────────┘           └──────────┘                         │
│                              │                                │
│                        ┌─────▼──────┐                        │
│                        │OpenWeather │                        │
│                        │    API     │                        │
│                        └────────────┘                        │
└──────────────────────────────────────────────────────────────┘
```

## 📦 Componentes

### 1. Hardware Layer (ESP32)

**Responsabilidades:**
- Lectura de sensores de voltaje/corriente
- Control de relés para conmutación
- Comunicación WiFi con backend
- Protecciones locales de hardware

**Tecnologías:**
- ESP32 (Dual-core, FreeRTOS)
- Sensores ADC
- Módulos de relés/MOSFETs
- C++ con Arduino Framework

**Tareas FreeRTOS:**
```
Core 0:
├── taskSensorRead (Prioridad: Alta)
│   └── Lee sensores cada 5s
└── taskControlLogic (Prioridad: Media)
    └── Lógica de protección local

Core 1:
└── taskServerComm (Prioridad: Media)
    └── Envía datos al servidor cada 10s
```

### 2. Backend Layer (FastAPI)

**Responsabilidades:**
- API RESTful para todos los componentes
- Gestión de base de datos
- Ejecución de IA predictiva
- Integración con API meteorológica
- WebSocket para tiempo real
- Toma de decisiones inteligentes

**Arquitectura:**
```
backend/
├── main.py                 # Servidor FastAPI principal
├── config.py               # Configuración
├── database.py             # Modelos SQLAlchemy
├── schemas.py              # Pydantic schemas
├── ai_predictor.py         # IA predictiva
├── weather_service.py      # Servicio meteorológico
├── inverter_controller.py  # Controlador inteligente
└── simulator.py            # Simulador para pruebas
```

**Flujo de Datos:**
```
1. ESP32 → POST /api/energy/record → Database
2. Scheduler → Weather API → Database
3. AI Predictor → Weather + History → Predictions
4. Controller → Predictions + Current → Decision
5. WebSocket → Broadcast → Frontend
```

### 3. AI/ML Layer

**Modelo Predictivo:**
- **Algoritmo**: Random Forest Regressor
- **Features**: 
  - Temporales (hora, día, mes, estacionalidad)
  - Meteorológicas (temperatura, nubosidad, viento)
  - Históricas (consumo previo, generación)

**Predicciones:**
1. **Generación Solar**: f(hora, nubosidad, radiación, temperatura)
2. **Generación Eólica**: f(velocidad_viento, dirección, hora)
3. **Consumo**: f(hora, día_semana, temperatura, histórico)

**Pipeline:**
```
Weather Data + Historical Data
         ↓
   Feature Engineering
         ↓
   Random Forest Models
         ↓
   24h Predictions
         ↓
   Energy Balance Calculation
         ↓
   Decision Logic
```

### 4. Frontend Layer (React)

**Responsabilidades:**
- Dashboard interactivo
- Visualización en tiempo real
- Gráficos de histórico y predicciones
- Panel de control manual
- Gestión de alertas

**Arquitectura de Componentes:**
```
App.jsx
├── Header
├── EnergyMetrics (6 cards)
├── EnergyCharts
│   ├── Historical Chart
│   ├── Battery Chart
│   └── Prediction Chart
├── PredictionPanel
│   ├── 24h Summary
│   └── Autonomy Display
├── WeatherWidget
├── ControlPanel
│   ├── Auto Mode Toggle
│   └── Manual Controls
└── AlertsPanel
```

**Flujo de Datos:**
```
WebSocket ──▶ React State ──▶ Components
    ↑              ↓
    │         Re-render
    │              ↓
    └───────── UI Update
```

## 🔄 Flujo de Decisiones

### Modo Automático (IA Activa)

```
┌─────────────────────────────────────────┐
│  1. Recopilar Estado Actual             │
│     - Generación solar/eólica           │
│     - SoC de batería                    │
│     - Consumo actual                    │
└────────────┬────────────────────────────┘
             ↓
┌─────────────────────────────────────────┐
│  2. Obtener Predicción Meteorológica    │
│     - API OpenWeatherMap (24h)          │
│     - Radiación solar estimada          │
│     - Velocidad del viento              │
└────────────┬────────────────────────────┘
             ↓
┌─────────────────────────────────────────┐
│  3. Ejecutar Modelo de IA               │
│     - Predecir generación 24h           │
│     - Predecir consumo 24h              │
│     - Calcular balance energético       │
└────────────┬────────────────────────────┘
             ↓
┌─────────────────────────────────────────┐
│  4. Tomar Decisión                      │
│     - Priorizar fuentes disponibles     │
│     - Calcular autonomía                │
│     - Detectar déficit futuro           │
└────────────┬────────────────────────────┘
             ↓
┌─────────────────────────────────────────┐
│  5. Ejecutar Acción                     │
│     - Conmutar relés (ESP32)            │
│     - Generar alertas                   │
│     - Notificar usuario                 │
└─────────────────────────────────────────┘
```

### Lógica de Priorización

```python
if battery_soc < MIN_SOC:
    priority = ["solar", "wind", "grid", "battery"]
    alert("CRITICAL: Battery Low")

elif battery_soc < 30:
    priority = ["solar", "wind", "battery", "grid"]
    alert("WARNING: Battery Low")

elif (solar + wind) > load * 1.5:
    priority = ["solar", "wind"]
    action("charge_battery")

elif (solar + wind) >= load:
    priority = ["solar", "wind"]

else:
    priority = ["battery"]
    calculate_autonomy()
```

## 💾 Base de Datos

### Esquema

```sql
energy_records
├── id (PK)
├── timestamp
├── solar_power_w
├── wind_power_w
├── battery_soc_percent
├── load_power_w
└── active_source

weather_data
├── id (PK)
├── timestamp
├── temperature_c
├── wind_speed_ms
├── cloud_cover_percent
└── solar_radiation_wm2

predictions
├── id (PK)
├── created_at
├── prediction_time
├── predicted_solar_w
├── predicted_wind_w
└── confidence_score

ai_decisions
├── id (PK)
├── timestamp
├── decision_type
├── selected_source
├── reason
└── predicted_autonomy_hours

alerts
├── id (PK)
├── timestamp
├── alert_type
├── severity
├── message
└── resolved
```

## 🔐 Seguridad

### Implementadas
- ✅ Validación de entrada (Pydantic)
- ✅ Protecciones de hardware local (ESP32)
- ✅ CORS configurado
- ✅ Timeouts en requests

### Recomendadas para Producción
- 🔒 Autenticación JWT
- 🔒 HTTPS/TLS
- 🔒 Rate limiting
- 🔒 Validación de origen ESP32
- 🔒 Encriptación de datos sensibles

## 📈 Escalabilidad

### Horizontal
- Backend puede ejecutarse en múltiples instancias
- Load balancer (Nginx)
- Base de datos PostgreSQL (en lugar de SQLite)

### Vertical
- Modelos de IA más complejos (LSTM, Transformers)
- Más fuentes de datos (satélites, estaciones)
- Procesamiento en tiempo real más rápido

## 🧪 Testing

### Niveles de Testing
1. **Unit Tests**: Funciones individuales
2. **Integration Tests**: API endpoints
3. **Hardware Tests**: Simulador
4. **End-to-End**: Sistema completo

### Modo Simulación
Permite probar sin hardware:
```python
SIMULATION_MODE=true
```

## 📊 Monitoreo

### Métricas Clave
- Uptime del sistema
- Latencia de API
- Precisión de predicciones
- Estado de batería
- Generación vs Consumo

### Logs
- Backend: Archivo + Console
- ESP32: Serial Monitor
- Frontend: Browser Console

## 🔄 Ciclo de Actualización

```
Backend:     30 segundos
Frontend:    30 segundos (polling) + WebSocket (real-time)
ESP32:       5-10 segundos
AI Predictions: 5 minutos
Weather Data: 10 minutos
```

## 🌐 Despliegue

### Desarrollo
```
Local Machine
├── Backend: localhost:8000
├── Frontend: localhost:3000
└── ESP32: WiFi local
```

### Producción
```
Cloud/VPS
├── Backend: api.dominio.com (Nginx + Gunicorn)
├── Frontend: dominio.com (Static files)
├── Database: PostgreSQL
└── ESP32: Internet → VPN/Port Forward
```

## 🎯 Próximas Mejoras

1. **MQTT** para comunicación más eficiente
2. **Base de datos time-series** (InfluxDB)
3. **Notificaciones push** (Firebase, Telegram)
4. **App móvil** (React Native)
5. **Múltiples dispositivos** ESP32
6. **Dashboard administrativo**
7. **Exportación de reportes** (PDF)
8. **Integración con Home Assistant**
