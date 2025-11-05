from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta
import asyncio
import json
from pathlib import Path

from database import get_db, init_db, EnergyRecord, WeatherData, Prediction, AIDecision, Alert
from schemas import (
    EnergyStatus, WeatherInfo, PredictionData, Prediction24h,
    ControlCommand, AutoModeConfig, ESP32SensorData, DashboardData
)
from config import get_settings, get_user_config
from inverter_controller import inverter_controller
from weather_service import weather_service
from ai_predictor import energy_predictor
from recommendation_service import recommendation_service
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

# CORS - Permitir todos los orígenes para pruebas remotas
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# Servir archivos estáticos del frontend (si existen)
try:
    app.mount("/static", StaticFiles(directory="static"), name="static")
except:
    pass  # Si no existe el directorio, no pasa nada

# WebSocket connections manager (para frontend)
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

# ===== WEBSOCKET MANAGER PARA ESP32 CON COLA PERSISTENTE Y ACK =====
class ESP32WebSocketManager:
    def __init__(self):
        # {device_id: websocket}
        self.connections: dict = {}
        
        # Cola persistente de comandos con estado ACK
        # {device_id: [{"id": uuid, "command": str, "parameter": str, "status": "pending/sent/acked", "timestamp": str, "sent_at": str, "acked_at": str}]}
        self.command_queue: dict = {}
        
        # Último comando ACK recibido por device
        # {device_id: {"command_id": uuid, "timestamp": str}}
        self.last_ack: dict = {}
        
    async def connect(self, device_id: str, websocket: WebSocket):
        """Conectar un ESP32"""
        await websocket.accept()
        self.connections[device_id] = websocket
        print(f"🔌 ESP32 WebSocket conectado: {device_id}")
        
        # Enviar comandos pendientes inmediatamente
        await self.send_pending_commands(device_id)
    
    def disconnect(self, device_id: str):
        """Desconectar un ESP32"""
        if device_id in self.connections:
            del self.connections[device_id]
            print(f"🔌 ESP32 WebSocket desconectado: {device_id}")
    
    def enqueue_command(self, device_id: str, command: str, parameter: str = None) -> str:
        """Encolar comando con ID único"""
        import uuid
        
        if device_id not in self.command_queue:
            self.command_queue[device_id] = []
        
        command_id = str(uuid.uuid4())
        cmd_entry = {
            "id": command_id,
            "command": command,
            "parameter": parameter,
            "status": "pending",
            "timestamp": datetime.now().isoformat(),
            "sent_at": None,
            "acked_at": None
        }
        
        self.command_queue[device_id].append(cmd_entry)
        print(f"📤 Comando encolado [{command_id[:8]}]: {command}({parameter})")
        
        return command_id
    
    async def send_pending_commands(self, device_id: str):
        """Enviar comandos pendientes por WebSocket"""
        if device_id not in self.connections:
            return
        
        if device_id not in self.command_queue:
            return
        
        websocket = self.connections[device_id]
        pending_commands = [cmd for cmd in self.command_queue[device_id] if cmd["status"] == "pending"]
        
        for cmd in pending_commands:
            try:
                # Enviar comando con ID para tracking
                message = {
                    "type": "command",
                    "id": cmd["id"],
                    "command": cmd["command"],
                    "parameter": cmd["parameter"],
                    "timestamp": cmd["timestamp"]
                }
                
                await websocket.send_json(message)
                
                # Marcar como enviado
                cmd["status"] = "sent"
                cmd["sent_at"] = datetime.now().isoformat()
                
                print(f"✅ Comando enviado [{cmd['id'][:8]}]: {cmd['command']}({cmd['parameter']})")
                
            except Exception as e:
                print(f"❌ Error enviando comando [{cmd['id'][:8]}]: {e}")
    
    def mark_ack(self, device_id: str, command_id: str):
        """Marcar comando como confirmado (ACK)"""
        if device_id not in self.command_queue:
            return False
        
        for cmd in self.command_queue[device_id]:
            if cmd["id"] == command_id:
                cmd["status"] = "acked"
                cmd["acked_at"] = datetime.now().isoformat()
                
                self.last_ack[device_id] = {
                    "command_id": command_id,
                    "timestamp": datetime.now().isoformat()
                }
                
                print(f"✅ ACK recibido [{command_id[:8]}]: {cmd['command']}({cmd['parameter']})")
                return True
        
        return False
    
    def get_command_status(self, device_id: str, command_id: str) -> dict:
        """Obtener estado de un comando"""
        if device_id not in self.command_queue:
            return None
        
        for cmd in self.command_queue[device_id]:
            if cmd["id"] == command_id:
                return cmd
        
        return None
    
    def cleanup_old_commands(self, device_id: str, max_age_minutes: int = 5):
        """Limpiar comandos viejos ya confirmados"""
        if device_id not in self.command_queue:
            return
        
        from datetime import timedelta
        cutoff = datetime.now() - timedelta(minutes=max_age_minutes)
        
        # Mantener solo comandos recientes o no confirmados
        self.command_queue[device_id] = [
            cmd for cmd in self.command_queue[device_id]
            if cmd["status"] != "acked" or datetime.fromisoformat(cmd["acked_at"]) > cutoff
        ]

esp32_ws_manager = ESP32WebSocketManager()


# ===== ENDPOINT BASICO DE PRUEBA =====
@app.get("/")
def root():
    return {"status": "online", "message": "Backend funcionando"}

@app.get("/health")
def health_check():
    return {"status": "ok"}


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
    # Cargar store desde disco al iniciar
    load_store_from_disk()
    print("")
    print("=" * 60)
    print("🚀 VERSIÓN NUEVA - BACKEND REINICIADO")
    print("=" * 60)
    print("✅ Sistema Inversor Inteligente iniciado")
    try:
        print(f"📍 Ubicación: {inverter_controller.ubicacion['latitud']}, {inverter_controller.ubicacion['longitud']}")
        print(f"🔋 Capacidad batería: {inverter_controller.configuracion.get('capacidad_bateria_wh', 0)} Wh")
    except:
        print("📍 Ubicación: No configurada")
        print("🔋 Capacidad batería: No configurada")
    print("=" * 60)
    print("")
    
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
    """WebSocket para actualizaciones en tiempo real (frontend)"""
    await manager.connect(websocket)
    try:
        while True:
            # Mantener conexión viva
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)


@app.websocket("/api/ws/esp32/{device_id}")
async def esp32_websocket_endpoint(websocket: WebSocket, device_id: str):
    """WebSocket dedicado para comunicación ESP32 ↔ Backend
    
    El ESP32 se conecta aquí y recibe comandos en tiempo real.
    También envía ACK cuando ejecuta comandos.
    """
    await esp32_ws_manager.connect(device_id, websocket)
    
    try:
        while True:
            # Recibir mensajes del ESP32 (ACK, heartbeat, etc)
            data = await websocket.receive_json()
            
            # Procesar ACK de comandos ejecutados
            if data.get("type") == "ack":
                command_id = data.get("command_id")
                if command_id:
                    esp32_ws_manager.mark_ack(device_id, command_id)
                    
                    # Broadcast a frontend si está conectado
                    await manager.broadcast({
                        "type": "esp32_command_ack",
                        "device_id": device_id,
                        "command_id": command_id,
                        "timestamp": datetime.now().isoformat()
                    })
            
            # Procesar heartbeat
            elif data.get("type") == "heartbeat":
                print(f"💓 Heartbeat ESP32: {device_id}")
            
            # Limpiar comandos viejos cada 10 mensajes
            if hasattr(esp32_websocket_endpoint, 'msg_count'):
                esp32_websocket_endpoint.msg_count += 1
            else:
                esp32_websocket_endpoint.msg_count = 1
            
            if esp32_websocket_endpoint.msg_count % 10 == 0:
                esp32_ws_manager.cleanup_old_commands(device_id)
                
    except WebSocketDisconnect:
        esp32_ws_manager.disconnect(device_id)
    except Exception as e:
        print(f"❌ Error en WebSocket ESP32 [{device_id}]: {e}")
        esp32_ws_manager.disconnect(device_id)


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
            'status': 'online'
        }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

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
async def obtener_configuracion():
    """
    Obtener configuración del usuario
    """
    # Intentar leer desde archivo si existe
    config_file = Path("user_config.json")
    if config_file.exists():
        import json
        with open(config_file, 'r') as f:
            return json.load(f)
    
    # Si no existe, devolver configuración por defecto
    config = get_user_config()
    return config


@app.post("/api/configuracion/usuario")
async def guardar_configuracion(config: dict):
    """
    Guardar configuración del usuario
    """
    try:
        import json
        from pathlib import Path
        
        # Guardar en archivo JSON
        config_file = Path("user_config.json")
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)
        
        print(f"✅ Configuración guardada:")
        print(f"   📍 Ubicación: ({config.get('latitude')}, {config.get('longitude')})")
        print(f"   ⚙️ Modo: {config.get('mode')}")
        
        return {
            'status': 'success',
            'message': 'Configuración guardada correctamente'
        }
    except Exception as e:
        print(f"❌ Error guardando configuración: {e}")
        return {
            'status': 'error',
            'message': str(e)
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

# ===== ESTADO GLOBAL (compartido entre POST y GET) =====
# Evita inconsistencias con atributos en funciones cuando el reloader crea procesos/hilos.
DEVICES_STORE = {}
LAST_SEQ = {}
UPLINK_LOST = {}

# Persistencia simple en disco para evitar pérdida de estado entre procesos/reloads
from pathlib import Path
import json as _json
STORE_PATH = Path(__file__).parent / "devices_store.json"

def load_store_from_disk():
    global DEVICES_STORE
    try:
        if STORE_PATH.exists():
            with STORE_PATH.open('r', encoding='utf-8') as f:
                data = _json.load(f)
                if isinstance(data, dict):
                    DEVICES_STORE = data
                    print(f"🗂️  [STORE] Cargado desde disco: {len(DEVICES_STORE)} dispositivos")
    except Exception as e:
        print(f"⚠️  [STORE] Error cargando store: {e}")

def save_store_to_disk():
    try:
        with STORE_PATH.open('w', encoding='utf-8') as f:
            _json.dump(DEVICES_STORE, f, ensure_ascii=False)
        # print("🗂️  [STORE] Guardado en disco")
    except Exception as e:
        print(f"⚠️  [STORE] Error guardando store: {e}")

# ===== CONTADOR GLOBAL PARA DEBUG =====
contador_paquetes_esp32 = 0

@app.post("/api/esp32/telemetry")
async def recibir_telemetria_esp32(telemetria: dict):
    """
    Recibir telemetría del ESP32
    Incluye ACK de comandos ejecutados
        "v_load_v": 1.890
    }
    
    Legacy format also supported for compatibility.
    """
    try:
        print(f"🔵 [DEBUG] Recibiendo telemetría...")
        data = telemetria  # Fix: rename parameter
        device_id = data.get('device_id', 'UNKNOWN')
        print(f"🔵 [DEBUG] Device ID: {device_id}, tiene seq: {'seq' in data}, tiene raw_adc: {'raw_adc' in data}")
        
        # ===== STAGE 1: Packet loss tracking =====
        if 'seq' in data:
            seq = data.get('seq', 0)
            
            # Track packet loss usando estado global
            if device_id in LAST_SEQ:
                expected_seq = LAST_SEQ[device_id] + 1
                if seq > expected_seq:
                    lost = seq - expected_seq
                    UPLINK_LOST[device_id] = UPLINK_LOST.get(device_id, 0) + lost
                elif seq < expected_seq:
                    # Duplicate/out of order - don't count as lost
                    pass
            else:
                UPLINK_LOST[device_id] = 0
            
            LAST_SEQ[device_id] = seq
            
            # Console log Stage 1 format
            v_bat = data.get('v_bat_v', 0.0)
            v_wind = data.get('v_wind_v_dc', 0.0)
            v_solar = data.get('v_solar_v', 0.0)
            v_load = data.get('v_load_v', 0.0)
            ts = data.get('ts', 0)
            turbine_rpm = data.get('turbine_rpm', 0.0)
            lost_total = UPLINK_LOST.get(device_id, 0)
            
            print(f"[TELEM] {device_id} seq={seq} ts={ts} Vbat={v_bat:.3f}V Vwind_DC={v_wind:.3f}V Vsolar={v_solar:.3f}V Vload={v_load:.3f}V RPM={turbine_rpm:.1f} Lost={lost_total} | OK")

            # Si el firmware envía telemetría extendida con raw_adc (cada ~5s),
            # mostrar los voltajes por GPIO (0–3.3V) - SOLO 4 ADC REALES
            raw_adc = data.get('raw_adc')
            if isinstance(raw_adc, dict):
                # Mapeo correcto según firmware (CORREGIDO):
                # GPIO34: Batería (adc1_bat1)
                # GPIO35: Eólica DC (adc2_eolica) ← NOMBRE CORRECTO
                # GPIO36: Solar (adc5_solar) ← NOMBRE CORRECTO
                # GPIO39: Carga (adc6_load)
                gpio34_bat = raw_adc.get('adc1_bat1', None)
                gpio35_eolica = raw_adc.get('adc2_eolica', None)
                gpio36_solar = raw_adc.get('adc5_solar', None)
                gpio39_carga = raw_adc.get('adc6_load', None)
                
                # Imprimir solo si al menos uno está presente
                if any(v is not None for v in [gpio34_bat, gpio35_eolica, gpio36_solar, gpio39_carga]):
                    def f(val):
                        try:
                            return f"{float(val):.3f}V"
                        except Exception:
                            return "--"
                    print("📊 ADC RAW (0-3.3V):")
                    print("  GPIO34 → Batería:", f(gpio34_bat))
                    print("  GPIO35 → Eólica DC:", f(gpio35_eolica))
                    print("  GPIO36 → Solar:", f(gpio36_solar))
                    print("  GPIO39 → Carga:", f(gpio39_carga))
        
        device_id = data.get('device_id', 'UNKNOWN')
        
        # Incrementar contador global
        global contador_paquetes_esp32
        contador_paquetes_esp32 += 1
        contador = contador_paquetes_esp32
        
        # Registrar dispositivo en almacén global
        # (no dependemos de atributos en la función para evitar estados separados)
        
        # Mantener registered_at si ya existe
        registered_at = DEVICES_STORE.get(device_id, {}).get('registered_at', datetime.now().isoformat())
        
        # Extraer raw_adc del ESP32
        raw_adc_from_esp = data.get('raw_adc', {})
        
        # Si no viene raw_adc en este paquete, mantener el anterior
        old_device_data = DEVICES_STORE.get(device_id, {})
        old_raw_adc = old_device_data.get('raw_adc', {})
        old_relays = old_device_data.get('relays', {})
        
        # Usar el nuevo si existe, sino mantener el viejo
        final_raw_adc = raw_adc_from_esp if raw_adc_from_esp else old_raw_adc
        
        # Relays: siempre usar los nuevos si vienen
        relays_from_esp = data.get('relays', {})
        final_relays = {
            'solar': relays_from_esp.get('solar', old_relays.get('solar', False)),
            'wind': relays_from_esp.get('eolica', old_relays.get('wind', False)),
            'grid': relays_from_esp.get('red', old_relays.get('grid', False)),
            'load': relays_from_esp.get('carga', old_relays.get('load', False))
        }
        
        DEVICES_STORE[device_id] = {
            'last_seen': datetime.now().isoformat(),
            'registered_at': registered_at,
            'contador': contador,  # ← CONTADOR PARA DEBUG
            'heartbeat': {
                'device_id': device_id,
                'uptime': data.get('uptime', 0),
                'free_heap': data.get('free_heap', 0),
                'rssi': data.get('rssi', 0),
                'timestamp': datetime.now().isoformat()
            },
            'telemetry': {
                'battery_voltage': data.get('voltaje_promedio', 0),
                'battery_soc': data.get('soc', 0),
                'solar_power': data.get('potencia_solar', 0),
                'wind_power': data.get('potencia_eolica', 0),
                'load_power': data.get('potencia_consumo', 0),
                'temperature': data.get('temperatura', 0),
                'v_bat_v': data.get('v_bat_v', 0),
                'v_wind_v_dc': data.get('v_wind_v_dc', 0),
                'v_solar_v': data.get('v_solar_v', 0),
                'v_load_v': data.get('v_load_v', 0),
                'rpm': data.get('rpm', 0),
                'frequency_hz': data.get('frequency_hz', 0),
                'turbine_rpm': float(data.get('turbine_rpm', 0.0)) if data.get('turbine_rpm', 0.0) >= 0 else 0.0
            },
            'relays': final_relays,
            'raw_adc': {
                # 4 ADC reales del hardware (NOMBRES CORREGIDOS):
                # GPIO34: Batería (adc1_bat1)
                # GPIO35: Eólica DC (adc2_eolica) ← CORREGIDO
                # GPIO36: Solar (adc5_solar) ← CORREGIDO
                # GPIO39: Carga (adc6_load)
                'adc1_bat1': final_raw_adc.get('adc1_bat1', 0),        # GPIO34 - Batería
                'adc1_bat1_raw': final_raw_adc.get('adc1_bat1_raw', 0),
                'adc2_eolica': final_raw_adc.get('adc2_eolica', 0),    # GPIO35 - Eólica DC
                'adc2_eolica_raw': final_raw_adc.get('adc2_eolica_raw', 0),
                'adc5_solar': final_raw_adc.get('adc5_solar', 0),      # GPIO36 - Solar
                'adc5_solar_raw': final_raw_adc.get('adc5_solar_raw', 0),
                'adc6_load': final_raw_adc.get('adc6_load', 0),        # GPIO39 - Carga
                'adc6_load_raw': final_raw_adc.get('adc6_load_raw', 0)
            }
        }
        
        # Debug: imprimir lo que se guardó
        if raw_adc_from_esp:
            print(f"💾 [GUARDAR NUEVO #{contador}] raw_adc para {device_id}:", DEVICES_STORE[device_id]['raw_adc'])
        else:
            print(f"♻️ [MANTENER #{contador}] raw_adc para {device_id} (paquete sin ADC)")
        
        print(f"✅ [{contador}] {device_id} actualizado - Voltaje: {data.get('voltaje_promedio', 0)}V")
        # Guardar en disco para compartir estado entre procesos
        save_store_to_disk()
        
        return {
            'status': 'success',
            'message': 'Telemetría recibida',
            'device_id': device_id,
            'timestamp': datetime.now().isoformat(),
            'turbine_rpm': float(data.get('turbine_rpm', 0.0)) if data.get('turbine_rpm', 0.0) >= 0 else 0.0
        }
        
    except Exception as e:
        print(f"❌ Error procesando telemetría: {e}")
        return {
            'status': 'error',
            'message': str(e)
        }


@app.get("/api/esp32/diagnostico")
async def diagnostico_esp32():
    """
    Diagnóstico del sistema ESP32
    """
    global contador_paquetes_esp32
    
    diagnostico = {
        'backend_funcionando': True,
        'timestamp': datetime.now().isoformat(),
        'contador_total_paquetes': contador_paquetes_esp32,
        'dispositivos_registrados': len(DEVICES_STORE),
        'device_ids': list(DEVICES_STORE.keys()),
        'ultimo_paquete': None
    }
    
    if DEVICES_STORE:
        # Encontrar el dispositivo más reciente
        for device_id, info in DEVICES_STORE.items():
            last_seen = datetime.fromisoformat(info['last_seen'])
            seconds_ago = (datetime.now() - last_seen).total_seconds()
            diagnostico['ultimo_paquete'] = {
                'device_id': device_id,
                'hace_segundos': round(seconds_ago, 1),
                'contador': info.get('contador', 0),
                'tiene_raw_adc': bool(info.get('raw_adc', {}))
            }
            break
    
    return diagnostico

# Endpoint /api/esp32/devices movido a esp32_router.py para evitar duplicación
# El router se encarga de leer DEVICES_STORE y devolver la lista correcta

# Endpoint de depuración para ver el store crudo
@app.get("/api/esp32/devices/raw_store")
async def ver_store_crudo():
    print(f"🟠 [GET /devices/raw_store] keys={list(DEVICES_STORE.keys())}")
    return DEVICES_STORE


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


@app.get("/api/esp32/estado/{device_id}")
async def obtener_estado_dispositivo(device_id: str):
    """
    Obtener estado actual del dispositivo ESP32 (GPIO + relés)
    Frontend lo consulta para actualizar UI
    """
    if not hasattr(recibir_telemetria_esp32, 'devices'):
        return {"status": "error", "message": "Dispositivo no encontrado"}
    
    device = recibir_telemetria_esp32.devices.get(device_id)
    if not device:
        return {"status": "error", "message": "Dispositivo no encontrado"}
    
    return {
        "status": "success",
        "device_id": device_id,
        "last_seen": device.get('last_seen'),
        "telemetry": device.get('telemetry', {}),
        "relays": device.get('relays', {}),
        "raw_adc": device.get('raw_adc', {})
    }


@app.post("/api/esp32/command/{device_id}")
async def enviar_comando_esp32(device_id: str, command: dict):
    """
    Enviar comando a un dispositivo ESP32 (con ACK tracking)
    
    Comandos disponibles:
    - {"command": "eolica", "parameter": "on/off"}
    - {"command": "solar", "parameter": "on/off"}
    - {"command": "red", "parameter": "on/off"}
    - {"command": "carga", "parameter": "on/off"}
    - {"command": "freno", "parameter": "on/off"}
    - {"command": "reboot"}
    """
    cmd = command.get('command')
    param = command.get('parameter') or command.get('params')
    
    # Encolar en el nuevo sistema con ACK
    command_id = esp32_ws_manager.enqueue_command(device_id, cmd, param)
    
    # Si el ESP32 está conectado por WebSocket, enviar inmediatamente
    if device_id in esp32_ws_manager.connections:
        await esp32_ws_manager.send_pending_commands(device_id)
    else:
        # Si no está conectado, queda en cola para HTTP polling (fallback)
        # Mantener compatibilidad con HTTP polling
        if not hasattr(enviar_comando_esp32, 'command_queue'):
            enviar_comando_esp32.command_queue = {}
        
        if device_id not in enviar_comando_esp32.command_queue:
            enviar_comando_esp32.command_queue[device_id] = []
        
        cmd_entry = {
            'command': cmd,
            'timestamp': datetime.now().isoformat()
        }
        if param:
            cmd_entry['parameter'] = param
        
        enviar_comando_esp32.command_queue[device_id].append(cmd_entry)
        print(f"📤 Comando encolado para HTTP polling (ESP32 no conectado): {cmd}({param})")
    
    return {
        'status': 'success',
        'device_id': device_id,
        'command_id': command_id,
        'command': cmd,
        'parameter': param,
        'timestamp': datetime.now().isoformat(),
        'delivery_method': 'websocket' if device_id in esp32_ws_manager.connections else 'http_polling'
    }


@app.get("/api/esp32/commands/{device_id}")
async def obtener_comandos_esp32(device_id: str):
    """
    ESP32 pregunta si hay comandos pendientes (HTTP Polling - FALLBACK)
    
    STAGE 1: Retorna {"status":"OK"} si no hay comandos,
             {"status":"CMD", "commands":[...]} si hay comandos
    
    NOTA: Este endpoint es fallback. Si ESP32 usa WebSocket, los comandos
    se envían automáticamente por ahí.
    """
    # Obtener comandos de la cola
    if hasattr(enviar_comando_esp32, 'command_queue'):
        commands = enviar_comando_esp32.command_queue.get(device_id, [])
        
        # Limpiar cola después de entregar
        if device_id in enviar_comando_esp32.command_queue:
            enviar_comando_esp32.command_queue[device_id] = []
        
        if commands:
            # Log command sent (Stage 1)
            def fmt(c):
                cmd = c.get("command", "unknown")
                par = c.get("parameter")
                return f"{cmd}({par})" if par is not None else cmd
            cmd_str = ", ".join([fmt(c) for c in commands])
            print(f"[CMD] {device_id} → Sent: {cmd_str}")
            
            return {
                'status': 'CMD',
                'device_id': device_id,
                'commands': commands,
                'count': len(commands)
            }
    
    # No commands - return OK status (Stage 1)
    return {
        'status': 'OK',
        'device_id': device_id,
        'commands': [],
        'count': 0
    }


@app.get("/api/esp32/command/{device_id}/status/{command_id}")
async def verificar_estado_comando(device_id: str, command_id: str):
    """
    Verificar estado de un comando específico (para ACK tracking)
    
    Returns:
    - status: "pending" | "sent" | "acked" | "not_found"
    - timestamp: cuando fue encolado
    - sent_at: cuando fue enviado
    - acked_at: cuando fue confirmado
    """
    cmd_status = esp32_ws_manager.get_command_status(device_id, command_id)
    
    if not cmd_status:
        return {
            'status': 'not_found',
            'device_id': device_id,
            'command_id': command_id,
            'message': 'Comando no encontrado o ya expiró'
        }
    
    return {
        'status': cmd_status['status'],
        'device_id': device_id,
        'command_id': command_id,
        'command': cmd_status['command'],
        'parameter': cmd_status['parameter'],
        'timestamp': cmd_status['timestamp'],
        'sent_at': cmd_status['sent_at'],
        'acked_at': cmd_status['acked_at']
    }


# ===== ENDPOINTS DE PRUEBA DE HARDWARE =====

@app.get("/api/hardware/test")
async def obtener_datos_hardware_test():
    """
    Obtener datos de prueba de hardware (ADCs y relés)
    """
    try:
        # Simular datos de ADCs (en producción vendrían del ESP32)
        adcs = [
            {
                'pin': 'GPIO34',
                'channel': 'ADC1_CH6',
                'function': 'Voltaje Batería 1',
                'raw_value': 3250,
                'converted_value': '47.5V',
                'is_connected': True
            },
            {
                'pin': 'GPIO35',
                'channel': 'ADC1_CH7',
                'function': 'Voltaje Batería 2',
                'raw_value': 3280,
                'converted_value': '48.0V',
                'is_connected': True
            },
            {
                'pin': 'GPIO32',
                'channel': 'ADC1_CH4',
                'function': 'Voltaje Batería 3',
                'raw_value': 3265,
                'converted_value': '47.8V',
                'is_connected': True
            },
            {
                'pin': 'GPIO33',
                'channel': 'ADC1_CH5',
                'function': 'Corriente Solar',
                'raw_value': 2250,
                'converted_value': '14.8A',
                'is_connected': True
            },
            {
                'pin': 'GPIO36',
                'channel': 'ADC1_CH0',
                'function': 'Corriente Eólica',
                'raw_value': 2180,
                'converted_value': '9.5A',
                'is_connected': True
            },
            {
                'pin': 'GPIO39',
                'channel': 'ADC1_CH3',
                'function': 'Corriente Consumo',
                'raw_value': 2350,
                'converted_value': '22.1A',
                'is_connected': True
            },
            {
                'pin': 'GPIO25',
                'channel': 'ADC2_CH8',
                'function': 'Irradiancia (LDR)',
                'raw_value': 2900,
                'converted_value': '850 W/m²',
                'is_connected': True
            },
            {
                'pin': 'GPIO26',
                'channel': 'GPIO',
                'function': 'Velocidad Viento',
                'raw_value': 0,
                'converted_value': '6.5 m/s',
                'is_connected': True
            }
        ]
        
        # Estado de relés actual
        relays = {
            'solar': True,
            'wind': True,
            'grid': False,
            'load': True,
            'brake': False
        }
        
        # Cargar umbrales guardados
        import json
        from pathlib import Path
        thresholds_file = Path("protection_thresholds.json")
        if thresholds_file.exists():
            with open(thresholds_file, 'r') as f:
                thresholds = json.load(f)
        else:
            thresholds = {
                'max_wind_speed': 25.0,
                'max_wind_power': 2000,
                'max_voltage': 65.0,
                'brake_enabled': True
            }
        
        # Estado actual del generador (simular)
        current_wind_speed = 6.5
        current_wind_power = 450
        current_voltage = 48.2
        
        return {
            'status': 'success',
            'timestamp': datetime.now().isoformat(),
            'adcs': adcs,
            'relays': relays,
            'thresholds': thresholds,
            'current_wind_speed': current_wind_speed,
            'current_wind_power': current_wind_power,
            'current_voltage': current_voltage
        }
    except Exception as e:
        print(f"❌ Error en hardware test: {e}")
        return {'status': 'error', 'message': str(e)}


@app.post("/api/hardware/relay")
async def controlar_rele(request: dict):
    """
    Controlar estado de un relé
    """
    try:
        relay_name = request.get('relay')
        state = request.get('state')
        
        print(f"🔌 Control relé: {relay_name} → {'ON' if state else 'OFF'}")
        
        # TODO: Enviar comando al ESP32
        
        return {
            'status': 'success',
            'relay': relay_name,
            'state': state,
            'message': f"Relé {relay_name} {'activado' if state else 'desactivado'}"
        }
    except Exception as e:
        print(f"❌ Error controlando relé: {e}")
        return {'status': 'error', 'message': str(e)}


@app.post("/api/hardware/thresholds")
async def guardar_umbrales_proteccion(request: dict):
    """
    Guardar umbrales de protección contra embalamiento
    """
    try:
        import json
        from pathlib import Path
        
        thresholds = {
            'max_wind_speed': request.get('max_wind_speed', 25.0),
            'max_wind_power': request.get('max_wind_power', 2000),
            'max_voltage': request.get('max_voltage', 65.0),
            'brake_enabled': request.get('brake_enabled', True)
        }
        
        # Guardar en archivo
        config_file = Path("protection_thresholds.json")
        with open(config_file, 'w') as f:
            json.dump(thresholds, f, indent=2)
        
        print(f"✅ Umbrales de protección guardados:")
        print(f"   💨 Viento máx: {thresholds['max_wind_speed']} m/s")
        print(f"   ⚡ Potencia máx: {thresholds['max_wind_power']} W")
        print(f"   🔌 Voltaje máx: {thresholds['max_voltage']} V")
        print(f"   🛡️ Protección: {'ACTIVA' if thresholds['brake_enabled'] else 'INACTIVA'}")
        
        return {
            'status': 'success',
            'message': 'Umbrales guardados correctamente',
            'thresholds': thresholds
        }
    except Exception as e:
        print(f"❌ Error guardando umbrales: {e}")
        return {'status': 'error', 'message': str(e)}


# ===== ENDPOINT DE DATOS CLIMÁTICOS NASA =====

@app.get("/api/climate/historical")
async def obtener_datos_climaticos(latitude: float, longitude: float, years: int = 5):
    """
    Obtener datos climáticos históricos de NASA POWER
    """
    try:
        from nasa_power_service import nasa_power_service
        data = nasa_power_service.get_prediction_model_data(latitude, longitude)
        return data
    except Exception as e:
        print(f"❌ Error obteniendo datos climáticos: {e}")
        return {'status': 'error', 'message': str(e)}


# ===== ENDPOINTS DE RECOMENDACIONES =====

@app.post("/api/recommendation/by-demand")
async def recomendar_por_demanda(request: dict):
    """
    Recomendar equipamiento según demanda de potencia
    """
    try:
        result = recommendation_service.calculate_by_demand(
            target_power_w=request.get('target_power_w', 3000),
            latitude=request.get('latitude', -38.7183),
            longitude=request.get('longitude', -62.2663)
        )
        return result
    except Exception as e:
        print(f"❌ Error en recomendación por demanda: {e}")
        return {'status': 'error', 'message': str(e)}


@app.post("/api/recommendation/by-resources")
async def recomendar_por_recursos(request: dict):
    """
    Calcular potencial según recursos existentes
    """
    try:
        result = recommendation_service.calculate_by_resources(
            solar_panel_w=request.get('solar_panel_w', 0),
            solar_panel_area_m2=request.get('solar_panel_area_m2', 0),
            wind_turbine_w=request.get('wind_turbine_w', 0),
            wind_turbine_diameter_m=request.get('wind_turbine_diameter_m', 0),
            battery_capacity_wh=request.get('battery_capacity_wh', 0),
            latitude=request.get('latitude', -38.7183),
            longitude=request.get('longitude', -62.2663)
        )
        return result
    except Exception as e:
        print(f"❌ Error en recomendación por recursos: {e}")
        return {'status': 'error', 'message': str(e)}


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
