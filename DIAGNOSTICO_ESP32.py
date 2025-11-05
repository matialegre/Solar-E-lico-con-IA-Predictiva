import requests
import json

print("=" * 70)
print("🔍 DIAGNÓSTICO ESP32 - ¿POR QUÉ MUESTRA 0.000V?")
print("=" * 70)
print()

# 1. Verificar si el backend está funcionando
print("1️⃣ Verificando backend...")
try:
    response = requests.get('http://localhost:11113/api/esp32/diagnostico', timeout=2)
    if response.status_code == 200:
        data = response.json()
        print("   ✅ Backend funcionando")
        print(f"   📊 Contador total de paquetes: {data['contador_total_paquetes']}")
        print(f"   📱 Dispositivos registrados: {data['dispositivos_registrados']}")
        
        if data['contador_total_paquetes'] == 0:
            print()
            print("   ❌ ¡PROBLEMA ENCONTRADO!")
            print("   ⚠️  EL BACKEND NO HA RECIBIDO NINGÚN PAQUETE DEL ESP32")
            print()
            print("   Posibles causas:")
            print("   1. El ESP32 no está encendido")
            print("   2. El ESP32 no está conectado al WiFi")
            print("   3. El ESP32 está enviando a otra IP")
            print("   4. El firmware del ESP32 no está corriendo")
            print()
        else:
            print(f"   ✅ Backend ha recibido {data['contador_total_paquetes']} paquetes")
            
            if data['ultimo_paquete']:
                ultimo = data['ultimo_paquete']
                print()
                print("2️⃣ Último paquete recibido:")
                print(f"   Device ID: {ultimo['device_id']}")
                print(f"   Hace: {ultimo['hace_segundos']} segundos")
                print(f"   Contador: {ultimo['contador']}")
                print(f"   Tiene raw_adc: {ultimo['tiene_raw_adc']}")
                
                if ultimo['hace_segundos'] > 10:
                    print()
                    print("   ⚠️  PROBLEMA: Último paquete hace más de 10 segundos")
                    print("   El ESP32 se considera OFFLINE")
                else:
                    print()
                    print("   ✅ ESP32 está enviando datos (< 10 seg)")
                    
                    if not ultimo['tiene_raw_adc']:
                        print("   ⚠️  PROBLEMA: El dispositivo NO tiene raw_adc guardado")
        
        print()
        print("3️⃣ Verificando endpoint /api/esp32/devices...")
        response2 = requests.get('http://localhost:11113/api/esp32/devices', timeout=2)
        devices_data = response2.json()
        
        if devices_data['devices']:
            device = devices_data['devices'][0]
            print(f"   ✅ Device encontrado: {device['device_id']}")
            print(f"   Status: {device['status']}")
            print(f"   Contador: {device.get('contador', 'N/A')}")
            
            if device.get('raw_adc'):
                print()
                print("   ✅ raw_adc PRESENTE:")
                for key, val in device['raw_adc'].items():
                    if not key.endswith('_raw'):
                        print(f"      {key}: {val} V")
            else:
                print()
                print("   ❌ raw_adc NO ESTÁ EN EL DEVICE")
                print("   Esto explica por qué el frontend muestra 0.000V")
        else:
            print("   ❌ No hay dispositivos en la respuesta")
            print("   El ESP32 nunca envió telemetría")
    
except Exception as e:
    print(f"   ❌ Error: {e}")

print()
print("=" * 70)
print("INSTRUCCIONES:")
print("=" * 70)
print()
print("Si el contador es 0:")
print("  → Verifica que el ESP32 esté encendido")
print("  → Abre el monitor serial del ESP32")
print("  → Busca logs de conexión WiFi")
print("  → Verifica que la IP del backend sea correcta en el firmware")
print()
print("Si el contador > 0 pero raw_adc está vacío:")
print("  → El ESP32 está conectado pero no envía raw_adc")
print("  → Verifica que el firmware esté enviando el campo 'raw_adc'")
print()
