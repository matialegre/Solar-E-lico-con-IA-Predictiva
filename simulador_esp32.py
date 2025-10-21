"""
Simulador de Sensores ESP32 para Pruebas
Simula datos de sensores y los envía al backend vía HTTP

Uso:
    python simulador_esp32.py
    python simulador_esp32.py --mode solar   # Solo simular solar
    python simulador_esp32.py --mode wind    # Solo simular eólico
    python simulador_esp32.py --interval 2   # Enviar cada 2 segundos
"""

import requests
import time
import random
import math
import json
import argparse
from datetime import datetime

# ===== CONFIGURACIÓN =====
BACKEND_URL = "http://localhost:8801"
DEVICE_ID = "ESP32_SIMULATOR_001"
SEND_INTERVAL = 5  # segundos

# ===== CLASE SIMULADOR =====
class ESP32Simulator:
    def __init__(self, mode="hybrid", interval=5):
        self.mode = mode
        self.interval = interval
        self.time_offset = 0
        
        print("╔═══════════════════════════════════════════════════════════╗")
        print("║         🔬 SIMULADOR ESP32 - SENSORES HÍBRIDOS 🔬        ║")
        print("╚═══════════════════════════════════════════════════════════╝")
        print(f"\n⚙️  Configuración:")
        print(f"   Modo: {mode}")
        print(f"   Intervalo: {interval} segundos")
        print(f"   Backend: {BACKEND_URL}")
        print(f"   Device ID: {DEVICE_ID}\n")
        
    def simulate_solar(self, hour_of_day):
        """Simular generación solar según hora del día"""
        # Curva sinusoidal: máximo al mediodía, cero de noche
        if hour_of_day < 6 or hour_of_day > 20:
            # Noche
            irradiance = 0
            voltage = 0
            current = 0
        else:
            # Día: curva sinusoidal
            progress = (hour_of_day - 6) / 14.0  # 0 a 1 entre 6am y 8pm
            sun_angle = math.sin(progress * math.pi)
            
            # Irradiancia: 0-1000 W/m²
            irradiance = sun_angle * 1000 * random.uniform(0.85, 1.0)
            
            # Panel de 3000W nominal
            # Eficiencia ~18%, área ~16m²
            max_power = 3000
            voltage = 48 * sun_angle * random.uniform(0.9, 1.0)
            current = (max_power * sun_angle / voltage) * random.uniform(0.85, 1.0) if voltage > 0 else 0
        
        return {
            'voltage': round(voltage, 2),
            'current': round(current, 2),
            'power': round(voltage * current, 2),
            'irradiance': round(irradiance, 2)
        }
    
    def simulate_wind(self):
        """Simular generación eólica con variación realista"""
        # Velocidad de viento: 0-20 m/s con variación
        base_speed = random.uniform(4, 12)
        gust = random.uniform(-2, 3)
        wind_speed = max(0, base_speed + gust)
        
        # Turbina de 2000W nominal
        # Cut-in: 3.5 m/s, Rated: 12 m/s, Cut-out: 25 m/s
        if wind_speed < 3.5:
            power = 0
            voltage = 0
            current = 0
        elif wind_speed > 25:
            # Cut-out por seguridad
            power = 0
            voltage = 0
            current = 0
        else:
            # Curva cúbica hasta velocidad nominal
            if wind_speed <= 12:
                power_ratio = (wind_speed / 12) ** 3
            else:
                power_ratio = 1.0
            
            max_power = 2000
            power = max_power * power_ratio * random.uniform(0.9, 1.0)
            voltage = 48 * random.uniform(0.95, 1.0)
            current = power / voltage if voltage > 0 else 0
        
        return {
            'voltage': round(voltage, 2),
            'current': round(current, 2),
            'power': round(power, 2),
            'wind_speed': round(wind_speed, 2)
        }
    
    def simulate_battery(self, solar_power, wind_power, load_power):
        """Simular estado de batería"""
        # Batería de 5000Wh (5kWh)
        generation = solar_power + wind_power
        net_power = generation - load_power
        
        # SOC base: 50% +/- variación
        base_soc = 50
        soc_variation = (net_power / 5000) * 10  # Variación basada en balance
        soc = max(20, min(100, base_soc + soc_variation))
        
        # Voltaje según SOC (batería 48V)
        # 44V (0%) a 52V (100%)
        voltage = 44 + (soc / 100) * 8
        
        # Corriente: positiva si carga, negativa si descarga
        current = net_power / voltage if voltage > 0 else 0
        
        return {
            'voltage': round(voltage, 2),
            'current': round(current, 2),
            'power': round(net_power, 2),
            'soc': round(soc, 1)
        }
    
    def simulate_load(self):
        """Simular consumo de la casa"""
        # Consumo típico residencial: 300-1500W
        base_load = 650  # Promedio
        variation = random.uniform(-200, 400)
        load = max(100, base_load + variation)
        
        return round(load, 2)
    
    def simulate_temperature(self):
        """Simular temperatura ambiente"""
        # Temperatura: 10-35°C con variación diaria
        hour = datetime.now().hour
        
        # Curva de temperatura: min a las 6am, max a las 3pm
        if hour < 6:
            temp_factor = 0.3
        elif hour < 15:
            temp_factor = 0.3 + (hour - 6) / 9 * 0.7
        else:
            temp_factor = 1.0 - (hour - 15) / 9 * 0.7
        
        base_temp = 15
        temp_range = 20
        temp = base_temp + temp_range * temp_factor + random.uniform(-2, 2)
        
        return round(temp, 1)
    
    def generate_sensor_data(self):
        """Generar datos completos de sensores"""
        now = datetime.now()
        hour = now.hour
        
        # Simular cada subsistema
        solar = self.simulate_solar(hour)
        wind = self.simulate_wind()
        load_power = self.simulate_load()
        battery = self.simulate_battery(solar['power'], wind['power'], load_power)
        temperature = self.simulate_temperature()
        
        data = {
            'device_id': DEVICE_ID,
            'timestamp': now.isoformat(),
            'solar': solar,
            'wind': wind,
            'battery': battery,
            'load_power_w': load_power,
            'temperature_c': temperature
        }
        
        return data
    
    def send_to_backend(self, data):
        """Enviar datos al backend"""
        try:
            response = requests.post(
                f"{BACKEND_URL}/api/esp32/telemetry",
                json=data,
                timeout=5
            )
            
            if response.status_code == 200:
                return True, "OK"
            else:
                return False, f"HTTP {response.status_code}"
                
        except requests.exceptions.ConnectionError:
            return False, "Backend no disponible"
        except Exception as e:
            return False, str(e)
    
    def print_data(self, data):
        """Imprimir datos en consola"""
        print("\n" + "─" * 60)
        print(f"⏰ {data['timestamp']}")
        print("─" * 60)
        
        if self.mode in ['hybrid', 'solar']:
            print(f"☀️  SOLAR:")
            print(f"   {data['solar']['voltage']:6.2f} V  │  {data['solar']['current']:6.2f} A  │  {data['solar']['power']:7.2f} W")
            print(f"   Irradiancia: {data['solar']['irradiance']:6.2f} W/m²")
        
        if self.mode in ['hybrid', 'wind']:
            print(f"\n💨 EÓLICO:")
            print(f"   {data['wind']['voltage']:6.2f} V  │  {data['wind']['current']:6.2f} A  │  {data['wind']['power']:7.2f} W")
            print(f"   Viento: {data['wind']['wind_speed']:5.2f} m/s")
        
        print(f"\n🔋 BATERÍA:")
        print(f"   {data['battery']['voltage']:6.2f} V  │  {data['battery']['current']:6.2f} A  │  {data['battery']['power']:7.2f} W")
        print(f"   SOC: {data['battery']['soc']:5.1f} %")
        
        print(f"\n🏠 CONSUMO: {data['load_power_w']:7.2f} W")
        print(f"🌡️  TEMP: {data['temperature_c']:5.1f} °C")
        print(f"\n⚡ BALANCE: {data['solar']['power'] + data['wind']['power'] - data['load_power_w']:+7.2f} W")
    
    def run(self):
        """Ejecutar simulador"""
        print("🚀 Simulador iniciado")
        print("   Presiona Ctrl+C para detener\n")
        
        iteration = 0
        
        try:
            while True:
                iteration += 1
                
                # Generar datos
                data = self.generate_sensor_data()
                
                # Mostrar en consola
                self.print_data(data)
                
                # Enviar al backend
                success, message = self.send_to_backend(data)
                
                if success:
                    print(f"✅ Enviado al backend ({iteration})")
                else:
                    print(f"❌ Error enviando: {message}")
                
                # Esperar
                time.sleep(self.interval)
                
        except KeyboardInterrupt:
            print("\n\n👋 Simulador detenido")
            print(f"   Total de iteraciones: {iteration}")

# ===== MAIN =====
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simulador ESP32 de sensores híbridos")
    parser.add_argument("--mode", choices=['hybrid', 'solar', 'wind'], default='hybrid',
                        help="Modo de simulación (default: hybrid)")
    parser.add_argument("--interval", type=int, default=5,
                        help="Intervalo de envío en segundos (default: 5)")
    parser.add_argument("--backend", type=str, default="http://localhost:8801",
                        help="URL del backend (default: http://localhost:8801)")
    
    args = parser.parse_args()
    
    BACKEND_URL = args.backend
    
    simulator = ESP32Simulator(mode=args.mode, interval=args.interval)
    simulator.run()
