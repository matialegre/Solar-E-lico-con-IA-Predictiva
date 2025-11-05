@echo off
setlocal

set "CURL_EXE=curl"
if exist "C:\Users\Mundo Outdoor\Downloads\curl-8.16.0_9-win64a-mingw\bin\curl.exe" set "CURL_EXE=C:\Users\Mundo Outdoor\Downloads\curl-8.16.0_9-win64a-mingw\bin\curl.exe"

echo ========================================
echo   TEST RAW ADC - ESP32
echo ========================================
echo.
echo Consultando endpoint: /api/esp32/devices
echo.

"%CURL_EXE%" -s http://localhost:11113/api/esp32/devices | python -c "import sys, json; data = json.load(sys.stdin); device = data['devices'][0]; print('Device:', device['device_id']); print('Status:', device['status']); print(''); print('RAW_ADC:'); adc = device['telemetry']['raw_adc']; print('  adc1_bat1:', adc.get('adc1_bat1', 'N/A'), 'V'); print('  adc2_bat2:', adc.get('adc2_bat2', 'N/A'), 'V'); print('  adc3_bat3:', adc.get('adc3_bat3', 'N/A'), 'V'); print('  adc4_solar:', adc.get('adc4_solar', 'N/A'), 'V'); print('  adc5_wind:', adc.get('adc5_wind', 'N/A'), 'V'); print('  adc6_load:', adc.get('adc6_load', 'N/A'), 'V')"

echo.
echo.
pause
