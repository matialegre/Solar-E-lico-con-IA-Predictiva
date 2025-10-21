# 📚 Referencia de API

## Base URL
```
http://localhost:8000
```

## Autenticación
Actualmente no requiere autenticación. En producción, implementar JWT o API Keys.

---

## 📊 Endpoints de Energía

### GET /api/energy/current
Obtener estado actual del sistema de energía.

**Response:**
```json
{
  "timestamp": "2024-01-15T10:30:00",
  "solar_power_w": 1245.5,
  "wind_power_w": 567.8,
  "total_generation_w": 1813.3,
  "battery_voltage_v": 48.2,
  "battery_current_a": -5.3,
  "battery_soc_percent": 75.4,
  "battery_power_w": -255.5,
  "load_power_w": 450.0,
  "active_source": "solar",
  "grid_connected": false,
  "auto_mode_enabled": true
}
```

### GET /api/energy/history
Obtener histórico de energía.

**Query Parameters:**
- `hours` (int, default: 24): Horas de histórico

**Response:**
```json
{
  "count": 288,
  "records": [
    {
      "timestamp": "2024-01-15T10:30:00",
      "solar_power_w": 1245.5,
      "wind_power_w": 567.8,
      "battery_soc_percent": 75.4,
      "load_power_w": 450.0,
      "active_source": "solar"
    }
  ]
}
```

### POST /api/energy/record
Registrar datos desde ESP32 o dispositivo IoT.

**Request Body:**
```json
{
  "solar_voltage_v": 45.2,
  "solar_current_a": 5.3,
  "wind_voltage_v": 38.5,
  "wind_current_a": 3.2,
  "battery_voltage_v": 48.1,
  "battery_current_a": -2.5,
  "load_current_a": 6.8,
  "temperature_c": 35.2
}
```

**Response:**
```json
{
  "status": "ok",
  "message": "Datos registrados"
}
```

---

## 🌤️ Endpoints de Clima

### GET /api/weather/current
Obtener clima actual.

**Response:**
```json
{
  "timestamp": "2024-01-15T10:30:00",
  "temperature_c": 22.5,
  "humidity_percent": 65.0,
  "pressure_hpa": 1013.2,
  "wind_speed_ms": 5.2,
  "wind_direction_deg": 180,
  "cloud_cover_percent": 25,
  "rain_1h_mm": 0.0,
  "solar_radiation_wm2": 850.0,
  "description": "Parcialmente nublado"
}
```

### GET /api/weather/forecast
Obtener pronóstico meteorológico.

**Query Parameters:**
- `hours` (int, default: 24): Horas de pronóstico

**Response:**
```json
{
  "count": 24,
  "forecast": [
    {
      "timestamp": "2024-01-15T11:00:00",
      "temperature_c": 23.0,
      "wind_speed_ms": 5.5,
      "cloud_cover_percent": 30,
      "solar_radiation_wm2": 900.0
    }
  ]
}
```

---

## 🤖 Endpoints de Predicción IA

### GET /api/predictions/24h
Obtener predicciones de energía para las próximas 24 horas.

**Response:**
```json
{
  "generated_at": "2024-01-15T10:30:00",
  "predictions": [
    {
      "prediction_time": "2024-01-15T11:00:00",
      "predicted_solar_w": 1300.0,
      "predicted_wind_w": 550.0,
      "predicted_consumption_w": 480.0,
      "predicted_battery_soc": 76.5,
      "confidence_score": 0.85
    }
  ],
  "total_solar_24h_wh": 15600,
  "total_wind_24h_wh": 12800,
  "total_consumption_24h_wh": 11200,
  "autonomy_hours": 18.5,
  "energy_deficit_hours": [18, 19, 20]
}
```

### GET /api/predictions/autonomy
Calcular autonomía actual de la batería.

**Response:**
```json
{
  "autonomy_hours": 12.5,
  "battery_soc": 75.4,
  "current_consumption_w": 450.0,
  "timestamp": "2024-01-15T10:30:00"
}
```

---

## 🎛️ Endpoints de Control

### POST /api/control/manual
Control manual de fuentes de energía.

**Request Body:**
```json
{
  "source": "solar",
  "action": "enable",
  "value": null
}
```

**Sources:** `solar`, `wind`, `battery`, `grid`, `generator`  
**Actions:** `enable`, `disable`, `priority`

**Response:**
```json
{
  "success": true,
  "message": "Modo manual activado: solar habilitado"
}
```

### POST /api/control/auto
Activar/desactivar modo automático IA.

**Request Body:**
```json
{
  "enabled": true,
  "min_battery_soc": 20,
  "max_battery_soc": 100,
  "priority_list": ["solar", "wind", "battery", "grid"]
}
```

**Response:**
```json
{
  "success": true,
  "message": "Modo automático activado"
}
```

### GET /api/control/decision
Obtener última decisión de la IA.

**Response:**
```json
{
  "selected_source": "solar",
  "reason": "Renovables suficientes (1813W)",
  "actions": ["Usar energía renovable", "Posible carga de batería"],
  "priority_level": 0
}
```

---

## 🚨 Endpoints de Alertas

### GET /api/alerts/current
Obtener alertas activas del sistema.

**Response:**
```json
{
  "count": 2,
  "alerts": [
    {
      "type": "battery_low",
      "severity": "warning",
      "message": "Batería baja: 25.3%",
      "action": "Considerar reducir consumo o activar generador"
    },
    {
      "type": "predicted_deficit",
      "severity": "info",
      "message": "Déficit energético previsto en 3 horas de las próximas 24h",
      "action": "Planificar uso eficiente de energía"
    }
  ]
}
```

### GET /api/alerts/history
Obtener histórico de alertas.

**Response:**
```json
{
  "count": 15,
  "alerts": [
    {
      "id": 1,
      "timestamp": "2024-01-15T08:30:00",
      "type": "battery_critical",
      "severity": "critical",
      "message": "Batería en nivel crítico: 18.5%",
      "resolved": true
    }
  ]
}
```

---

## 📊 Endpoints de Dashboard

### GET /api/dashboard
Obtener todos los datos para el dashboard (combinado).

**Response:**
```json
{
  "energy_status": { /* ... */ },
  "weather": { /* ... */ },
  "latest_prediction": { /* ... */ },
  "autonomy_hours": 12.5,
  "alerts": [ /* ... */ ],
  "auto_mode": true
}
```

---

## 🔧 Endpoints de Sistema

### GET /api/system/status
Estado general del sistema.

**Response:**
```json
{
  "status": "online",
  "version": "1.0.0",
  "auto_mode": true,
  "simulation_mode": false,
  "uptime": "N/A",
  "battery_capacity_wh": 5000,
  "max_solar_power_w": 3000,
  "max_wind_power_w": 2000
}
```

---

## 🔌 WebSocket

### WS /ws
Conexión WebSocket para actualizaciones en tiempo real.

**Mensaje de actualización:**
```json
{
  "type": "update",
  "data": {
    "energy": { /* estado de energía */ },
    "weather": { /* clima actual */ },
    "decision": { /* decisión de IA */ },
    "timestamp": "2024-01-15T10:30:00"
  }
}
```

**Ejemplo de uso (JavaScript):**
```javascript
const ws = new WebSocket('ws://localhost:8000/ws');

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Actualización:', data);
};
```

---

## 📖 Documentación Interactiva

Swagger UI disponible en:
```
http://localhost:8000/docs
```

ReDoc disponible en:
```
http://localhost:8000/redoc
```

---

## ⚠️ Códigos de Error

| Código | Descripción |
|--------|-------------|
| 200 | OK - Petición exitosa |
| 400 | Bad Request - Datos inválidos |
| 404 | Not Found - Recurso no encontrado |
| 500 | Internal Server Error - Error del servidor |
| 503 | Service Unavailable - Servicio no disponible |

---

## 🔐 Seguridad (Producción)

Para producción, implementar:

1. **Autenticación JWT**
2. **Rate Limiting**
3. **HTTPS/TLS**
4. **CORS configurado**
5. **Validación de entrada**

Ejemplo con token:
```bash
curl -H "Authorization: Bearer <token>" \
     http://api.ejemplo.com/api/energy/current
```
