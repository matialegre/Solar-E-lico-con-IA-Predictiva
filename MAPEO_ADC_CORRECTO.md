# ✅ MAPEO ADC CORRECTO - ESP32

## 🔴 PROBLEMA ANTERIOR

El backend mostraba logs incorrectos:
- ❌ GPIO32 como "Batería 3" → **GPIO32 es RELÉ RED, NO es ADC**
- ❌ GPIO33 como "Solar" → **GPIO33 es RELÉ CARGA, NO es ADC**
- ❌ GPIO35 como "Batería 2" → **GPIO35 es EÓLICA, NO batería**
- ❌ GPIO36 como "Eólica" → **GPIO36 es SOLAR, NO eólica**

---

## ✅ MAPEO CORRECTO (4 ADC reales)

Según el firmware (`config.h`):

### **Pines ADC (solo 4):**

| GPIO | ADC Channel | Función Real | Nombre Código |
|------|-------------|--------------|---------------|
| **GPIO34** | ADC1_CH6 | 🔋 **Batería** | `adc1_bat1` |
| **GPIO35** | ADC1_CH7 | 💨 **Eólica DC** | `adc2_eolica` (antes `adc2_bat2`) |
| **GPIO36** | ADC1_CH0 | ☀️ **Solar** | `adc5_solar` (antes `adc5_wind`) |
| **GPIO39** | ADC1_CH3 | ⚡ **Carga/Consumo** | `adc6_load` |

### **Pines de RELÉS (NO son ADC):**

| GPIO | Función |
|------|---------|
| **GPIO26** | Relé Solar |
| **GPIO25** | Relé Eólica |
| **GPIO32** | Relé Red ❌ NO ES ADC |
| **GPIO33** | Relé Carga ❌ NO ES ADC |

---

## 🔧 CAMBIOS REALIZADOS

### 1️⃣ **Backend (`main.py`)**

#### Logs corregidos:
**ANTES:**
```python
print("GPIO34 → Batería1 (0–3.3V):", f(gpio34))
print("GPIO35 → Batería2 (0–3.3V):", f(gpio35))  # ❌ INCORRECTO
print("GPIO32 → Batería3 (0–3.3V):", f(gpio32))  # ❌ NO EXISTE
print("GPIO33 → Corriente Solar (0–3.3V):", f(gpio33))  # ❌ NO EXISTE
print("GPIO36 → Corriente Eólica RAW (0–3.3V):", f(gpio36))  # ❌ ES SOLAR
```

**AHORA:**
```python
print("📊 ADC RAW (0-3.3V):")
print("  GPIO34 → Batería:", f(gpio34_bat))
print("  GPIO35 → Eólica DC:", f(gpio35_eolica))
print("  GPIO36 → Solar:", f(gpio36_solar))
print("  GPIO39 → Carga:", f(gpio39_carga))
```

#### Estructura de datos limpia:
```python
'raw_adc': {
    'adc1_bat1': 0.547,       # GPIO34 - Batería
    'adc2_eolica': 0.578,     # GPIO35 - Eólica DC
    'adc5_solar': 0.017,      # GPIO36 - Solar
    'adc6_load': 0.000        # GPIO39 - Carga
}
```

---

### 2️⃣ **Frontend (`ESP32Monitor.jsx`)**

Grid de **4 ADC** (no 6):

```jsx
<div className="grid grid-cols-2 md:grid-cols-4 gap-4">
  {/* GPIO34 - Batería */}
  <div>
    <p>GPIO34 (ADC1)</p>
    <p>🔋 Batería</p>
    <p>{getADCValue('adc1_bat1')} V</p>
  </div>

  {/* GPIO35 - Eólica */}
  <div>
    <p>GPIO35 (ADC2)</p>
    <p>💨 Eólica</p>
    <p>{getADCValue('adc2_eolica')} V</p>
  </div>

  {/* GPIO36 - Solar */}
  <div>
    <p>GPIO36 (ADC5)</p>
    <p>☀️ Solar</p>
    <p>{getADCValue('adc5_solar')} V</p>
  </div>

  {/* GPIO39 - Carga */}
  <div>
    <p>GPIO39 (ADC6)</p>
    <p>⚡ Carga</p>
    <p>{getADCValue('adc6_load')} V</p>
  </div>
</div>
```

---

## 📊 EJEMPLO DE LOG CORRECTO

### Backend:
```
[TELEM] ESP32_INVERSOR_001 seq=851 ts=2038 Vbat=0.577V Vwind_DC=0.002V Vsolar=0.017V Vload=0.000V Lost=0 | OK
📊 ADC RAW (0-3.3V):
  GPIO34 → Batería: 0.583V
  GPIO35 → Eólica DC: 0.578V
  GPIO36 → Solar: 0.017V
  GPIO39 → Carga: 0.000V
💾 [GUARDAR] raw_adc para ESP32_INVERSOR_001: {'adc1_bat1': 0.583, 'adc2_eolica': 0.578, 'adc5_solar': 0.017, 'adc6_load': 0.0}
```

### Frontend:
```
┌─────────────┬─────────────┬─────────────┬─────────────┐
│ GPIO34      │ GPIO35      │ GPIO36      │ GPIO39      │
│ 🔋 Batería  │ 💨 Eólica   │ ☀️ Solar    │ ⚡ Carga    │
│   0.583 V   │   0.578 V   │   0.017 V   │   0.000 V   │
└─────────────┴─────────────┴─────────────┴─────────────┘
```

---

## 🧪 CÓMO VERIFICAR

### 1. Reinicia el backend:
```cmd
Ctrl+C
python main.py
```

### 2. Busca en los logs:
```
📊 ADC RAW (0-3.3V):
  GPIO34 → Batería: X.XXX V
  GPIO35 → Eólica DC: X.XXX V
  GPIO36 → Solar: X.XXX V
  GPIO39 → Carga: X.XXX V
```

### 3. Refresca el frontend (F5)

Deberías ver **4 cajas con valores reales**, no 0.000V.

---

## 🎯 RESUMEN

✅ **GPIO34** = Batería  
✅ **GPIO35** = Eólica DC  
✅ **GPIO36** = Solar  
✅ **GPIO39** = Carga  

❌ **GPIO32** = Relé RED (NO ADC)  
❌ **GPIO33** = Relé CARGA (NO ADC)  

---

**¡Mapeo corregido! 🎉**
