"""
Sistema de Protección y Optimización de Batería
Mantiene la batería en zona óptima (25-80%) para maximizar vida útil
Prioriza uso directo de renovables sobre batería
"""
from typing import Dict
from datetime import datetime

class BatteryProtectionSystem:
    """
    Protege la batería y optimiza su uso para máxima longevidad
    """
    
    def __init__(
        self,
        min_soc_optimal: float = 25.0,  # Mínimo óptimo (evitar descargas profundas)
        max_soc_optimal: float = 80.0,  # Máximo óptimo (evitar sobrecarga constante)
        critical_min_soc: float = 20.0,  # Crítico - cortar carga
        critical_max_soc: float = 95.0   # Crítico - cortar carga
    ):
        self.min_soc_optimal = min_soc_optimal
        self.max_soc_optimal = max_soc_optimal
        self.critical_min_soc = critical_min_soc
        self.critical_max_soc = critical_max_soc
        
        # Contadores para estadísticas
        self.cycles_in_optimal_zone = 0
        self.cycles_outside_optimal = 0
        self.deep_discharge_events = 0
        self.overcharge_events = 0
        
    def analyze_battery_strategy(
        self,
        battery_soc: float,
        solar_power_w: float,
        wind_power_w: float,
        load_power_w: float,
        battery_power_w: float
    ) -> Dict:
        """
        Analiza la estrategia óptima de uso de batería
        
        PRIORIDADES:
        1. Usar renovables DIRECTAMENTE para alimentar la casa
        2. Excedente → Batería (solo si está en zona óptima)
        3. Batería → Casa (solo si renovables no alcanzan)
        
        Returns:
            Dict con estrategia y recomendaciones
        """
        
        # Calcular fuentes
        total_renewables = solar_power_w + wind_power_w
        renewable_surplus = total_renewables - load_power_w
        
        # Estado de zona de batería
        in_optimal_zone = self.min_soc_optimal <= battery_soc <= self.max_soc_optimal
        is_low = battery_soc < self.min_soc_optimal
        is_high = battery_soc > self.max_soc_optimal
        is_critical_low = battery_soc < self.critical_min_soc
        is_critical_high = battery_soc > self.critical_max_soc
        
        # Determinar modo de operación
        if renewable_surplus > 50:  # Hay excedente
            mode = "charging_from_surplus"
            recommendation = "✅ Usando renovables directamente + cargando batería con excedente"
            should_charge = in_optimal_zone or is_low
            should_discharge = False
            
        elif renewable_surplus < -50:  # Falta energía
            mode = "supplementing_from_battery"
            recommendation = "⚠️ Complementando con batería (renovables insuficientes)"
            should_charge = False
            should_discharge = not is_critical_low
            
        else:  # Balance perfecto
            mode = "direct_renewable_use"
            recommendation = "🌱 Usando 100% renovables directamente (ideal)"
            should_charge = False
            should_discharge = False
        
        # Validaciones de seguridad
        if is_critical_low:
            recommendation = "🚨 BATERÍA CRÍTICA - Reducir consumo o activar red backup"
            should_discharge = False
            
        if is_critical_high:
            recommendation = "🚨 BATERÍA LLENA - Desviar excedente a resistencia o red"
            should_charge = False
        
        # Calcular cobertura de renovables
        renewable_coverage_percent = (total_renewables / load_power_w * 100) if load_power_w > 0 else 0
        
        # Calcular uso de batería vs renovables
        battery_usage_percent = (abs(battery_power_w) / load_power_w * 100) if load_power_w > 0 else 0
        
        # Actualizar contadores
        if in_optimal_zone:
            self.cycles_in_optimal_zone += 1
        else:
            self.cycles_outside_optimal += 1
            
        if is_critical_low:
            self.deep_discharge_events += 1
            
        if is_critical_high:
            self.overcharge_events += 1
        
        return {
            'status': 'success',
            'timestamp': datetime.now().isoformat(),
            'battery': {
                'soc_percent': battery_soc,
                'power_w': battery_power_w,
                'in_optimal_zone': in_optimal_zone,
                'zone': self._get_zone_name(battery_soc),
                'is_charging': battery_power_w > 0,
                'is_discharging': battery_power_w < 0
            },
            'mode': mode,
            'recommendation': recommendation,
            'should_charge': should_charge,
            'should_discharge': should_discharge,
            'sources': {
                'solar_w': solar_power_w,
                'wind_w': wind_power_w,
                'total_renewables_w': total_renewables,
                'load_w': load_power_w,
                'surplus_w': renewable_surplus
            },
            'coverage': {
                'renewable_coverage_percent': round(renewable_coverage_percent, 1),
                'battery_usage_percent': round(battery_usage_percent, 1),
                'direct_renewable_use': renewable_coverage_percent >= 90
            },
            'thresholds': {
                'optimal_min': self.min_soc_optimal,
                'optimal_max': self.max_soc_optimal,
                'critical_min': self.critical_min_soc,
                'critical_max': self.critical_max_soc
            },
            'statistics': {
                'cycles_in_optimal': self.cycles_in_optimal_zone,
                'cycles_outside_optimal': self.cycles_outside_optimal,
                'optimal_zone_percentage': round(
                    (self.cycles_in_optimal_zone / (self.cycles_in_optimal_zone + self.cycles_outside_optimal) * 100)
                    if (self.cycles_in_optimal_zone + self.cycles_outside_optimal) > 0 else 0,
                    1
                ),
                'deep_discharge_events': self.deep_discharge_events,
                'overcharge_events': self.overcharge_events
            },
            'health_impact': self._calculate_health_impact(in_optimal_zone, is_critical_low, is_critical_high)
        }
    
    def _get_zone_name(self, soc: float) -> str:
        """Retorna el nombre de la zona donde está la batería"""
        if soc < self.critical_min_soc:
            return "CRÍTICO - Muy bajo"
        elif soc < self.min_soc_optimal:
            return "BAJO - Fuera de zona óptima"
        elif soc <= self.max_soc_optimal:
            return "ÓPTIMO - Máxima vida útil"
        elif soc < self.critical_max_soc:
            return "ALTO - Fuera de zona óptima"
        else:
            return "CRÍTICO - Muy alto"
    
    def _calculate_health_impact(self, in_optimal: bool, critical_low: bool, critical_high: bool) -> Dict:
        """Calcula el impacto en la salud de la batería"""
        if critical_low or critical_high:
            impact = "ALTO - Daño acelerado"
            expected_life_years = 5
            estimated_cycles = 2000
        elif not in_optimal:
            impact = "MEDIO - Desgaste aumentado"
            expected_life_years = 8
            estimated_cycles = 4000
        else:
            impact = "BAJO - Máxima longevidad"
            expected_life_years = 15
            estimated_cycles = 6000
        
        return {
            'impact_level': impact,
            'expected_life_years': expected_life_years,
            'estimated_cycles_remaining': estimated_cycles,
            'recommendation': self._get_health_recommendation(in_optimal, critical_low, critical_high)
        }
    
    def _get_health_recommendation(self, in_optimal: bool, critical_low: bool, critical_high: bool) -> str:
        """Genera recomendación para salud de batería"""
        if critical_low:
            return "⚠️ URGENTE: Recargar batería inmediatamente. Daño permanente en progreso."
        elif critical_high:
            return "⚠️ URGENTE: Desviar carga. Sobrecarga reduce vida útil drásticamente."
        elif not in_optimal:
            return "💡 Mantener batería entre 25-80% extiende su vida útil hasta 3 veces más."
        else:
            return "✅ Operación ideal. Batería en zona óptima para máxima longevidad."
    
    def get_battery_life_projection(
        self,
        current_soc: float,
        daily_cycles: float = 1.0,
        battery_capacity_kwh: float = 5.0
    ) -> Dict:
        """
        Proyecta la vida útil de la batería basándose en uso actual
        """
        in_optimal = self.min_soc_optimal <= current_soc <= self.max_soc_optimal
        
        # Factores de degradación
        if in_optimal:
            degradation_factor = 1.0  # Degradación normal
            expected_cycles = 6000
        else:
            degradation_factor = 2.0  # Degradación duplicada
            expected_cycles = 3000
        
        # Proyección de vida
        years_at_current_usage = (expected_cycles / daily_cycles) / 365
        
        # Costo de reemplazo estimado
        replacement_cost_ars = battery_capacity_kwh * 76000  # ~$76k/kWh para LiFePO4
        
        # Ahorro por usar zona óptima
        if in_optimal:
            savings_ars = replacement_cost_ars  # Duplica la vida = ahorra un reemplazo
            extra_years = years_at_current_usage
        else:
            savings_ars = 0
            extra_years = 0
        
        return {
            'current_usage': {
                'in_optimal_zone': in_optimal,
                'daily_cycles': daily_cycles,
                'degradation_factor': degradation_factor
            },
            'projection': {
                'expected_total_cycles': expected_cycles,
                'years_at_current_usage': round(years_at_current_usage, 1),
                'calendar_life_estimate': '15-20 años' if in_optimal else '7-10 años'
            },
            'economics': {
                'battery_capacity_kwh': battery_capacity_kwh,
                'replacement_cost_ars': round(replacement_cost_ars, 0),
                'potential_savings_ars': round(savings_ars, 0),
                'extra_years_gained': round(extra_years, 1)
            },
            'recommendation': 'Mantener en zona 25-80% puede ahorrar hasta $' + f'{savings_ars:,.0f}' + ' en reemplazos'
        }


# Instancia global
battery_protection = BatteryProtectionSystem(
    min_soc_optimal=25.0,
    max_soc_optimal=80.0,
    critical_min_soc=20.0,
    critical_max_soc=95.0
)
