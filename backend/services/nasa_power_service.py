"""
Servicio para obtener datos históricos de clima usando NASA POWER API

API NASA POWER: https://power.larc.nasa.gov/docs/services/api/
Datos disponibles:
- Irradiancia solar (40 años históricos)
- Velocidad del viento
- Temperatura
- Humedad
- Presión

GRATIS y sin límite de requests
"""

import httpx
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import asyncio

class NASAPowerService:
    """
    Cliente para NASA POWER API
    """
    
    BASE_URL = "https://power.larc.nasa.gov/api/temporal"
    
    # Parámetros disponibles
    SOLAR_PARAMS = [
        "ALLSKY_SFC_SW_DWN",  # Irradiancia solar (kWh/m²/day)
        "CLRSKY_SFC_SW_DWN",  # Irradiancia cielo despejado
        "T2M",                 # Temperatura 2m (°C)
        "T2M_MAX",             # Temp máxima
        "T2M_MIN",             # Temp mínima
    ]
    
    WIND_PARAMS = [
        "WS50M",               # Velocidad viento 50m (m/s)
        "WS10M",               # Velocidad viento 10m (m/s)
        "WD50M",               # Dirección viento 50m (°)
    ]
    
    def __init__(self):
        self.client = httpx.AsyncClient(timeout=30.0)
    
    async def close(self):
        """Cerrar cliente HTTP"""
        await self.client.aclose()
    
    async def get_monthly_data(
        self,
        latitude: float,
        longitude: float,
        start_year: int,
        end_year: int,
        parameters: Optional[List[str]] = None
    ) -> Dict:
        """
        Obtener datos mensuales históricos
        
        Args:
            latitude: Latitud (-90 a 90)
            longitude: Longitud (-180 a 180)
            start_year: Año inicio (1981 - presente)
            end_year: Año fin
            parameters: Lista de parámetros a obtener
        
        Returns:
            Dict con datos mensuales
        """
        if parameters is None:
            parameters = self.SOLAR_PARAMS + self.WIND_PARAMS
        
        params_str = ",".join(parameters)
        
        url = f"{self.BASE_URL}/monthly/point"
        
        params = {
            "parameters": params_str,
            "community": "RE",  # Renewable Energy
            "longitude": longitude,
            "latitude": latitude,
            "start": start_year,
            "end": end_year,
            "format": "JSON"
        }
        
        response = await self.client.get(url, params=params)
        response.raise_for_status()
        
        return response.json()
    
    async def get_daily_data(
        self,
        latitude: float,
        longitude: float,
        start_date: str,  # YYYYMMDD
        end_date: str,     # YYYYMMDD
        parameters: Optional[List[str]] = None
    ) -> Dict:
        """
        Obtener datos diarios históricos
        
        Args:
            latitude: Latitud
            longitude: Longitud
            start_date: Fecha inicio YYYYMMDD
            end_date: Fecha fin YYYYMMDD
            parameters: Parámetros a obtener
        
        Returns:
            Dict con datos diarios
        """
        if parameters is None:
            parameters = self.SOLAR_PARAMS + self.WIND_PARAMS
        
        params_str = ",".join(parameters)
        
        url = f"{self.BASE_URL}/daily/point"
        
        params = {
            "parameters": params_str,
            "community": "RE",
            "longitude": longitude,
            "latitude": latitude,
            "start": start_date,
            "end": end_date,
            "format": "JSON"
        }
        
        response = await self.client.get(url, params=params)
        response.raise_for_status()
        
        return response.json()
    
    async def get_historical_average(
        self,
        latitude: float,
        longitude: float,
        years_back: int = 10
    ) -> Dict:
        """
        Calcular promedios históricos de los últimos N años
        
        Args:
            latitude: Latitud
            longitude: Longitud
            years_back: Años hacia atrás para calcular promedio
        
        Returns:
            Dict con promedios:
            {
                "solar_irradiance_avg": float,  # kWh/m²/día
                "wind_speed_avg": float,         # m/s
                "temperature_avg": float,        # °C
                "solar_irradiance_monthly": [...],  # Por mes
                "wind_speed_monthly": [...]      # Por mes
            }
        """
        end_year = datetime.now().year - 1  # Último año completo
        start_year = end_year - years_back + 1
        
        data = await self.get_monthly_data(
            latitude, longitude,
            start_year, end_year
        )
        
        # Extraer parámetros
        params = data["properties"]["parameter"]
        
        # Calcular promedios
        solar_values = []
        wind_values = []
        temp_values = []
        
        # Promedios por mes (12 meses)
        solar_monthly = [[] for _ in range(12)]
        wind_monthly = [[] for _ in range(12)]
        
        for key, value in params.get("ALLSKY_SFC_SW_DWN", {}).items():
            if isinstance(value, (int, float)):
                solar_values.append(value)
                month = int(key[-2:]) - 1  # Extraer mes
                solar_monthly[month].append(value)
        
        for key, value in params.get("WS50M", {}).items():
            if isinstance(value, (int, float)):
                wind_values.append(value)
                month = int(key[-2:]) - 1
                wind_monthly[month].append(value)
        
        for key, value in params.get("T2M", {}).items():
            if isinstance(value, (int, float)):
                temp_values.append(value)
        
        # Calcular promedios mensuales
        solar_monthly_avg = [
            sum(month) / len(month) if month else 0
            for month in solar_monthly
        ]
        
        wind_monthly_avg = [
            sum(month) / len(month) if month else 0
            for month in wind_monthly
        ]
        
        return {
            "solar_irradiance_avg": sum(solar_values) / len(solar_values) if solar_values else 0,
            "wind_speed_avg": sum(wind_values) / len(wind_values) if wind_values else 0,
            "temperature_avg": sum(temp_values) / len(temp_values) if temp_values else 0,
            "solar_irradiance_monthly": solar_monthly_avg,
            "wind_speed_monthly": wind_monthly_avg,
            "years_analyzed": years_back,
            "period": f"{start_year}-{end_year}"
        }


# Singleton instance
nasa_service = NASAPowerService()


async def get_location_climate_data(latitude: float, longitude: float) -> Dict:
    """
    Obtener datos climáticos históricos para una ubicación
    
    Args:
        latitude: Latitud
        longitude: Longitud
    
    Returns:
        Dict con datos de clima históricos y promedios
    """
    avg_data = await nasa_service.get_historical_average(latitude, longitude, years_back=10)
    
    return {
        "location": {
            "latitude": latitude,
            "longitude": longitude
        },
        "historical_data": avg_data,
        "solar": {
            "annual_avg_kwh_m2_day": avg_data["solar_irradiance_avg"],
            "monthly_avg": avg_data["solar_irradiance_monthly"],
            "best_month": max(enumerate(avg_data["solar_irradiance_monthly"]), key=lambda x: x[1])[0] + 1,
            "worst_month": min(enumerate(avg_data["solar_irradiance_monthly"]), key=lambda x: x[1])[0] + 1
        },
        "wind": {
            "annual_avg_ms": avg_data["wind_speed_avg"],
            "monthly_avg": avg_data["wind_speed_monthly"],
            "best_month": max(enumerate(avg_data["wind_speed_monthly"]), key=lambda x: x[1])[0] + 1,
            "worst_month": min(enumerate(avg_data["wind_speed_monthly"]), key=lambda x: x[1])[0] + 1
        },
        "temperature": {
            "annual_avg_c": avg_data["temperature_avg"]
        },
        "data_source": "NASA POWER API",
        "period": avg_data["period"]
    }
