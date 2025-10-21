"""
Sistema de Protección contra Embalamiento de Turbina Eólica
Monitorea velocidad/voltaje y activa resistencia de frenado automáticamente
"""
from datetime import datetime
from typing import Dict, Optional
import math

class WindProtectionSystem:
    """
    Sistema de seguridad para prevenir daños por embalamiento de turbina eólica
    """
    
    def __init__(
        self,
        max_wind_speed_ms: float = 25.0,  # Velocidad de viento cut-out
        max_rpm: float = 500,  # RPM máximo antes de embalamiento
        max_voltage: float = 65,  # Voltaje máximo antes de daño
        brake_resistor_ohms: float = 10.0,  # Resistencia de frenado (Ohms)
        brake_resistor_watts: float = 2000.0  # Potencia de resistencia
    ):
        self.max_wind_speed_ms = max_wind_speed_ms
        self.max_rpm = max_rpm
        self.max_voltage = max_voltage
        self.brake_resistor_ohms = brake_resistor_ohms
        self.brake_resistor_watts = brake_resistor_watts
        
        # Estado del sistema
        self.brake_active = False
        self.turbine_connected = True
        self.protection_triggered = False
        self.last_trigger_time = None
        self.trigger_reason = None
        
        # Umbrales de advertencia (90% del máximo)
        self.warning_wind_speed = max_wind_speed_ms * 0.9
        self.warning_rpm = max_rpm * 0.9
        self.warning_voltage = max_voltage * 0.9
        
    def check_overspeed_conditions(
        self,
        current_wind_speed_ms: float,
        current_voltage: float,
        current_rpm: Optional[float] = None
    ) -> Dict:
        """
        Verifica condiciones de embalamiento y activa protección si es necesario
        
        Returns:
            Dict con estado de protección y acciones tomadas
        """
        
        danger_level = "normal"
        warnings = []
        actions_taken = []
        should_activate_brake = False
        reason = None
        
        # === VERIFICAR VELOCIDAD DE VIENTO ===
        if current_wind_speed_ms >= self.max_wind_speed_ms:
            danger_level = "critical"
            should_activate_brake = True
            reason = f"Velocidad de viento crítica: {current_wind_speed_ms:.1f} m/s (máx: {self.max_wind_speed_ms})"
            warnings.append("⚠️ VIENTO EXCESIVO - Activando protección")
            
        elif current_wind_speed_ms >= self.warning_wind_speed:
            danger_level = "warning"
            warnings.append(f"⚡ Viento alto: {current_wind_speed_ms:.1f} m/s")
        
        # === VERIFICAR VOLTAJE ===
        if current_voltage >= self.max_voltage:
            danger_level = "critical"
            should_activate_brake = True
            reason = f"Sobrevoltaje crítico: {current_voltage:.1f}V (máx: {self.max_voltage}V)"
            warnings.append("⚠️ SOBREVOLTAJE - Activando protección")
            
        elif current_voltage >= self.warning_voltage:
            if danger_level != "critical":
                danger_level = "warning"
            warnings.append(f"⚡ Voltaje alto: {current_voltage:.1f}V")
        
        # === VERIFICAR RPM (si está disponible) ===
        if current_rpm is not None:
            if current_rpm >= self.max_rpm:
                danger_level = "critical"
                should_activate_brake = True
                reason = f"RPM crítico: {current_rpm:.0f} RPM (máx: {self.max_rpm})"
                warnings.append("⚠️ EMBALAMIENTO DETECTADO - Activando protección")
                
            elif current_rpm >= self.warning_rpm:
                if danger_level != "critical":
                    danger_level = "warning"
                warnings.append(f"⚡ RPM alto: {current_rpm:.0f}")
        
        # === ACTIVAR PROTECCIÓN SI ES NECESARIO ===
        if should_activate_brake and not self.brake_active:
            self._activate_brake_resistor(reason)
            actions_taken.append("🛑 Turbina DESCONECTADA del sistema")
            actions_taken.append("⚡ Resistencia de frenado ACTIVADA")
            actions_taken.append(f"🔥 Disipando energía: {self._calculate_brake_power(current_voltage):.0f}W")
            
        elif self.brake_active and danger_level == "normal":
            # Condiciones normales - desactivar freno
            self._deactivate_brake_resistor()
            actions_taken.append("✅ Protección desactivada - Condiciones normales")
            actions_taken.append("🔌 Turbina RECONECTADA al sistema")
        
        return {
            'status': 'active' if self.brake_active else 'normal',
            'danger_level': danger_level,
            'brake_active': self.brake_active,
            'turbine_connected': self.turbine_connected,
            'protection_triggered': self.protection_triggered,
            'trigger_reason': self.trigger_reason,
            'last_trigger': self.last_trigger_time.isoformat() if self.last_trigger_time else None,
            'warnings': warnings,
            'actions_taken': actions_taken,
            'metrics': {
                'wind_speed_ms': current_wind_speed_ms,
                'voltage_v': current_voltage,
                'rpm': current_rpm,
                'brake_power_w': self._calculate_brake_power(current_voltage) if self.brake_active else 0
            },
            'thresholds': {
                'max_wind_speed': self.max_wind_speed_ms,
                'max_voltage': self.max_voltage,
                'max_rpm': self.max_rpm,
                'warning_wind_speed': self.warning_wind_speed,
                'warning_voltage': self.warning_voltage,
                'warning_rpm': self.warning_rpm
            }
        }
    
    def _activate_brake_resistor(self, reason: str):
        """Activa la resistencia de frenado y desconecta turbina"""
        self.brake_active = True
        self.turbine_connected = False
        self.protection_triggered = True
        self.last_trigger_time = datetime.now()
        self.trigger_reason = reason
        
        print(f"\n🚨 PROTECCIÓN EÓLICA ACTIVADA 🚨")
        print(f"Razón: {reason}")
        print(f"Tiempo: {self.last_trigger_time}")
        print(f"Acciones:")
        print(f"  1. Relé turbina → ABIERTO (desconectada)")
        print(f"  2. Relé resistencia → CERRADO (frenando)")
        print(f"  3. Sistema → Solo solar + batería\n")
    
    def _deactivate_brake_resistor(self):
        """Desactiva la resistencia de frenado y reconecta turbina"""
        self.brake_active = False
        self.turbine_connected = True
        
        print(f"\n✅ PROTECCIÓN EÓLICA DESACTIVADA")
        print(f"Condiciones normales restablecidas")
        print(f"Turbina reconectada al sistema\n")
    
    def _calculate_brake_power(self, voltage: float) -> float:
        """
        Calcula la potencia disipada en la resistencia de frenado
        P = V² / R
        """
        return (voltage ** 2) / self.brake_resistor_ohms
    
    def manual_brake_activation(self, reason: str = "Activación manual"):
        """Permite activación manual del freno"""
        self._activate_brake_resistor(reason)
        return {
            'status': 'success',
            'message': 'Freno de emergencia activado manualmente',
            'brake_active': True
        }
    
    def manual_brake_deactivation(self):
        """Permite desactivación manual del freno (solo si condiciones son seguras)"""
        self._deactivate_brake_resistor()
        self.protection_triggered = False
        return {
            'status': 'success',
            'message': 'Freno desactivado manualmente',
            'brake_active': False,
            'warning': 'Asegúrate de que las condiciones sean seguras'
        }
    
    def get_brake_resistor_specs(self) -> Dict:
        """Retorna especificaciones de la resistencia de frenado"""
        return {
            'resistance_ohms': self.brake_resistor_ohms,
            'max_power_watts': self.brake_resistor_watts,
            'max_voltage_safe': math.sqrt(self.brake_resistor_watts * self.brake_resistor_ohms),
            'max_current_amps': math.sqrt(self.brake_resistor_watts / self.brake_resistor_ohms),
            'recommended_type': 'Resistencia de alambre, cerámica o rejilla de frenado',
            'mounting': 'Con disipador o ventilación forzada',
            'safety_note': 'ADVERTENCIA: Se calienta mucho durante operación'
        }
    
    def get_relay_configuration(self) -> Dict:
        """Retorna configuración de relés para protección eólica"""
        return {
            'relay_turbine': {
                'name': 'Relé Turbina Eólica',
                'function': 'Conecta/desconecta turbina del sistema',
                'normal_state': 'CERRADO (conectada)',
                'protection_state': 'ABIERTO (desconectada)',
                'rating': '30A, 250VAC',
                'gpio_pin': 'GPIO17'
            },
            'relay_brake': {
                'name': 'Relé Resistencia de Frenado',
                'function': 'Activa resistencia para disipar energía',
                'normal_state': 'ABIERTO (inactiva)',
                'protection_state': 'CERRADO (frenando)',
                'rating': '30A, 250VAC',
                'gpio_pin': 'GPIO23'
            },
            'interlock': 'Los relés son mutuamente excluyentes - nunca ambos cerrados'
        }


# Instancia global
wind_protection = WindProtectionSystem(
    max_wind_speed_ms=25.0,  # Cut-out típico de turbinas pequeñas
    max_rpm=500,
    max_voltage=65,  # Para sistema 48V
    brake_resistor_ohms=10.0,
    brake_resistor_watts=2000.0
)
