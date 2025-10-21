"""
Router para verificar estado de servicios
"""

from fastapi import APIRouter
from datetime import datetime
import httpx
from config import get_settings

router = APIRouter(prefix="/api/status", tags=["Status"])

settings = get_settings()


@router.get("/health")
async def health_check():
    """
    Verificar estado de TODOS los servicios
    
    Chequea:
    - Servidor backend (este)
    - OpenWeather API
    - NASA POWER API
    - ESP32 conectados
    """
    
    status = {
        "timestamp": datetime.now().isoformat(),
        "services": {}
    }
    
    # 1. Backend (este servidor)
    status["services"]["backend"] = {
        "status": "online",
        "name": "FastAPI Backend",
        "uptime": "calculando...",
        "version": "1.0.0"
    }
    
    # 2. OpenWeather API
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            # Test API key
            url = f"https://api.openweathermap.org/data/2.5/weather?lat={settings.latitude}&lon={settings.longitude}&appid={settings.openweather_api_key}"
            response = await client.get(url)
            
            if response.status_code == 200:
                data = response.json()
                status["services"]["openweather"] = {
                    "status": "online",
                    "name": "OpenWeather API",
                    "response_time_ms": int(response.elapsed.total_seconds() * 1000),
                    "api_key_valid": True,
                    "location": data.get("name", "Unknown"),
                    "last_update": datetime.fromtimestamp(data.get("dt", 0)).isoformat()
                }
            elif response.status_code == 401:
                status["services"]["openweather"] = {
                    "status": "error",
                    "name": "OpenWeather API",
                    "error": "API key inválida",
                    "api_key_valid": False
                }
            else:
                status["services"]["openweather"] = {
                    "status": "error",
                    "name": "OpenWeather API",
                    "error": f"HTTP {response.status_code}"
                }
    except Exception as e:
        status["services"]["openweather"] = {
            "status": "offline",
            "name": "OpenWeather API",
            "error": str(e)
        }
    
    # 3. NASA POWER API
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            url = "https://power.larc.nasa.gov/api/temporal/daily/point"
            params = {
                "parameters": "ALLSKY_SFC_SW_DWN",
                "community": "RE",
                "longitude": settings.longitude,
                "latitude": settings.latitude,
                "start": "20240101",
                "end": "20240107",
                "format": "JSON"
            }
            response = await client.get(url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                status["services"]["nasa_power"] = {
                    "status": "online",
                    "name": "NASA POWER API",
                    "response_time_ms": int(response.elapsed.total_seconds() * 1000),
                    "data_available": True,
                    "source": data.get("header", {}).get("title", "NASA POWER")
                }
            else:
                status["services"]["nasa_power"] = {
                    "status": "error",
                    "name": "NASA POWER API",
                    "error": f"HTTP {response.status_code}"
                }
    except Exception as e:
        status["services"]["nasa_power"] = {
            "status": "offline",
            "name": "NASA POWER API",
            "error": str(e)
        }
    
    # 4. ESP32 dispositivos
    from routers.esp32_router import dispositivos_db
    
    total_devices = len(dispositivos_db)
    online_devices = sum(1 for d in dispositivos_db.values() if d.get("status") == "online")
    
    if total_devices > 0:
        status["services"]["esp32"] = {
            "status": "online" if online_devices > 0 else "warning",
            "name": "Dispositivos ESP32",
            "total": total_devices,
            "online": online_devices,
            "offline": total_devices - online_devices,
            "devices": [
                {
                    "device_id": d["device_id"],
                    "status": d["status"],
                    "ip_local": d.get("ip_local"),
                    "last_seen": d.get("last_seen")
                }
                for d in dispositivos_db.values()
            ]
        }
    else:
        status["services"]["esp32"] = {
            "status": "warning",
            "name": "Dispositivos ESP32",
            "total": 0,
            "online": 0,
            "message": "No hay dispositivos registrados"
        }
    
    # 5. Machine Learning
    from services.ml_predictor_service import ml_predictor
    
    if ml_predictor.metrics is not None:
        status["services"]["machine_learning"] = {
            "status": "ready",
            "name": "Machine Learning",
            "models_trained": True,
            "solar_accuracy": ml_predictor.metrics["modelo_solar"]["validacion"]["r2"],
            "wind_accuracy": ml_predictor.metrics["modelo_eolico"]["validacion"]["r2"],
            "training_date": ml_predictor.metrics["datos_entrenamiento"]["periodo"]
        }
    else:
        status["services"]["machine_learning"] = {
            "status": "not_trained",
            "name": "Machine Learning",
            "models_trained": False,
            "message": "Modelos no entrenados. Ejecutar /api/ml/train"
        }
    
    # Calcular estado general
    all_services = list(status["services"].values())
    online_count = sum(1 for s in all_services if s.get("status") in ["online", "ready"])
    total_count = len(all_services)
    
    status["summary"] = {
        "all_services_count": total_count,
        "online_count": online_count,
        "offline_count": total_count - online_count,
        "health_percentage": (online_count / total_count * 100) if total_count > 0 else 0,
        "overall_status": "healthy" if online_count == total_count else "degraded" if online_count > 0 else "offline"
    }
    
    return status


@router.get("/forecast")
async def forecast_summary():
    """
    Resumen de pronóstico climático para los próximos 5 días
    Usado por ML para mejorar predicciones
    """
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            url = f"https://api.openweathermap.org/data/2.5/forecast?lat={settings.latitude}&lon={settings.longitude}&appid={settings.openweather_api_key}&units=metric"
            response = await client.get(url)
            
            if response.status_code != 200:
                return {"error": "No se pudo obtener pronóstico"}
            
            data = response.json()
            forecast_list = data.get("list", [])
            
            # Agrupar por día
            daily_summary = {}
            
            for item in forecast_list[:40]:  # 5 días × 8 (cada 3 horas)
                date = item["dt_txt"].split(" ")[0]
                
                if date not in daily_summary:
                    daily_summary[date] = {
                        "date": date,
                        "temps": [],
                        "wind_speeds": [],
                        "clouds": [],
                        "rain": 0,
                        "conditions": []
                    }
                
                daily_summary[date]["temps"].append(item["main"]["temp"])
                daily_summary[date]["wind_speeds"].append(item["wind"]["speed"])
                daily_summary[date]["clouds"].append(item["clouds"]["all"])
                
                if "rain" in item and "3h" in item["rain"]:
                    daily_summary[date]["rain"] += item["rain"]["3h"]
                
                daily_summary[date]["conditions"].append(item["weather"][0]["main"])
            
            # Calcular promedios
            forecast_days = []
            for date, data in daily_summary.items():
                forecast_days.append({
                    "date": date,
                    "temp_avg": sum(data["temps"]) / len(data["temps"]),
                    "temp_max": max(data["temps"]),
                    "temp_min": min(data["temps"]),
                    "wind_avg_ms": sum(data["wind_speeds"]) / len(data["wind_speeds"]),
                    "wind_max_ms": max(data["wind_speeds"]),
                    "clouds_avg": sum(data["clouds"]) / len(data["clouds"]),
                    "rain_total_mm": data["rain"],
                    "condition": max(set(data["conditions"]), key=data["conditions"].count),
                    "solar_factor": 1.0 - (sum(data["clouds"]) / len(data["clouds"]) / 100) * 0.7,  # Reducción por nubes
                    "wind_factor": sum(data["wind_speeds"]) / len(data["wind_speeds"]) / 10.0  # Normalizado
                })
            
            return {
                "location": {
                    "city": data["city"]["name"],
                    "lat": data["city"]["coord"]["lat"],
                    "lon": data["city"]["coord"]["lon"]
                },
                "forecast_days": forecast_days,
                "summary": {
                    "avg_temp": sum(d["temp_avg"] for d in forecast_days) / len(forecast_days),
                    "avg_wind": sum(d["wind_avg_ms"] for d in forecast_days) / len(forecast_days),
                    "total_rain": sum(d["rain_total_mm"] for d in forecast_days),
                    "avg_solar_factor": sum(d["solar_factor"] for d in forecast_days) / len(forecast_days),
                    "good_solar_days": sum(1 for d in forecast_days if d["solar_factor"] > 0.7),
                    "good_wind_days": sum(1 for d in forecast_days if d["wind_avg_ms"] > 4.0)
                }
            }
            
    except Exception as e:
        return {"error": str(e)}
