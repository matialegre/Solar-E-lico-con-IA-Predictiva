# 🔧 Modo 2: Tengo Componentes → ¿Qué Puedo Alimentar?

## 🎯 ¿Para qué sirve este modo?

Si **YA TIENES** paneles solares, turbina eólica o batería instalados, este modo te dice:
- ⚡ **Cuánta potencia** puedes alimentar continuamente
- 📊 **Cuánta energía** vas a generar por día
- 🔋 **Cuántas horas** de autonomía tienes
- 💡 **Ejemplos** de qué electrodomésticos puedes usar

---

## 🚀 Cómo Usarlo:

### 1. Ejecutar Configurador:
```cmd
CONFIGURAR_SISTEMA.bat
```

### 2. Seleccionar Modo 2:
```
Selecciona modo (1/2): 2
```

### 3. El sistema te pregunta:

#### 📍 **Ubicación** (para obtener datos climáticos):
```
Ciudad: Bahía Blanca
Latitud: -38.7183
Longitud: -62.2663
```
→ El sistema obtiene viento y sol de tu zona desde OpenWeather API

#### ☀️ **¿Tienes paneles solares?**
```
¿Tienes paneles solares? (s/n): s
¿Cuántos paneles?: 4
¿Potencia de cada panel (W)? (ej: 300): 300
```

#### 💨 **¿Tienes turbina eólica?**
```
¿Tienes turbina eólica? (s/n): s
¿Potencia nominal (W)? (ej: 1000): 1000
```

#### 🔋 **¿Tienes batería?**
```
¿Tienes batería? (s/n): s
¿Voltaje (V)? (ej: 12, 24, 48): 48
¿Capacidad (Ah)? (ej: 100): 100
```

---

## 📊 Ejemplo de Salida:

```
✅ ANÁLISIS DE TU SISTEMA:

📊 GENERACIÓN ESTIMADA:
   ☀️  Solar: 4.3 kWh/día (180 W promedio)
   💨 Eólica: 6.0 kWh/día (250 W promedio)
   ⚡ TOTAL: 10.3 kWh/día (430 W promedio)

🔋 BATERÍA:
   • Capacidad: 4.8 kWh
   • Capacidad útil (80%): 3.8 kWh
   • Autonomía estimada: 8.8 horas

⚡ POTENCIA QUE PUEDES ALIMENTAR:
   • Continua (24h): 300 W
   • Picos cortos: 645 W

📱 EJEMPLOS DE LO QUE PUEDES ALIMENTAR CON 300 W:
   ✅ Heladera + iluminación LED + cargadores
```

---

## 🧮 Cómo Se Calcula:

### **Generación Solar:**
```python
Horas de sol = f(latitud)  # 4-6 horas en Argentina
Generación = Paneles (W) × Horas sol × 0.8 (eficiencia)
```

### **Generación Eólica:**
```python
Factor capacidad = f(viento promedio zona)
  - Viento >= 8 m/s → 35%
  - Viento >= 6 m/s → 25%
  - Viento < 6 m/s → 15%

Generación = Turbina (W) × 24h × Factor
```

### **Potencia Continua:**
```python
Potencia recomendada = Generación promedio × 0.7
  (Factor conservador para no descargar batería)
```

---

## 💾 Archivo Generado:

`configuracion_usuario.json`:
```json
{
  "modo": "componentes_existentes",
  "componentes": {
    "paneles": {
      "cantidad": 4,
      "potencia_w": 300,
      "potencia_total_w": 1200
    },
    "turbina": {
      "potencia_w": 1000
    },
    "bateria": {
      "voltaje": 48,
      "ah": 100,
      "kwh": 4.8
    }
  },
  "capacidad_sistema": {
    "generacion_total_dia_kwh": 10.3,
    "potencia_continua_recomendada_w": 300,
    "potencia_pico_max_w": 645,
    "autonomia_horas": 8.8
  }
}
```

---

## 📱 En el Dashboard:

Al iniciar el sistema, verás:

```
╔═══════════════════════════════════════════════════════╗
║  Tu Sistema Configurado ✅                            ║
║                                                       ║
║  ☀️ Paneles: 4x 300W (1.2 kW)                       ║
║  💨 Turbina: 1x 1000W                               ║
║  🔋 Batería: 48V 100Ah (4.8 kWh)                    ║
║                                                       ║
║  ⚡ CAPACIDAD:                                        ║
║  • Continua: 300 W                                   ║
║  • Picos: 645 W                                      ║
║  • Generación: 10.3 kWh/día                         ║
║  • Autonomía: 8.8 horas                              ║
╚═══════════════════════════════════════════════════════╝
```

---

## 🎯 Casos de Uso:

### **Caso 1: Sistema pequeño existente**
```
Input:
- 2 paneles de 150W
- Sin turbina
- Batería 12V 50Ah

Output:
- 1.4 kWh/día
- 65 W continuos
- "Iluminación LED + cargadores + laptop"
```

### **Caso 2: Sistema medio**
```
Input:
- 4 paneles de 300W
- Turbina 1000W
- Batería 48V 100Ah

Output:
- 10.3 kWh/día
- 300 W continuos
- "Heladera + TV + iluminación + cargadores"
```

### **Caso 3: Sistema grande**
```
Input:
- 8 paneles de 300W
- Turbina 2000W
- Batería 48V 200Ah

Output:
- 22.6 kWh/día
- 660 W continuos
- "Casa completa pequeña"
```

---

## ⚠️ Notas Importantes:

1. **Factor conservador (70%):** Para no descargar la batería completamente
2. **Datos climáticos reales:** Usa API para calcular según TU zona
3. **Picos cortos:** Puedes usar más watts por períodos breves (microondas, etc.)
4. **Sin batería:** Solo tendrás energía cuando haya sol/viento

---

## 🔄 Diferencias entre Modo 1 y Modo 2:

| Modo 1: Consumo → Componentes | Modo 2: Componentes → Potencia |
|-------------------------------|--------------------------------|
| Dices cuánto consumís | Dices qué componentes tenés |
| Te recomienda qué comprar | Te dice qué podés alimentar |
| Para planificar compra | Para usar lo que ya tenés |
| Output: Lista de shopping | Output: Potencia disponible |

---

## 🎉 ¡Listo!

Ahora el sistema tiene **2 formas de configurarse**:
1. **Planificación:** Dime consumo → Te recomiendo componentes
2. **Evaluación:** Dime componentes → Te digo capacidad

**Ejecuta:** `CONFIGURAR_SISTEMA.bat` y selecciona el modo que necesites.
