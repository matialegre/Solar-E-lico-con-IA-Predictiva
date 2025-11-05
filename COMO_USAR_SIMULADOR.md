# 🚀 Cómo Usar el Simulador ESP32

## 📋 Pre-requisitos

1. **Backend corriendo** en puerto `11113`
2. **Python** instalado
3. **Biblioteca requests** (se instala automáticamente)

---

## ⚡ Inicio Rápido

### Opción 1: Ejecutable BAT (Recomendado)

**Doble clic en**:
```
EJECUTAR_SIMULADOR.bat
```

El script hará todo automáticamente:
- ✅ Verifica Python
- ✅ Instala dependencias
- ✅ Ejecuta el simulador

### Opción 2: Manual

```bash
python simulador_esp32_completo.py
```

---

## 📊 Qué Hace el Simulador

Envía telemetría **cada 2 segundos** al backend, simulando un ESP32 real:

### ADCs Simulados (0-3.3V)

| GPIO | Canal | Rango | Descripción |
|------|-------|-------|-------------|
| 34 | `adc1_bat1` | 0.5-0.6V | Batería (muy estable) |
| 35 | `adc2_eolica` | 0.52-0.59V | Eólica DC (AC rectificado) |
| 36 | `adc5_solar` | 0.0-0.04V | Solar (baja generación) |
| 39 | `adc6_load` | 0.0-0.005V | Carga (bajo consumo) |

### Otros Datos

- **RPM Turbina**: 0-450 RPM (aleatorio)
- **Frecuencia**: 0-75 Hz (aleatorio)
- **Relés**: Estados ON/OFF aleatorios
- **Contador**: Incrementa con cada paquete

---

## 🖥️ Salida del Simulador

### Logs por Paquete
```
✅ [1] Paquete enviado - ADC: bat=0.563V solar=0.012V RPM=234.5 - Total: 1
✅ [2] Paquete enviado - ADC: bat=0.551V solar=0.028V RPM=189.3 - Total: 2
✅ [3] Paquete enviado - ADC: bat=0.579V solar=0.003V RPM=412.7 - Total: 3
```

### Estadísticas (cada 5 paquetes)
```
📊 Estadísticas: Exitosos=5 Fallidos=0
   Último raw_adc enviado:
   - adc1_bat1 (GPIO34 Batería): 0.563V (raw: 698)
   - adc2_eolica (GPIO35 Eólica): 0.551V (raw: 683)
   - adc5_solar (GPIO36 Solar): 0.012V (raw: 14)
   - adc6_load (GPIO39 Carga): 0.003V (raw: 3)
   🎯 RPM: 234.5 RPM | Freq: 39.12 Hz
```

---

## 🔍 Verificar en el Frontend

1. **Abre** http://localhost:3000
2. **Ve a** "Dispositivos" → "Monitor ESP32"
3. **Verás**:
   - Estado: **CONECTADO** (verde)
   - Contador incrementando cada 2 seg
   - ADCs con valores estables
   - **Tarjeta morada RPM** (arriba de ADCs):
     ```
     RPM Turbina Eólica: 234 RPM
     Frecuencia Eléctrica: 39.12 Hz
     ```

---

## 🛑 Detener el Simulador

Presiona **Ctrl+C** en la terminal del simulador:

```
🛑 SIMULADOR DETENIDO
Total paquetes enviados: 47
Total paquetes fallidos: 0
```

---

## 🧪 Probar Valores Específicos

### Modificar Rangos de ADC

Edita `simulador_esp32_completo.py`:

```python
# Líneas 21-24
adc1_bat1 = random.uniform(0.5, 0.6)    # ← Cambiar rango aquí
adc2_eolica = random.uniform(0.52, 0.59)
adc5_solar = random.uniform(0.0, 0.04)
adc6_load = random.uniform(0.0, 0.005)
```

**Ejemplo - Probar voltaje fijo de 2.5V**:
```python
adc1_bat1 = 2.5  # Voltaje fijo en vez de aleatorio
```

### Modificar RPM

```python
# Línea 49
"turbine_rpm": random.uniform(0, 450),  # ← Cambiar rango
```

**Ejemplo - RPM fijo de 300**:
```python
"turbine_rpm": 300,  # RPM constante
```

---

## ⚠️ Troubleshooting

### Error: "Connection refused"
```
❌ [1] Error: Connection refused
```

**Causa**: Backend no está corriendo.

**Solución**:
```bash
cd backend
uvicorn main:app --host 0.0.0.0 --port 11113
```

### Error: "No module named 'requests'"
```
❌ Error: No module named 'requests'
```

**Solución**:
```bash
pip install requests
```

### Frontend muestra 0.000V
**Causa**: Backend no está procesando los datos.

**Solución**:
1. Revisa logs del backend (debe mostrar `[TELEM]`)
2. Verifica que el simulador muestre `✅ Paquete enviado`
3. Recarga frontend (F5)

---

## 📈 Probar Estabilidad de ADC

### Test 1: Valor Constante
Edita el simulador para generar voltaje fijo:
```python
adc1_bat1 = 2.5  # Fijo
```

**Resultado esperado**:
- Backend: `GPIO34 → Batería: 2.500V`
- Frontend: `2.500V` **sin saltos**

### Test 2: Valores Estables
Deja el simulador corriendo 30 segundos.

**Resultado esperado**:
- Variación < 0.01V
- No saltos bruscos (ej: 0.5V → 3.2V → 0.5V)

---

## 📊 JSON Enviado (Ejemplo)

```json
{
  "device_id": "ESP32_INVERSOR_001",
  "seq": 123,
  "ts": 1729701234,
  "turbine_rpm": 234.5,
  "frequency_hz": 39.12,
  "raw_adc": {
    "adc1_bat1": 0.563,
    "adc1_bat1_raw": 698,
    "adc2_eolica": 0.551,
    "adc2_eolica_raw": 683,
    "adc5_solar": 0.012,
    "adc5_solar_raw": 14,
    "adc6_load": 0.003,
    "adc6_load_raw": 3
  },
  "relays": {
    "solar": true,
    "eolica": false,
    "red": true,
    "carga": false
  }
}
```

---

## ✅ Checklist de Prueba

- [ ] Backend corriendo (puerto 11113)
- [ ] Simulador ejecutándose
- [ ] Backend logs muestran `[TELEM]`
- [ ] Frontend muestra "CONECTADO"
- [ ] Contador incrementa cada 2 seg
- [ ] ADCs muestran valores (no 0.000V)
- [ ] **Tarjeta morada RPM** visible
- [ ] RPM muestra valores (no 0 RPM)
- [ ] Valores estables sin saltos

**Si todos ✅ → Sistema funcionando correctamente! 🎉**
