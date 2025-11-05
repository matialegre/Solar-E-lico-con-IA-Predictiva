import requests
import json

# Test endpoint
response = requests.get('http://localhost:11113/api/esp32/devices')
data = response.json()

print("=" * 60)
print("RESPONSE del endpoint /api/esp32/devices")
print("=" * 60)

if 'devices' in data and len(data['devices']) > 0:
    device = data['devices'][0]
    
    print(f"\n✅ Device ID: {device['device_id']}")
    print(f"✅ Status: {device['status']}")
    print(f"✅ Last seen: {device['last_seen']}")
    print(f"📊 CONTADOR: {device.get('contador', 'N/A')}")  # ← NUEVO
    
    print("\n📊 TELEMETRY:")
    telemetry = device.get('telemetry', {})
    print(f"  - battery_voltage: {telemetry.get('battery_voltage')}")
    print(f"  - v_bat_v: {telemetry.get('v_bat_v')}")
    
    print("\n🔧 RAW_ADC:")
    raw_adc = device.get('raw_adc', {})  # ← Nivel superior, no telemetry
    if raw_adc:
        print(f"  - adc1_bat1 (GPIO34): {raw_adc.get('adc1_bat1', 'N/A')} V")
        print(f"  - adc2_eolica (GPIO35): {raw_adc.get('adc2_eolica', 'N/A')} V")
        print(f"  - adc5_solar (GPIO36): {raw_adc.get('adc5_solar', 'N/A')} V")
        print(f"  - adc6_load (GPIO39): {raw_adc.get('adc6_load', 'N/A')} V")
    else:
        print("  ❌ raw_adc está vacío o no existe")
    
    print("\n🔌 RELAYS:")
    relays = device.get('relays', {})  # ← Nivel superior, no telemetry
    if relays:
        for key, value in relays.items():
            print(f"  - {key}: {value}")
    else:
        print("  ❌ relays está vacío o no existe")
    
    print("\n" + "=" * 60)
    print("JSON COMPLETO DE TELEMETRY:")
    print("=" * 60)
    print(json.dumps(telemetry, indent=2))
else:
    print("❌ No hay dispositivos en la respuesta")
