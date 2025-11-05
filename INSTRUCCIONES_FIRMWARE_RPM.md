# Instrucciones para implementar RPM en el Firmware ESP32

## Objetivo
Integrar la medición de frecuencia → RPM desde una señal digital 0–3V (alto en semiciclo positivo, bajo en negativo) en el firmware del ESP32.

---

## 1. Configuración en `config.h`

Agregar estos `#define` junto a los pines/parametría del sistema:

```cpp
// ===== RPM (frecuencia eléctrica -> RPM) =====
// Señal 0–3 V: HIGH en semiciclo positivo, LOW en negativo.
// Contaremos flanco ascendente (RISING) => 1 flanco por ciclo eléctrico.
#define PIN_RPM_INPUT                  13      // GPIO para RPM (ajustar según tu hardware)
#define RPM_EDGES_PER_ELECTRICAL_CYCLE 1       // flancos útiles por ciclo eléctrico (1 = RISING por semiciclo positivo)
#define RPM_MEASURE_WINDOW_MS          500     // ventana de integración (ms)
#define RPM_DEBOUNCE_US                500     // anti-rebote por ruido (µs)

// Conversión frecuencia eléctrica -> RPM mecánica:
//   RPM = (freq_electrica_Hz * 60) / POLE_PAIRS / GEAR_RATIO
// POLE_PAIRS: pares de polos del generador. GEAR_RATIO: 1.0 si es directo.
#define TURBINE_POLE_PAIRS             10      // ⚠️ Configurable por proyecto
#define TURBINE_GEAR_RATIO             1.0f    // 1.0 = acople directo
```

---

## 2. Variables globales y ISR (en `sensors.cpp` o donde midas sensores)

Agregar estas variables/ISR:

```cpp
#include "config.h"
extern "C" { #include "esp_timer.h" }

// Variables globales para conteo de RPM
volatile uint32_t rpm_edge_count = 0;
volatile uint64_t rpm_last_edge_us = 0;
static float rpm_current = 0.0f;

// ISR para contar flancos (IRAM_ATTR para que esté en RAM rápida)
IRAM_ATTR void rpm_isr() {
  const uint64_t now = esp_timer_get_time(); // µs
  if (now - rpm_last_edge_us >= RPM_DEBOUNCE_US) {
    rpm_edge_count++;
    rpm_last_edge_us = now;
  }
}
```

---

## 3. Inicialización (en `init_sensors()` o `setupSensors()`)

```cpp
// === Entrada RPM por flanco ascendente (0–3 V) ===
pinMode(PIN_RPM_INPUT, INPUT); // usar INPUT_PULLDOWN si la etapa lo requiere
attachInterrupt(digitalPinToInterrupt(PIN_RPM_INPUT), rpm_isr, RISING);
```

---

## 4. Cálculo periódico (en tu loop de sensado)

```cpp
// === Cálculo de frecuencia y RPM ===
static uint32_t window_ms_start = millis();
const uint32_t now_ms = millis();

if (now_ms - window_ms_start >= RPM_MEASURE_WINDOW_MS) {
  // Leer y resetear contador de flancos
  noInterrupts();
  uint32_t edges = rpm_edge_count;
  rpm_edge_count = 0;
  interrupts();

  // Calcular frecuencia eléctrica
  const float window_s = (float)RPM_MEASURE_WINDOW_MS / 1000.0f;
  float freq_electrica_hz = 0.0f;
  
  if (RPM_EDGES_PER_ELECTRICAL_CYCLE > 0 && window_s > 0.0f) {
    freq_electrica_hz = (edges / (float)RPM_EDGES_PER_ELECTRICAL_CYCLE) / window_s;
  }

  // Convertir frecuencia eléctrica a RPM mecánica
  if (TURBINE_POLE_PAIRS > 0 && TURBINE_GEAR_RATIO > 0.0f) {
    rpm_current = (freq_electrica_hz * 60.0f) / ((float)TURBINE_POLE_PAIRS * TURBINE_GEAR_RATIO);
  } else {
    rpm_current = 0.0f;
  }

  #if DEBUG_SENSORS
  Serial.printf("[RPM] edges=%u freq=%.2fHz rpm=%.1f\n", edges, freq_electrica_hz, rpm_current);
  #endif

  window_ms_start = now_ms;
}
```

---

## 5. Telemetría HTTP - Incluir `turbine_rpm`

En la función que arma el JSON del POST (donde ya envías `battery_voltage`, etc.):

```cpp
payload["battery_voltage"] = battery_voltage;
payload["solar_current"]   = solar_current;
payload["wind_speed_ms"]   = wind_speed_ms;
payload["irradiance_wm2"]  = irradiance;
payload["turbine_rpm"]     = rpm_current;  // ← NUEVO
```

Si usas ArduinoJson, aumentar capacidad del `DynamicJsonDocument` si es necesario.

---

## 6. Ejemplo de validación

**Con una señal de prueba de 50 Hz:**
- `TURBINE_POLE_PAIRS = 10`
- `GEAR_RATIO = 1.0`
- **RPM esperado ≈ 300 RPM**

Cálculo: `(50 Hz × 60) / 10 / 1.0 = 300 RPM`

---

## 7. Logs esperados en Serial

```
[RPM] edges=25 freq=50.00Hz rpm=300.0
[TELEM] ESP32_INVERSOR_001 seq=123 Vbat=12.345V ... RPM=300.0 Lost=0 | OK
```

---

## Backend y Frontend ya están listos ✅

- **Backend** acepta, guarda y sirve `turbine_rpm` ✅
- **Frontend** muestra RPM en tiempo real ✅
- **Simulador** genera valores de prueba ✅

**Solo falta implementar estas modificaciones en el firmware ESP32.**

---

## Notas importantes

- Si tu generador tiene un número diferente de pares de polos, ajusta `TURBINE_POLE_PAIRS`
- Si hay ruido en la señal, aumenta `RPM_DEBOUNCE_US`
- Si la señal es muy rápida (>1 kHz), reduce `RPM_MEASURE_WINDOW_MS` a 200-300ms
- El GPIO13 es solo un ejemplo, usa el GPIO que tengas disponible en tu PCB
