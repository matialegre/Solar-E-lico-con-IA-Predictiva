"""
Sistema de aprendizaje de patrones de consumo
Aprende cuándo se encienden electrodomésticos y optimiza la carga de batería
"""
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from collections import defaultdict
import statistics
import json

class ConsumptionPattern:
    """Representa un patrón de consumo detectado"""
    def __init__(self, hour: int, avg_power_w: float, frequency: float):
        self.hour = hour
        self.avg_power_w = avg_power_w
        self.frequency = frequency  # 0-1, qué tan seguido ocurre
        self.device_name = self._identify_device(avg_power_w)
    
    def _identify_device(self, power_w: float) -> str:
        """Identifica el electrodoméstico basándose en el consumo"""
        if power_w < 100:
            return "dispositivos_standby"
        elif power_w < 200:
            return "iluminación"
        elif 200 <= power_w < 400:
            return "heladera_compresor"
        elif 400 <= power_w < 800:
            return "lavarropas"
        elif 800 <= power_w < 1500:
            return "microondas"
        elif 1500 <= power_w < 2500:
            return "aire_acondicionado"
        else:
            return "calefactor_horno"


class PatternLearner:
    """
    Aprende patrones de consumo de la casa
    """
    def __init__(self, learning_days: int = 30):
        self.learning_days = learning_days
        self.consumption_history: List[Dict] = []
        self.patterns: Dict[int, ConsumptionPattern] = {}
        self.peak_hours: List[int] = []
        self.low_hours: List[int] = []
        
    def add_consumption_record(self, timestamp: datetime, power_w: float):
        """Agrega un registro de consumo al historial"""
        self.consumption_history.append({
            'timestamp': timestamp,
            'power_w': power_w,
            'hour': timestamp.hour,
            'day_of_week': timestamp.weekday(),
            'is_weekend': timestamp.weekday() >= 5
        })
        
        # Mantener solo los últimos N días
        cutoff_date = datetime.now() - timedelta(days=self.learning_days)
        self.consumption_history = [
            r for r in self.consumption_history 
            if r['timestamp'] > cutoff_date
        ]
    
    def analyze_patterns(self) -> Dict:
        """
        Analiza el historial y detecta patrones
        """
        if len(self.consumption_history) < 24:  # Necesitamos al menos 24 horas de datos
            return {
                'status': 'insufficient_data',
                'records': len(self.consumption_history),
                'patterns': []
            }
        
        # Agrupar por hora del día
        hourly_consumption = defaultdict(list)
        for record in self.consumption_history:
            hourly_consumption[record['hour']].append(record['power_w'])
        
        # Calcular estadísticas por hora
        patterns_list = []
        for hour in range(24):
            if hour in hourly_consumption:
                consumptions = hourly_consumption[hour]
                avg_power = statistics.mean(consumptions)
                frequency = len(consumptions) / self.learning_days
                
                pattern = ConsumptionPattern(hour, avg_power, frequency)
                self.patterns[hour] = pattern
                
                patterns_list.append({
                    'hour': hour,
                    'avg_power_w': round(avg_power, 1),
                    'min_power_w': round(min(consumptions), 1),
                    'max_power_w': round(max(consumptions), 1),
                    'frequency': round(frequency, 2),
                    'identified_device': pattern.device_name,
                    'samples': len(consumptions)
                })
        
        # Detectar horas pico y valle
        sorted_by_power = sorted(patterns_list, key=lambda x: x['avg_power_w'])
        self.low_hours = [p['hour'] for p in sorted_by_power[:6]]  # 6 horas más bajas
        self.peak_hours = [p['hour'] for p in sorted_by_power[-6:]]  # 6 horas más altas
        
        # Calcular consumo total diario promedio
        all_powers = [r['power_w'] for r in self.consumption_history]
        avg_daily_consumption = statistics.mean(all_powers) * 24 if all_powers else 0
        
        return {
            'status': 'success',
            'records': len(self.consumption_history),
            'days_analyzed': min(self.learning_days, len(self.consumption_history) / 24),
            'patterns': patterns_list,
            'peak_hours': sorted(self.peak_hours),
            'low_hours': sorted(self.low_hours),
            'avg_daily_consumption_wh': round(avg_daily_consumption, 0),
            'avg_power_w': round(statistics.mean(all_powers), 1) if all_powers else 0
        }
    
    def predict_next_hours(self, hours_ahead: int = 4) -> List[Dict]:
        """
        Predice el consumo de las próximas horas basándose en patrones
        """
        now = datetime.now()
        predictions = []
        
        for i in range(hours_ahead):
            future_hour = (now.hour + i) % 24
            
            if future_hour in self.patterns:
                pattern = self.patterns[future_hour]
                predictions.append({
                    'hour': future_hour,
                    'predicted_power_w': round(pattern.avg_power_w, 1),
                    'device': pattern.device_name,
                    'confidence': round(pattern.frequency * 100, 1)
                })
            else:
                # Si no hay datos, usar promedio general
                predictions.append({
                    'hour': future_hour,
                    'predicted_power_w': 500,  # Valor por defecto
                    'device': 'unknown',
                    'confidence': 0
                })
        
        return predictions
    
    def get_battery_charging_recommendation(self) -> Dict:
        """
        Recomienda cuándo cargar la batería basándose en patrones aprendidos
        """
        if not self.patterns:
            return {
                'status': 'no_patterns',
                'recommendation': 'Cargar durante horas de máxima generación'
            }
        
        current_hour = datetime.now().hour
        
        # Verificar si la próxima hora es de alto consumo
        next_peak_hours = [h for h in self.peak_hours if h > current_hour]
        if not next_peak_hours:
            next_peak_hours = self.peak_hours  # Wrap around
        
        next_peak = min(next_peak_hours) if next_peak_hours else current_hour
        hours_to_peak = (next_peak - current_hour) % 24
        
        # Si estamos en horas de bajo consumo y falta poco para pico, cargar
        should_charge = (current_hour in self.low_hours and hours_to_peak <= 2)
        
        return {
            'status': 'success',
            'current_hour': current_hour,
            'next_peak_hour': next_peak,
            'hours_to_peak': hours_to_peak,
            'should_charge_now': should_charge,
            'recommendation': self._get_recommendation_text(current_hour, next_peak, should_charge),
            'peak_hours_today': self.peak_hours,
            'low_hours_today': self.low_hours
        }
    
    def _get_recommendation_text(self, current_hour: int, next_peak: int, should_charge: bool) -> str:
        """Genera texto de recomendación"""
        if should_charge:
            return f"⚡ Cargar batería ahora. Pico de consumo en {next_peak}:00 hrs"
        elif current_hour in self.peak_hours:
            return f"⏸️ Hora pico. Usar batería si es necesario"
        elif current_hour in self.low_hours:
            return f"✅ Hora valle. Buen momento para cargar batería"
        else:
            return f"⏳ Próximo pico a las {next_peak}:00 hrs. Preparar carga"
    
    def detect_appliance_event(self, current_power_w: float, previous_power_w: float, threshold_w: float = 150) -> Optional[Dict]:
        """
        Detecta cuando se enciende un electrodoméstico
        (aumento súbito de consumo)
        """
        power_increase = current_power_w - previous_power_w
        
        if power_increase >= threshold_w:
            device_name = ConsumptionPattern(0, power_increase, 0)._identify_device(power_increase)
            
            return {
                'event': 'appliance_turned_on',
                'power_increase_w': round(power_increase, 1),
                'identified_device': device_name,
                'current_total_w': round(current_power_w, 1),
                'timestamp': datetime.now().isoformat(),
                'recommendation': f"Electrodoméstico detectado: {device_name}. Considerar usar batería."
            }
        
        return None


# Instancia global
pattern_learner = PatternLearner(learning_days=30)
