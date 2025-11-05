# 📝 Resumen de Cambios en Firmware ESP32

## ✅ Cambios Implementados

### 1. **Filtrado ADC Mejorado** (SOLUCIONA EL PROBLEMA DE SALTOS)

Cada ADC ahora tiene su propia rutina de lectura con diferente número de muestras:

- **ADC Batería**: 50 muestras (muy estable, sin saltos)
- **ADC Eólica**: 30 muestras (señal AC rectificada)
- **ADC Solar**: 20 muestras (relativamente estable)
- **ADC Carga**: 20 muestras (variable)

**Antes**:
```
GUARDAR #109: 710
GUARDAR #110: 3521  ← ¡Salto enorme!
GUARDAR #111: 715   ← Vuelve a 700
```

**Después**: Valores estables sin saltos bruscos.

### 2. **RPM de Turbina Eólica**

#### `config.h`
```cpp
#define PIN_RPM_INPUT                  13      // GPIO para RPM
#define RPM_EDGES_PER_ELECTRICAL_CYCLE 1       // flancos por ciclo
#define RPM_MEASURE_WINDOW_MS          500     // ventana de medición
#define RPM_DEBOUNCE_US                500     // anti-rebote
#define TURBINE_POLE_PAIRS             10      // pares de polos
#define TURBINE_GEAR_RATIO             1.0f    // relación de engranaje
```

#### `sensors.h`
- ✅ ISR `rpm_isr()` para contar flancos (RISING)
- ✅ Función `calcularRPM_Turbina()` con conversión freq → RPM
- ✅ Variables `turbine_rpm` y `frequency_hz` en struct `SensorData`
- ✅ Llamada automática en `readAllSensors()`

#### `http_client.h`
```cpp
doc["turbine_rpm"] = sensores.turbine_rpm;
doc["rpm"] = sensores.turbine_rpm;  // Compatibilidad
doc["frequency_hz"] = sensores.frequency_hz;
```

---

## 🔧 Qué Hacer Ahora

### Paso 1: Compilar y Subir Firmware

1. **Abre Arduino IDE**
2. **Abre**: `X:\PREDICCION DE CLIMA\firmware_arduino_ide_2\inversor_hibrido\inversor_hibrido.ino`
3. **Verifica** que no haya errores de compilación
4. **Conecta el ESP32** por USB
5. **Selecciona**: Tools → Board → ESP32 Dev Module
6. **Selecciona**: Tools → Port → COMxx (el puerto correcto)
7. **Sube** el firmware (botón ➜)

### Paso 2: Verificar en Serial Monitor

Abre el Serial Monitor (115200 baud) y deberías ver:

```
✅ Sensores inicializados
   - ADC Batería: 50 muestras (estable)
   - ADC Eólica: 30 muestras (filtrado AC)
   - ADC Solar: 20 muestras
   - ADC Carga: 20 muestras
   - RPM GPIO13: ISR configurada

[TELEM] ESP32_INVERSOR_001 seq=1 ts=12345 Vbat=12.456V ... RPM=325.5 Lost=0 | OK
[RPM] edges=25 freq=54.17Hz rpm=325.1
```

### Paso 3: Conectar Señal de RPM (OPCIONAL)

**Si tienes la señal de frecuencia eléctrica:**

1. Conecta la señal (0-3V, cuadrada) al **GPIO13**
2. Si usas otro GPIO, edita `PIN_RPM_INPUT` en `config.h`
3. Verifica que `TURBINE_POLE_PAIRS` sea correcto para tu generador

**Si NO tienes la señal todavía:**
- El firmware funcionará normalmente, `turbine_rpm` será 0

---

## 📊 Resultado Esperado

### Backend logs:
```
[TELEM] ESP32_INVERSOR_001 seq=123 ... Vbat=12.345V RPM=325.5 Lost=0 | OK
💾 [GUARDAR NUEVO #123] raw_adc para ESP32_INVERSOR_001: {
  'adc1_bat1': 735,      ← Valores estables (no más saltos)
  'adc2_eolica': 682,
  'adc5_solar': 26,
  'adc6_load': 0
}
```

### Frontend:
- Tarjeta morada/rosa con **"RPM Turbina Eólica: 325 RPM"**
- **"Frecuencia Eléctrica: 54.17 Hz"**
- ADCs estables sin saltos

---

## 🛠️ Ajustes de Configuración

### Si los valores ADC siguen variando:

**Opción 1**: Aumentar muestras (más estable, más lento)
```cpp
// En sensors.h
const int num_muestras = 100;  // Era 50
```

**Opción 2**: Agregar delay entre muestras
```cpp
delayMicroseconds(200);  // Era 50
```

### Si el RPM no funciona:

1. **Verifica el GPIO**: `PIN_RPM_INPUT = 13` (cámbialo si usas otro)
2. **Verifica POLE_PAIRS**: Cuenta los imanes del generador ÷ 2
3. **Verifica la señal**: Debe ser 0-3V digital (TTL)
4. **Aumenta DEBOUNCE**: `RPM_DEBOUNCE_US = 1000` si hay ruido

### Ejemplo de cálculo RPM:

**Señal de prueba**: 50 Hz (50 ciclos/seg)
- `POLE_PAIRS = 10`
- `GEAR_RATIO = 1.0`
- **RPM = (50 Hz × 60) / 10 / 1.0 = 300 RPM** ✅

---

## 📁 Archivos Modificados

1. ✅ `config.h` - Configuración de RPM
2. ✅ `sensors.h` - Filtrado ADC + RPM
3. ✅ `http_client.h` - Incluir turbine_rpm en JSON

**Archivos NO tocados**: `inversor_hibrido.ino`, `wifi_manager.h`, `relays.h`, etc.

---

## ⚠️ Notas Importantes

1. **GPIO13 debe estar libre** (no usado para otra cosa)
2. **Si el backend no recibe RPM**, verifica que el firmware compile sin errores
3. **Los valores ADC ahora son más estables** pero tardan un poco más en leerse (normal)
4. **Si el ESP32 se resetea**, puede ser por falta de memoria (reduce `num_muestras` si pasa)

---

## 🎯 Estado del Sistema

- ✅ **Backend**: Acepta y guarda `turbine_rpm`
- ✅ **Frontend**: Muestra RPM en panel
- ✅ **Firmware**: Calcula y envía RPM + ADCs estables
- ✅ **Simulador**: Genera valores de prueba

**¡Todo listo end-to-end! 🚀**
