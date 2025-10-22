from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from functools import lru_cache
import json
import os


class Settings(BaseSettings):
    """Configuración del sistema"""
    
    # API Keys
    openweather_api_key: str
    
    # Database
    database_url: str = "sqlite:///./inversor.db"
    
    # Location
    latitude: float = -38.7183
    longitude: float = -62.2663
    
    # System Configuration
    battery_capacity_wh: float = 5000.0
    max_solar_power_w: float = 3000.0
    max_wind_power_w: float = 2000.0
    min_battery_soc: float = 20.0
    max_battery_soc: float = 100.0
    
    # House Consumption
    average_house_consumption_w: float = 650.0
    
    # Machine Learning
    enable_pattern_learning: bool = True
    pattern_learning_days: int = 30
    
    # Server
    host: str = "0.0.0.0"
    port: int = 11113
    
    # Simulation
    simulation_mode: bool = False
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"  # Ignorar campos extra del .env
    )


def load_user_configuration():
    """Carga la configuración del usuario desde configuracion_usuario.json"""
    config_file = "configuracion_usuario.json"
    if os.path.exists(config_file):
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"⚠️  Error cargando configuración de usuario: {e}")
            return None
    return None


@lru_cache()
def get_settings():
    return Settings()


@lru_cache()
def get_user_config():
    """Obtiene la configuración personalizada del usuario"""
    return load_user_configuration()
