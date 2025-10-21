from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta
import asyncio
import json

from database import get_db, init_db, EnergyRecord, WeatherData, Prediction, AIDecision, Alert
from schemas import (
    EnergyStatus, WeatherInfo, PredictionData, Prediction24h,
    ControlCommand, AutoModeConfig, ESP32SensorData, DashboardData
)
from config import get_settings, get_user_config
from inverter_controller import inverter_controller
from weather_service import weather_service
from ai_predictor import energy_predictor
from system_calculator import get_system_calculator
from pattern_learner import pattern_learner
from wind_protection import wind_protection
from battery_protection import battery_protection
from efficiency_monitor import efficiency_monitor
from smart_strategy import smart_strategy

# Importar nuevos routers
from routers import esp32_router, dimensionamiento_router, ml_router, status_router

settings = get_settings()

# Inicializar FastAPI
app = FastAPI(
    title="Sistema Inversor Inteligente Híbrido",
    description="API para control de inversor solar-eólico-batería con IA predictiva",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Servir archivos estáticos del frontend (si existen)
try:
    app.mount("/static", StaticFiles(directory="static"), name="static")
except:
    pass  # Si no existe el directorio, no pasa nada

# WebSocket connections manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except:
                pass

manager = ConnectionManager()

# ===== INCLUIR ROUTERS =====
app.include_router(esp32_router.router)
app.include_router(dimensionamiento_router.router)
app.include_router(ml_router.router)
app.include_router(status_router.router)


# ===== EVENTOS =====

@app.on_event("startup")
async def startup_event():
    """Inicializar aplicación"""
    init_db()
    print("✅ Sistema Inversor Inteligente iniciado")
    print(f"📍 Ubicación: {settings.latitude}, {settings.longitude}")
    print(f"🔋 Capacidad batería: {settings.battery_capacity_wh} Wh")
    
    # Iniciar tarea de actualización periódica
    asyncio.create_task(periodic_update())


# ===== TAREAS PERIÓDICAS =====

async def periodic_update():
    """Actualización periódica del sistema (cada 30 segundos)"""
    while True:
        try:
            # Obtener datos actuales (en producción vendrían del ESP32)
            # En modo simulación, usar datos simulados
            
            # Actualizar clima
            weather = weather_service.get_current_weather()
            
            # Tomar decisión de IA
            decision = inverter_controller.make_decision()
            
            # Broadcast a clientes WebSocket
            await manager.broadcast({
                'type': 'update',
                'data': {
                    'energy': inverter_controller.current_state,
                    'weather': weather,
                    'decision': decision,
                    'timestamp': datetime.now().isoformat()
                }
            })
            
        except Exception as e:
            print(f"Error en actualización periódica: {e}")
        
        await asyncio.sleep(30)


# ===== ENDPOINTS DE ENERGÍA =====

@app.get("/api/energy/current", response_model=EnergyStatus)
async def get_current_energy(db: Session = Depends(get_db)):
    """Obtener estado actual de energía"""
    
    state = inverter_controller.current_state
    
    return EnergyStatus(
        timestamp=datetime.now(),
        solar_power_w=state['solar_power_w'],
        wind_power_w=state['wind_power_w'],
        total_generation_w=state['solar_power_w'] + state['wind_power_w'],
        battery_voltage_v=state.get('battery_voltage_v', 48.0),
        battery_current_a=state.get('battery_current_a', 0.0),
        battery_soc_percent=state['battery_soc_percent'],
        battery_power_w=state['battery_power_w'],
        load_power_w=state['load_power_w'],
        active_source=inverter_controller.current_source,
        grid_connected=state['grid_available'],
        auto_mode_enabled=inverter_controller.auto_mode
    )


@app.get("/api/energy/history")
async def get_energy_history(
    hours: int = 24,
    db: Session = Depends(get_db)
):
    """Obtener histórico de energía"""
    
    cutoff = datetime.now() - timedelta(hours=hours)
    
    records = db.query(EnergyRecord)\
        .filter(EnergyRecord.timestamp >= cutoff)\
        .order_by(EnergyRecord.timestamp.desc())\
        .limit(1000)\
        .all()
    
    return {
        'count': len(records),
        'records': [
            {
                'timestamp': r.timestamp.isoformat(),
                'solar_power_w': r.solar_power_w,
                'wind_power_w': r.wind_power_w,
                'battery_soc_percent': r.battery_soc_percent,
                'load_power_w': r.load_power_w,
                'active_source': r.active_source
            }
            for r in reversed(records)
        ]
    }


@app.post("/api/energy/record")
async def record_energy_data(
    data: ESP32SensorData,
    db: Session = Depends(get_db)
):
    """Registrar datos desde ESP32"""
    
    # Calcular potencias
    solar_power = data.solar_voltage_v * data.solar_current_a
    wind_power = data.wind_voltage_v * data.wind_current_a
    battery_power = data.battery_voltage_v * data.battery_current_a
    load_power = data.battery_voltage_v * data.load_current_a
    
    # Calcular SoC (simplificado)
    # En producción usar modelo más preciso
    battery_soc = min(100, max(0, (data.battery_voltage_v - 44) / (54.6 - 44) * 100))
    
    # Actualizar controlador
    inverter_controller.update_state({
        'solar_power_w': solar_power,
        'wind_power_w': wind_power,
        'battery_soc_percent': battery_soc,
        'battery_power_w': battery_power,
        'load_power_w': load_power,
        'battery_voltage_v': data.battery_voltage_v,
        'battery_current_a': data.battery_current_a,
    })
    
    # Guardar en DB
    record = EnergyRecord(
        solar_power_w=solar_power,
        wind_power_w=wind_power,
        total_generation_w=solar_power + wind_power,
        battery_voltage_v=data.battery_voltage_v,
        battery_current_a=data.battery_current_a,
        battery_soc_percent=battery_soc,
        battery_power_w=battery_power,
        load_power_w=load_power,
        active_source=inverter_controller.current_source
    )
    
    db.add(record)
    db.commit()
    
    return {'status': 'ok', 'message': 'Datos registrados'}


# ===== ENDPOINTS DE CLIMA =====

@app.get("/api/weather/current", response_model=WeatherInfo)
async def get_current_weather():
    """Obtener clima actual"""
    
    weather = weather_service.get_current_weather()
    
    return WeatherInfo(**weather)


@app.get("/api/weather/forecast")
async def get_weather_forecast():
    """Obtener pronóstico de 5 días con estimación solar"""
    forecast_data = weather_service.get_forecast_5days()
    return forecast_data


@app.get("/api/weather/forecast/hours")
async def get_weather_forecast_hours(hours: int = 24):
    """Obtener pronóstico meteorológico"""
    
    if hours <= 24:
        forecast = weather_service.get_hourly_forecast_24h()
    else:
        forecast = weather_service.get_forecast_5days()
    
    return {
        'count': len(forecast),
        'forecast': [
            {
                'timestamp': f['timestamp'].isoformat(),
                **{k: v for k, v in f.items() if k != 'timestamp'}
            }
            for f in forecast[:hours]
        ]
    }


# ===== ENDPOINTS DE PREDICCIÓN =====

@app.get("/api/predictions/24h", response_model=Prediction24h)
async def get_predictions_24h():
    """Obtener predicciones para 24 horas"""
    
    prediction_data = inverter_controller.predict_energy_balance_24h()
    
    predictions = [
        PredictionData(
            prediction_time=p['timestamp'],
            predicted_solar_w=p['predicted_solar_w'],
            predicted_wind_w=p['predicted_wind_w'],
            predicted_consumption_w=p['predicted_consumption_w'],
            predicted_battery_soc=0,  # Se calcula en balance
            confidence_score=0.85
        )
        for p in prediction_data['predictions']
    ]
    
    return Prediction24h(
        generated_at=datetime.now(),
        predictions=predictions,
        total_solar_24h_wh=prediction_data['total_solar_24h_wh'],
        total_wind_24h_wh=prediction_data['total_wind_24h_wh'],
        total_consumption_24h_wh=prediction_data['total_consumption_24h_wh'],
        autonomy_hours=prediction_data['autonomy_hours'],
        energy_deficit_hours=prediction_data['deficit_hours']
    )


@app.get("/api/predictions/autonomy")
async def get_autonomy():
    """Calcular autonomía actual"""
    
    autonomy = inverter_controller.calculate_autonomy()
    
    return {
        'autonomy_hours': autonomy,
        'battery_soc': inverter_controller.current_state['battery_soc_percent'],
        'current_consumption_w': inverter_controller.current_state['load_power_w'],
        'timestamp': datetime.now().isoformat()
    }


# ===== ENDPOINTS DE CONTROL =====

@app.post("/api/control/manual")
async def manual_control(command: ControlCommand):
    """Control manual de fuentes"""
    
    result = inverter_controller.set_manual_control(
        command.source,
        command.action == "enable"
    )
    
    return result


@app.post("/api/control/auto")
async def auto_mode_control(config: AutoModeConfig):
    """Activar/desactivar modo automático"""
    
    result = inverter_controller.set_auto_mode(config.enabled)
    
    return result


@app.get("/api/control/decision")
async def get_ai_decision():
    """Obtener última decisión de IA"""
    
    decision = inverter_controller.make_decision()
    
    return decision


# ===== ENDPOINTS DE ALERTAS =====

@app.get("/api/alerts/current")
async def get_current_alerts():
    """Obtener alertas activas"""
    
    alerts = inverter_controller.check_alerts()
    
    return {
        'count': len(alerts),
        'alerts': alerts
    }


@app.get("/api/alerts/history")
async def get_alerts_history(db: Session = Depends(get_db)):
    """Obtener histórico de alertas"""
    
    alerts = db.query(Alert)\
        .order_by(Alert.timestamp.desc())\
        .limit(100)\
        .all()
    
    return {
        'count': len(alerts),
        'alerts': [
            {
                'id': a.id,
                'timestamp': a.timestamp.isoformat(),
                'type': a.alert_type,
                'severity': a.severity,
                'message': a.message,
                'resolved': a.resolved
            }
            for a in alerts
        ]
    }


# ===== DASHBOARD =====

@app.get("/api/dashboard", response_model=DashboardData)
async def get_dashboard_data(db: Session = Depends(get_db)):
    """Obtener todos los datos para el dashboard"""
    
    energy_status = await get_current_energy(db)
    
    try:
        weather = await get_current_weather()
    except:
        weather = None
    
    try:
        prediction_24h = await get_predictions_24h(db)
        latest_prediction = prediction_24h.predictions[0] if prediction_24h.predictions else None
    except:
        latest_prediction = None
    
    alerts = inverter_controller.check_alerts()
    autonomy = inverter_controller.calculate_autonomy()
    
    return DashboardData(
        energy_status=energy_status,
        weather=weather,
        latest_prediction=latest_prediction,
        autonomy_hours=autonomy,
        alerts=alerts,
        auto_mode=inverter_controller.auto_mode
    )


# ===== WEBSOCKET =====

@app.websocket("/api/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket para actualizaciones en tiempo real"""
    await manager.connect(websocket)
    try:
        while True:
            # Mantener conexión viva
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)


# ===== ESTADO DEL SISTEMA =====

@app.get("/api/system/status")
async def get_system_status():
    """Estado general del sistema"""
    
    return {
        'status': 'online',
        'version': '1.0.0',
        'auto_mode': inverter_controller.auto_mode,
        'simulation_mode': settings.simulation_mode,
        'uptime': 'N/A',
        'battery_capacity_wh': settings.battery_capacity_wh,
        'max_solar_power_w': settings.max_solar_power_w,
        'max_wind_power_w': settings.max_wind_power_w,
    }


# ===== DIMENSIONAMIENTO Y MACHINE LEARNING =====

@app.get("/api/system/calculate")
async def calculate_system_requirements():
    """
    Calcula los requerimientos del sistema híbrido basándose en:
    - Consumo promedio de la casa
    - Ubicación geográfica (latitud/longitud)
    - Datos meteorológicos históricos
    """
    calculator = get_system_calculator(settings.latitude, settings.longitude)
    
    # Obtener datos meteorológicos promedio
    try:
        weather_data = weather_service.get_current_weather()
        solar_radiation = 5.0  # Default
        wind_speed = 6.0  # Default
    except:
        solar_radiation = 5.0
        wind_speed = 6.0
    
    requirements = calculator.calculate_system_requirements(
        average_consumption_w=settings.average_house_consumption_w,
        battery_capacity_wh=settings.battery_capacity_wh,
        avg_solar_radiation_kwh_m2=solar_radiation,
        avg_wind_speed_ms=wind_speed,
        autonomy_days=2.0
    )
    
    return requirements


@app.get("/api/patterns/analyze")
async def analyze_consumption_patterns():
    """
    Analiza los patrones de consumo aprendidos
    """
    if not settings.enable_pattern_learning:
        return {
            'status': 'disabled',
            'message': 'El aprendizaje de patrones está deshabilitado'
        }
    
    analysis = pattern_learner.analyze_patterns()
    return analysis


@app.get("/api/patterns/predict")
async def predict_consumption(hours: int = 4):
    """
    Predice el consumo de las próximas horas basándose en patrones aprendidos
    """
    if not settings.enable_pattern_learning:
        return {
            'status': 'disabled',
            'predictions': []
        }
    
    predictions = pattern_learner.predict_next_hours(hours_ahead=hours)
    return {
        'status': 'success',
        'hours_ahead': hours,
        'predictions': predictions
    }


@app.get("/api/patterns/battery-recommendation")
async def get_battery_recommendation():
    """
    Obtiene recomendación de cuándo cargar la batería
    basándose en patrones de consumo aprendidos
    """
    if not settings.enable_pattern_learning:
        return {
            'status': 'disabled',
            'recommendation': 'Aprendizaje de patrones deshabilitado'
        }
    
    recommendation = pattern_learner.get_battery_charging_recommendation()
    return recommendation


@app.post("/api/patterns/record")
async def record_consumption(power_w: float, previous_power_w: float = 0):
    """
    Registra un punto de consumo para el aprendizaje de patrones
    También detecta eventos de electrodomésticos
    """
    if not settings.enable_pattern_learning:
        return {'status': 'disabled'}
    
    # Agregar al historial
    pattern_learner.add_consumption_record(datetime.now(), power_w)
    
    # Detectar eventos (heladera, microondas, etc.)
    event = pattern_learner.detect_appliance_event(power_w, previous_power_w)
    
    return {
        'status': 'success',
        'recorded': True,
        'event': event,
        'total_records': len(pattern_learner.consumption_history)
    }


# ===== PROTECCIÓN EÓLICA =====

@app.get("/api/wind/protection/status")
async def get_wind_protection_status(
    wind_speed: float = 10.0,
    voltage: float = 48.0,
    rpm: float = None
):
    """
    Verifica estado de protección contra embalamiento eólico
    """
    status = wind_protection.check_overspeed_conditions(
        current_wind_speed_ms=wind_speed,
        current_voltage=voltage,
        current_rpm=rpm
    )
    return status


@app.post("/api/wind/protection/brake/activate")
async def activate_emergency_brake(reason: str = "Activación manual de emergencia"):
    """
    Activa manualmente el freno de emergencia eólico
    """
    result = wind_protection.manual_brake_activation(reason)
    return result


@app.post("/api/wind/protection/brake/deactivate")
async def deactivate_emergency_brake():
    """
    Desactiva el freno de emergencia (solo si es seguro)
    """
    result = wind_protection.manual_brake_deactivation()
    return result


@app.get("/api/wind/protection/specs")
async def get_protection_specs():
    """
    Obtiene especificaciones del sistema de protección eólica
    """
    return {
        'brake_resistor': wind_protection.get_brake_resistor_specs(),
        'relay_configuration': wind_protection.get_relay_configuration(),
        'thresholds': {
            'max_wind_speed_ms': wind_protection.max_wind_speed_ms,
            'max_rpm': wind_protection.max_rpm,
            'max_voltage': wind_protection.max_voltage,
            'warning_wind_speed_ms': wind_protection.warning_wind_speed,
            'warning_rpm': wind_protection.warning_rpm,
            'warning_voltage': wind_protection.warning_voltage
        }
    }


# ===== PROTECCIÓN DE BATERÍA =====

@app.get("/api/battery/protection/status")
async def get_battery_protection_status(
    battery_soc: float = 50.0,
    solar_power: float = 0.0,
    wind_power: float = 0.0,
    load_power: float = 650.0,
    battery_power: float = 0.0
):
    """
    Analiza la estrategia de uso de batería y protección
    """
    strategy = battery_protection.analyze_battery_strategy(
        battery_soc=battery_soc,
        solar_power_w=solar_power,
        wind_power_w=wind_power,
        load_power_w=load_power,
        battery_power_w=battery_power
    )
    return strategy


@app.get("/api/battery/protection/projection")
async def get_battery_life_projection(
    current_soc: float = 50.0,
    daily_cycles: float = 1.0,
    battery_capacity_kwh: float = 5.0
):
    """
    Proyecta la vida útil de la batería basándose en uso actual
    """
    projection = battery_protection.get_battery_life_projection(
        current_soc=current_soc,
        daily_cycles=daily_cycles,
        battery_capacity_kwh=battery_capacity_kwh
    )
    return projection


@app.get("/")
async def root():
    """Endpoint raíz - Servir el frontend"""
    try:
        return FileResponse("static/index.html")
    except:
        return {
            'name': 'Sistema Inversor Inteligente Híbrido',
            'version': '1.0.0',
            'status': 'online',
            'docs': '/docs',
            'note': 'Frontend no encontrado. Ejecuta BUILD_Y_SERVIR.bat'
        }

@app.get("/api")
async def api_root():
    """Información de la API"""
    return {
        'name': 'Sistema Inversor Inteligente Híbrido',
        'version': '1.0.0',
        'status': 'online',
        'docs': '/docs'
    }


# ===== CONFIGURACIÓN DE USUARIO =====

@app.get("/api/configuracion/usuario")
async def obtener_configuracion_usuario():
    """
    Obtiene la configuración personalizada del usuario
    """
    user_config = get_user_config()
    if user_config:
        return {
            'status': 'success',
            'configurado': True,
            'configuracion': user_config
        }
    else:
        return {
            'status': 'not_configured',
            'configurado': False,
            'mensaje': 'No hay configuración personalizada. Ejecuta CONFIGURAR_SISTEMA.bat'
        }


# ===== MONITOREO DE EFICIENCIA =====

@app.get("/api/efficiency/solar")
async def monitorear_eficiencia_solar(
    irradiancia_w_m2: float = 800.0,  # De sensor LDR
    area_paneles_m2: float = 6.0,  # Área total paneles
    potencia_generada_w: float = 850.0,  # De sensor corriente
    temperatura_c: float = 25.0  # De sensor temperatura
):
    """
    Monitorea eficiencia de paneles solares en tiempo real
    Compara irradiancia solar vs potencia generada
    """
    eficiencia = efficiency_monitor.calcular_eficiencia_solar(
        irradiancia_w_m2=irradiancia_w_m2,
        area_paneles_m2=area_paneles_m2,
        potencia_generada_w=potencia_generada_w,
        temperatura_ambiente_c=temperatura_c
    )
    return eficiencia


@app.get("/api/efficiency/wind")
async def monitorear_eficiencia_eolica(
    velocidad_viento_ms: float = 8.0,  # De anemómetro o API
    potencia_generada_w: float = 400.0,  # De sensor corriente
    potencia_nominal_w: float = 1000.0,  # De configuración
    area_barrido_m2: float = None  # Opcional
):
    """
    Monitorea eficiencia de turbina eólica en tiempo real
    Compara velocidad viento vs potencia generada
    """
    eficiencia = efficiency_monitor.calcular_eficiencia_eolica(
        velocidad_viento_ms=velocidad_viento_ms,
        potencia_generada_w=potencia_generada_w,
        potencia_nominal_turbina_w=potencia_nominal_w,
        area_barrido_m2=area_barrido_m2
    )
    return eficiencia


@app.get("/api/efficiency/tendencia/{componente}")
async def analizar_tendencia_eficiencia(componente: str):
    """
    Analiza tendencia de eficiencia en el tiempo
    componente: 'solar' o 'eolica'
    """
    tendencia = efficiency_monitor.analizar_tendencia(componente=componente)
    return tendencia


@app.get("/api/strategy/smart")
async def obtener_estrategia_inteligente():
    """
    Analiza pronóstico del clima y genera estrategia inteligente de carga
    """
    try:
        # Obtener pronóstico
        forecast = weather_service.get_forecast_5days()
        
        if not forecast or 'forecast' not in forecast:
            return {
                'status': 'error',
                'mensaje': 'No se pudo obtener pronóstico'
            }
        
        # Analizar y generar estrategia
        estrategia = smart_strategy.analizar_pronostico(forecast['forecast'])
        
        return estrategia
    except Exception as e:
        return {
            'status': 'error',
            'mensaje': str(e)
        }


@app.get("/api/strategy/charging-target")
async def calcular_objetivo_carga(
    bateria_actual: float = 50.0,
    consumo_diario_kwh: float = 15.0,
    capacidad_bateria_kwh: float = 5.0
):
    """
    Calcula nivel de carga objetivo basándose en pronóstico
    """
    try:
        # Obtener pronóstico
        forecast = weather_service.get_forecast_5days()
        estrategia = smart_strategy.analizar_pronostico(forecast['forecast'])
        
        # Calcular objetivo
        objetivo = smart_strategy.calcular_carga_objetivo(
            bateria_actual_percent=bateria_actual,
            dias_sin_sol=estrategia['analisis']['dias_sin_sol'],
            consumo_diario_kwh=consumo_diario_kwh,
            capacidad_bateria_kwh=capacidad_bateria_kwh
        )
        
        return {
            'status': 'success',
            'objetivo': objetivo,
            'estrategia_resumida': estrategia['estrategia'].get('accion_inmediata')
        }
    except Exception as e:
        return {
            'status': 'error',
            'mensaje': str(e)
        }


@app.get("/api/efficiency/dashboard")
async def obtener_dashboard_eficiencia(
    # Solar
    irradiancia_w_m2: float = 800.0,
    area_paneles_m2: float = 6.0,
    potencia_solar_w: float = 850.0,
    temperatura_c: float = 25.0,
    # Eólica
    velocidad_viento_ms: float = 8.0,
    potencia_eolica_w: float = 400.0,
    potencia_nominal_turbina_w: float = 1000.0
):
    """
    Dashboard completo de eficiencia de todos los componentes
    """
    solar = efficiency_monitor.calcular_eficiencia_solar(
        irradiancia_w_m2=irradiancia_w_m2,
        area_paneles_m2=area_paneles_m2,
        potencia_generada_w=potencia_solar_w,
        temperatura_ambiente_c=temperatura_c
    )
    
    eolica = efficiency_monitor.calcular_eficiencia_eolica(
        velocidad_viento_ms=velocidad_viento_ms,
        potencia_generada_w=potencia_eolica_w,
        potencia_nominal_turbina_w=potencia_nominal_turbina_w
    )
    
    return {
        'status': 'success',
        'timestamp': datetime.now().isoformat(),
        'solar': solar,
        'eolica': eolica,
        'alertas_activas': (solar.get('alerta', False) or eolica.get('alerta', False))
    }


# ===== ESP32 / IOT DEVICES =====

@app.post("/api/esp32/telemetry")
async def recibir_telemetria_esp32(data: dict):
    """
    Recibir telemetría desde ESP32
    
    Formato esperado:
    {
        "device_id": "ESP32_001",
        "timestamp": "2025-10-21T08:00:00",
        "solar": {"voltage": 48.2, "current": 12.5, "power": 602.5, "irradiance": 850},
        "wind": {"voltage": 47.8, "current": 5.2, "power": 248.5, "wind_speed": 8.5},
        "battery": {"voltage": 50.1, "current": 8.3, "power": 415.8, "soc": 65.5},
        "load_power_w": 435.0,
        "temperature_c": 22.5
    }
    """
    try:
        device_id = data.get('device_id', 'UNKNOWN')
        
        # Actualizar estado del controlador con datos reales
        inverter_controller.current_state.update({
            'solar_power_w': data.get('solar', {}).get('power', 0),
            'wind_power_w': data.get('wind', {}).get('power', 0),
            'battery_voltage_v': data.get('battery', {}).get('voltage', 48.0),
            'battery_soc_percent': data.get('battery', {}).get('soc', 50.0),
            'battery_power_w': data.get('battery', {}).get('power', 0),
            'load_power_w': data.get('load_power_w', 0),
            'timestamp': data.get('timestamp', datetime.now().isoformat())
        })
        
        # Broadcast a clientes WebSocket
        await manager.broadcast({
            'type': 'esp32_update',
            'device_id': device_id,
            'data': data
        })
        
        print(f"📡 Telemetría recibida de {device_id}")
        
        return {
            'status': 'success',
            'message': 'Telemetría recibida',
            'device_id': device_id,
            'timestamp': datetime.now().isoformat()
        }
        
    except Exception as e:
        print(f"❌ Error procesando telemetría: {e}")
        return {
            'status': 'error',
            'message': str(e)
        }


@app.get("/api/esp32/status/{device_id}")
async def obtener_estado_esp32(device_id: str):
    """
    Obtener último estado conocido de un dispositivo ESP32
    """
    # En una implementación real, esto vendría de una base de datos
    # Por ahora devolvemos el estado actual del controlador
    
    return {
        'status': 'success',
        'device_id': device_id,
        'online': True,
        'last_seen': datetime.now().isoformat(),
        'data': inverter_controller.current_state
    }


@app.post("/api/esp32/command/{device_id}")
async def enviar_comando_esp32(device_id: str, command: dict):
    """
    Enviar comando a un dispositivo ESP32
    
    Comandos disponibles:
    - {"command": "calibrate_ldr"}
    - {"command": "reset_wind"}
    - {"command": "reboot"}
    - {"command": "clear_logs"}
    """
    # Guardar comando en cola (en producción sería Redis/DB)
    if not hasattr(enviar_comando_esp32, 'command_queue'):
        enviar_comando_esp32.command_queue = {}
    
    if device_id not in enviar_comando_esp32.command_queue:
        enviar_comando_esp32.command_queue[device_id] = []
    
    enviar_comando_esp32.command_queue[device_id].append({
        'command': command.get('command'),
        'params': command.get('params', {}),
        'timestamp': datetime.now().isoformat()
    })
    
    print(f"📤 Comando encolado para {device_id}: {command}")
    
    return {
        'status': 'success',
        'device_id': device_id,
        'command': command.get('command'),
        'timestamp': datetime.now().isoformat()
    }


@app.get("/api/esp32/commands/{device_id}")
async def obtener_comandos_esp32(device_id: str):
    """
    ESP32 pregunta si hay comandos pendientes (HTTP Polling)
    
    El ESP32 hace GET cada X segundos para ver si hay comandos nuevos.
    Esto funciona sin abrir puertos en el router del ESP32.
    """
    # Obtener comandos de la cola
    if hasattr(enviar_comando_esp32, 'command_queue'):
        commands = enviar_comando_esp32.command_queue.get(device_id, [])
        
        # Limpiar cola después de entregar
        if device_id in enviar_comando_esp32.command_queue:
            enviar_comando_esp32.command_queue[device_id] = []
        
        if commands:
            print(f"📩 Entregando {len(commands)} comando(s) a {device_id}")
        
        return {
            'status': 'success',
            'device_id': device_id,
            'commands': commands,
            'count': len(commands)
        }
    else:
        return {
            'status': 'success',
            'device_id': device_id,
            'commands': [],
            'count': 0
        }


if __name__ == "__main__":
    import uvicorn
    import sys
    
    # Permitir puerto personalizado desde línea de comandos
    port = settings.port
    if "--port" in sys.argv:
        try:
            port_idx = sys.argv.index("--port")
            port = int(sys.argv[port_idx + 1])
            print(f"🔧 Usando puerto personalizado: {port}")
        except (IndexError, ValueError):
            print("⚠️ Puerto inválido, usando puerto por defecto")
    
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=port,
        reload=True
    )
