from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List


class EnergyStatus(BaseModel):
    """Estado actual de energía"""
    timestamp: datetime
    
    # Generación
    solar_power_w: float = 0.0
    wind_power_w: float = 0.0
    total_generation_w: float = 0.0
    
    # Batería
    battery_voltage_v: float = 0.0
    battery_current_a: float = 0.0
    battery_soc_percent: float = 0.0
    battery_power_w: float = 0.0
    
    # Consumo
    load_power_w: float = 0.0
    
    # Estado
    active_source: str = "battery"
    grid_connected: bool = False
    auto_mode_enabled: bool = True
    
    class Config:
        from_attributes = True


class WeatherInfo(BaseModel):
    """Información meteorológica"""
    timestamp: datetime
    temperature_c: float
    humidity_percent: float
    pressure_hpa: float
    wind_speed_ms: float
    wind_direction_deg: float
    cloud_cover_percent: float
    rain_1h_mm: float = 0.0
    solar_radiation_wm2: float = 0.0
    description: str


class PredictionData(BaseModel):
    """Datos de predicción"""
    prediction_time: datetime
    predicted_solar_w: float
    predicted_wind_w: float
    predicted_consumption_w: float
    predicted_battery_soc: float
    confidence_score: float = 0.0


class Prediction24h(BaseModel):
    """Predicción para 24 horas"""
    generated_at: datetime
    predictions: List[PredictionData]
    total_solar_24h_wh: float
    total_wind_24h_wh: float
    total_consumption_24h_wh: float
    autonomy_hours: float
    energy_deficit_hours: List[int] = []


class ControlCommand(BaseModel):
    """Comando de control manual"""
    source: str = Field(..., description="solar, wind, battery, grid, generator")
    action: str = Field(..., description="enable, disable, priority")
    value: Optional[float] = None


class AutoModeConfig(BaseModel):
    """Configuración modo automático"""
    enabled: bool
    min_battery_soc: Optional[float] = None
    max_battery_soc: Optional[float] = None
    priority_list: Optional[List[str]] = None


class ESP32SensorData(BaseModel):
    """Datos desde ESP32"""
    solar_voltage_v: float
    solar_current_a: float
    wind_voltage_v: float
    wind_current_a: float
    battery_voltage_v: float
    battery_current_a: float
    load_current_a: float
    temperature_c: float = 0.0


class SystemAlert(BaseModel):
    """Alerta del sistema"""
    alert_type: str
    severity: str
    message: str
    timestamp: datetime
    resolved: bool = False


class DashboardData(BaseModel):
    """Datos completos para dashboard"""
    energy_status: EnergyStatus
    weather: Optional[WeatherInfo] = None
    latest_prediction: Optional[PredictionData] = None
    autonomy_hours: float
    alerts: List[SystemAlert] = []
    auto_mode: bool = True
