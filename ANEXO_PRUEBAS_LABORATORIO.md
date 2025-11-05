# 🧪 Anexo - Pruebas de Laboratorio Detalladas

## 1. Prueba de Rectificador Trifásico

**Objetivo**: Verificar conversión AC → DC y ripple.

**Equipo necesario**:
- Osciloscopio (o módulo DSO138)
- Multímetro
- Fuente AC variable (o generador)
- Cargas resistivas

**Procedimiento**:
1. Aplicar 18V AC trifásico a entrada rectificador
2. Medir voltaje DC salida (esperado: ~24V)
3. Conectar osciloscopio a salida:
   - Canal 1: Voltaje DC
   - Observar ripple (debe ser <5% = 1.2Vpp)
4. Si ripple alto → Aumentar capacitor filtro
5. Medir temperatura diodos tras 10 min (no exceder 60°C)
6. Probar con diferentes cargas (0A, 5A, 10A, 15A)

**Tabla de resultados**:
| Carga (A) | V_DC (V) | Ripple (Vpp) | Temp diodos (°C) | Estado |
|-----------|----------|--------------|------------------|--------|
| 0 | 24.3 | 0.5 | 25 | ✅ |
| 5 | 23.8 | 0.8 | 35 | ✅ |
| 10 | 23.2 | 1.1 | 48 | ✅ |
| 15 | 22.5 | 1.5 | 58 | ✅ |
| 20 | 21.8 | 2.0 | 65 | ⚠️ Límite |

**Criterio aprobación**: V_DC = 1.35 × V_AC ±5%, ripple <5%, temp <60°C

---

## 2. Prueba de DC/DC con Carga Variable

**Objetivo**: Validar regulación 14V bajo diferentes corrientes.

**Procedimiento**:
1. Configurar fuente entrada 12V (simular batería baja)
2. Conectar carga resistiva variable (reóstato 0-10Ω)
3. Ajustar carga para corrientes: 1A, 3A, 5A, 8A, 10A
4. Medir voltaje salida en cada paso
5. Medir temperatura DC/DC
6. Calcular eficiencia: η = (V_out × I_out) / (V_in × I_in)

**Tabla resultados**:
| I_out (A) | V_out (V) | V_in (V) | I_in (A) | P_in (W) | P_out (W) | η (%) | Temp (°C) |
|-----------|-----------|----------|----------|----------|-----------|-------|-----------|
| 1 | 14.0 | 12.0 | 1.2 | 14.4 | 14.0 | 97 | 35 |
| 3 | 14.0 | 12.0 | 3.6 | 43.2 | 42.0 | 97 | 42 |
| 5 | 13.9 | 12.0 | 6.1 | 73.2 | 69.5 | 95 | 55 |
| 8 | 13.8 | 12.0 | 9.8 | 117.6 | 110.4 | 94 | 68 |
| 10 | 13.7 | 12.0 | 12.3 | 147.6 | 137.0 | 93 | 75 |

**Criterio aprobación**: η >85% hasta 8A, temp <70°C

**Pruebas adicionales**:
- Variación V_in: 8V, 10V, 12V, 15V, 20V, 25V
- Verificar regulación en todos los casos
- Probar transitorios (cambio brusco de carga)

---

## 3. Prueba de Inversor con Heladera Real

**Objetivo**: Validar arranque de compresor y operación continua.

**Procedimiento**:
1. Conectar batería 12V 100Ah cargada al inversor
2. Conectar heladera al inversor (sin otras cargas)
3. Encender heladera y registrar:
   - Corriente pico arranque (usar pinza amperimétrica)
   - Duración pico (típico 2-5 segundos)
   - Corriente operación normal
4. Dejar heladera 2 horas y registrar:
   - Ciclos ON/OFF del compresor
   - Duración cada ciclo
   - Voltaje batería al inicio y final
5. Calcular consumo real

**Datos esperados**:
- Corriente pico: 40-60A DC (480-720W)
- Corriente operación: 8-12A DC (96-144W)
- Ciclo trabajo: 30-40%
- Consumo 2h: 0.15-0.25 kWh

**Registro temporal**:
| Tiempo | Estado | I_DC (A) | V_bat (V) | P (W) | Notas |
|--------|--------|----------|-----------|-------|-------|
| 0:00 | OFF | 0.5 | 12.8 | 6 | Standby |
| 0:01 | ARRANQUE | 55 | 12.2 | 671 | Pico 3s |
| 0:05 | ON | 10 | 12.6 | 126 | Normal |
| 0:15 | ON | 10 | 12.5 | 125 | Normal |
| 0:20 | OFF | 0.5 | 12.7 | 6 | Ciclo completo |
| 0:35 | ARRANQUE | 52 | 12.3 | 640 | 2do ciclo |

**Cálculo consumo**:
```
E = (V_inicial - V_final) × Ah_batería × η_descarga
E = (12.8 - 12.3) × 100 × 0.9 = 45 Wh (2 horas)
→ Consumo diario estimado: 45 × 12 = 540 Wh
```

---

## 4. Prueba de Dump Load (Sobrevoltaje)

**Objetivo**: Verificar activación automática y disipación.

**Procedimiento**:
1. Simular sobrevoltaje con fuente ajustable
2. Aumentar voltaje lentamente: 14V → 15V → 16V
3. Verificar activación relé dump load a 16.0V
4. Medir corriente en resistencia: I = V / R
5. Medir potencia disipada: P = V² / R
6. Medir temperatura resistencia cada minuto
7. Reducir voltaje a 14V → Verificar desactivación

**Tabla temporal**:
| Tiempo (min) | V (V) | I (A) | P (W) | Temp resistencia (°C) | Estado relé |
|--------------|-------|-------|-------|-----------------------|-------------|
| 0 | 14.0 | 0 | 0 | 25 | OFF |
| 1 | 15.0 | 0 | 0 | 25 | OFF |
| 2 | 16.0 | 16 | 256 | 35 | ON ✅ |
| 3 | 16.0 | 16 | 256 | 55 | ON |
| 5 | 16.0 | 16 | 256 | 85 | ON |
| 10 | 16.0 | 16 | 256 | 125 | ON |
| 11 | 14.0 | 0 | 0 | 115 | OFF ✅ |
| 15 | 14.0 | 0 | 0 | 65 | OFF |

**Criterio aprobación**: 
- Activación precisa a 16.0V ±0.2V
- Temp <150°C tras 10 min
- Desactivación correcta al bajar voltaje

---

## 5. Prueba de Protección Descarga Profunda

**Objetivo**: Verificar desconexión inversor a voltaje mínimo.

**Procedimiento**:
1. Conectar batería parcialmente descargada (12.5V)
2. Conectar carga 100W al inversor
3. Dejar descargar batería monitoreando voltaje
4. Verificar que ESP32 desconecta inversor a 11.5V
5. Confirmar LED/relé indica estado "descarga profunda"
6. Recargar batería y verificar reconexión automática a 12.5V

**Registro descarga**:
| Tiempo (min) | V_bat (V) | I_carga (A) | Estado inversor | Acción ESP32 |
|--------------|-----------|-------------|-----------------|--------------|
| 0 | 12.5 | 8.5 | ON | Normal |
| 10 | 12.2 | 8.7 | ON | Normal |
| 20 | 11.9 | 9.0 | ON | Normal |
| 30 | 11.6 | 9.2 | ON | Alerta |
| 35 | 11.5 | 0 | OFF ✅ | Desconectado |
| 40 | 11.5 | 0 | OFF | Protegido |

**Recarga y reconexión**:
| Tiempo (min) | V_bat (V) | Estado inversor | Acción ESP32 |
|--------------|-----------|-----------------|--------------|
| 0 | 11.5 | OFF | Cargando |
| 30 | 12.0 | OFF | Cargando |
| 60 | 12.5 | ON ✅ | Reconectado |

**Criterio aprobación**: 
- Desconexión a 11.5V ±0.1V
- Reconexión a 12.5V ±0.1V
- Sin oscilación (histéresis correcta)

---

## 6. Prueba de Sensores (Calibración)

### 6.1 Voltaje

**Procedimiento**:
1. Aplicar voltajes conocidos: 5.0V, 10.0V, 12.0V, 14.0V, 16.0V
2. Comparar lectura ESP32 vs multímetro calibrado
3. Calcular error: ε = (V_ESP32 - V_real) / V_real × 100%
4. Ajustar `VOLTAJE_FACTOR` en `config.h` si necesario

**Tabla calibración**:
| V_real (V) | V_ESP32 (V) | Error (%) | ADC raw | Estado |
|------------|-------------|-----------|---------|--------|
| 5.00 | 5.02 | +0.4 | 1560 | ✅ |
| 10.00 | 10.05 | +0.5 | 3125 | ✅ |
| 12.00 | 12.03 | +0.25 | 3740 | ✅ |
| 14.00 | 14.06 | +0.43 | 4370 | ✅ |
| 16.00 | 16.10 | +0.63 | 5005 | ⚠️ Ajustar |

**Ajuste**:
```cpp
// config.h
// ANTES
#define VOLTAJE_FACTOR 0.00322  // 3.3V / 1024

// DESPUÉS (corregir +0.5% error promedio)
#define VOLTAJE_FACTOR 0.00320  // Reducir 0.6%
```

### 6.2 Corriente (Sensor Hall ACS758)

**Procedimiento**:
1. Conectar carga resistiva conocida (ej. 10Ω)
2. Medir corriente con pinza amperimétrica calibrada
3. Comparar con lectura ESP32
4. Ajustar offset y ganancia

**Tabla calibración**:
| I_real (A) | I_ESP32 (A) | Error (%) | ADC raw | V_sensor (V) |
|------------|-------------|-----------|---------|--------------|
| 0.0 | 0.05 | - | 2048 | 2.50 | ← Offset
| 5.0 | 5.12 | +2.4 | 2560 | 2.75 |
| 10.0 | 10.18 | +1.8 | 3072 | 3.00 |
| 15.0 | 15.25 | +1.7 | 3584 | 3.25 |
| 20.0 | 20.35 | +1.75 | 4096 | 3.50 |

**Ajuste firmware**:
```cpp
// sensors.h
float leerCorriente(int pin) {
  int adc_raw = analogRead(pin);
  float V_sensor = adc_raw * 3.3 / 4095.0;
  
  // ACS758-50A: 40mV/A, Vcc/2 = 2.5V
  float I = (V_sensor - 2.50) / 0.040;  // Offset 2.50V, ganancia 40mV/A
  
  return I;
}
```

---

## 7. Prueba de Integración Completa

**Objetivo**: Validar sistema completo funcionando.

**Setup**:
```
Fuente AC variable (aerogenerador simulado)
    ↓
Rectificador → DC/DC → Batería
                         ↓
                    Inversor → Carga AC (heladera)
                         ↓
                    ESP32 (telemetría)
```

**Procedimiento**:
1. Iniciar con fuente AC a 12V (viento bajo)
2. Verificar DC/DC eleva a 14V
3. Aumentar fuente AC a 24V (viento alto)
4. Verificar DC/DC reduce a 14V
5. Conectar heladera y monitorear:
   - Voltaje batería estable
   - Corriente carga/descarga
   - Temperatura componentes
6. Simular sobrevoltaje (30V AC) → Dump load activa
7. Simular descarga profunda → Inversor desconecta
8. Verificar telemetría ESP32 en frontend

**Duración**: 4 horas continuas

**Criterio aprobación**: Sistema opera sin intervención manual, todas las protecciones funcionan.

---

**Complementa**: `PLAN_ELECTRONICA_POTENCIA_DETALLADO.md`
