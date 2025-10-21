"""
Simulador de datos de energía y sensores
Permite probar el sistema sin hardware físico
"""

import random
import math
import time
import requests
from datetime import datetime
import schedule
import threading


class EnergySimulator:
    """Simula generación solar, eólica, batería y consumo"""
    
    def __init__(self, api_url: str = "http://localhost:8000"):
        self.api_url = api_url
        self.running = False
        
        # Estado de batería
        self.battery_voltage = 48.0  # Voltaje nominal 48V
        self.battery_soc = 75.0
        
        # Parámetros de simulación
        self.base_consumption = 500  # Watts base
        
    def get_solar_power(self) -> tuple:
        """Simular generación solar basada en hora del día"""
        
        hour = datetime.now().hour
        
        # Solar solo durante el día (6am - 8pm)
        if hour < 6 or hour > 20:
            return 0.0, 0.0
        
        # Curva sinusoidal para simular el día
        hour_factor = math.sin(math.pi * (hour - 6) / 14)
        
        # Potencia máxima 3000W al mediodía
        max_power = 3000
        base_power = max_power * hour_factor
        
        # Añadir variabilidad (nubes)
        noise = random.uniform(-0.2, 0.1)
        power = max(0, base_power * (1 + noise))
        
        # Calcular voltaje y corriente
        voltage = random.uniform(40, 60)
        current = power / voltage if voltage > 0 else 0
        
        return voltage, current
    
    def get_wind_power(self) -> tuple:
        """Simular generación eólica"""
        
        hour = datetime.now().hour
        
        # El viento es más fuerte en tarde/noche
        if 14 <= hour <= 23:
            wind_factor = 1.0
        elif 0 <= hour <= 6:
            wind_factor = 0.8
        else:
            wind_factor = 0.5
        
        # Potencia máxima 2000W
        max_power = 2000
        base_power = max_power * wind_factor
        
        # Variabilidad del viento
        noise = random.uniform(-0.3, 0.3)
        power = max(0, base_power * (1 + noise))
        
        # Calcular voltaje y corriente
        voltage = random.uniform(35, 55)
        current = power / voltage if voltage > 0 else 0
        
        return voltage, current
    
    def get_battery_state(self, solar_power: float, wind_power: float, 
                          load_power: float, dt: float = 1.0) -> tuple:
        """
        Simular estado de batería
        dt: tiempo transcurrido en horas
        """
        
        total_generation = solar_power + wind_power
        net_power = total_generation - load_power
        
        # Capacidad de batería (Wh)
        battery_capacity = 5000  # 5 kWh
        
        # Cambio en energía (Wh)
        energy_change = net_power * dt
        
        # Cambio en SoC (%)
        soc_change = (energy_change / battery_capacity) * 100
        
        # Actualizar SoC
        self.battery_soc += soc_change
        self.battery_soc = max(20, min(100, self.battery_soc))  # Limitar 20-100%
        
        # Voltaje varía con SoC (48V nominal, 44-54.6V rango)
        self.battery_voltage = 44 + (self.battery_soc - 20) / 80 * (54.6 - 44)
        
        # Corriente de batería (positiva=carga, negativa=descarga)
        battery_current = net_power / self.battery_voltage
        
        return self.battery_voltage, battery_current
    
    def get_load_consumption(self) -> float:
        """Simular consumo de carga"""
        
        hour = datetime.now().hour
        
        # Patrones de consumo realistas
        if 0 <= hour <= 6:
            # Noche: consumo bajo
            load_factor = 0.6
        elif 7 <= hour <= 9:
            # Mañana: pico de consumo
            load_factor = 1.2
        elif 10 <= hour <= 18:
            # Día: consumo medio
            load_factor = 0.9
        elif 19 <= hour <= 23:
            # Tarde/noche: pico de consumo
            load_factor = 1.3
        else:
            load_factor = 0.8
        
        consumption = self.base_consumption * load_factor
        
        # Añadir variabilidad
        noise = random.uniform(-0.1, 0.1)
        consumption *= (1 + noise)
        
        return max(0, consumption)
    
    def generate_sensor_data(self) -> dict:
        """Generar datos de sensores simulados"""
        
        # Generación solar
        solar_voltage, solar_current = self.get_solar_power()
        solar_power = solar_voltage * solar_current
        
        # Generación eólica
        wind_voltage, wind_current = self.get_wind_power()
        wind_power = wind_voltage * wind_current
        
        # Consumo
        load_power = self.get_load_consumption()
        load_current = load_power / self.battery_voltage
        
        # Estado de batería (actualizar cada 1 minuto = 1/60 hora)
        battery_voltage, battery_current = self.get_battery_state(
            solar_power, wind_power, load_power, dt=1/60
        )
        
        return {
            'solar_voltage_v': round(solar_voltage, 2),
            'solar_current_a': round(solar_current, 2),
            'wind_voltage_v': round(wind_voltage, 2),
            'wind_current_a': round(wind_current, 2),
            'battery_voltage_v': round(battery_voltage, 2),
            'battery_current_a': round(battery_current, 2),
            'load_current_a': round(load_current, 2),
            'temperature_c': round(20 + random.uniform(-5, 15), 1)
        }
    
    def send_data(self):
        """Enviar datos al servidor"""
        
        try:
            data = self.generate_sensor_data()
            
            response = requests.post(
                f"{self.api_url}/api/energy/record",
                json=data,
                timeout=5
            )
            
            if response.status_code == 200:
                print(f"✓ [{datetime.now().strftime('%H:%M:%S')}] "
                      f"Solar: {data['solar_voltage_v']*data['solar_current_a']:.0f}W | "
                      f"Viento: {data['wind_voltage_v']*data['wind_current_a']:.0f}W | "
                      f"Batería: {self.battery_soc:.1f}% | "
                      f"Consumo: {data['load_current_a']*data['battery_voltage_v']:.0f}W")
            else:
                print(f"✗ Error al enviar datos: {response.status_code}")
        
        except requests.exceptions.ConnectionError:
            print("✗ No se puede conectar al servidor. ¿Está ejecutándose?")
        except Exception as e:
            print(f"✗ Error: {e}")
    
    def start(self, interval_seconds: int = 10):
        """Iniciar simulación"""
        
        print("🔄 Iniciando simulador de energía...")
        print(f"📡 Enviando datos cada {interval_seconds} segundos")
        print(f"🔗 Servidor: {self.api_url}")
        print(f"🔋 Batería inicial: {self.battery_soc:.1f}%\n")
        
        self.running = True
        
        # Programar envío periódico
        schedule.every(interval_seconds).seconds.do(self.send_data)
        
        # Enviar primer dato inmediatamente
        self.send_data()
        
        # Loop principal
        try:
            while self.running:
                schedule.run_pending()
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n⏹️ Simulación detenida por usuario")
            self.running = False
    
    def stop(self):
        """Detener simulación"""
        self.running = False


class ScenarioSimulator:
    """Simula escenarios específicos"""
    
    @staticmethod
    def simulate_cloudy_day():
        """Día nublado - poca generación solar"""
        print("☁️ Simulando día nublado...")
        # Implementar
    
    @staticmethod
    def simulate_high_consumption():
        """Alto consumo - batería se descarga rápido"""
        print("⚡ Simulando alto consumo...")
        # Implementar
    
    @staticmethod
    def simulate_battery_critical():
        """Batería en nivel crítico"""
        print("🔋 Simulando batería crítica...")
        # Implementar


def main():
    """Función principal"""
    
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Simulador de sistema inversor híbrido"
    )
    parser.add_argument(
        '--url',
        default='http://localhost:8000',
        help='URL del servidor API (ej: http://localhost:8111)'
    )
    parser.add_argument(
        '--interval',
        type=int,
        default=10,
        help='Intervalo de envío en segundos'
    )
    parser.add_argument(
        '--scenario',
        choices=['normal', 'cloudy', 'high_consumption', 'critical_battery'],
        default='normal',
        help='Escenario a simular'
    )
    
    args = parser.parse_args()
    
    simulator = EnergySimulator(api_url=args.url)
    
    if args.scenario == 'normal':
        simulator.start(interval_seconds=args.interval)
    elif args.scenario == 'cloudy':
        ScenarioSimulator.simulate_cloudy_day()
    elif args.scenario == 'high_consumption':
        ScenarioSimulator.simulate_high_consumption()
    elif args.scenario == 'critical_battery':
        ScenarioSimulator.simulate_battery_critical()


if __name__ == "__main__":
    main()
