"""
Calculador de dimensionamiento del sistema híbrido
Calcula cuántos paneles solares y turbinas eólicas se necesitan
basándose en consumo, ubicación geográfica y datos meteorológicos
"""
import math
from typing import Dict
from datetime import datetime

class SystemCalculator:
    def __init__(self, latitude: float, longitude: float):
        self.latitude = latitude
        self.longitude = longitude
        
    def calculate_system_requirements(
        self,
        average_consumption_w: float,
        battery_capacity_wh: float,
        avg_solar_radiation_kwh_m2: float = 5.0,
        avg_wind_speed_ms: float = 6.0,
        autonomy_days: float = 2.0
    ) -> Dict:
        """
        Calcula los requerimientos del sistema híbrido
        
        Args:
            average_consumption_w: Consumo promedio de la casa en watts
            battery_capacity_wh: Capacidad de batería en Wh
            avg_solar_radiation_kwh_m2: Radiación solar promedio diaria (kWh/m²/día)
            avg_wind_speed_ms: Velocidad de viento promedio (m/s)
            autonomy_days: Días de autonomía deseados
            
        Returns:
            Dict con especificaciones del sistema
        """
        
        # Consumo diario (Wh/día)
        daily_consumption_wh = average_consumption_w * 24
        
        # ===== CÁLCULO SOLAR =====
        # Horas de sol pico efectivas basadas en latitud
        peak_sun_hours = self._calculate_peak_sun_hours(avg_solar_radiation_kwh_m2)
        
        # Potencia solar necesaria considerando eficiencia (17%) y pérdidas (20%)
        solar_efficiency = 0.17
        system_losses = 0.80  # 20% de pérdidas
        
        # Potencia solar pico necesaria (W)
        required_solar_w = (daily_consumption_wh * 0.6) / (peak_sun_hours * solar_efficiency * system_losses)
        
        # Cantidad de paneles (asumiendo paneles de 300W)
        panel_wattage = 300
        solar_panels_needed = math.ceil(required_solar_w / panel_wattage)
        actual_solar_power_w = solar_panels_needed * panel_wattage
        
        # ===== CÁLCULO EÓLICO =====
        # Factor de capacidad basado en velocidad del viento
        wind_capacity_factor = self._calculate_wind_capacity_factor(avg_wind_speed_ms)
        
        # Potencia eólica necesaria para cubrir el 40% del consumo
        required_wind_w = (daily_consumption_wh * 0.4) / (24 * wind_capacity_factor)
        
        # Cantidad de turbinas (asumiendo turbinas de 1000W)
        turbine_wattage = 1000
        wind_turbines_needed = math.ceil(required_wind_w / turbine_wattage)
        actual_wind_power_w = wind_turbines_needed * turbine_wattage
        
        # ===== BATERÍA =====
        # Capacidad de batería requerida (Wh) para autonomía
        required_battery_wh = daily_consumption_wh * autonomy_days
        
        # Considerando DoD (Depth of Discharge) del 80%
        dod = 0.80
        recommended_battery_wh = required_battery_wh / dod
        
        # Voltaje recomendado del sistema
        if recommended_battery_wh < 5000:
            system_voltage = 24
        elif recommended_battery_wh < 15000:
            system_voltage = 48
        else:
            system_voltage = 96
            
        battery_ah = recommended_battery_wh / system_voltage
        
        # ===== GENERACIÓN ESTIMADA =====
        # Generación solar diaria (Wh)
        solar_generation_wh = actual_solar_power_w * peak_sun_hours * solar_efficiency * system_losses
        
        # Generación eólica diaria (Wh)
        wind_generation_wh = actual_wind_power_w * 24 * wind_capacity_factor
        
        # Total generación
        total_generation_wh = solar_generation_wh + wind_generation_wh
        
        # Balance energético
        energy_balance_wh = total_generation_wh - daily_consumption_wh
        energy_balance_percent = (energy_balance_wh / daily_consumption_wh) * 100
        
        # ===== OPTIMIZACIÓN POR UBICACIÓN =====
        optimization = self._optimize_by_location(
            self.latitude,
            avg_solar_radiation_kwh_m2,
            avg_wind_speed_ms
        )
        
        return {
            "consumption": {
                "average_power_w": average_consumption_w,
                "daily_consumption_wh": daily_consumption_wh,
                "monthly_consumption_kwh": round(daily_consumption_wh * 30 / 1000, 1)
            },
            "solar": {
                "panels_needed": solar_panels_needed,
                "panel_wattage_w": panel_wattage,
                "total_capacity_w": actual_solar_power_w,
                "peak_sun_hours": round(peak_sun_hours, 1),
                "daily_generation_wh": round(solar_generation_wh, 0),
                "daily_generation_kwh": round(solar_generation_wh / 1000, 2),
                "coverage_percent": round((solar_generation_wh / daily_consumption_wh) * 100, 1)
            },
            "wind": {
                "turbines_needed": wind_turbines_needed,
                "turbine_wattage_w": turbine_wattage,
                "total_capacity_w": actual_wind_power_w,
                "avg_wind_speed_ms": avg_wind_speed_ms,
                "capacity_factor": round(wind_capacity_factor * 100, 1),
                "daily_generation_wh": round(wind_generation_wh, 0),
                "daily_generation_kwh": round(wind_generation_wh / 1000, 2),
                "coverage_percent": round((wind_generation_wh / daily_consumption_wh) * 100, 1)
            },
            "battery": {
                "current_capacity_wh": battery_capacity_wh,
                "recommended_capacity_wh": round(recommended_battery_wh, 0),
                "recommended_capacity_kwh": round(recommended_battery_wh / 1000, 1),
                "system_voltage_v": system_voltage,
                "capacity_ah": round(battery_ah, 0),
                "autonomy_days": autonomy_days,
                "needs_upgrade": battery_capacity_wh < recommended_battery_wh
            },
            "generation": {
                "total_daily_wh": round(total_generation_wh, 0),
                "total_daily_kwh": round(total_generation_wh / 1000, 2),
                "balance_wh": round(energy_balance_wh, 0),
                "balance_percent": round(energy_balance_percent, 1),
                "is_sufficient": energy_balance_wh >= 0,
                "solar_percent": round((solar_generation_wh / total_generation_wh) * 100, 1),
                "wind_percent": round((wind_generation_wh / total_generation_wh) * 100, 1)
            },
            "optimization": optimization,
            "location": {
                "latitude": self.latitude,
                "longitude": self.longitude
            }
        }
    
    def _calculate_peak_sun_hours(self, avg_radiation_kwh_m2: float) -> float:
        """
        Calcula las horas de sol pico basándose en la radiación promedio
        """
        # La radiación en kWh/m²/día se puede interpretar como horas de sol pico
        # ya que 1 kWh/m² = 1 hora de sol a 1000 W/m²
        return avg_radiation_kwh_m2
    
    def _calculate_wind_capacity_factor(self, avg_wind_speed_ms: float) -> float:
        """
        Calcula el factor de capacidad de la turbina eólica
        basándose en la velocidad promedio del viento
        
        Turbinas pequeñas típicas:
        - Cut-in: 3.5 m/s
        - Rated: 12 m/s
        - Cut-out: 25 m/s
        """
        if avg_wind_speed_ms < 3.5:
            return 0.0
        elif avg_wind_speed_ms < 12:
            # Factor cúbico normalizado
            return min(0.35 * pow(avg_wind_speed_ms / 12, 3), 0.35)
        else:
            return 0.35  # Factor de capacidad típico máximo para turbinas pequeñas
    
    def _optimize_by_location(
        self,
        latitude: float,
        solar_radiation: float,
        wind_speed: float
    ) -> Dict:
        """
        Optimiza la proporción solar/eólico basándose en la ubicación geográfica
        """
        # Determinar hemisferio
        hemisphere = "sur" if latitude < 0 else "norte"
        
        # Ángulo óptimo de paneles = latitud del lugar
        optimal_panel_angle = abs(latitude)
        
        # Evaluar potencial solar vs eólico
        solar_potential = solar_radiation  # kWh/m²/día
        wind_potential = wind_speed  # m/s
        
        # Determinar mejor fuente
        if solar_potential > 5.5 and wind_potential < 5:
            recommendation = "solar"
            priority = "Priorizar energía solar (excelente radiación)"
        elif wind_potential > 7 and solar_potential < 4:
            recommendation = "wind"
            priority = "Priorizar energía eólica (excelente viento)"
        else:
            recommendation = "hybrid"
            priority = "Sistema híbrido balanceado (buena radiación y viento)"
        
        return {
            "hemisphere": hemisphere,
            "optimal_panel_angle_degrees": round(optimal_panel_angle, 1),
            "solar_potential_rating": self._rate_potential(solar_potential, [3, 4, 5, 6]),
            "wind_potential_rating": self._rate_potential(wind_potential, [3, 5, 7, 9]),
            "recommended_priority": recommendation,
            "recommendation_text": priority,
            "latitude_zone": self._get_latitude_zone(latitude)
        }
    
    def _rate_potential(self, value: float, thresholds: list) -> str:
        """Clasifica el potencial en: bajo, regular, bueno, excelente"""
        if value < thresholds[0]:
            return "bajo"
        elif value < thresholds[1]:
            return "regular"
        elif value < thresholds[2]:
            return "bueno"
        elif value < thresholds[3]:
            return "muy bueno"
        else:
            return "excelente"
    
    def _get_latitude_zone(self, latitude: float) -> str:
        """Determina la zona climática basada en latitud"""
        abs_lat = abs(latitude)
        if abs_lat < 23.5:
            return "tropical"
        elif abs_lat < 35:
            return "subtropical"
        elif abs_lat < 50:
            return "templada"
        else:
            return "fría"


# Instancia global
system_calculator = None

def get_system_calculator(latitude: float, longitude: float) -> SystemCalculator:
    """Obtiene o crea una instancia del calculador"""
    global system_calculator
    if system_calculator is None:
        system_calculator = SystemCalculator(latitude, longitude)
    return system_calculator
