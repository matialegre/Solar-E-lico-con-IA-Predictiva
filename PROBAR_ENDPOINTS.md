# 🧪 PROBAR ENDPOINTS NUEVOS

Documentación de los nuevos endpoints del backend.

---

## 📡 ESP32 - Gestión de Dispositivos

### **1. Registrar ESP32**
```http
POST http://localhost:11113/api/esp32/register

Body:
{
  "device_id": "ESP32_INVERSOR_001",
  "ip_local": "192.168.0.150",
  "mac_address": "AA:BB:CC:DD:EE:FF",
  "firmware_version": "2.0",
  "latitude": -38.7183,
  "longitude": -62.2663
}

Response:
{
  "status": "registered",
  "device_id": "ESP32_INVERSOR_001",
  "message": "Dispositivo registrado correctamente",
  "timestamp": "2025-01-21T13:45:00"
}
```

### **2. Heartbeat**
```http
POST http://localhost:11113/api/esp32/heartbeat

Body:
{
  "device_id": "ESP32_INVERSOR_001",
  "uptime": 3600,
  "free_heap": 245000,
  "rssi": -45
}

Response:
{
  "status": "ok",
  "timestamp": "2025-01-21T13:45:30"
}
```

### **3. Listar Dispositivos**
```http
GET http://localhost:11113/api/esp32/devices

Response:
{
  "devices": [
    {
      "device_id": "ESP32_INVERSOR_001",
      "ip_local": "192.168.0.150",
      "mac_address": "AA:BB:CC:DD:EE:FF",
      "firmware_version": "2.0",
      "latitude": -38.7183,
      "longitude": -62.2663,
      "registered_at": "2025-01-21T13:45:00",
      "last_seen": "2025-01-21T13:45:30",
      "status": "online",
      "heartbeat": {
        "uptime": 3600,
        "free_heap": 245000,
        "rssi": -45
      }
    }
  ],
  "total": 1,
  "online": 1,
  "offline": 0
}
```

### **4. Obtener Configuración**
```http
GET http://localhost:11113/api/esp32/config/ESP32_INVERSOR_001

Response:
{
  "device_id": "ESP32_INVERSOR_001",
  "latitude": -38.7183,
  "longitude": -62.2663,
  "battery_capacity_wh": 5000.0,
  "solar_area_m2": 16.0,
  "wind_power_w": 2000.0,
  "proteccion_activa": true,
  "aprendizaje_activo": false
}
```

### **5. Actualizar Configuración**
```http
POST http://localhost:11113/api/esp32/config/ESP32_INVERSOR_001

Body:
{
  "latitude": -34.6037,
  "longitude": -58.3816,
  "battery_capacity_wh": 10000.0,
  "solar_area_m2": 20.0,
  "wind_power_w": 3000.0,
  "proteccion_activa": true,
  "aprendizaje_activo": true
}

Response:
{
  "status": "updated",
  "device_id": "ESP32_INVERSOR_001",
  "config": {...},
  "timestamp": "2025-01-21T14:00:00"
}
```

---

## 🧮 DIMENSIONAMIENTO

### **6. Opción 1: Desde Consumo**
```http
POST http://localhost:11113/api/dimensionamiento/opcion1

Body:
{
  "latitude": -38.7183,
  "longitude": -62.2663,
  "consumo_diario_kwh": 15.6,
  "dias_autonomia": 2,
  "voltaje_sistema": 48
}

Response:
{
  "tipo": "opcion1_desde_consumo",
  "ubicacion": {
    "latitude": -38.7183,
    "longitude": -62.2663,
    "zona": "Argentina"
  },
  "clima_historico": {
    "location": {...},
    "historical_data": {
      "solar_irradiance_avg": 4.3,
      "wind_speed_avg": 5.2,
      "solar_irradiance_monthly": [4.5, 4.2, ...],
      "wind_speed_monthly": [5.1, 5.3, ...]
    },
    "solar": {
      "annual_avg_kwh_m2_day": 4.3,
      "best_month": 1,
      "worst_month": 7
    },
    "wind": {
      "annual_avg_ms": 5.2,
      "best_month": 12,
      "worst_month": 3
    }
  },
  "entrada": {
    "consumo_diario_kwh": 15.6,
    "consumo_mensual_kwh": 468,
    "consumo_anual_kwh": 5694
  },
  "sistema_solar": {
    "calculos": {
      "paso1": {
        "nombre": "Horas Sol Pico (HSP)",
        "ecuacion": "HSP = Irradiancia_diaria",
        "valores": "HSP = 4.3",
        "resultado": "4.30 horas"
      },
      "paso2": {
        "nombre": "Energía solar necesaria",
        "ecuacion": "E_solar = Consumo_diario × 60%",
        "valores": "E_solar = 15.6 × 0.60",
        "resultado": "9.36 kWh/día"
      },
      "paso3": {
        "nombre": "Potencia pico necesaria",
        "ecuacion": "P_pico = E_solar / (HSP × η_sistema)",
        "valores": "P_pico = 9360 / (4.30 × 0.85)",
        "resultado": "2562 W"
      },
      "paso4": {
        "nombre": "Número de paneles",
        "ecuacion": "N = ceil(P_pico / P_panel)",
        "valores": "N = ceil(2562 / 400)",
        "resultado": "7 paneles"
      }
    },
    "resultado": {
      "paneles": {
        "modelo": "Panel 400W Monocristalino",
        "cantidad": 7,
        "potencia_unitaria_w": 400,
        "potencia_total_w": 2800,
        "area_total_m2": 14.0,
        "eficiencia": 0.20
      },
      "generacion": {
        "diaria_kwh": 10.2,
        "mensual_kwh": 306,
        "anual_kwh": 3723
      },
      "cobertura": {
        "porcentaje": 65.4,
        "excedente_kwh": 0.84
      },
      "costo": {
        "paneles_usd": 1400,
        "estructura_usd": 210,
        "inversor_usd": 840,
        "instalacion_usd": 280,
        "total_estimado_usd": 2310
      }
    }
  },
  "sistema_eolico": {
    "calculos": {
      "paso1": {
        "nombre": "Área de barrido",
        "ecuacion": "A = π × r²",
        "valores": "A = π × (1.8/2)²",
        "resultado": "2.54 m²"
      },
      "paso2": {
        "nombre": "Potencia del viento",
        "ecuacion": "P_viento = 0.5 × ρ × A × v³",
        "valores": "P = 0.5 × 1.225 × 2.54 × 5.2³",
        "resultado": "218 W"
      },
      "paso3": {
        "nombre": "Límite de Betz (máximo teórico)",
        "ecuacion": "P_max = P_viento × 59.3%",
        "valores": "P_max = 218 × 0.593",
        "resultado": "129 W"
      },
      "paso4": {
        "nombre": "Potencia real aprovechable",
        "ecuacion": "P_real = P_viento × η_turbina",
        "valores": "P_real = 218 × 0.35",
        "resultado": "76 W"
      },
      "paso5": {
        "nombre": "Generación diaria",
        "ecuacion": "E_diaria = P_real × 24h",
        "valores": "E = 76 × 24",
        "resultado": "1.83 kWh/día"
      }
    },
    "resultado": {
      "turbinas": {
        "modelo": "Turbina 1000W",
        "cantidad": 4,
        "potencia_unitaria_w": 1000,
        "diametro_m": 1.8,
        "velocidad_arranque_ms": 3.0
      },
      "generacion": {
        "diaria_kwh": 7.32,
        "mensual_kwh": 219.6,
        "anual_kwh": 2671.8
      },
      "cobertura": {
        "porcentaje": 46.9,
        "excedente_kwh": 1.08
      },
      "costo": {
        "turbinas_usd": 2600,
        "torre_usd": 1600,
        "controlador_usd": 800,
        "instalacion_usd": 650,
        "total_estimado_usd": 4160
      }
    }
  },
  "sistema_bateria": {
    "calculos": {...},
    "resultado": {
      "baterias": {
        "tipo": "LiFePO4 (recomendado)",
        "voltaje_unitario": 12,
        "capacidad_unitaria_ah": 200,
        "configuracion_serie": 4,
        "configuracion_paralelo": 2,
        "total_baterias": 8,
        "capacidad_total_kwh": 19.2,
        "voltaje_total": 48
      },
      "autonomia": {
        "dias": 2,
        "profundidad_descarga": 80.0
      },
      "costo": {
        "baterias_usd": 3600,
        "bms_usd": 300,
        "cables_usd": 150,
        "total_estimado_usd": 4050
      }
    }
  },
  "resumen": {
    "generacion_total_diaria_kwh": 17.52,
    "cobertura_porcentaje": 112.3,
    "balance_diario_kwh": 1.92,
    "autonomia_dias": 2,
    "costo_total_usd": 10520,
    "ahorro_anual_usd": 854.1,
    "payback_years": 12.3,
    "roi_anual_porcentaje": 8.1
  },
  "recomendacion": {
    "viabilidad": "EXCELENTE",
    "mensaje": "El sistema cubre el 112% del consumo",
    "siguiente_paso": "Configurar ESP32 con esta ubicación y comenzar monitoreo"
  }
}
```

### **7. Opción 2: Desde Recursos Existentes**
```http
POST http://localhost:11113/api/dimensionamiento/opcion2

Body:
{
  "latitude": -38.7183,
  "longitude": -62.2663,
  "potencia_solar_w": 3000,
  "area_solar_m2": 15.0,
  "potencia_eolica_w": 2000,
  "diametro_turbina_m": 2.5
}

Response:
{
  "tipo": "opcion2_desde_recursos",
  "ubicacion": {...},
  "clima_historico": {...},
  "entrada": {
    "potencia_solar_w": 3000,
    "area_solar_m2": 15.0,
    "potencia_eolica_w": 2000,
    "diametro_turbina_m": 2.5
  },
  "calculos": {
    "solar": {
      "ecuacion": "E_solar = (P_solar / 1000) × HSP × η_sistema",
      "valores": "E = (3000 / 1000) × 4.30 × 0.85",
      "resultado": "10.97 kWh/día"
    },
    "eolico": {
      "ecuacion": "P_eolica = 0.5 × ρ × A × v³ × η_turbina",
      "valores": "P = 0.5 × 1.225 × 4.91 × 5.2³ × 0.35",
      "resultado": "2.98 kWh/día"
    }
  },
  "resultado": {
    "generacion_solar_kwh_dia": 10.97,
    "generacion_eolica_kwh_dia": 2.98,
    "generacion_total_kwh_dia": 13.95,
    "generacion_mensual_kwh": 418.5,
    "generacion_anual_kwh": 5091.75,
    "consumo_maximo_soportable_kwh_dia": 12.56,
    "potencia_promedio_w": 523
  },
  "sistema_bateria_recomendado": {...},
  "recomendacion": {
    "mensaje": "Tu sistema puede generar hasta 13.9 kWh/día",
    "consumo_max": "Consumo máximo recomendado: 12.6 kWh/día",
    "suficiencia": "BUENA"
  }
}
```

### **8. Obtener Datos Climáticos**
```http
GET http://localhost:11113/api/dimensionamiento/clima/-38.7183/-62.2663

Response:
{
  "location": {
    "latitude": -38.7183,
    "longitude": -62.2663
  },
  "historical_data": {
    "solar_irradiance_avg": 4.3,
    "wind_speed_avg": 5.2,
    "temperature_avg": 15.8,
    "solar_irradiance_monthly": [4.5, 4.2, 4.0, 3.8, 3.5, 3.2, 3.4, 3.9, 4.2, 4.6, 4.8, 4.7],
    "wind_speed_monthly": [5.1, 5.3, 5.5, 5.2, 4.9, 4.7, 4.8, 5.0, 5.2, 5.3, 5.4, 5.6],
    "years_analyzed": 10,
    "period": "2014-2023"
  },
  "solar": {
    "annual_avg_kwh_m2_day": 4.3,
    "monthly_avg": [...],
    "best_month": 11,
    "worst_month": 6
  },
  "wind": {
    "annual_avg_ms": 5.2,
    "monthly_avg": [...],
    "best_month": 12,
    "worst_month": 6
  },
  "temperature": {
    "annual_avg_c": 15.8
  },
  "data_source": "NASA POWER API",
  "period": "2014-2023"
}
```

---

## 🧪 PROBAR CON CURL

```bash
# 1. Registrar ESP32
curl -X POST http://localhost:11113/api/esp32/register \
  -H "Content-Type: application/json" \
  -d '{"device_id":"ESP32_TEST","ip_local":"192.168.0.150","mac_address":"AA:BB:CC:DD:EE:FF","firmware_version":"2.0"}'

# 2. Listar dispositivos
curl http://localhost:11113/api/esp32/devices

# 3. Calcular dimensionamiento
curl -X POST http://localhost:11113/api/dimensionamiento/opcion1 \
  -H "Content-Type: application/json" \
  -d '{"latitude":-38.7183,"longitude":-62.2663,"consumo_diario_kwh":15.6,"dias_autonomia":2,"voltaje_sistema":48}'

# 4. Obtener clima
curl http://localhost:11113/api/dimensionamiento/clima/-38.7183/-62.2663
```

---

## 📊 SWAGGER DOCS

Abrir en navegador:
```
http://localhost:11113/docs
```

Verás todos los endpoints documentados automáticamente.

---

**¡Backend listo para probar!** 🚀
