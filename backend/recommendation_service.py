"""
Servicio de Recomendaciones
Calcula equipamiento necesario o potencial de generación
Integrado con ML para predicciones más precisas
"""

import math
from typing import Dict, Optional

try:
    from ml_predictor import ml_predictor
    ML_ENABLED = True
except Exception as e:
    print(f"⚠️ ML no disponible: {e}")
    ML_ENABLED = False
    ml_predictor = None


class RecommendationService:
    """Servicio para calcular recomendaciones"""
    
    def __init__(self):
        # Constantes
        self.SOLAR_EFFICIENCY = 0.18  # 18% eficiencia típica
        self.WIND_EFFICIENCY = 0.35   # 35% eficiencia (Betz limit ~59%)
        self.BATTERY_DOD = 0.80       # 80% depth of discharge
        self.AUTONOMY_DAYS = 2        # 2 días de autonomía
        
    def get_climate_data(self, latitude: float, longitude: float) -> Dict:
        """
        Obtener datos climáticos promedio para una ubicación
        Integrado con NASA POWER API
        """
        from nasa_power_service import nasa_power_service
        
        # Obtener datos reales de NASA POWER
        nasa_data = nasa_power_service.get_historical_data(latitude, longitude, years=5)
        
        if nasa_data['status'] == 'success':
            return {
                'avg_solar_irradiance_wm2': nasa_data['averages']['solar_irradiance_w_m2'],
                'avg_wind_speed_ms': nasa_data['averages']['wind_speed_ms'],
                'sun_hours_day': nasa_data['averages']['sun_hours_day'],
                'source': 'NASA POWER (5 años histórico)'
            }
        else:
            # Fallback a valores por defecto
            return {
                'avg_solar_irradiance_wm2': 850,
                'avg_wind_speed_ms': 6.5,
                'sun_hours_day': 5.5,
                'source': 'Valores por defecto'
            }
    
    def calculate_by_demand(
        self, 
        target_power_w: float,
        latitude: float,
        longitude: float
    ) -> Dict:
        """
        Calcular equipamiento necesario según demanda
        """
        # Obtener datos climáticos REALES de la ubicación
        climate = self.get_climate_data(latitude, longitude)
        
        # Energía diaria necesaria (Wh)
        daily_energy_wh = target_power_w * 24
        
        # === PANEL SOLAR ===
        # Potencia panel = energía_diaria / (horas_sol * eficiencia)
        solar_power_w = daily_energy_wh / (climate['sun_hours_day'] * self.SOLAR_EFFICIENCY)
        solar_area_m2 = solar_power_w / (climate['avg_solar_irradiance_wm2'] * self.SOLAR_EFFICIENCY)
        
        # === TURBINA EÓLICA ===
        # Potencia eólica = 0.5 * ρ * A * v³ * η
        # A = área barrida = π * r²
        # Asumimos contribución 40% solar, 60% eólica
        wind_contribution = target_power_w * 0.6
        rho_air = 1.225  # kg/m³ densidad del aire
        v_wind = climate['avg_wind_speed_ms']
        
        # Calcular área necesaria
        wind_area_m2 = (wind_contribution) / (
            0.5 * rho_air * (v_wind ** 3) * self.WIND_EFFICIENCY
        )
        wind_diameter_m = math.sqrt(4 * wind_area_m2 / math.pi)
        wind_power_w = wind_contribution
        
        # === BATERÍA ===
        # Capacidad = consumo_diario * días_autonomía / DOD
        battery_capacity_wh = (daily_energy_wh * self.AUTONOMY_DAYS) / self.BATTERY_DOD
        
        # Voltaje batería (48V típico para sistemas medianos)
        if target_power_w < 1500:
            battery_voltage = 24
        elif target_power_w < 4000:
            battery_voltage = 48
        else:
            battery_voltage = 96
        
        battery_ah = battery_capacity_wh / battery_voltage
        
        # === INVERSOR ===
        # Sobredimensionar 30% para picos
        inverter_power_w = target_power_w * 1.3
        
        return {
            'status': 'success',
            'mode': 'demand',
            'input': {
                'target_power_w': target_power_w,
                'latitude': latitude,
                'longitude': longitude
            },
            'climate': climate,
            'solar': {
                'power_w': round(solar_power_w),
                'area_m2': round(solar_area_m2, 2),
                'panels_300w': math.ceil(solar_power_w / 300),
                'estimated_cost_usd': round(solar_power_w * 0.8)  # $0.8/W típico
            },
            'wind': {
                'power_w': round(wind_power_w),
                'diameter_m': round(wind_diameter_m, 2),
                'blade_count': 3,
                'estimated_cost_usd': round(wind_power_w * 1.5)  # $1.5/W típico
            },
            'battery': {
                'capacity_wh': round(battery_capacity_wh),
                'voltage': battery_voltage,
                'amp_hours': round(battery_ah),
                'type': 'LiFePO4',
                'estimated_cost_usd': round(battery_capacity_wh * 0.3)  # $0.3/Wh típico
            },
            'inverter': {
                'power_w': round(inverter_power_w),
                'voltage_in': battery_voltage,
                'voltage_out': 220,
                'type': 'Pure Sine Wave',
                'estimated_cost_usd': round(inverter_power_w * 0.4)  # $0.4/W típico
            },
            'total_estimated_cost_usd': round(
                solar_power_w * 0.8 +
                wind_power_w * 1.5 +
                battery_capacity_wh * 0.3 +
                inverter_power_w * 0.4
            )
        }
    
    def calculate_by_resources(
        self,
        solar_panel_w: float,
        solar_panel_area_m2: float,
        wind_turbine_w: float,
        wind_turbine_diameter_m: float,
        battery_capacity_wh: float,
        latitude: float,
        longitude: float
    ) -> Dict:
        """
        Calcular potencial de generación según recursos existentes
        """
        # Obtener datos climáticos REALES de la ubicación
        climate = self.get_climate_data(latitude, longitude)
        
        # === GENERACIÓN SOLAR (CON ML SI ESTÁ DISPONIBLE) ===
        if ML_ENABLED and ml_predictor and ml_predictor.ml_available:
            # Usar predicción ML
            ml_prediction = ml_predictor.predict_daily_generation(
                latitude=latitude,
                avg_irradiance=climate['avg_solar_irradiance_wm2'],
                avg_wind_speed=climate['avg_wind_speed_ms']
            )
            solar_daily_kwh = ml_prediction['solar_kwh_day'] * (solar_panel_w / 1000)
            wind_daily_kwh = ml_prediction['wind_kwh_day'] * (wind_turbine_w / 1000)
            print(f"✅ Usando predicción ML")
        else:
            # Fallback a cálculo tradicional
            solar_daily_kwh = (solar_panel_w * climate['sun_hours_day'] * 0.85) / 1000
            
            # === GENERACIÓN EÓLICA ===
            if wind_turbine_diameter_m > 0:
                rho_air = 1.225
                wind_area_m2 = math.pi * (wind_turbine_diameter_m / 2) ** 2
                wind_theoretical_w = 0.5 * rho_air * wind_area_m2 * (climate['avg_wind_speed_ms'] ** 3) * self.WIND_EFFICIENCY
                wind_actual_w = min(wind_theoretical_w, wind_turbine_w)
            else:
                wind_actual_w = 0
            wind_daily_kwh = (wind_actual_w * 24) / 1000
            print(f"⚠️ Usando cálculo tradicional (ML no disponible)")
        
        solar_avg_power_w = (solar_daily_kwh * 1000) / 24
        wind_avg_power_w = (wind_daily_kwh * 1000) / 24
        
        # === TOTAL ===
        total_daily_kwh = solar_daily_kwh + wind_daily_kwh
        avg_power_w = (total_daily_kwh * 1000) / 24
        max_power_w = solar_panel_w + wind_turbine_w
        
        # === AUTONOMÍA ===
        autonomy_hours = battery_capacity_wh / avg_power_w if avg_power_w > 0 else 0
        
        return {
            'status': 'success',
            'mode': 'resources',
            'input': {
                'solar_panel_w': solar_panel_w,
                'wind_turbine_w': wind_turbine_w,
                'battery_capacity_wh': battery_capacity_wh,
                'latitude': latitude,
                'longitude': longitude
            },
            'climate': climate,
            'solar_generation': {
                'daily_kwh': round(solar_daily_kwh, 2),
                'avg_power_w': round(solar_avg_power_w),
                'peak_power_w': solar_panel_w
            },
            'wind_generation': {
                'daily_kwh': round(wind_daily_kwh, 2),
                'avg_power_w': round(wind_avg_power_w),
                'peak_power_w': wind_turbine_w
            },
            'total': {
                'daily_generation_kwh': round(total_daily_kwh, 2),
                'monthly_generation_kwh': round(total_daily_kwh * 30, 2),
                'avg_power_w': round(avg_power_w),
                'max_power_w': round(max_power_w)
            },
            'battery': {
                'capacity_wh': battery_capacity_wh,
                'autonomy_hours': round(autonomy_hours, 1),
                'autonomy_days': round(autonomy_hours / 24, 2)
            }
        }


# Instancia global
recommendation_service = RecommendationService()
