# 🧭 Plan Maestro - Sistema Híbrido Solar + Eólico (ESP32)

## 0. Objetivo del Documento
Guía integral para:
- ✅ Entender arquitectura actual
- ✅ Medir y validar cada subsistema (firmware, backend, frontend)
- ✅ Definir plan de pruebas y datos a recolectar
- ✅ Organizar roadmap de mejoras (Blue Pill, MQTT, IA)
- ✅ Documentar herramientas y checklists de mantenimiento

---

## 1. Arquitectura Actual del Sistema

| Capa | Componentes | Responsabilidad | Estado |
|------|-------------|-----------------|--------|
| **Hardware** | ESP32, sensores ADC (GPIO34/35/36/39), entrada RPM (GPIO13) | Adquisición de datos y envío | ✅ Implementado
| **Firmware** | `sensors.h`, `http_client.h`, ISR RPM, filtros ADC | Filtrado, cálculo, telemetría | ✅ Estable (0.5 s)
| **Backend** | FastAPI (`main.py`, `routers/esp32_router.py`), DEVICES_STORE | Recepción, almacenamiento, API REST | ✅ Operativo
| **Frontend** | React (`ESP32Monitor.jsx`) | Monitoreo en tiempo real, control relés | ✅ 0.5 s polling
| **Simulador** | `simulador_esp32_completo.py` + scripts `.bat` | Testing con datos sintéticos | ✅ Disponible
| **Documentación** | `CAMBIOS_FIRMWARE_VELOCIDAD.md`, `ARQUITECTURA_BLUEPILL_ESP32.md` | Historial de cambios, decisiones | ✅ Actualizado

### Flujo de Datos (Tiempo real 0.5 s)
```
[ Sensores ] -> ESP32 (filtra + calcula) -> HTTP POST -> Backend -> Frontend (polling 0.5s)
```

---

## 2. Métricas Clave a Medir

| Categoría | Métrica | Cómo medir | Umbral aceptable |
|-----------|---------|------------|-------------------|
| **Voltaje Batería** | `sensores.v_bat_v` | Serial monitor / Frontend | ±0.05 V del valor real
| **Corriente Solar/Eólica/Carga** | `sensores.v_solar_v`, etc. | Serial / Backend logs | Variación < 0.02 V (ruido)
| **RPM Turbina** | `sensores.turbine_rpm` | Serial (tabla) / Frontend | 0 si sin señal, ±5% si con señal real
| **Latencia Telemetría** | Tiempo entre POST y dato visible | Cronometrar: envío → frontend | < 1 s (objetivo actual 0.5 s)
| **Estabilidad ADC** | Desviación estándar con señal fija | Serial monitor (modo tabla) | σ < 0.01 V tras filtrado
| **Conectividad WiFi** | RSSI | Tabla logs Serial | > -70 dBm ideal (< -85 dBm problema)
| **Estado Backend** | HTTP POST codes | Serial / Backend console | 200 OK constante
| **Heartbeat** | Paquetes cada 30 s | Backend logs | Debe existir aunque no haya telemetría

### Métricas Futuras
- Temperatura ESP32 (para disipaciones)
- Tiempo de reconexión WiFi
- Consumo energético (si se agrega sensor)

---

## 3. Plan de Pruebas Paso a Paso

### 3.1 Validación Firmware (sin backend)
1. **Preparar**: Abrir Serial Monitor (115200) → RESET ESP32
2. **Verificar logs**:
   - Aparecen líneas `⚡[...]` cada 0.5 s (compacto)
   - Cada 5 s aparece tabla completa con ADC RAW + RPM + RSSI
3. **Test 1 - Voltaje fijo**:
   - Conectar fuente 2.500 V a GPIO34
   - Esperar 30 s
   - Verificar en tabla: `GPIO34 (Batería): 2.500V ± 0.01`
4. **Test 2 - Sin sensores**:
   - Desconectar ADC → Debe mostrar `0.000V [raw: 0/4095]`
   - Confirma detección de cable/sensor suelto
5. **Test 3 - RPM simulada**:
   - Inyectar señal 50 Hz en GPIO13
   - Tabla debe mostrar `RPM ≈ 300`, `Frecuencia ≈ 50 Hz`
6. **Verificar POST**: `POST:200` constante (si WiFi conectado)

### 3.2 Validación Backend + Frontend (con ESP32 real)
1. Backend ON (`uvicorn main:app --host 0.0.0.0 --port 11113`)
2. Frontend ON (`npm start`)
3. En frontend → Monitor ESP32 → Debe mostrar tarjeta RPM y ADCs en 0.5 s
4. Confirmar en backend logs: `[TELEM] ... Vbat=... RPM=...`
5. Simular desconexión WiFi → Verificar reconexión (POST retrasado)
6. Opcional: Ejecutar `PROBAR_RPM.bat` para prueba end-to-end con simulador

### 3.3 Validación con Simulador (sin hardware)
1. Backend y Frontend arriba
2. Ejecutar `PROBAR_RPM.bat`
3. Ver logs:
   - Simulador → envía cada 0.5 s (muestra voltajes y RPM)
   - Backend → `[TELEM]` con datos del simulador
   - Frontend → Tarjeta RPM activa (valores 150-400)
4. Detener (Ctrl+C) y confirmar backend marca dispositivo offline tras ~30 s

### 3.4 Pruebas de Estrés (avance futuro)
- Reducir SEND_INTERVAL a 250 ms y medir estabilidad
- Simular 10 dispositivos (simulador con IDs distintos)
- Probar reinicios del backend mientras ESP32 sigue enviando

### 3.5 Plan de Campo y Captura de Datos Reales

**Objetivo**: obtener datos físicos confiables (voltajes, corrientes, RPM, potencia mecánica/eléctrica) durante campañas de 1 día y 1 semana para validar el sistema, entrenar modelos de Machine Learning y diseñar electrónica de potencia (carga de baterías, etapa DC/DC, etc.).

#### Instrumentación recomendada

| Componente | Función | Notas |
|------------|---------|-------|
| ESP32 actual | Telemetría + conectividad | Usar versión con logging a SD (opcional) |
| Sensor Hall de corriente (p.ej. ACS758/ACS712) | Medir corriente en cargas/batería | Calibrar con carga conocida |
| Divisores resistivos precisos (1%) | Medir voltaje DC (generador, batería) | Añadir filtro RC para reducir ruido |
| Tacómetro óptico / encoder / sensor Hall | Medir RPM de referencia | Sirve para validar ISR del ESP32 |
| Anemómetro (si no está integrado) | Medir velocidad de viento | Preferible digital con salida por pulsos |
| Cargas resistivas/variable (reóstato, resistencias de potencia) | Ensayar entrega de potencia | Seleccionar potencia ≥ potencia esperada del aerogenerador |
| Banco de baterías objetivo (12/24/48 V) | Validar etapa de carga | Supervisar temperatura de baterías |
| Data logger externo (opcional) | Redundancia de datos | Puede ser otra MCU o laptop con USB |

#### Preparación y montaje

1. **Ubicación**: techo libre de obstrucciones con buena exposición al viento.
2. **Anclaje seguro** del aerogenerador y mástil (inspeccionar tensores, bases, pararrayos si aplica).
3. **Cableado**: separar líneas de potencia y señal; usar blindaje o pares trenzados para sensores analógicos.
4. **Protecciones**: fusibles DC, interruptor de corte rápido, resistencia de frenado conectada vía relé.
5. **Sincronización de reloj**: configurar ESP32 con NTP o timestamp manual para correlacionar con APIs meteorológicas.

#### Campaña de 1 día (baseline)

1. Ejecutar firmware con logs mejorados y verificar en campo que Serial Monitor/SD registran datos.
2. Registrar manualmente condiciones iniciales: hora, clima, estado de baterías, configuración de carga.
3. **Rutas de medición** (cada 10 minutos):
   - RPM promedio (ESP32 vs tacómetro externo)
   - Voltaje DC generador antes de rectificación
   - Voltaje DC después de rectificación/regulación
   - Corriente hacia carga/batería
   - Estado de relés y temperatura de componentes críticos (cojinete, resistencias, disipadores)
4. Ejecutar pruebas escalonadas de carga:
   - Carga abierta (sin consumidor) → medir tensión máxima en vacío
   - Carga resistiva baja (30% potencia nominal) → registrar corriente y calentamiento
   - Carga resistiva alta (80-100% potencia nominal) → monitorear estabilidad y activar freno si excede límites
5. Al finalizar el día, descargar datos del backend (`DEVICES_STORE`) y de la SD (si se usa).

#### Campaña de 1 semana (dataset para ML)

1. Mantener sistema operando continuamente con verificación diaria (checklist sección 6).
2. Programar backend para exportar telemetría a JSON/CSV cada hora (timestamp, adc raw, valores filtrados, RPM, relés).
3. Paralelamente, consumir API de clima (OpenWeather u otra) cada hora y guardar:
   - Velocidad y dirección del viento
   - Temperatura, presión, humedad
   - Nubosidad, radiación solar estimada
   - Códigos de condición climática (para features categóricas)
4. Emparejar datos físicos y meteorológicos por timestamp → construir tabla para entrenamiento ML (features: viento API, viento real si se dispone, RPM, voltajes, corrientes, relés, temperatura; label: potencia entregada, SOC batería, etc.).
5. Realizar al menos **dos eventos controlados**:
   - Activar/desactivar resistencia de frenado para observar respuesta de RPM
   - Cambiar ángulo/orientación del aerogenerador (si es posible) para evaluar sensibilidad

#### Validación de potencia máxima y electrónica de carga

1. Determinar curva P vs RPM: usar datos 1 semana para graficar `Potencia eléctrica = Voltaje * Corriente` vs `RPM`.
2. Identificar RPM nominal y máxima segura (definir umbrales de corte para firmware y relés).
3. Diseñar/seleccionar etapa de elevación de voltaje (DC/DC boost o buck/boost):
   - Medir tensión mínima/máxima generador
   - Decidir topología según tensión batería (p.ej. boost a 48 V)
   - Registrar eficiencia del convertidor bajo diferentes corrientes
4. Validar carga de batería real:
   - Conectar convertidor DC/DC a banco de baterías con BMS
   - Medir corriente de carga, temperatura baterías, SOC estimado
   - Registrar comportamiento durante ráfagas de viento (picos de corriente)

#### Datos mínimos para Machine Learning

| Categoría | Variables recomendadas |
|-----------|------------------------|
| Sensores físicos | Voltajes ADC (raw y escalados), corrientes, RPM, frecuencia, temperatur asif medida |
| Estados | Relés, modo freno, estado carga, alarmas |
| Energía | Potencia instantánea, energía acumulada (kWh) diaria |
| Externos | Datos API de clima, hora del día, día de la semana |
| Meta/labels | Potencia entregada real, SOC batería, eficiencia (Potencia real / Potencia teórica viento) |

Guardar datasets en formato `CSV` o `Parquet` con timestamps ISO8601. Documentar calibraciones, cambio de sensores o mantenimiento para usar como features adicionales.

#### Control de calidad de datos

- Validar calibración de cada sensor antes y después de la campaña (mismo valor conocido).
- Marcar periodos con fallos (cortes de red, sensores desconectados); excluir o etiquetar en dataset.
- Usar gráficos rápidos (Jupyter/Excel) para detectar outliers o huecos de datos.
- Mantener bitácora diaria con observaciones de campo (clima real, ruidos, vibraciones).

---

## 4. Datos a Registrar y Cómo Guardarlos

| Registro | Frecuencia | Medio | Comentarios |
|----------|------------|-------|-------------|
| Logs Serial (producción) | 1 vez por prueba | Guardar en archivo `.log` | Usar botón "Copy" del monitor IDE o `idf.py monitor` si ESP-IDF
| Telemetría Backend | Automático | `DEVICES_STORE` (memoria) → Implementar persistencia JSON | Considerar exportación cada hora
| Estados Frontend | Manual | Screenshots clave | Útil para documentación
| Configuraciones Firmware | Cada cambio | `CAMBIOS_FIRMWARE_VELOCIDAD.md` | Mantener historial
| Planes y Roadmap | Mensual | Este documento + README general | Actualizar con tareas completadas

**Sugerencia**: Crear script para guardar `DEVICES_STORE` en JSON cada 1 min → evita pérdida de datos si backend reinicia.

---

## 5. Roadmap Recomendado (Prioridades)

### Corto Plazo (0-2 semanas)
1. ✅ (Hecho) Ajustar SEND_INTERVAL a 0.5 s en firmware
2. ✅ (Hecho) Mejorar logs Serial Monitor (tabla + compacto)
3. 🔲 Automatizar guardado de telemetría (backend → JSON)
4. 🔲 Crear dashboard simple en frontend para histórico (gráficas)
5. 🔲 Mejorar control de relés desde frontend (confirmaciones)

### Mediano Plazo (2-6 semanas)
1. 🔲 Evaluar Server-Sent Events (SSE) o WebSocket para datos push
2. 🔲 Implementar alertas (backend → notifier) si Vbat fuera de rango
3. 🔲 Agregar autenticación básica a backend/frontend
4. 🔲 Documentar despliegue completo (scripts, servicios Windows/Linux)

### Largo Plazo (6-12 semanas)
1. 🔲 Prototipo Blue Pill + ESP32 (ver `ARQUITECTURA_BLUEPILL_ESP32.md`)
2. 🔲 Migrar telemetría a MQTT (broker Mosquitto)
3. 🔲 Integrar IA para pronósticos (potencia esperada vs real)
4. 🔲 Crear app móvil / PWA para monitoreo remoto

---

## 6. Checklist de Mantenimiento Diario/Semanal

### Diario
- [ ] Verificar **Monitor ESP32**: ¿Estado `CONECTADO`?
- [ ] Verificar tarjeta RPM: ¿Valores razonables?
- [ ] Revisar backend logs: ¿POST 200? ¿Sin errores?
- [ ] Confirmar WiFi RSSI > -70 dBm
- [ ] Guardar screenshot para historial

### Semanal
- [ ] Verificar calibración ADC (aplicar voltaje conocido)
- [ ] Validar reintentos HTTP (forzar desconexión)
- [ ] Respaldar configuraciones (`config.h`)
- [ ] Revisar `DEVICES_STORE` (datos actualizados)
- [ ] Actualizar documentación con cambios relevantes

### Mensual
- [ ] Analizar estabilidad de sensores durante 24 h
- [ ] Actualizar firmware si hay mejoras pendientes
- [ ] Testear respaldo del backend (export JSON)
- [ ] Revisar roadmap y completar tareas

---

## 7. Herramientas y Recursos

| Área | Herramienta | Archivo/Comando |
|------|-------------|------------------|
| **Firmware** | Arduino IDE 2.0 / PlatformIO | `firmware_arduino_ide_2/inversor_hibrido.ino`
| **Serial Monitor** | Arduino Serial Monitor / `idf.py monitor` | 115200 baud
| **Backend** | FastAPI + Uvicorn | `uvicorn main:app --host 0.0.0.0 --port 11113`
| **Frontend** | React + Vite/CRA | `npm start` en `/frontend`
| **Simulador** | Python + requests | `simulador_esp32_completo.py`, `PROBAR_RPM.bat`
| **Documentación** | Markdown | `CAMBIOS_FIRMWARE_VELOCIDAD.md`, `ARQUITECTURA_BLUEPILL_ESP32.md`, este documento

---

## 8. Ideas y Notas para el Futuro

- **Sensores adicionales**: temperatura batería, presión viento, inclinación paneles
- **Perfil de consumo**: integrar medidor de energía AC (ej. PZEM-004T)
- **Alertas**: Telegram/WhatsApp usando backend (FastAPI + Bot API)
- **Dashboard histórico**: Grafana/InfluxDB o Chart.js en frontend para 24h/7d
- **Edge Processing**: Blue Pill/STM32 con filtrado Kalman + MQTT
- **Integración domótica**: Home Assistant (via MQTT)
- **Pruebas automáticas**: Scripts que difieren valores y verifican respuestas

---

## 9. Próximos Pasos Inmediatos (Sugeridos)
1. ✅ Compilar y subir firmware actualizado (logs claros, envío 0.5 s)
2. ✅ Validar con simulador que backend/frontend responden rápido
3. 🔲 Ejecutar pruebas con hardware real (ADC + RPM)
4. 🔲 Implementar script de exportación de telemetría (backend)
5. 🔲 Documentar resultados de pruebas en carpeta `/test_logs/`
6. 🔲 Agendar sesión para discutir migración a SSE / MQTT / Blue Pill

---

## 10. Contacto y Notas Finales

- Mantener este documento actualizado con fecha de edición
- Registrar dudas o ideas en `TODO.md` (si se crea)
- Probar siempre en simulador ANTES de hardware real
- Priorizar cambios que impacten estabilidad y datos (ADC/RPM)

**Última actualización**: {{FECHA_ACTUAL}}
