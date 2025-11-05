"""
Script para verificar qué hay realmente en memoria del backend
"""
import requests

# Trigger el endpoint para que imprima los logs
url = 'http://localhost:11113/api/esp32/devices'

print("=" * 60)
print("Consultando endpoint...")
print("=" * 60)
print(f"URL: {url}")
print()
print("⚠️ REVISA LA CONSOLA DEL BACKEND para ver los logs:")
print("   - 🔍 [API /devices] Dispositivos en memoria")
print("   - 🔍 [API] Keys en info")
print("   - 🔍 [API] relays_data")
print("   - 🔍 [API] raw_adc_data keys")
print()

response = requests.get(url)
print("Respuesta HTTP:", response.status_code)
print()
input("Presiona Enter para continuar...")
