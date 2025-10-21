# 🔬 Monitor de Eficiencia Real - Detección Inteligente de Problemas

## 🎯 ¿Qué Hace?

El sistema **compara la generación REAL vs TEÓRICA** para detectar automáticamente:
- ☀️ **Paneles sucios** (reducen eficiencia 20-40%)
- 🌳 **Sombras** en paneles (reducen eficiencia 30-60%)
- 💨 **Turbina con fricción** (rodamientos, palas)
- ⚙️ **Palas dañadas o sucias**
- 🌡️ **Efecto de temperatura** en paneles

---

## 🧮 Cómo Funciona:

### ☀️ **Paneles Solares:**

#### **Sensores Necesarios:**
1. **LDR (Fotoresistor)** → Mide irradiancia solar (W/m²)
2. **ACS712 (Sensor corriente)** → Mide potencia real generada (W)
3. **DS18B20 (Sensor temperatura)** → Temperatura ambiente (°C)

#### **Cálculo:**
```python
# 1. Potencia solar disponible
Potencia_disponible = Irradiancia (W/m²) × Área_paneles (m²)

# 2. Potencia teórica ideal
Eficiencia_ideal = 18% (paneles policristalinos)
Factor_temperatura = 1 - (0.005 × (Temp - 25°C))
Potencia_teórica = Potencia_disponible × 0.18 × Factor_temperatura

# 3. Eficiencia real
Eficiencia_real = (Potencia_real / Potencia_teórica) × 100%
```

#### **Ejemplo Real:**
```
📊 Condiciones:
- Irradiancia: 800 W/m²
- Área paneles: 6 m² (6 paneles de 1m²)
- Temperatura: 30°C
- Potencia real: 700 W

🧮 Cálculo:
- Potencia disponible: 800 × 6 = 4800 W
- Factor temperatura: 1 - (0.005 × 5) = 0.975
- Potencia teórica: 4800 × 0.18 × 0.975 = 842 W
- Eficiencia: (700 / 842) × 100 = 83.1% ✅

✅ Resultado: NORMAL - Paneles operando bien
```

---

### 💨 **Turbina Eólica:**

#### **Sensores Necesarios:**
1. **Anemómetro** → Velocidad del viento (m/s) [o de API]
2. **ACS712 (Sensor corriente)** → Potencia real generada (W)

#### **Cálculo (Ley de Betz):**
```python
# 1. Potencia del viento
Densidad_aire = 1.225 kg/m³
Área_barrido = π × (Diámetro_palas/2)²
Potencia_viento = 0.5 × Densidad × Área × Velocidad³

# 2. Potencia teórica (límite de Betz: 59.3%)
Eficiencia_ideal = 45% (turbinas reales: 40-50%)
Potencia_teórica = Potencia_viento × 0.45
Potencia_teórica = min(Potencia_teórica, Potencia_nominal)

# 3. Eficiencia real
Eficiencia_real = (Potencia_real / Potencia_teórica) × 100%
```

#### **Ejemplo Real:**
```
📊 Condiciones:
- Viento: 10 m/s
- Área barrido: 4.9 m² (turbina 1000W)
- Potencia real: 500 W

🧮 Cálculo:
- Potencia viento: 0.5 × 1.225 × 4.9 × (10³) = 3001 W
- Potencia teórica: 3001 × 0.45 = 1350 W
- Limitado por nominal: min(1350, 1000) = 1000 W
- Eficiencia: (500 / 1000) × 100 = 50% ⚠️

⚠️ Resultado: ADVERTENCIA - Revisar turbina
   Posibles causas: Fricción, palas sucias, desalineación
```

---

## 📊 Niveles de Alerta:

| Eficiencia | Nivel | Color | Significado |
|-----------|-------|-------|-------------|
| **≥ 85%** | ✅ EXCELENTE | Verde | Operación perfecta |
| **75-84%** | 🟢 NORMAL | Azul | Funcionamiento correcto |
| **60-74%** | ⚠️ ADVERTENCIA | Amarillo | Necesita mantenimiento |
| **< 60%** | 🚨 CRÍTICO | Rojo | Problema serio - Revisar urgente |

---

## 🔍 Diagnósticos Automáticos:

### ☀️ **Paneles Solares:**

| Eficiencia | Diagnóstico | Causas Probables |
|-----------|-------------|------------------|
| **< 40%** | 🚨 CRÍTICO | Paneles MUY sucios, sombra total, panel roto |
| **40-50%** | ⚠️ Muy sucios | Suciedad espesa, sombra parcial grande |
| **50-60%** | ⚠️ Necesitan limpieza | Polvo acumulado, sombra pequeña |
| **60-75%** | 💡 Revisar | Limpieza ligera, orientación |
| **75-85%** | 🟢 Normal | Operación correcta |
| **> 85%** | ✅ Excelente | Condiciones ideales |

### 💨 **Turbina Eólica:**

| Eficiencia | Diagnóstico | Causas Probables |
|-----------|-------------|------------------|
| **< 40%** | 🚨 CRÍTICO | Rodamientos trabados, palas rotas |
| **40-50%** | ⚠️ Fricción alta | Rodamientos sin lubricar, palas dañadas |
| **50-60%** | ⚠️ Mantenimiento | Palas sucias, desalineación |
| **60-75%** | 💡 Revisar | Lubricación, limpieza ligera |
| **75-85%** | 🟢 Normal | Operación correcta |
| **> 85%** | ✅ Excelente | Condiciones ideales |

---

## 🛠️ Recomendaciones Automáticas:

### **Ejemplo: Paneles al 65% de eficiencia**
```
🔧 RECOMENDACIONES:
✓ Limpiar paneles con agua y paño suave
✓ Verificar que no haya sombras de árboles o edificios
✓ Inspeccionar visualmente en busca de daños
✓ Programar limpieza de paneles
```

### **Ejemplo: Turbina al 58% de eficiencia**
```
🔧 RECOMENDACIONES:
✓ Revisar rodamientos y lubricar si es necesario
✓ Inspeccionar palas en busca de daños o suciedad
✓ Verificar alineación del rotor
✓ Apretar todos los tornillos y conexiones
```

---

## 📈 Análisis de Tendencias:

El sistema guarda historial y detecta:
- **DEGRADACIÓN:** Eficiencia cayó >10% → Mantenimiento urgente
- **DISMINUCIÓN:** Eficiencia bajó 5-10% → Monitorear
- **ESTABLE:** Variación <5% → Todo bien
- **MEJORA:** Eficiencia subió >5% → Excelente (post-mantenimiento)

---

## 🔌 Hardware Necesario:

### **Para Paneles Solares:**
```
1. LDR GL5528 ($500)
   └─ Mide luz solar → Irradiancia

2. ACS712 30A ($3,500)
   └─ Mide corriente DC → Potencia

3. DS18B20 ($2,500)
   └─ Mide temperatura ambiente

Total: ~$6,500 por panel de medición
```

### **Para Turbina Eólica:**
```
1. Anemómetro digital ($15,000-25,000)
   └─ Mide velocidad viento
   └─ O usar datos de API (gratis pero menos preciso)

2. ACS712 30A ($3,500)
   └─ Mide corriente DC → Potencia

Total: ~$18,500-28,500
```

---

## 📱 En el Dashboard:

```
╔══════════════════════════════════════════════════════╗
║  MONITOR DE EFICIENCIA REAL                          ║
╠══════════════════════════════════════════════════════╣
║                                                      ║
║  ☀️ PANELES SOLARES                                 ║
║  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  ║
║  Eficiencia: 83.1% ✅ NORMAL                        ║
║                                                      ║
║  📊 Mediciones:                                      ║
║  • Irradiancia: 800 W/m²                            ║
║  • Potencia teórica: 842 W                          ║
║  • Potencia real: 700 W                             ║
║  • Pérdida: 142 W                                   ║
║                                                      ║
║  ✅ Paneles operando correctamente                  ║
║                                                      ║
╠══════════════════════════════════════════════════════╣
║                                                      ║
║  💨 TURBINA EÓLICA                                  ║
║  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  ║
║  Eficiencia: 65% ⚠️ ADVERTENCIA                    ║
║                                                      ║
║  📊 Mediciones:                                      ║
║  • Viento: 10 m/s                                   ║
║  • Potencia teórica: 1000 W                         ║
║  • Potencia real: 650 W                             ║
║  • Pérdida: 350 W                                   ║
║                                                      ║
║  ⚠️ Eficiencia reducida - Revisar turbina          ║
║                                                      ║
║  🔧 RECOMENDACIONES:                                ║
║  • Revisar rodamientos y lubricar                   ║
║  • Inspeccionar palas                               ║
║  • Verificar alineación                             ║
║                                                      ║
╚══════════════════════════════════════════════════════╝
```

---

## 🎯 Ventajas del Sistema:

### ✅ **Detección Proactiva:**
- Detecta problemas ANTES de que fallen componentes
- Ahorra dinero en reparaciones caras
- Maximiza generación de energía

### ✅ **Alertas Inteligentes:**
- No solo dice "está mal", dice QUÉ está mal
- Recomendaciones específicas de mantenimiento
- Priorización (crítico, advertencia, normal)

### ✅ **Datos Reales:**
- Compara con física real (Ley de Betz, eficiencia semiconductores)
- Considera temperatura ambiente
- Ajusta por condiciones reales

### ✅ **ROI Mejorado:**
- Paneles limpios → +20-30% generación
- Turbina mantenida → +15-25% generación
- Vida útil extendida de componentes

---

## 💰 Ejemplo de Ahorro:

### **Sin Monitor:**
```
Paneles sucios (65% eficiencia):
- Generación: 6.5 kWh/día
- Pérdida: 3.5 kWh/día × $50/kWh = $175/día
- Pérdida mensual: $5,250
- NO LO SABES HASTA QUE VES LA FACTURA
```

### **Con Monitor:**
```
Sistema detecta: "⚠️ Paneles al 65% - Necesitan limpieza"
- Limpias los paneles (15 minutos)
- Eficiencia vuelve a 85%
- Ahorras $5,250/mes
- ¡Monitor se paga solo en 1-2 meses!
```

---

## 🔬 Fórmulas Técnicas:

### **Irradiancia Solar:**
```python
# De sensor LDR (resistencia variable con luz)
V_ldr = analogRead(LDR_PIN) * (5.0 / 1023.0)
R_ldr = (10000 * V_ldr) / (5.0 - V_ldr)
Irradiancia_W_m2 = calibration_curve(R_ldr)
```

### **Potencia Solar Teórica:**
```python
# Considerando eficiencia de silicio y temperatura
η_silicon = 0.18  # 18% para policristalino
α_temp = 0.005   # -0.5%/°C
T_ref = 25       # °C

η_real = η_silicon * (1 - α_temp * (T_ambient - T_ref))
P_teorica = Irradiancia * Area * η_real
```

### **Potencia Eólica (Ley de Betz):**
```python
# Potencia del viento
ρ = 1.225  # kg/m³ densidad aire
A = π * (D/2)²  # Área barrido
v = velocidad_viento  # m/s

P_viento = 0.5 * ρ * A * v³
P_teorica = P_viento * 0.45  # 45% eficiencia real
```

---

## 📊 Endpoints de API:

```
GET /api/efficiency/solar
    - Params: irradiancia_w_m2, area_paneles_m2, 
              potencia_generada_w, temperatura_c
    - Return: Eficiencia, diagnóstico, recomendaciones

GET /api/efficiency/wind
    - Params: velocidad_viento_ms, potencia_generada_w,
              potencia_nominal_w
    - Return: Eficiencia, diagnóstico, recomendaciones

GET /api/efficiency/dashboard
    - Params: Todos los anteriores
    - Return: Eficiencia solar + eólica + alertas

GET /api/efficiency/tendencia/{componente}
    - Return: Análisis de tendencia en el tiempo
```

---

## 🚀 Para Implementar:

### **1. Hardware:**
```
Comprar sensores:
- LDR GL5528
- ACS712 30A (x2)
- DS18B20 (x2)
- Anemómetro (opcional)
```

### **2. Conexiones ESP32:**
```
LDR → GPIO34 (ADC)
ACS712 Solar → GPIO35 (ADC)
ACS712 Eólica → GPIO32 (ADC)
DS18B20 → GPIO4 (OneWire)
```

### **3. Calibración:**
```
- Medir irradiancia real con piranómetro
- Ajustar curva de calibración del LDR
- Verificar lecturas de corriente
```

### **4. Ver en Dashboard:**
```
INICIAR_TODO.bat
http://localhost:3002
```

---

## 🎉 ¡Listo!

Ahora el sistema:
- ✅ Detecta paneles sucios automáticamente
- ✅ Detecta problemas en turbina
- ✅ Te dice QUÉ hacer para solucionarlo
- ✅ Maximiza tu generación de energía
- ✅ Ahorra dinero en mantenimiento

**¡Es como tener un ingeniero monitoreando 24/7!** 🔬⚡
