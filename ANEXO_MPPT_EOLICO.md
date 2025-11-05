# 🎯 Anexo - MPPT Eólico Implementación

## 1. ¿Por qué MPPT en Eólico?

A diferencia de paneles solares (voltaje casi constante), los aerogeneradores tienen voltaje y frecuencia variables con RPM. El MPPT eólico ajusta la carga para mantener la turbina en su **TSR óptimo** (Tip Speed Ratio).

**TSR óptimo**: Relación entre velocidad punta de pala y velocidad del viento.
```
TSR = (ω × R) / v

Donde:
ω = velocidad angular (rad/s)
R = radio pala (m)
v = velocidad viento (m/s)

TSR_óptimo ≈ 6-8 para turbinas pequeñas
```

---

## 2. Algoritmo Perturb & Observe (P&O)

**Pseudocódigo**:
```cpp
float duty_cycle = 0.5;  // PWM DC/DC inicial 50%
float P_anterior = 0;
float delta_duty = 0.01;  // Paso 1%

void loop_MPPT() {
  float V = leerVoltaje();
  float I = leerCorriente();
  float P = V * I;
  
  if (P > P_anterior) {
    // Potencia aumentó, seguir en misma dirección
    duty_cycle += delta_duty;
  } else {
    // Potencia disminuyó, invertir dirección
    delta_duty = -delta_duty;
    duty_cycle += delta_duty;
  }
  
  duty_cycle = constrain(duty_cycle, 0.2, 0.9);
  analogWrite(PIN_PWM_DCDC, duty_cycle * 255);
  
  P_anterior = P;
  delay(100);  // Ejecutar cada 100ms
}
```

---

## 3. Implementación con ESP32

**Hardware adicional**:
- DC/DC con entrada PWM (ej. módulo con pin EN o FB)
- O construir DC/DC con MOSFET + driver controlado por ESP32

**Firmware** (`sensors.h`):
```cpp
// Variables globales MPPT
float mppt_duty = 0.5;
float mppt_P_prev = 0;
float mppt_delta = 0.01;

void mppt_eolico() {
  float V = sensores.v_wind_v_dc;
  float I = sensores.corriente_eolica;
  float P = V * I;
  
  if (P > mppt_P_prev + 0.5) {  // Umbral 0.5W para evitar oscilación
    mppt_duty += mppt_delta;
  } else if (P < mppt_P_prev - 0.5) {
    mppt_delta = -mppt_delta;
    mppt_duty += mppt_delta;
  }
  
  mppt_duty = constrain(mppt_duty, 0.3, 0.9);
  ledcWrite(PWM_CHANNEL_MPPT, mppt_duty * 255);
  
  mppt_P_prev = P;
  
  #if DEBUG_MPPT
  Serial.printf("[MPPT] P=%.1fW duty=%.2f delta=%.3f\n", P, mppt_duty, mppt_delta);
  #endif
}
```

**Configuración PWM ESP32** (`config.h`):
```cpp
#define PWM_CHANNEL_MPPT 0
#define PWM_FREQ_MPPT 25000  // 25 kHz
#define PWM_RESOLUTION_MPPT 8  // 8-bit (0-255)
#define PIN_PWM_MPPT 25  // GPIO25

// En setup():
ledcSetup(PWM_CHANNEL_MPPT, PWM_FREQ_MPPT, PWM_RESOLUTION_MPPT);
ledcAttachPin(PIN_PWM_MPPT, PWM_CHANNEL_MPPT);
```

**Llamar en loop principal**:
```cpp
void loop() {
  static unsigned long lastMPPT = 0;
  
  if (millis() - lastMPPT >= 100) {  // Cada 100ms
    mppt_eolico();
    lastMPPT = millis();
  }
  
  // ... resto del código
}
```

---

## 4. Beneficios Medibles

**Sin MPPT** (carga fija):
- Potencia promedio: 50W a 6 m/s viento

**Con MPPT**:
- Potencia promedio: 65W a 6 m/s viento
- **Mejora**: +30%

**Energía adicional por día**:
```
ΔE = (65W - 50W) × 6h = 90 Wh/día
ΔE_año = 90 × 365 = 32.85 kWh/año
```

---

## 5. Alternativa: MPPT por RPM

Si tienes anemómetro, puedes calcular RPM óptimo directamente:

```cpp
float calcular_rpm_optimo(float velocidad_viento) {
  // TSR óptimo = 7, radio pala = 0.6m
  float omega_opt = (7 * velocidad_viento) / 0.6;  // rad/s
  float rpm_opt = omega_opt * 60 / (2 * PI);  // RPM
  return rpm_opt;
}

void mppt_por_rpm() {
  float v_viento = sensores.velocidad_viento;  // De anemómetro
  float rpm_objetivo = calcular_rpm_optimo(v_viento);
  float rpm_actual = sensores.turbine_rpm;
  
  if (rpm_actual < rpm_objetivo) {
    mppt_duty -= 0.01;  // Reducir carga → aumentar RPM
  } else {
    mppt_duty += 0.01;  // Aumentar carga → reducir RPM
  }
  
  mppt_duty = constrain(mppt_duty, 0.3, 0.9);
  ledcWrite(PWM_CHANNEL_MPPT, mppt_duty * 255);
}
```

---

**Complementa**: `PLAN_ELECTRONICA_POTENCIA_DETALLADO.md`
