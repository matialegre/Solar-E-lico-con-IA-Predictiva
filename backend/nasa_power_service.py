"""
Servicio para obtener datos históricos de NASA POWER API
Datos reales de radiación solar y viento por ubicación
"""

import requests
from datetime import datetime, timedelta
from typing import Dict, List
import statistics


class NASAPowerService:
    """Servicio para obtener datos climáticos históricos de NASA POWER"""
    
    def __init__(self):
        self.base_url = "https://power.larc.nasa.gov/api/temporal/daily/point"
        
    def get_historical_data(
        self, 
        latitude: float, 
        longitude: float,
        years: int = 5
    ) -> Dict:
        """
        Obtener datos históricos de radiación solar y viento
        
        Args:
            latitude: Latitud del lugar
            longitude: Longitud del lugar
            years: Años de histórico (default 5)
            
        Returns:
            Dict con promedios mensuales de radiación solar y viento
        """
        # Fechas (últimos N años)
        end_date = datetime.now()
        start_date = end_date - timedelta(days=years * 365)
        
        # Parámetros NASA POWER
        params = {
            'parameters': 'ALLSKY_SFC_SW_DWN,WS10M',  # Radiación solar y viento a 10m
            'community': 'RE',  # Renewable Energy
            'longitude': longitude,
            'latitude': latitude,
            'start': start_date.strftime('%Y%m%d'),
            'end': end_date.strftime('%Y%m%d'),
            'format': 'JSON'
        }
        
        try:
            print(f"🌍 Obteniendo datos NASA POWER para ({latitude}, {longitude})")
            response = requests.get(self.base_url, params=params, timeout=30)
            
            if response.status_code != 200:
                print(f"⚠️ Error NASA POWER: {response.status_code}")
                return self._get_default_data()
            
            data = response.json()
            
            # Extraer datos
            solar_data = data['properties']['parameter']['ALLSKY_SFC_SW_DWN']
            wind_data = data['properties']['parameter']['WS10M']
            
            # Procesar datos por mes
            monthly_solar = self._process_monthly_averages(solar_data)
            monthly_wind = self._process_monthly_averages(wind_data)
            
            # Calcular promedios generales
            avg_solar = statistics.mean([v for v in solar_data.values() if v != -999])
            avg_wind = statistics.mean([v for v in wind_data.values() if v != -999])
            
            print(f"✅ Datos obtenidos: Solar={avg_solar:.1f} kWh/m²/día, Viento={avg_wind:.1f} m/s")
            
            return {
                'status': 'success',
                'source': 'NASA POWER',
                'location': {
                    'latitude': latitude,
                    'longitude': longitude
                },
                'period': {
                    'start': start_date.strftime('%Y-%m-%d'),
                    'end': end_date.strftime('%Y-%m-%d'),
                    'years': years
                },
                'averages': {
                    'solar_irradiance_kwh_m2_day': round(avg_solar, 2),
                    'solar_irradiance_w_m2': round(avg_solar * 1000 / 24, 2),  # Promedio por hora
                    'wind_speed_ms': round(avg_wind, 2),
                    'sun_hours_day': round(avg_solar / 0.85, 1)  # Estimado (asumiendo 850W/m² pico)
                },
                'monthly': {
                    'solar_kwh_m2_day': monthly_solar,
                    'wind_ms': monthly_wind
                }
            }
            
        except Exception as e:
            print(f"❌ Error obteniendo datos NASA POWER: {e}")
            return self._get_default_data()
    
    def _process_monthly_averages(self, data: Dict) -> Dict[str, float]:
        """Calcular promedios mensuales"""
        monthly = {i: [] for i in range(1, 13)}
        
        for date_str, value in data.items():
            if value == -999:  # Valor inválido
                continue
            try:
                date = datetime.strptime(date_str, '%Y%m%d')
                monthly[date.month].append(value)
            except:
                continue
        
        return {
            month: round(statistics.mean(values), 2) if values else 0
            for month, values in monthly.items()
        }
    
    def _get_default_data(self) -> Dict:
        """Datos por defecto si falla la API"""
        return {
            'status': 'default',
            'source': 'Default values',
            'averages': {
                'solar_irradiance_kwh_m2_day': 5.5,
                'solar_irradiance_w_m2': 850,
                'wind_speed_ms': 6.5,
                'sun_hours_day': 5.5
            }
        }
    
    def get_prediction_model_data(
        self, 
        latitude: float, 
        longitude: float
    ) -> Dict:
        """
        Obtener datos para el modelo de predicción
        Incluye patrones estacionales y promedios
        """
        historical = self.get_historical_data(latitude, longitude, years=5)
        
        if historical['status'] == 'default':
            return historical
        
        # Calcular patrones estacionales (hemisferio sur)
        monthly_solar = historical['monthly']['solar_kwh_m2_day']
        monthly_wind = historical['monthly']['wind_ms']
        
        # Verano (Dic-Feb), Otoño (Mar-May), Invierno (Jun-Ago), Primavera (Sep-Nov)
        seasons = {
            'summer': [12, 1, 2],
            'autumn': [3, 4, 5],
            'winter': [6, 7, 8],
            'spring': [9, 10, 11]
        }
        
        seasonal_data = {}
        for season, months in seasons.items():
            solar_avg = statistics.mean([monthly_solar.get(m, 0) for m in months])
            wind_avg = statistics.mean([monthly_wind.get(m, 0) for m in months])
            seasonal_data[season] = {
                'solar_kwh_m2_day': round(solar_avg, 2),
                'wind_ms': round(wind_avg, 2)
            }
        
        return {
            'status': 'success',
            'source': 'NASA POWER',
            'location': historical['location'],
            'period': historical['period'],
            'averages': historical['averages'],
            'monthly': historical['monthly'],
            'seasonal': seasonal_data,
            'best_month_solar': max(monthly_solar, key=monthly_solar.get),
            'best_month_wind': max(monthly_wind, key=monthly_wind.get),
            'worst_month_solar': min(monthly_solar, key=monthly_solar.get),
            'worst_month_wind': min(monthly_wind, key=monthly_wind.get)
        }


# Instancia global
nasa_power_service = NASAPowerService()
