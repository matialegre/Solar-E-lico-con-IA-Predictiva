from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
from config import get_settings
from ai_predictor import energy_predictor
from weather_service import weather_service
import math

settings = get_settings()


class InverterController:
    """
    Controlador inteligente del inversor híbrido
    Toma decisiones basadas en IA y estado del sistema
    """
    
    def __init__(self):
        self.auto_mode = True
        self.current_source = "battery"
        self.priority_list = ["solar", "wind", "battery", "grid"]
        
        # Estado actual
        self.current_state = {
            'solar_power_w': 0.0,
            'wind_power_w': 0.0,
            'battery_soc_percent': 50.0,
            'battery_power_w': 0.0,
            'load_power_w': 500.0,
            'grid_available': False,
        }
        
        # Histórico de consumo para calcular promedio
        self.consumption_history = []
        self.max_history_size = 100
    
    def update_state(self, sensor_data: Dict):
        """Actualizar estado del sistema con datos de sensores"""
        
        self.current_state.update({
            'solar_power_w': sensor_data.get('solar_power_w', 0.0),
            'wind_power_w': sensor_data.get('wind_power_w', 0.0),
            'battery_soc_percent': sensor_data.get('battery_soc_percent', 50.0),
            'battery_power_w': sensor_data.get('battery_power_w', 0.0),
            'load_power_w': sensor_data.get('load_power_w', 500.0),
            'grid_available': sensor_data.get('grid_available', False),
        })
        
        # Agregar al histórico de consumo
        self.consumption_history.append({
            'timestamp': datetime.now(),
            'consumption_w': self.current_state['load_power_w']
        })
        
        # Mantener tamaño limitado
        if len(self.consumption_history) > self.max_history_size:
            self.consumption_history.pop(0)
    
    def get_average_consumption(self, hours: int = 1) -> float:
        """Calcular consumo promedio en las últimas N horas"""
        
        if not self.consumption_history:
            return self.current_state['load_power_w']
        
        cutoff_time = datetime.now() - timedelta(hours=hours)
        recent = [
            item['consumption_w'] 
            for item in self.consumption_history 
            if item['timestamp'] > cutoff_time
        ]
        
        if not recent:
            return self.current_state['load_power_w']
        
        return sum(recent) / len(recent)
    
    def calculate_autonomy(self) -> float:
        """
        Calcular autonomía restante (horas) con consumo actual
        """
        
        battery_soc = self.current_state['battery_soc_percent']
        battery_capacity_wh = settings.battery_capacity_wh
        min_soc = settings.min_battery_soc
        
        # Energía disponible en batería
        usable_soc = max(0, battery_soc - min_soc)
        available_energy_wh = (usable_soc / 100.0) * battery_capacity_wh
        
        # Consumo actual
        current_consumption_w = self.current_state['load_power_w']
        
        if current_consumption_w <= 0:
            return float('inf')
        
        # Horas disponibles
        autonomy_hours = available_energy_wh / current_consumption_w
        
        return autonomy_hours
    
    def make_decision(self) -> Dict:
        """
        Tomar decisión inteligente sobre qué fuente utilizar
        Retorna: {
            'selected_source': str,
            'reason': str,
            'actions': List[str],
            'priority_level': int
        }
        """
        
        if not self.auto_mode:
            return {
                'selected_source': self.current_source,
                'reason': 'Modo manual activo',
                'actions': [],
                'priority_level': 0
            }
        
        solar = self.current_state['solar_power_w']
        wind = self.current_state['wind_power_w']
        battery_soc = self.current_state['battery_soc_percent']
        load = self.current_state['load_power_w']
        
        total_renewable = solar + wind
        
        decision = {
            'selected_source': 'battery',
            'reason': '',
            'actions': [],
            'priority_level': 0
        }
        
        # Nivel crítico de batería
        if battery_soc < settings.min_battery_soc:
            decision['priority_level'] = 3  # Crítico
            decision['reason'] = f'Batería crítica ({battery_soc:.1f}%), buscar fuente alternativa'
            
            if total_renewable > load:
                decision['selected_source'] = 'solar' if solar > wind else 'wind'
                decision['actions'].append('Usar renovable y cargar batería')
            elif self.current_state['grid_available']:
                decision['selected_source'] = 'grid'
                decision['actions'].append('Usar red eléctrica y cargar batería')
            else:
                decision['selected_source'] = 'battery'
                decision['actions'].append('⚠️ ALERTA: Batería crítica sin alternativa')
                decision['actions'].append('Reducir consumo inmediatamente')
        
        # Batería baja
        elif battery_soc < 30:
            decision['priority_level'] = 2  # Alta
            decision['reason'] = f'Batería baja ({battery_soc:.1f}%), priorizar renovables'
            
            if total_renewable > load * 0.5:
                decision['selected_source'] = 'solar' if solar > wind else 'wind'
                decision['actions'].append('Usar renovable disponible')
            else:
                decision['selected_source'] = 'battery'
                decision['actions'].append('Minimizar uso de batería')
        
        # Exceso de renovables
        elif total_renewable > load * 1.5 and battery_soc < settings.max_battery_soc:
            decision['priority_level'] = 0  # Info
            decision['selected_source'] = 'solar' if solar > wind else 'wind'
            decision['reason'] = f'Exceso renovable, cargar batería (SoC: {battery_soc:.1f}%)'
            decision['actions'].append('Cargar batería con excedente')
        
        # Renovables suficientes
        elif total_renewable >= load:
            decision['priority_level'] = 0  # Info
            decision['selected_source'] = 'solar' if solar > wind else 'wind'
            decision['reason'] = f'Renovables suficientes ({total_renewable:.0f}W)'
            decision['actions'].append('Usar energía renovable')
            
            if battery_soc < 80:
                decision['actions'].append('Posible carga de batería')
        
        # Batería normal
        else:
            decision['priority_level'] = 1  # Normal
            decision['selected_source'] = 'battery'
            decision['reason'] = f'Renovables insuficientes, usar batería (SoC: {battery_soc:.1f}%)'
            
            autonomy = self.calculate_autonomy()
            decision['actions'].append(f'Autonomía estimada: {autonomy:.1f} horas')
        
        return decision
    
    def predict_energy_balance_24h(self) -> Dict:
        """
        Predecir balance energético para las próximas 24 horas
        """
        
        # Obtener pronóstico meteorológico
        weather_forecast = weather_service.get_hourly_forecast_24h()
        
        # Obtener predicciones de IA
        current_consumption = self.get_average_consumption(hours=1)
        predictions = energy_predictor.predict_24h(weather_forecast, current_consumption)
        
        # Calcular totales
        total_solar = sum(p['predicted_solar_w'] for p in predictions)
        total_wind = sum(p['predicted_wind_w'] for p in predictions)
        total_consumption = sum(p['predicted_consumption_w'] for p in predictions)
        
        total_generation = total_solar + total_wind
        
        # Balance
        balance_wh = total_generation - total_consumption
        
        # Simular evolución de batería
        battery_soc = self.current_state['battery_soc_percent']
        battery_capacity_wh = settings.battery_capacity_wh
        
        hourly_soc = [battery_soc]
        deficit_hours = []
        
        for i, pred in enumerate(predictions):
            generation = pred['predicted_solar_w'] + pred['predicted_wind_w']
            consumption = pred['predicted_consumption_w']
            
            net_power = generation - consumption
            
            # Cambio en Wh (1 hora)
            energy_change_wh = net_power
            
            # Cambio en SoC
            soc_change = (energy_change_wh / battery_capacity_wh) * 100
            
            new_soc = battery_soc + soc_change
            new_soc = max(settings.min_battery_soc, min(settings.max_battery_soc, new_soc))
            
            battery_soc = new_soc
            hourly_soc.append(battery_soc)
            
            # Detectar déficit (batería cerca del mínimo)
            if battery_soc < settings.min_battery_soc + 10:
                deficit_hours.append(i)
        
        # Calcular autonomía al final del período
        final_soc = hourly_soc[-1]
        usable_soc = max(0, final_soc - settings.min_battery_soc)
        available_energy_wh = (usable_soc / 100.0) * battery_capacity_wh
        
        avg_consumption = total_consumption / 24
        autonomy_hours = available_energy_wh / avg_consumption if avg_consumption > 0 else float('inf')
        
        return {
            'predictions': predictions,
            'total_solar_24h_wh': total_solar,
            'total_wind_24h_wh': total_wind,
            'total_generation_24h_wh': total_generation,
            'total_consumption_24h_wh': total_consumption,
            'balance_24h_wh': balance_wh,
            'final_battery_soc': final_soc,
            'autonomy_hours': autonomy_hours,
            'deficit_hours': deficit_hours,
            'hourly_soc_evolution': hourly_soc,
        }
    
    def check_alerts(self) -> List[Dict]:
        """Verificar y generar alertas"""
        
        alerts = []
        battery_soc = self.current_state['battery_soc_percent']
        autonomy = self.calculate_autonomy()
        
        # Alerta batería crítica
        if battery_soc < settings.min_battery_soc:
            alerts.append({
                'type': 'battery_critical',
                'severity': 'critical',
                'message': f'Batería en nivel crítico: {battery_soc:.1f}%',
                'action': 'Activar fuente alternativa inmediatamente'
            })
        
        # Alerta batería baja
        elif battery_soc < 30:
            alerts.append({
                'type': 'battery_low',
                'severity': 'warning',
                'message': f'Batería baja: {battery_soc:.1f}%',
                'action': 'Considerar reducir consumo o activar generador'
            })
        
        # Alerta autonomía baja
        if autonomy < 2 and autonomy != float('inf'):
            alerts.append({
                'type': 'low_autonomy',
                'severity': 'warning',
                'message': f'Autonomía reducida: {autonomy:.1f} horas',
                'action': 'Reducir consumo no esencial'
            })
        
        # Verificar predicción 24h
        prediction_24h = self.predict_energy_balance_24h()
        
        if prediction_24h['deficit_hours']:
            hours_count = len(prediction_24h['deficit_hours'])
            alerts.append({
                'type': 'predicted_deficit',
                'severity': 'info',
                'message': f'Déficit energético previsto en {hours_count} horas de las próximas 24h',
                'action': 'Planificar uso eficiente de energía'
            })
        
        return alerts
    
    def set_manual_control(self, source: str, enabled: bool):
        """Control manual de fuente"""
        self.auto_mode = False
        self.current_source = source
        return {
            'success': True,
            'message': f'Modo manual activado: {source} {"habilitado" if enabled else "deshabilitado"}'
        }
    
    def set_auto_mode(self, enabled: bool):
        """Activar/desactivar modo automático"""
        self.auto_mode = enabled
        return {
            'success': True,
            'message': f'Modo automático {"activado" if enabled else "desactivado"}'
        }


# Instancia global del controlador
inverter_controller = InverterController()
