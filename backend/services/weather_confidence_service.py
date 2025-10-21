"""
Servicio de confianza meteorológica
Combina múltiples fuentes y detecta discrepancias
"""

import httpx
from typing import Dict, List
from datetime import datetime
from config import get_settings

settings = get_settings()


class WeatherConfidenceService:
    """
    Evalúa confianza de predicciones combinando múltiples fuentes
    """
    
    async def get_multi_source_weather(
        self,
        latitude: float,
        longitude: float
    ) -> Dict:
        """
        Obtener clima de múltiples fuentes y comparar
        
        Fuentes:
        1. OpenWeather (principal)
        2. WeatherAPI.com (alternativa)
        3. Open-Meteo (gratis, sin API key)
        """
        
        results = {
            "timestamp": datetime.now().isoformat(),
            "location": {"latitude": latitude, "longitude": longitude},
            "sources": {},
            "consensus": {},
            "alerts": []
        }
        
        # 1. OpenWeather (ya tenemos)
        try:
            openweather_data = await self._get_openweather(latitude, longitude)
            results["sources"]["openweather"] = openweather_data
        except Exception as e:
            results["sources"]["openweather"] = {"error": str(e)}
        
        # 2. Open-Meteo (GRATIS, sin API key)
        try:
            open_meteo_data = await self._get_open_meteo(latitude, longitude)
            results["sources"]["open_meteo"] = open_meteo_data
        except Exception as e:
            results["sources"]["open_meteo"] = {"error": str(e)}
        
        # 3. Calcular consenso
        results["consensus"] = self._calculate_consensus(results["sources"])
        
        # 4. Detectar discrepancias
        results["alerts"] = self._detect_discrepancies(results["sources"])
        
        return results
    
    async def _get_openweather(self, lat: float, lon: float) -> Dict:
        """Obtener datos de OpenWeather"""
        async with httpx.AsyncClient(timeout=5.0) as client:
            url = f"https://api.openweathermap.org/data/2.5/weather"
            params = {
                "lat": lat,
                "lon": lon,
                "appid": settings.openweather_api_key,
                "units": "metric"
            }
            response = await client.get(url, params=params)
            data = response.json()
            
            return {
                "source": "OpenWeather",
                "condition": data["weather"][0]["main"],
                "description": data["weather"][0]["description"],
                "temperature": data["main"]["temp"],
                "humidity": data["main"]["humidity"],
                "clouds": data["clouds"]["all"],
                "wind_speed": data["wind"]["speed"],
                "rain_1h": data.get("rain", {}).get("1h", 0),
                "timestamp": data["dt"],
                "update_frequency": "1-3 horas"
            }
    
    async def _get_open_meteo(self, lat: float, lon: float) -> Dict:
        """
        Obtener datos de Open-Meteo (GRATIS, sin API key)
        Fuente europea, muy precisa
        """
        async with httpx.AsyncClient(timeout=5.0) as client:
            url = "https://api.open-meteo.com/v1/forecast"
            params = {
                "latitude": lat,
                "longitude": lon,
                "current": "temperature_2m,relative_humidity_2m,precipitation,cloud_cover,wind_speed_10m",
                "hourly": "precipitation_probability",
                "forecast_days": 1
            }
            response = await client.get(url, params=params)
            data = response.json()
            
            current = data["current"]
            hourly = data["hourly"]
            
            # Calcular probabilidad próximas horas
            next_3h_precip_prob = sum(hourly["precipitation_probability"][:3]) / 3
            
            # Determinar condición
            if current["precipitation"] > 0:
                condition = "Rain"
            elif current["cloud_cover"] > 70:
                condition = "Clouds"
            else:
                condition = "Clear"
            
            return {
                "source": "Open-Meteo",
                "condition": condition,
                "temperature": current["temperature_2m"],
                "humidity": current["relative_humidity_2m"],
                "clouds": current["cloud_cover"],
                "wind_speed": current["wind_speed_10m"],
                "precipitation_current": current["precipitation"],
                "precipitation_probability_3h": next_3h_precip_prob,
                "timestamp": current["time"],
                "update_frequency": "15 minutos"
            }
    
    def _calculate_consensus(self, sources: Dict) -> Dict:
        """
        Calcular consenso entre fuentes
        """
        valid_sources = [s for s in sources.values() if "error" not in s]
        
        if not valid_sources:
            return {"error": "No hay fuentes válidas"}
        
        # Promedios
        avg_temp = sum(s["temperature"] for s in valid_sources) / len(valid_sources)
        avg_humidity = sum(s["humidity"] for s in valid_sources) / len(valid_sources)
        avg_clouds = sum(s["clouds"] for s in valid_sources) / len(valid_sources)
        avg_wind = sum(s["wind_speed"] for s in valid_sources) / len(valid_sources)
        
        # Condiciones
        conditions = [s["condition"] for s in valid_sources]
        
        # Consenso de condición (mayoría)
        from collections import Counter
        condition_votes = Counter(conditions)
        consensus_condition = condition_votes.most_common(1)[0][0]
        agreement = condition_votes[consensus_condition] / len(conditions)
        
        # Nivel de confianza
        if agreement == 1.0:
            confidence = "ALTA"
            confidence_level = 95
        elif agreement >= 0.5:
            confidence = "MEDIA"
            confidence_level = 70
        else:
            confidence = "BAJA"
            confidence_level = 40
        
        return {
            "condition": consensus_condition,
            "temperature": round(avg_temp, 1),
            "humidity": round(avg_humidity, 1),
            "clouds": round(avg_clouds, 1),
            "wind_speed": round(avg_wind, 1),
            "agreement": round(agreement * 100, 1),
            "confidence": confidence,
            "confidence_level": confidence_level,
            "sources_count": len(valid_sources),
            "votes": dict(condition_votes)
        }
    
    def _detect_discrepancies(self, sources: Dict) -> List[Dict]:
        """
        Detectar discrepancias significativas entre fuentes
        """
        alerts = []
        valid_sources = [s for s in sources.values() if "error" not in s]
        
        if len(valid_sources) < 2:
            return alerts
        
        # Comparar condiciones
        conditions = [s["condition"] for s in valid_sources]
        if len(set(conditions)) > 1:
            # Hay discrepancia
            alerts.append({
                "type": "DISCREPANCIA_CONDICIÓN",
                "severity": "WARNING",
                "message": f"Las fuentes NO coinciden: {', '.join(conditions)}",
                "recommendation": "⚠️ Verificar radar local para condiciones actuales",
                "detail": {
                    source["source"]: source["condition"] 
                    for source in valid_sources
                }
            })
        
        # Comparar precipitación
        precipitations = []
        for source in valid_sources:
            if "rain_1h" in source and source["rain_1h"] > 0:
                precipitations.append(("rain", source["source"]))
            elif "precipitation_current" in source and source["precipitation_current"] > 0:
                precipitations.append(("rain", source["source"]))
            elif "precipitation_probability_3h" in source and source["precipitation_probability_3h"] > 50:
                precipitations.append(("probable_rain", source["source"]))
        
        if precipitations:
            rain_sources = [p[1] for p in precipitations if p[0] == "rain"]
            if len(rain_sources) > 0 and len(rain_sources) < len(valid_sources):
                alerts.append({
                    "type": "DISCREPANCIA_PRECIPITACIÓN",
                    "severity": "HIGH",
                    "message": f"⚠️ {len(rain_sources)} fuente(s) reportan lluvia, otras NO",
                    "recommendation": "🌧️ Revisar radar meteorológico local inmediatamente",
                    "detail": {
                        "fuentes_con_lluvia": rain_sources,
                        "total_fuentes": len(valid_sources)
                    }
                })
        
        # Comparar nubes
        clouds = [s["clouds"] for s in valid_sources]
        cloud_diff = max(clouds) - min(clouds)
        if cloud_diff > 40:  # Más de 40% diferencia
            alerts.append({
                "type": "DISCREPANCIA_NUBOSIDAD",
                "severity": "INFO",
                "message": f"Diferencia de {cloud_diff:.0f}% en nubosidad entre fuentes",
                "recommendation": "Usar promedio o fuente más actualizada",
                "detail": {
                    source["source"]: source["clouds"]
                    for source in valid_sources
                }
            })
        
        return alerts


# Singleton
weather_confidence = WeatherConfidenceService()
