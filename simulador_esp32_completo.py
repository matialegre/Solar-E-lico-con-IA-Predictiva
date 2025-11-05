"""
Simulador ESP32 - Envía telemetría completa al backend
"""
import requests
import time
import random

# Configuración
BACKEND_URL = "http://localhost:11113/api/esp32/telemetry"
DEVICE_ID = "ESP32_INVERSOR_001"

# Contador de secuencia
seq = 0

def generar_telemetria():
    """Genera telemetría simulada como el ESP32 real"""
    global seq
    seq += 1
    
    # Simular voltajes ADC (0-3.3V)
    adc1_bat1 = random.uniform(0.5, 0.6)
    adc2_eolica = random.uniform(0.52, 0.59)
    adc5_solar = random.uniform(0.0, 0.04)
    adc6_load = random.uniform(0.0, 0.005)
    
    telemetria = {
        "device_id": DEVICE_ID,
        "seq": seq,
        "ts": int(time.time()),
        "uptime": seq * 2,
        "free_heap": 150000,
        "rssi": random.randint(-60, -40),
        
        # Voltajes procesados
        "v_bat_v": adc1_bat1 * 12.5,  # Escalado a 12V
        "v_wind_v_dc": adc2_eolica * 0.5,
        "v_solar_v": adc5_solar * 2.0,
        "v_load_v": adc6_load * 1.0,
        
        # Potencias
        "voltaje_promedio": random.uniform(10, 13),
        "soc": random.randint(60, 80),
        "potencia_solar": random.uniform(0, 50),
        "potencia_eolica": random.uniform(0, 30),
        "potencia_consumo": random.uniform(5, 20),
        "temperatura": random.uniform(20, 30),
        
        # RPM de la turbina eólica (valores más visibles)
        "turbine_rpm": random.uniform(150, 400),  # Rango medio-alto visible
        "rpm": random.uniform(150, 400),  # Legacy compatibility
        "frequency_hz": random.uniform(25, 65),  # 25-65 Hz típico
        
        # Relés
        "relays": {
            "solar": random.choice([True, False]),
            "eolica": random.choice([True, False]),
            "red": random.choice([True, False]),
            "carga": random.choice([True, False])
        },
        
        # RAW ADC - NOMBRES CORREGIDOS (solo 4 ADC reales)
        "raw_adc": {
            "adc1_bat1": round(adc1_bat1, 9),              # GPIO34 - Batería
            "adc1_bat1_raw": int(adc1_bat1 * 4095 / 3.3),
            "adc2_eolica": round(adc2_eolica, 9),          # GPIO35 - Eólica DC
            "adc2_eolica_raw": int(adc2_eolica * 4095 / 3.3),
            "adc5_solar": round(adc5_solar, 9),            # GPIO36 - Solar
            "adc5_solar_raw": int(adc5_solar * 4095 / 3.3),
            "adc6_load": round(adc6_load, 9),              # GPIO39 - Carga
            "adc6_load_raw": int(adc6_load * 4095 / 3.3)
        }
    }
    
    return telemetria

def main():
    print("=" * 80)
    print("🚀 SIMULADOR ESP32 - INICIADO (Versión Actualizada 2024)")
    print("=" * 80)
    print(f"Backend: {BACKEND_URL}")
    print(f"Device ID: {DEVICE_ID}")
    print()
    print("📊 Datos Simulados:")
    print("   • GPIO34 (Batería): 0.5-0.6V → Voltaje estable")
    print("   • GPIO35 (Eólica): 0.52-0.59V → Señal AC rectificada")
    print("   • GPIO36 (Solar): 0.0-0.04V → Muy baja generación")
    print("   • GPIO39 (Carga): 0.0-0.005V → Consumo bajo")
    print("   • RPM Turbina: 0-450 RPM aleatorio")
    print("   • Frecuencia: 0-75 Hz aleatorio")
    print()
    print("⚡ Enviando telemetría cada 0.5 segundos (TIEMPO REAL)...")
    print("⌨️  Presiona Ctrl+C para detener")
    print("=" * 80)
    print()
    
    paquetes_exitosos = 0
    paquetes_fallidos = 0
    
    while True:
        try:
            # Generar telemetría
            telemetria = generar_telemetria()
            
            # Enviar al backend
            response = requests.post(BACKEND_URL, json=telemetria, timeout=2)
            
            if response.status_code == 200:
                paquetes_exitosos += 1
                rpm_val = telemetria.get('turbine_rpm', 0)
                print(f"✅ [{seq}] Paquete enviado - ADC: bat={telemetria['raw_adc']['adc1_bat1']:.3f}V solar={telemetria['raw_adc']['adc5_solar']:.3f}V RPM={rpm_val:.1f} - Total: {paquetes_exitosos}")
            else:
                paquetes_fallidos += 1
                print(f"❌ [{seq}] Error {response.status_code}")
            
            # Cada 5 paquetes, mostrar estadísticas
            if seq % 5 == 0:
                print()
                print(f"📊 Estadísticas: Exitosos={paquetes_exitosos} Fallidos={paquetes_fallidos}")
                print(f"   Último raw_adc enviado:")
                print(f"   - adc1_bat1 (GPIO34 Batería): {telemetria['raw_adc']['adc1_bat1']:.3f}V (raw: {telemetria['raw_adc']['adc1_bat1_raw']})")
                print(f"   - adc2_eolica (GPIO35 Eólica): {telemetria['raw_adc']['adc2_eolica']:.3f}V (raw: {telemetria['raw_adc']['adc2_eolica_raw']})")
                print(f"   - adc5_solar (GPIO36 Solar): {telemetria['raw_adc']['adc5_solar']:.3f}V (raw: {telemetria['raw_adc']['adc5_solar_raw']})")
                print(f"   - adc6_load (GPIO39 Carga): {telemetria['raw_adc']['adc6_load']:.3f}V (raw: {telemetria['raw_adc']['adc6_load_raw']})")
                print(f"   🎯 RPM: {telemetria['turbine_rpm']:.1f} RPM | Freq: {telemetria['frequency_hz']:.2f} Hz")
                print()
            
            # Esperar 0.5 segundos (4 veces más rápido)
            time.sleep(0.5)
            
        except KeyboardInterrupt:
            print()
            print("=" * 70)
            print("🛑 SIMULADOR DETENIDO")
            print(f"Total paquetes enviados: {paquetes_exitosos}")
            print(f"Total paquetes fallidos: {paquetes_fallidos}")
            print("=" * 70)
            break
        except Exception as e:
            paquetes_fallidos += 1
            print(f"❌ [{seq}] Error: {e}")
            time.sleep(2)

if __name__ == "__main__":
    main()
