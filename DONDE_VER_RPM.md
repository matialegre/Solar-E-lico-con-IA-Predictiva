# 🔍 Dónde Ver RPM y Frecuencia

## 📍 Ubicación en el Frontend

El **RPM** y la **Frecuencia** ahora se muestran **SIEMPRE** en el **Monitor ESP32**, justo encima de los ADCs:

```
┌─────────────────────────────────────────────────┐
│  Monitor ESP32                                  │
│  Inversor Híbrido - Tiempo Real                │
│  ✅ CONECTADO                                   │
├─────────────────────────────────────────────────┤
│  Device ID: ESP32_INVERSOR_001                  │
│  Contador: 127                                  │
│  Última actualización: 13:33:04                 │
│  RSSI: -45 dBm                                  │
├─────────────────────────────────────────────────┤
│  Control de Relés                               │
│  ☀️ Solar  💨 Eólica  🔌 Red  ⚡ Carga         │
├─────────────────────────────────────────────────┤
│  Mediciones ADC (0-3.3V)                        │
│                                                 │
│  ┌───────────────────────────────────────────┐ │
│  │ 🎯 RPM Turbina Eólica  Frecuencia Eléct. │ │ ← AQUÍ ESTÁ
│  │                                           │ │
│  │    0 RPM              0.00 Hz             │ │
│  └───────────────────────────────────────────┘ │
│                                                 │
│  GPIO34 (ADC1)  GPIO35 (ADC2)                  │
│  🔋 Batería     💨 Eólica                       │
│  0.000V         0.000V                          │
│                                                 │
│  GPIO36 (ADC5)  GPIO39 (ADC6)                  │
│  ☀️ Solar       ⚡ Carga                        │
│  0.000V         0.000V                          │
└─────────────────────────────────────────────────┘
```

---

## 🔄 Cómo Verificar

### 1. Abre el Frontend
```
http://localhost:3000
```

### 2. Ve a "Monitor ESP32"
- Haz clic en **"Dispositivos"** en el menú lateral
- O navega directamente a la sección de Monitor

### 3. Busca la Tarjeta Morada/Rosa
- **Color**: Gradiente púrpura a rosa
- **Ubicación**: Justo arriba de los 4 ADCs (GPIO34, GPIO35, GPIO36, GPIO39)
- **Contenido**:
  - Izquierda: **RPM Turbina Eólica**
  - Derecha: **Frecuencia Eléctrica**

---

## 🧪 Valores Esperados

### Sin Señal RPM Conectada (ACTUAL)
```
RPM Turbina Eólica: 0 RPM
Frecuencia Eléctrica: 0.00 Hz
```

### Con Señal de 50 Hz en GPIO13
```
RPM Turbina Eólica: 300 RPM
Frecuencia Eléctrica: 50.00 Hz
```

**Fórmula**: `RPM = (50 Hz × 60) / 10 pole_pairs / 1.0 gear_ratio = 300 RPM`

---

## 📊 Verificar en Backend

### Logs del Backend (Terminal)
Deberías ver en los logs:

```bash
[TELEM] ESP32_INVERSOR_001 seq=127 ts=1234 Vbat=2.840V ... RPM=0.0 Lost=9691 | OK
                                                              ^^^^^^^^ AQUÍ
```

### API Response (Manual)
Prueba manualmente:
```bash
curl http://localhost:11113/api/esp32/devices
```

Busca en la respuesta:
```json
{
  "devices": [{
    "telemetry": {
      "turbine_rpm": 0.0,      ← AQUÍ
      "frequency_hz": 0.0,     ← AQUÍ
      "rpm": 0.0
    }
  }]
}
```

---

## ⚠️ Si NO lo Ves

### Problema 1: Frontend no actualizado
```bash
# En la carpeta frontend/
npm start
# O si ya está corriendo:
Ctrl+C
npm start
```

### Problema 2: Backend no envía datos
Verifica en logs del backend:
```
💾 [GUARDAR #127] raw_adc para ESP32_INVERSOR_001: {...}
```

Si no aparece, el ESP32 no está enviando datos.

### Problema 3: ESP32 sin compilar/subir
```
1. Abre Arduino IDE
2. Compila firmware
3. Sube al ESP32
4. Espera 10 segundos
5. Recarga frontend (F5)
```

---

## 🎯 Para Probar con Señal Real

### Hardware Necesario
- Generador de señales (0-3V, cuadrada)
- O función PWM de otro microcontrolador
- Conectar a **GPIO13**

### Ejemplo con Arduino
```cpp
// En otro Arduino/ESP32
void setup() {
  pinMode(9, OUTPUT);
}

void loop() {
  // Generar 50 Hz (período 20ms)
  digitalWrite(9, HIGH);
  delayMicroseconds(10000); // 10ms HIGH
  digitalWrite(9, LOW);
  delayMicroseconds(10000); // 10ms LOW
}
```

Conecta salida digital → GPIO13 del ESP32 principal.

**Resultado Esperado**:
```
RPM Turbina Eólica: 300 RPM
Frecuencia Eléctrica: 50.00 Hz
```

---

## 📝 Resumen

| Aspecto | Estado | Ubicación |
|---------|--------|-----------|
| **Frontend** | ✅ Listo | Monitor ESP32 → Tarjeta morada |
| **Backend** | ✅ Listo | `turbine_rpm` en telemetry |
| **Firmware** | ✅ Listo | GPIO13 + ISR RISING |
| **Visible** | ✅ Siempre | Incluso con 0 RPM |

**Ahora deberías ver la tarjeta morada/rosa con "0 RPM" y "0.00 Hz" en el Monitor ESP32.** 🎉

Si no la ves:
1. Recarga la página (F5)
2. Verifica que estés en la pestaña correcta
3. Scroll down hasta después de los relés
