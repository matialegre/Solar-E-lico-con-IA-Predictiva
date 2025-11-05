# ✅ CAMBIOS FINALES - Sistema Corregido

## 🎯 Cambios Implementados

### 1. **FIRMWARE - Solo 1 Batería** ✅

**Archivo**: `sensors.h`

- ✅ **Solo lee GPIO34** (PIN_VOLTAJE_BAT1) con 50 muestras
- ✅ Copia el mismo valor a bat2 y bat3 (compatibilidad)
- ✅ **Nombres correctos en JSON**:
  - `adc1_bat1` → GPIO34 Batería
  - `adc2_eolica` → GPIO35 Eólica DC
  - `adc5_solar` → GPIO36 Solar
  - `adc6_load` → GPIO39 Carga

**Archivo**: `http_client.h`

- ✅ Solo envía 4 ADC reales (no más duplicados)
- ✅ Nombres corregidos en `raw_adc`

### 2. **RPM - Configuración Verificada** ✅

- ✅ **Solo flancos RISING** (ascendentes)
- ✅ GPIO13 por defecto (configurable)
- ✅ Anti-rebote 500µs
- ✅ Ventana de medición 500ms
- ✅ Fórmula: `RPM = (freq_Hz × 60) / pole_pairs / gear_ratio`

**Configuración en `config.h`**:
```cpp
#define PIN_RPM_INPUT          13      // GPIO para RPM
#define TURBINE_POLE_PAIRS     10      // Ajustar según generador
#define TURBINE_GEAR_RATIO     1.0f    // 1.0 = directo
```

### 3. **BACKEND - Nombres Corregidos** ✅

**Archivo**: `main.py`

- ✅ Mapeo correcto:
  - `adc2_eolica` (antes era `adc2_bat2`)
  - `adc5_solar` (antes era `adc5_wind`)
- ✅ Guarda con nombres correctos en `DEVICES_STORE`
- ✅ Logs muestran 4 GPIOs correctamente

### 4. **Filtrado ADC Específico** ✅

Cada ADC tiene su propia rutina:

| ADC | GPIO | Muestras | Delay | Uso |
|-----|------|----------|-------|-----|
| Batería | 34 | 50 | 50µs | Muy estable |
| Eólica | 35 | 30 | 100µs | Filtra AC |
| Solar | 36 | 20 | 100µs | Estable |
| Carga | 39 | 20 | 100µs | Responsive |

---

## 🧪 Cómo Probar

### Paso 1: Compilar y Subir Firmware

1. Abre Arduino IDE
2. Abre `inversor_hibrido.ino`
3. **Compila** (Verifica errores)
4. **Sube** al ESP32

### Paso 2: Prueba de ADC con Voltaje Fijo

**Conecta cada ADC a una fuente fija** (ejemplo: 2.5V):

1. **GPIO34 (Batería)** → Conecta 2.5V
2. **Abre Serial Monitor** → Deberías ver: `GPIO34 → Batería: 2.500V`
3. **Abre Frontend** → Debería mostrar **2.500V estable** (sin saltos)
4. **Deja 30 segundos** → Valor debe mantenerse **2.495-2.505V** (muy estable)

Repite para cada GPIO:
- GPIO35 (Eólica DC)
- GPIO36 (Solar)
- GPIO39 (Carga)

### Paso 3: Verificar RPM (Opcional)

**Si tienes señal de frecuencia**:

1. Conecta señal 0-3V al **GPIO13**
2. Verifica que sea **cuadrada** (digital)
3. Serial debe mostrar: `[RPM] edges=25 freq=50.00Hz rpm=300.0`
4. Frontend debe mostrar: **"RPM Turbina Eólica: 300 RPM"**

**Si NO tienes señal**:
- RPM mostrará `0.0` (normal)
- El resto funciona igual

---

## 📊 Logs Esperados

### Serial Monitor (ESP32):
```
✅ Sensores inicializados
   - ADC Batería (GPIO34): 50 muestras
   - ADC Eólica (GPIO35): 30 muestras
   - ADC Solar (GPIO36): 20 muestras
   - ADC Carga (GPIO39): 20 muestras
   - RPM (GPIO13): ISR RISING

[TELEM] ESP32_INVERSOR_001 seq=1 Vbat=2.500V Vwind_DC=2.500V Vsolar=2.500V Vload=2.500V RPM=0.0 | OK

📊 ADC RAW (0-3.3V):
  GPIO34 → Batería: 2.500V
  GPIO35 → Eólica DC: 2.500V
  GPIO36 → Solar: 2.500V
  GPIO39 → Carga: 2.500V
```

### Backend Logs:
```
[TELEM] ESP32_INVERSOR_001 seq=1 ... Vbat=2.500V Vwind_DC=2.500V ... RPM=0.0 | OK

📊 ADC RAW (0-3.3V):
  GPIO34 → Batería: 2.500V
  GPIO35 → Eólica DC: 2.500V
  GPIO36 → Solar: 2.500V
  GPIO39 → Carga: 2.500V

💾 [GUARDAR #1] raw_adc: {
  'adc1_bat1': 2.5,         ← ESTABLE
  'adc1_bat1_raw': 3100,    ← ESTABLE
  'adc2_eolica': 2.5,       ← ESTABLE
  'adc5_solar': 2.5,        ← ESTABLE
  'adc6_load': 2.5          ← ESTABLE
}
```

### Frontend:
- **GPIO34 (Batería)**: `2.500V` ← SIN SALTOS
- **GPIO35 (Eólica)**: `2.500V` ← SIN SALTOS
- **GPIO36 (Solar)**: `2.500V` ← SIN SALTOS
- **GPIO39 (Carga)**: `2.500V` ← SIN SALTOS

---

## ⚠️ Troubleshooting

### ADC sigue saltando
1. **Aumenta muestras**: `num_muestras = 100` en `leerADC_Bateria()`
2. **Aumenta delay**: `delayMicroseconds(200)`
3. **Verifica conexiones**: Cable suelto causa ruido

### RPM no funciona
1. **Verifica GPIO**: ¿Usas GPIO13? Si no, cambia `PIN_RPM_INPUT`
2. **Verifica señal**: Debe ser 0-3V **digital** (no analógica)
3. **Verifica POLE_PAIRS**: Cuenta imanes del generador ÷ 2
4. **Serial Debug**: ¿Ves `[RPM] edges=...`? Si no, la ISR no se dispara

### Frontend muestra 0.000V
1. **Revisa logs backend**: ¿Aparece `📊 ADC RAW`?
2. **Si backend recibe pero frontend no**: Problema de red/proxy
3. **Si backend NO recibe**: Problema de firmware (no compila/sube)

---

## 🎯 Mapeo Final de Hardware

| GPIO | ADC | Nombre Firmware | Nombre Backend | Función |
|------|-----|-----------------|----------------|---------|
| 34 | ADC1_CH6 | `adc1_bat1` | `adc1_bat1` | Batería |
| 35 | ADC1_CH7 | `adc2_eolica` | `adc2_eolica` | Eólica DC |
| 36 | ADC1_CH0 | `adc5_solar` | `adc5_solar` | Solar |
| 39 | ADC1_CH3 | `adc6_load` | `adc6_load` | Carga |
| 13 | Digital | `rpm_isr` | `turbine_rpm` | RPM (RISING) |

---

## 📁 Archivos Modificados

### Firmware:
1. ✅ `config.h` - RPM config
2. ✅ `sensors.h` - Filtrado ADC + RPM + Solo 1 batería
3. ✅ `http_client.h` - Nombres correctos JSON

### Backend:
1. ✅ `main.py` - Mapeo nombres corregido

### Frontend:
- No requiere cambios (usa `raw_adc` genéricamente)

---

## ✅ Estado Final

- ✅ **1 Batería** (GPIO34) con 50 muestras → Muy estable
- ✅ **Eólica** (GPIO35) con 30 muestras → Filtra AC
- ✅ **Solar** (GPIO36) con 20 muestras → Estable
- ✅ **Carga** (GPIO39) con 20 muestras → Responsive
- ✅ **RPM** (GPIO13) con ISR RISING → Correcto
- ✅ **Nombres consistentes** Firmware ↔ Backend ↔ Frontend

**¡Sistema listo para pruebas de voltaje continuo! 🚀**
