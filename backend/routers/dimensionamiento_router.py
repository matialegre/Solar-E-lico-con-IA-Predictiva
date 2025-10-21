"""
Router para cálculos de dimensionamiento
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from services.dimensionamiento_service import dimensionamiento_service
from services.nasa_power_service import get_location_climate_data
from services.ml_predictor_service import ml_predictor

router = APIRouter(prefix="/api/dimensionamiento", tags=["Dimensionamiento"])


class DimensionamientoOpcion1(BaseModel):
    """
    Opción 1: Tengo X consumo, ¿qué sistema necesito?
    """
    latitude: float
    longitude: float
    consumo_diario_kwh: float
    dias_autonomia: int = 2
    voltaje_sistema: int = 48


class DimensionamientoOpcion2(BaseModel):
    """
    Opción 2: Tengo estos recursos, ¿qué potencia puedo sacar?
    """
    latitude: float
    longitude: float
    potencia_solar_w: float
    area_solar_m2: float
    potencia_eolica_w: float
    diametro_turbina_m: float


@router.post("/opcion1")
async def calcular_opcion1(request: DimensionamientoOpcion1):
    """
    OPCIÓN 1: Calcular sistema necesario desde consumo
    
    Flujo:
    1. Obtener datos climáticos históricos (NASA API)
    2. Calcular dimensionamiento solar
    3. Calcular dimensionamiento eólico
    4. Calcular batería
    5. Retornar recomendación completa con ecuaciones
    """
    try:
        # 1. Obtener datos climáticos históricos
        print(f"📡 Obteniendo datos climáticos para: {request.latitude}, {request.longitude}")
        clima_data = await get_location_climate_data(request.latitude, request.longitude)
        
        irradiancia_kwh_m2_dia = clima_data["solar"]["annual_avg_kwh_m2_day"]
        velocidad_viento_ms = clima_data["wind"]["annual_avg_ms"]
        
        # 2. Dimensionamiento solar
        print(f"☀️ Calculando sistema solar...")
        solar_result = dimensionamiento_service.dimensionar_solar_opcion1(
            consumo_diario_kwh=request.consumo_diario_kwh,
            irradiancia_kwh_m2_dia=irradiancia_kwh_m2_dia,
            dias_autonomia=request.dias_autonomia
        )
        
        # 3. Dimensionamiento eólico
        print(f"💨 Calculando sistema eólico...")
        eolico_result = dimensionamiento_service.dimensionar_eolico_opcion1(
            consumo_diario_kwh=request.consumo_diario_kwh,
            velocidad_viento_promedio_ms=velocidad_viento_ms
        )
        
        # 4. Dimensionamiento batería
        print(f"🔋 Calculando batería...")
        bateria_result = dimensionamiento_service.dimensionar_bateria(
            consumo_diario_kwh=request.consumo_diario_kwh,
            dias_autonomia=request.dias_autonomia,
            voltaje_sistema=request.voltaje_sistema
        )
        
        # 5. Resumen total
        generacion_total_kwh = (
            solar_result["resultado"]["generacion"]["diaria_kwh"] +
            eolico_result["resultado"]["generacion"]["diaria_kwh"]
        )
        
        costo_total_usd = (
            solar_result["resultado"]["costo"]["total_estimado_usd"] +
            eolico_result["resultado"]["costo"]["total_estimado_usd"] +
            bateria_result["resultado"]["costo"]["total_estimado_usd"]
        )
        
        cobertura_porcentaje = (generacion_total_kwh / request.consumo_diario_kwh) * 100
        balance_kwh = generacion_total_kwh - request.consumo_diario_kwh
        
        roi_anual = (request.consumo_diario_kwh * 365 * 0.15) / costo_total_usd  # Asumiendo $0.15/kWh
        payback_years = 1 / roi_anual if roi_anual > 0 else 0
        
        return {
            "tipo": "opcion1_desde_consumo",
            "ubicacion": {
                "latitude": request.latitude,
                "longitude": request.longitude,
                "zona": "Argentina"  # TODO: geocoding
            },
            "clima_historico": clima_data,
            "entrada": {
                "consumo_diario_kwh": request.consumo_diario_kwh,
                "consumo_mensual_kwh": request.consumo_diario_kwh * 30,
                "consumo_anual_kwh": request.consumo_diario_kwh * 365,
                "dias_autonomia": request.dias_autonomia,
                "voltaje_sistema": request.voltaje_sistema
            },
            "sistema_solar": solar_result,
            "sistema_eolico": eolico_result,
            "sistema_bateria": bateria_result,
            "resumen": {
                "generacion_total_diaria_kwh": generacion_total_kwh,
                "cobertura_porcentaje": cobertura_porcentaje,
                "balance_diario_kwh": balance_kwh,
                "autonomia_dias": request.dias_autonomia,
                "costo_total_usd": costo_total_usd,
                "ahorro_anual_usd": request.consumo_diario_kwh * 365 * 0.15,
                "payback_years": round(payback_years, 1),
                "roi_anual_porcentaje": round(roi_anual * 100, 1)
            },
            "recomendacion": {
                "viabilidad": "EXCELENTE" if cobertura_porcentaje >= 100 else "BUENA" if cobertura_porcentaje >= 80 else "REGULAR",
                "mensaje": f"El sistema cubre el {cobertura_porcentaje:.0f}% del consumo",
                "siguiente_paso": "Configurar ESP32 con esta ubicación y comenzar monitoreo"
            }
        }
        
    except Exception as e:
        print(f"❌ Error en cálculo: {e}")
        raise HTTPException(status_code=500, detail=f"Error en cálculo: {str(e)}")


@router.post("/opcion2")
async def calcular_opcion2(request: DimensionamientoOpcion2):
    """
    OPCIÓN 2: Calcular potencia máxima desde recursos existentes
    
    Flujo:
    1. Obtener datos climáticos históricos (NASA API)
    2. Calcular potencia solar máxima posible
    3. Calcular potencia eólica máxima posible
    4. Recomendar batería para ese sistema
    5. Estimar consumo máximo soportable
    """
    try:
        # 1. Obtener datos climáticos
        print(f"📡 Obteniendo datos climáticos para: {request.latitude}, {request.longitude}")
        clima_data = await get_location_climate_data(request.latitude, request.longitude)
        
        irradiancia_kwh_m2_dia = clima_data["solar"]["annual_avg_kwh_m2_day"]
        velocidad_viento_ms = clima_data["wind"]["annual_avg_ms"]
        
        # 2. Calcular generación solar máxima
        hsp = irradiancia_kwh_m2_dia
        eficiencia_sistema = 0.85
        generacion_solar_kwh = (request.potencia_solar_w / 1000) * hsp * eficiencia_sistema
        
        # 3. Calcular generación eólica máxima
        import math
        area_barrido = math.pi * (request.diametro_turbina_m / 2) ** 2
        densidad_aire = 1.225
        eficiencia_turbina = 0.35
        
        potencia_viento = 0.5 * densidad_aire * area_barrido * (velocidad_viento_ms ** 3)
        potencia_eolica_real = potencia_viento * eficiencia_turbina
        generacion_eolica_kwh = (potencia_eolica_real * 24) / 1000
        
        # 4. Generación total
        generacion_total_kwh = generacion_solar_kwh + generacion_eolica_kwh
        
        # 5. Consumo máximo soportable
        consumo_maximo_kwh = generacion_total_kwh * 0.90  # 90% de seguridad
        
        # 6. Recomendar batería
        bateria_result = dimensionamiento_service.dimensionar_bateria(
            consumo_diario_kwh=consumo_maximo_kwh,
            dias_autonomia=2,
            voltaje_sistema=48
        )
        
        return {
            "tipo": "opcion2_desde_recursos",
            "ubicacion": {
                "latitude": request.latitude,
                "longitude": request.longitude
            },
            "clima_historico": clima_data,
            "entrada": {
                "potencia_solar_w": request.potencia_solar_w,
                "area_solar_m2": request.area_solar_m2,
                "potencia_eolica_w": request.potencia_eolica_w,
                "diametro_turbina_m": request.diametro_turbina_m
            },
            "calculos": {
                "solar": {
                    "ecuacion": "E_solar = (P_solar / 1000) × HSP × η_sistema",
                    "valores": f"E = ({request.potencia_solar_w} / 1000) × {hsp:.2f} × {eficiencia_sistema}",
                    "resultado": f"{generacion_solar_kwh:.2f} kWh/día"
                },
                "eolico": {
                    "ecuacion": "P_eolica = 0.5 × ρ × A × v³ × η_turbina",
                    "valores": f"P = 0.5 × {densidad_aire} × {area_barrido:.2f} × {velocidad_viento_ms}³ × {eficiencia_turbina}",
                    "resultado": f"{generacion_eolica_kwh:.2f} kWh/día"
                }
            },
            "resultado": {
                "generacion_solar_kwh_dia": generacion_solar_kwh,
                "generacion_eolica_kwh_dia": generacion_eolica_kwh,
                "generacion_total_kwh_dia": generacion_total_kwh,
                "generacion_mensual_kwh": generacion_total_kwh * 30,
                "generacion_anual_kwh": generacion_total_kwh * 365,
                "consumo_maximo_soportable_kwh_dia": consumo_maximo_kwh,
                "potencia_promedio_w": (consumo_maximo_kwh * 1000) / 24
            },
            "sistema_bateria_recomendado": bateria_result,
            "recomendacion": {
                "mensaje": f"Tu sistema puede generar hasta {generacion_total_kwh:.1f} kWh/día",
                "consumo_max": f"Consumo máximo recomendado: {consumo_maximo_kwh:.1f} kWh/día",
                "suficiencia": "EXCELENTE" if generacion_total_kwh > 15 else "BUENA" if generacion_total_kwh > 10 else "MODERADA"
            }
        }
        
    except Exception as e:
        print(f"❌ Error en cálculo opción 2: {e}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@router.get("/clima/{latitude}/{longitude}")
async def get_clima_ubicacion(latitude: float, longitude: float):
    """
    Obtener datos climáticos históricos de una ubicación
    
    Usado por el frontend para mostrar datos antes del cálculo
    """
    try:
        clima_data = await get_location_climate_data(latitude, longitude)
        return clima_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo datos: {str(e)}")
