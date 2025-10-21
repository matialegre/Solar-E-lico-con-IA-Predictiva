# 🧪 Guía de Testing y Verificación

## Verificación Rápida del Sistema

### ✅ Checklist de Componentes

```bash
# Verificar estructura de archivos
dir /s /b *.py *.jsx *.cpp
```

## 1️⃣ Testing del Backend

### Iniciar Backend
```bash
cd backend
python main.py
```

**Verificaciones**:
- ✅ Servidor inicia en puerto 8000
- ✅ Mensaje "Sistema Inversor Inteligente iniciado"
- ✅ Base de datos inicializada

### Test de Endpoints

```bash
# Test 1: Estado del sistema
curl http://localhost:8000/api/system/status

# Respuesta esperada:
# {"status":"online","version":"1.0.0",...}

# Test 2: Dashboard
curl http://localhost:8000/api/dashboard

# Test 3: Clima actual
curl http://localhost:8000/api/weather/current

# Test 4: Predicciones
curl http://localhost:8000/api/predictions/24h
```

### Test de Base de Datos

```python
# backend/test_db.py
from database import init_db, SessionLocal, EnergyRecord
from datetime import datetime

# Inicializar
init_db()

# Crear registro de prueba
db = SessionLocal()
record = EnergyRecord(
    solar_power_w=1500.0,
    wind_power_w=800.0,
    battery_soc_percent=75.0,
    load_power_w=500.0
)
db.add(record)
db.commit()
print("✅ Base de datos funcionando")
```

## 2️⃣ Testing del Simulador

### Iniciar Simulador
```bash
cd backend
python simulator.py --interval 5
```

**Verificaciones**:
- ✅ Conecta al servidor
- ✅ Envía datos cada 5 segundos
- ✅ Muestra valores en consola
- ✅ Estado de batería varía realistamente

### Test Manual de Datos
```python
from simulator import EnergySimulator

sim = EnergySimulator()
data = sim.generate_sensor_data()

print(f"Solar: {data['solar_voltage_v']*data['solar_current_a']:.0f}W")
print(f"Batería SoC: {sim.battery_soc:.1f}%")
```

## 3️⃣ Testing del Frontend

### Iniciar Frontend
```bash
cd frontend
npm start
```

**Verificaciones**:
- ✅ Compila sin errores
- ✅ Abre en http://localhost:3000
- ✅ Sin warnings en consola

### Test Visual

#### Checklist del Dashboard:
- [ ] Header muestra "Inversor Inteligente Híbrido"
- [ ] Estado "Conectado" en verde
- [ ] 6 métricas mostradas correctamente
- [ ] Gráfico histórico con datos
- [ ] Gráfico de batería visible
- [ ] Gráfico de predicción con barras
- [ ] Panel de clima con temperatura
- [ ] Panel de control con toggle
- [ ] Panel de alertas (sin alertas o con alertas)
- [ ] Panel de predicción 24h

### Test de Interacción

1. **Modo Automático**:
   - Click en toggle "Modo Automático IA"
   - Debería cambiar a OFF
   - Aparecen controles manuales

2. **Control Manual**:
   - Click en "Activar" para Solar
   - Mensaje de confirmación aparece

3. **Actualización en Tiempo Real**:
   - Esperar 30 segundos
   - Valores deberían actualizarse

### Test de WebSocket

Abrir DevTools (F12) → Console:
```javascript
const ws = new WebSocket('ws://localhost:8000/ws');
ws.onmessage = (e) => console.log('Mensaje:', JSON.parse(e.data));
```

**Esperado**: Mensajes cada 30s

## 4️⃣ Testing de IA

### Test de Predicción

```python
from ai_predictor import energy_predictor
from datetime import datetime

# Datos de prueba
weather = {
    'temperature_c': 25,
    'cloud_cover_percent': 20,
    'humidity_percent': 60,
    'wind_speed_ms': 5.0,
    'pressure_hpa': 1013
}

# Predecir solar
solar = energy_predictor.predict_solar(datetime.now(), weather)
print(f"Predicción solar: {solar:.0f}W")

# Predecir eólica
wind = energy_predictor.predict_wind(datetime.now(), weather)
print(f"Predicción eólica: {wind:.0f}W")
```

### Test de Entrenamiento

```python
import pandas as pd
from ai_predictor import energy_predictor

# Modelo debe entrenarse con datos sintéticos
energy_predictor._train_with_synthetic_data()
print(f"Modelo entrenado: {energy_predictor.is_trained}")
```

## 5️⃣ Testing del Firmware ESP32

### Test de Compilación

```bash
cd firmware
pio run
```

**Verificaciones**:
- ✅ Compila sin errores
- ✅ Tamaño del firmware < 1MB

### Test con Monitor Serial

```bash
pio device monitor
```

**Verificar en salida**:
```
Sistema Inversor Inteligente ESP32
✅ Pines configurados
✅ WiFi conectado
IP: 192.168.x.x
▶️ Tarea SensorRead iniciada
▶️ Tarea ServerComm iniciada
▶️ Tarea ControlLogic iniciada

--- Sensores ---
Solar: 45.20V, 5.30A (240W)
✓ Datos enviados - Código: 200
```

### Test de Sensores (Sin Hardware)

```cpp
// Modificar main.cpp temporalmente
float testVoltage = readVoltage(PIN_SOLAR_VOLTAGE);
Serial.printf("Test voltaje: %.2f\n", testVoltage);
```

## 6️⃣ Testing de Integración

### Scenario 1: Sistema Completo

```bash
# Terminal 1
cd backend && python main.py

# Terminal 2
cd backend && python simulator.py

# Terminal 3
cd frontend && npm start

# Navegador
http://localhost:3000
```

**Verificar**:
1. Dashboard carga correctamente
2. Métricas actualizándose
3. Gráficos con datos
4. Sin errores en consola

### Scenario 2: Alta Carga

```python
# Simular múltiples clientes
import asyncio
import aiohttp

async def fetch_data():
    async with aiohttp.ClientSession() as session:
        async with session.get('http://localhost:8000/api/dashboard') as resp:
            return await resp.json()

# 100 requests concurrentes
tasks = [fetch_data() for _ in range(100)]
await asyncio.gather(*tasks)
```

**Esperado**: Sin errores, respuestas < 1s

### Scenario 3: Batería Crítica

Modificar simulador:
```python
simulator.battery_soc = 15.0  # Nivel crítico
simulator.send_data()
```

**Verificar**:
- ✅ Alerta roja aparece en dashboard
- ✅ Mensaje "Batería crítica"
- ✅ Acción sugerida visible

## 7️⃣ Testing de Estrés

### Load Testing del Backend

Usar herramientas como `locust` o `ab`:

```bash
# Apache Bench
ab -n 1000 -c 10 http://localhost:8000/api/system/status

# Esperado: >100 req/s
```

### Memory Leaks

```bash
# Windows
tasklist | findstr python

# Monitorear memoria durante 30 minutos
# La memoria no debe crecer constantemente
```

## 8️⃣ Testing de Errores

### Test de Recuperación

1. **Desconectar WiFi**:
   - Frontend debe mostrar "Desconectado"
   - Reconecta automáticamente

2. **Matar Backend**:
   - Frontend intenta reconectar
   - Mensaje de error en consola

3. **Datos Inválidos**:
```bash
curl -X POST http://localhost:8000/api/energy/record \
  -H "Content-Type: application/json" \
  -d '{"invalid": "data"}'
  
# Esperado: Error 422 (Validation Error)
```

## 9️⃣ Testing de Seguridad

### Test de Entrada Maliciosa

```bash
# SQL Injection attempt
curl "http://localhost:8000/api/energy/history?hours='; DROP TABLE users--"

# XSS attempt
curl -X POST http://localhost:8000/api/energy/record \
  -d '{"solar_voltage_v": "<script>alert(1)</script>"}'
```

**Esperado**: Validación rechaza entradas inválidas

### Test de Rate Limiting (si está implementado)

```bash
for i in {1..1000}; do
  curl http://localhost:8000/api/dashboard &
done
```

## 🔟 Testing de Performance

### Métricas Objetivo

| Métrica | Objetivo | Test |
|---------|----------|------|
| API Response Time | <100ms | curl -w "@format.txt" |
| Dashboard Load | <2s | Chrome DevTools → Network |
| WebSocket Latency | <50ms | Consola browser |
| ESP32 Send Rate | 10s | Monitor serial |
| Database Query | <50ms | SQLAlchemy debug |

### Herramientas

```bash
# Backend performance
pip install py-spy
py-spy top --pid $(pgrep -f "python main.py")

# Frontend performance
# Chrome DevTools → Lighthouse → Run Audit
```

## 🐛 Troubleshooting de Tests

### Backend no inicia
```bash
# Verificar puerto 8000
netstat -ano | findstr :8000

# Instalar dependencias
pip install -r requirements.txt --upgrade
```

### Frontend no compila
```bash
# Limpiar cache
rm -rf node_modules package-lock.json
npm install
```

### Simulador no conecta
```bash
# Verificar backend corriendo
curl http://localhost:8000/api/system/status

# Verificar firewall
# Windows: Permitir Python en firewall
```

### ESP32 no compila
```bash
# Actualizar PlatformIO
pio upgrade

# Limpiar build
pio run --target clean
```

## ✅ Checklist Final

### Pre-Producción

- [ ] Todos los tests pasan
- [ ] Sin memory leaks
- [ ] Performance aceptable
- [ ] Documentación completa
- [ ] Variables de entorno configuradas
- [ ] API keys válidas
- [ ] Logs configurados
- [ ] Backups de DB configurados
- [ ] Monitoreo configurado
- [ ] Plan de recuperación definido

### Producción

- [ ] HTTPS habilitado
- [ ] Autenticación implementada
- [ ] Rate limiting activo
- [ ] Firewall configurado
- [ ] Logs centralizados
- [ ] Alertas configuradas
- [ ] Backups automáticos
- [ ] Documentación actualizada

---

## 📝 Reportar Bugs

Incluir:
1. Descripción del problema
2. Pasos para reproducir
3. Comportamiento esperado vs actual
4. Logs relevantes
5. Configuración del sistema
6. Screenshots (si aplica)

## 🎉 Test Completo Exitoso

Si todos los tests pasan:
- ✅ Sistema listo para uso
- ✅ Documentación completa
- ✅ Performance aceptable
- ✅ Sin errores críticos

**¡El sistema está operativo!** 🚀
