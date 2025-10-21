from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from config import get_settings

settings = get_settings()

# Crear engine
if settings.database_url.startswith("sqlite"):
    engine = create_engine(
        settings.database_url,
        connect_args={"check_same_thread": False}
    )
else:
    engine = create_engine(settings.database_url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Modelos de Base de Datos

class EnergyRecord(Base):
    """Registro de energía en tiempo real"""
    __tablename__ = "energy_records"
    
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Generación
    solar_power_w = Column(Float, default=0.0)
    wind_power_w = Column(Float, default=0.0)
    total_generation_w = Column(Float, default=0.0)
    
    # Batería
    battery_voltage_v = Column(Float, default=0.0)
    battery_current_a = Column(Float, default=0.0)
    battery_soc_percent = Column(Float, default=0.0)
    battery_power_w = Column(Float, default=0.0)
    
    # Consumo
    load_power_w = Column(Float, default=0.0)
    
    # Estado
    active_source = Column(String(50), default="battery")
    grid_connected = Column(Boolean, default=False)


class WeatherData(Base):
    """Datos meteorológicos"""
    __tablename__ = "weather_data"
    
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    
    temperature_c = Column(Float)
    humidity_percent = Column(Float)
    pressure_hpa = Column(Float)
    wind_speed_ms = Column(Float)
    wind_direction_deg = Column(Float)
    cloud_cover_percent = Column(Float)
    rain_1h_mm = Column(Float, default=0.0)
    solar_radiation_wm2 = Column(Float, default=0.0)
    description = Column(String(200))


class Prediction(Base):
    """Predicciones de energía"""
    __tablename__ = "predictions"
    
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    prediction_time = Column(DateTime, index=True)
    
    predicted_solar_w = Column(Float)
    predicted_wind_w = Column(Float)
    predicted_consumption_w = Column(Float)
    predicted_battery_soc = Column(Float)
    
    confidence_score = Column(Float, default=0.0)


class AIDecision(Base):
    """Decisiones de la IA"""
    __tablename__ = "ai_decisions"
    
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    
    decision_type = Column(String(100))
    selected_source = Column(String(50))
    reason = Column(Text)
    
    battery_soc_at_decision = Column(Float)
    predicted_autonomy_hours = Column(Float)
    energy_deficit_predicted = Column(Boolean, default=False)


class Alert(Base):
    """Alertas del sistema"""
    __tablename__ = "alerts"
    
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    
    alert_type = Column(String(100))
    severity = Column(String(20))  # info, warning, critical
    message = Column(Text)
    resolved = Column(Boolean, default=False)
    resolved_at = Column(DateTime, nullable=True)


class SystemParameter(Base):
    """Parámetros configurables del sistema"""
    __tablename__ = "system_parameters"
    
    id = Column(Integer, primary_key=True, index=True)
    parameter_name = Column(String(100), unique=True, index=True)
    parameter_value = Column(String(500))
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


# Crear tablas
def init_db():
    """Inicializar base de datos"""
    Base.metadata.create_all(bind=engine)
    print("✅ Base de datos inicializada")


# Dependency para obtener sesión
def get_db():
    """Obtener sesión de base de datos"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
