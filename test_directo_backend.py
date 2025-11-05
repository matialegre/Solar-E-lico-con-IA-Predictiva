"""
Test directo: Envía 1 paquete y verifica inmediatamente
"""
import requests
import json
import time

print("=" * 60)
print("TEST DIRECTO - Un paquete al backend")
print("=" * 60)

# 1. Enviar telemetría
telemetria = {
    "device_id": "ESP32_TEST_123",
    "seq": 999,
    "ts": int(time.time()),
    "uptime": 1000,
    "free_heap": 150000,
    "rssi": -50,
    "v_bat_v": 12.5,
    "v_wind_v_dc": 0.5,
    "v_solar_v": 2.0,
    "v_load_v": 1.0,
    "voltaje_promedio": 12.0,
    "soc": 75,
    "potencia_solar": 25,
    "potencia_eolica": 15,
    "potencia_consumo": 10,
    "temperatura": 25,
    "relays": {
        "solar": True,
        "eolica": False,
        "red": False,
        "carga": True
    },
    "raw_adc": {
        "adc1_bat1": 0.555,
        "adc1_bat1_raw": 688,
        "adc2_bat2": 0.577,
        "adc2_bat2_raw": 716,
        "adc3_bat3": 0.555,
        "adc3_bat3_raw": 688,
        "adc4_solar": 0.025,
        "adc4_solar_raw": 31,
        "adc5_wind": 0.025,
        "adc5_wind_raw": 31,
        "adc6_load": 0.003,
        "adc6_load_raw": 4,
        "adc7_ldr": 0,
        "adc7_ldr_raw": 0
    }
}

print("\n1️⃣ Enviando paquete de prueba...")
print(f"   Device ID: {telemetria['device_id']}")
print(f"   Seq: {telemetria['seq']}")
print(f"   raw_adc incluido: Sí ({len(telemetria['raw_adc'])} campos)")

try:
    response = requests.post(
        'http://localhost:11113/api/esp32/telemetry',
        json=telemetria,
        timeout=5
    )
    
    print(f"\n2️⃣ Respuesta del backend:")
    print(f"   Status: {response.status_code}")
    print(f"   Body: {response.json()}")
    
    if response.status_code == 200:
        print("\n   ✅ Backend aceptó el paquete")
        
        # Esperar 1 segundo para que se procese
        time.sleep(1)
        
        # 2. Verificar que esté guardado
        print("\n3️⃣ Verificando /api/esp32/devices...")
        response2 = requests.get('http://localhost:11113/api/esp32/devices', timeout=5)
        data = response2.json()
        
        print(f"   Total devices: {data['total']}")
        
        if data['devices']:
            for dev in data['devices']:
                print(f"\n   Device: {dev['device_id']}")
                print(f"   Status: {dev['status']}")
                print(f"   Contador: {dev.get('contador', 'N/A')}")
                
                if dev.get('raw_adc'):
                    print(f"   ✅ raw_adc PRESENTE:")
                    print(f"      - adc1_bat1: {dev['raw_adc'].get('adc1_bat1', 'N/A')}")
                    print(f"      - adc2_eolica: {dev['raw_adc'].get('adc2_eolica', 'N/A')}")
                    print(f"      - adc5_solar: {dev['raw_adc'].get('adc5_solar', 'N/A')}")
                    print(f"      - adc6_load: {dev['raw_adc'].get('adc6_load', 'N/A')}")
                else:
                    print(f"   ❌ raw_adc NO está en el device")
        else:
            print("   ❌ No hay dispositivos registrados")
            print("   El paquete no se guardó correctamente")
    else:
        print(f"\n   ❌ Error: {response.status_code}")
        
except Exception as e:
    print(f"\n   ❌ Error: {e}")

print("\n" + "=" * 60)
print("FIN DEL TEST")
print("=" * 60)
print("\n⚠️  AHORA REVISA LA CONSOLA DEL BACKEND")
print("    Deberías ver:")
print("    [TELEM] ESP32_TEST_123 seq=999 ...")
print("    💾 [GUARDAR NUEVO #X] raw_adc ...")
print("\n")
