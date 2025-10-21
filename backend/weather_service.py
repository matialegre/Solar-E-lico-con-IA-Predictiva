import requests
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from config import get_settings

settings = get_settings()


class WeatherService:
    """Servicio para obtener datos meteorológicos de OpenWeatherMap"""
    
    def __init__(self):
        self.api_key = settings.openweather_api_key
        self.lat = settings.latitude
        self.lon = settings.longitude
        self.base_url = "https://api.openweathermap.org/data/2.5"
    
    def get_forecast_5days(self) -> dict:
        """
        Obtener pronóstico de 5 días con datos cada 3 horas
        """
        try:
            url = f"{self.base_url}/forecast"
            params = {
                'lat': self.lat,
                'lon': self.lon,
                'appid': self.api_key,
                'units': 'metric',
                'lang': 'es'
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            # Procesar datos por día
            daily_forecast = {}
            for item in data.get('list', []):
                date = datetime.fromtimestamp(item['dt']).date()
                date_str = date.strftime('%Y-%m-%d')
                
                if date_str not in daily_forecast:
                    daily_forecast[date_str] = {
                        'date': date_str,
                        'temps': [],
                        'conditions': [],
                        'clouds': [],
                        'wind_speeds': [],
                        'humidity': [],
                        'rain': 0
                    }
                
                daily_forecast[date_str]['temps'].append(item['main']['temp'])
                daily_forecast[date_str]['conditions'].append(item['weather'][0]['description'])
                daily_forecast[date_str]['clouds'].append(item['clouds']['all'])
                daily_forecast[date_str]['wind_speeds'].append(item['wind']['speed'])
                daily_forecast[date_str]['humidity'].append(item['main']['humidity'])
                
                if 'rain' in item and '3h' in item['rain']:
                    daily_forecast[date_str]['rain'] += item['rain']['3h']
            
            # Calcular promedios y radiación solar estimada
            forecast_summary = []
            for date_str, day_data in sorted(daily_forecast.items())[:5]:
                avg_temp = sum(day_data['temps']) / len(day_data['temps'])
                max_temp = max(day_data['temps'])
                min_temp = min(day_data['temps'])
                avg_clouds = sum(day_data['clouds']) / len(day_data['clouds'])
                avg_wind = sum(day_data['wind_speeds']) / len(day_data['wind_speeds'])
                avg_humidity = sum(day_data['humidity']) / len(day_data['humidity'])
                
                # Estimación de radiación solar (kWh/m²/día)
                # Basado en: cielo despejado = 5-6 kWh/m²/día en Argentina
                clear_sky_radiation = 5.5
                cloud_factor = 1 - (avg_clouds / 100) * 0.7  # Las nubes reducen hasta 70%
                estimated_radiation = clear_sky_radiation * cloud_factor
                
                # Estimación de producción solar (para panel de 1kW)
                # Eficiencia promedio ~15-20%
                estimated_solar_production = estimated_radiation * 0.17 * 1000  # Wh por 1kW instalado
                
                # Estimación de producción eólica (para turbina de 1kW)
                # Fórmula cúbica: P = 0.5 * ρ * A * v³ * η
                # Simplificado: aprovechamos que la potencia es proporcional al cubo de la velocidad
                # Asumimos turbina pequeña con cut-in de 3.5 m/s
                if avg_wind >= 3.5:
                    # Factor cúbico normalizado
                    wind_power_factor = pow(avg_wind / 3.5, 3)
                    # Asumimos 24h de operación con factor de capacidad variable
                    estimated_wind_production = min(wind_power_factor * 50, 1000) * 24  # Wh por 1kW instalado
                else:
                    estimated_wind_production = 0
                
                forecast_summary.append({
                    'date': date_str,
                    'temp_avg': round(avg_temp, 1),
                    'temp_max': round(max_temp, 1),
                    'temp_min': round(min_temp, 1),
                    'condition': day_data['conditions'][len(day_data['conditions'])//2],
                    'clouds_percent': round(avg_clouds, 1),
                    'wind_speed': round(avg_wind, 1),
                    'humidity': round(avg_humidity, 1),
                    'rain_mm': round(day_data['rain'], 1),
                    'solar_radiation_kwh_m2': round(estimated_radiation, 2),
                    'estimated_solar_wh_per_kw': round(estimated_solar_production, 0),
                    'estimated_wind_wh_per_kw': round(estimated_wind_production, 0)
                })
            
            return {
                'success': True,
                'location': f"{data.get('city', {}).get('name', 'Desconocido')}",
                'forecast': forecast_summary
            }
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Error obteniendo pronóstico: {e}")
            return {
                'success': False,
                'error': str(e),
                'forecast': []
            }
    
    def get_current_weather(self) -> dict:
        """Obtener clima actual"""
        
        if not self.api_key:
            print("⚠️ API Key de OpenWeatherMap no configurada, usando datos simulados")
            return self._generate_mock_weather()
        
        try:
            url = f"{self.base_url}/weather"
            params = {
                'lat': self.lat,
                'lon': self.lon,
                'appid': self.api_key,
                'units': 'metric'
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            return self._parse_current_weather(data)
        
        except Exception as e:
            print(f"❌ Error obteniendo clima: {e}")
            return self._generate_mock_weather()
    
    def get_forecast_raw(self) -> List[Dict]:
        """Obtener pronóstico de 5 días (cada 3 horas) - formato raw"""
        
        if not self.api_key:
            print("⚠️ API Key no configurada, usando pronóstico simulado")
            return self._generate_mock_forecast()
        
        try:
            url = f"{self.base_url}/forecast"
            params = {
                'lat': self.lat,
                'lon': self.lon,
                'appid': self.api_key,
                'units': 'metric'
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            return self._parse_forecast(data)
        
        except Exception as e:
            print(f"❌ Error obteniendo pronóstico: {e}")
            return self._generate_mock_forecast()
    
    def get_hourly_forecast_24h(self) -> List[Dict]:
        """Obtener pronóstico horario para las próximas 24 horas"""
        
        # OpenWeatherMap API 3.0 tiene OneCall con pronóstico horario
        # Para API gratuita 2.5, interpolamos el pronóstico de 3 horas
        
        forecast_3h = self.get_forecast_raw()
        
        # Tomar solo las primeras 24 horas (8 intervalos de 3h)
        forecast_24h = forecast_3h[:8]
        
        # Interpolar para tener datos cada hora
        hourly_forecast = []
        
        for i, current in enumerate(forecast_24h):
            hourly_forecast.append(current)
            
            # Interpolar 2 puntos intermedios hasta el siguiente
            if i < len(forecast_24h) - 1:
                next_point = forecast_24h[i + 1]
                
                for j in range(1, 3):
                    ratio = j / 3.0
                    interpolated = self._interpolate_weather(current, next_point, ratio)
                    hourly_forecast.append(interpolated)
        
        # Retornar solo 24 puntos
        return hourly_forecast[:24]
    
    def _interpolate_weather(self, w1: Dict, w2: Dict, ratio: float) -> Dict:
        """Interpolar entre dos puntos meteorológicos"""
        
        return {
            'timestamp': w1['timestamp'] + timedelta(hours=ratio * 3),
            'temperature_c': w1['temperature_c'] + ratio * (w2['temperature_c'] - w1['temperature_c']),
            'humidity_percent': w1['humidity_percent'] + ratio * (w2['humidity_percent'] - w1['humidity_percent']),
            'pressure_hpa': w1['pressure_hpa'] + ratio * (w2['pressure_hpa'] - w1['pressure_hpa']),
            'wind_speed_ms': w1['wind_speed_ms'] + ratio * (w2['wind_speed_ms'] - w1['wind_speed_ms']),
            'wind_direction_deg': w1['wind_direction_deg'],
            'cloud_cover_percent': w1['cloud_cover_percent'] + ratio * (w2['cloud_cover_percent'] - w1['cloud_cover_percent']),
            'rain_1h_mm': w1.get('rain_1h_mm', 0),
            'description': w1['description'],
        }
    
    def _parse_current_weather(self, data: Dict) -> Dict:
        """Parsear respuesta de clima actual"""
        
        return {
            'timestamp': datetime.utcnow(),
            'temperature_c': data['main']['temp'],
            'humidity_percent': data['main']['humidity'],
            'pressure_hpa': data['main']['pressure'],
            'wind_speed_ms': data['wind']['speed'],
            'wind_direction_deg': data['wind'].get('deg', 0),
            'cloud_cover_percent': data['clouds']['all'],
            'rain_1h_mm': data.get('rain', {}).get('1h', 0),
            'description': data['weather'][0]['description'],
            'solar_radiation_wm2': self._estimate_solar_radiation(
                data['clouds']['all'], 
                data['main']['humidity']
            )
        }
    
    def _parse_forecast(self, data: Dict) -> List[Dict]:
        """Parsear respuesta de pronóstico"""
        
        forecast = []
        
        for item in data['list']:
            forecast.append({
                'timestamp': datetime.fromtimestamp(item['dt']),
                'temperature_c': item['main']['temp'],
                'humidity_percent': item['main']['humidity'],
                'pressure_hpa': item['main']['pressure'],
                'wind_speed_ms': item['wind']['speed'],
                'wind_direction_deg': item['wind'].get('deg', 0),
                'cloud_cover_percent': item['clouds']['all'],
                'rain_1h_mm': item.get('rain', {}).get('3h', 0) / 3.0,  # Dividir por 3h
                'description': item['weather'][0]['description'],
                'solar_radiation_wm2': self._estimate_solar_radiation(
                    item['clouds']['all'],
                    item['main']['humidity']
                )
            })
        
        return forecast
    
    def _estimate_solar_radiation(self, cloud_cover: float, humidity: float) -> float:
        """Estimar radiación solar (W/m²) basada en nubosidad"""
        
        hour = datetime.now().hour
        
        if hour < 6 or hour > 20:
            return 0.0
        
        # Radiación máxima teórica
        max_radiation = 1000.0
        
        # Factor por hora del día (curva sinusoidal)
        import numpy as np
        hour_factor = np.sin(np.pi * (hour - 6) / 14)
        
        # Factor de nubosidad
        cloud_factor = 1.0 - (cloud_cover / 100.0) * 0.75
        
        # Factor de humedad
        humidity_factor = 1.0 - (humidity / 100.0) * 0.1
        
        radiation = max_radiation * hour_factor * cloud_factor * humidity_factor
        
        return max(0.0, radiation)
    
    def _generate_mock_weather(self) -> Dict:
        """Generar datos meteorológicos simulados"""
        
        import random
        hour = datetime.now().hour
        
        # Temperatura varía según hora del día
        base_temp = 20 + 10 * (1 - abs(hour - 14) / 14)
        
        # Viento más fuerte en tarde
        base_wind = 3 + 7 * (hour / 24.0)
        
        return {
            'timestamp': datetime.utcnow(),
            'temperature_c': base_temp + random.uniform(-2, 2),
            'humidity_percent': random.uniform(40, 80),
            'pressure_hpa': 1013 + random.uniform(-5, 5),
            'wind_speed_ms': base_wind + random.uniform(-2, 2),
            'wind_direction_deg': random.uniform(0, 360),
            'cloud_cover_percent': random.uniform(0, 100),
            'rain_1h_mm': 0,
            'description': 'Simulado',
            'solar_radiation_wm2': self._estimate_solar_radiation(
                random.uniform(0, 50), 50
            )
        }
    
    def _generate_mock_forecast(self) -> List[Dict]:
        """Generar pronóstico simulado"""
        
        forecast = []
        now = datetime.now()
        
        for i in range(40):  # 5 días, cada 3 horas
            timestamp = now + timedelta(hours=i * 3)
            hour = timestamp.hour
            
            import random
            base_temp = 20 + 10 * (1 - abs(hour - 14) / 14)
            base_wind = 3 + 7 * (hour / 24.0)
            
            forecast.append({
                'timestamp': timestamp,
                'temperature_c': base_temp + random.uniform(-2, 2),
                'humidity_percent': random.uniform(40, 80),
                'pressure_hpa': 1013 + random.uniform(-5, 5),
                'wind_speed_ms': base_wind + random.uniform(-2, 2),
                'wind_direction_deg': random.uniform(0, 360),
                'cloud_cover_percent': random.uniform(0, 100),
                'rain_1h_mm': 0,
                'description': 'Simulado',
                'solar_radiation_wm2': self._estimate_solar_radiation(
                    random.uniform(0, 50), 50
                )
            })
        
        return forecast


# Instancia global
weather_service = WeatherService()
