# 🔧 Guía de Configuración Personalizada

## ¿Por qué configurar?

El sistema **SE ADAPTA A TU CASA** específicamente:
- ✅ **Tu consumo real** (no valores genéricos)
- ✅ **Tu ubicación exacta** (sol y viento de tu zona)
- ✅ **Tamaño y tipo de paneles** que vas a usar
- ✅ **Turbina eólica** adecuada para tu región
- ✅ **Batería correctamente dimensionada**

---

## 🚀 Paso 1: Ejecutar Configurador

```cmd
CONFIGURAR_SISTEMA.bat
```

---

## 📋 ¿Qué te va a preguntar?

### 1. **Ubicación**
```
Ciudad: Bahía Blanca
Latitud (ej: -38.7183): -38.7183
Longitud (ej: -62.2663): -62.2663
```

**El sistema:**
- 📡 Obtiene datos climáticos de tu zona de OpenWeather API
- 💨 Calcula viento promedio de tu región
- ☀️ Estima horas de sol según latitud
- 🌡️ Considera temperatura y humedad

### 2. **Consumo de tu Casa**

**Opción A:** Ya lo sabes (de la factura)
```
Consumo diario (kWh/día): 15.6
```

**Opción B:** Consumo mensual
```
Consumo mensual (kWh/mes): 468
```

**Opción C:** Estimarlo
El sistema te pregunta por cada electrodoméstico:
- Heladera
- TV
- Computadora
- Iluminación
- Microondas
- Lavarropas
- Otros

Y **calcula automáticamente** tu consumo total.

### 3. **Recomendación Automática**

El sistema analiza y te recomienda:

```
✅ SISTEMA RECOMENDADO:

☀️  PANELES SOLARES:
   - Cantidad: 6 paneles de 300W
   - Potencia total: 1800W (1.8 kW)
   - Generación estimada: 8.1 kWh/día

💨 TURBINA EÓLICA:
   - 1x 1000W
   - Viento promedio en tu zona: 6.2 m/s
   - Generación estimada: 7.2 kWh/día

🔋 BATERÍA:
   - Capacidad: 48V 100Ah (4.8 kWh)
   - Autonomía: ~10 horas
   - Tipo recomendado: LiFePO4

⚡ INVERSOR:
   - Potencia: 2600W continua
   - Pico: 5200W

📊 BALANCE ENERGÉTICO:
   - Consumo diario: 15.6 kWh
   - Generación estimada: 15.3 kWh/día
   - Cobertura: 98%

   ✅ Sistema bien dimensionado para autonomía total
```

---

## 💾 Archivo de Configuración

Se guarda en: **`configuracion_usuario.json`**

```json
{
  "ubicacion": {
    "latitud": -38.7183,
    "longitud": -62.2663,
    "ciudad": "Bahía Blanca, Argentina",
    "clima_historico": {
      "temperatura_promedio_c": 18,
      "viento_promedio_ms": 6.2,
      "viento_maximo_ms": 15.3
    }
  },
  "consumo": {
    "promedio_diario_kwh": 15.6,
    "promedio_watts": 650
  },
  "paneles_solares": {
    "cantidad": 6,
    "potencia_por_panel_w": 300,
    "potencia_total_w": 1800
  },
  "turbina_eolica": {
    "cantidad": 1,
    "potencia_nominal_w": 1000
  },
  "bateria": {
    "voltaje_nominal": 48,
    "capacidad_ah": 100,
    "capacidad_kwh": 4.8
  }
}
```

---

## 🔄 Uso de la Configuración

Una vez configurado, el sistema:

1. **Lee automáticamente** `configuracion_usuario.json` al iniciar
2. **Usa tus valores reales** en todos los cálculos
3. **Muestra en el dashboard** tu configuración específica
4. **IA aprende** basándose en tu consumo real

### Endpoint de API:

```
GET http://localhost:8801/api/configuracion/usuario
```

Respuesta:
```json
{
  "status": "success",
  "configurado": true,
  "configuracion": { ... }
}
```

---

## ✏️ Editar Configuración

### Opción 1: Reconfigurar (recomendado)
```cmd
CONFIGURAR_SISTEMA.bat
```

### Opción 2: Editar manualmente
Abre `configuracion_usuario.json` con un editor de texto y modifica los valores.

**Reinicia el sistema** después de cambios:
```cmd
DETENER_TODO.bat
INICIAR_TODO.bat
```

---

## 🎯 Ventajas de Configurar

### Sin Configuración:
❌ Usa valores genéricos
❌ No considera tu clima
❌ Puede subdimensionar o sobredimensionar
❌ Recomendaciones inexactas

### Con Configuración:
✅ **Dimensionamiento exacto** para tu caso
✅ **Datos climáticos reales** de tu zona
✅ **Cobertura calculada** con precisión
✅ **ROI real** basado en tu consumo
✅ **Dashboard personalizado** con tus componentes

---

## 📊 Ejemplo Real: Bahía Blanca

```
Ubicación: -38.7183, -62.2663
Consumo: 15.6 kWh/día (650W promedio)
Viento promedio: 6.2 m/s

RECOMENDACIÓN:
✅ 6 paneles de 300W = 1800W
✅ 1 turbina de 1000W
✅ Batería 48V 100Ah (4.8 kWh)
✅ Inversor 2600W

GENERACIÓN TOTAL: 15.3 kWh/día
COBERTURA: 98% ✅
AUTONOMÍA: 10 horas

PRESUPUESTO ESTIMADO: $1,850,000 ARS
```

---

## 🆘 Preguntas Frecuentes

### ¿Puedo cambiar la configuración después?
**Sí**, ejecuta `CONFIGURAR_SISTEMA.bat` de nuevo o edita `configuracion_usuario.json`.

### ¿Qué pasa si no configuro?
El sistema usa valores por defecto genéricos. Funciona, pero no está optimizado para tu caso.

### ¿Cómo sé mi consumo?
Mira tu factura de luz:
- **kWh/mes** → divide entre 30 = kWh/día
- Si no la tienes, usa el estimador del configurador

### ¿Cómo obtengo mi latitud/longitud?
- Google Maps: Click derecho → copiar coordenadas
- O busca tu ciudad en Google: "latitud longitud [tu ciudad]"

### ¿El sistema obtiene datos climáticos reales?
**Sí**, usa OpenWeather API para obtener:
- Viento promedio de tu zona
- Temperatura
- Pronóstico 5 días

---

## 🎉 ¡Listo!

Después de configurar:

1. ✅ Archivo `configuracion_usuario.json` creado
2. ✅ Sistema personalizado para tu casa
3. ✅ Ejecuta `INICIAR_TODO.bat`
4. ✅ Dashboard muestra TU configuración

**El sistema ahora está optimizado específicamente para ti.** 🚀
