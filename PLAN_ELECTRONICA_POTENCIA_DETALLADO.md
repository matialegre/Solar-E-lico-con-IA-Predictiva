# 🔌 Plan Detallado - Electrónica de Potencia y Pruebas de Campo

## 0. Objetivo General
Diseñar, construir y validar un sistema híbrido solar + eólico capaz de:
- Generar energía útil incluso con **viento mínimo** (cut-in ~2-3 m/s)
- Mantener **voltaje estable** (14 VDC nominal) para carga de baterías 12V
- Alimentar cargas AC (heladera ~150-300W) mediante inversor DC/AC
- Medir potencia entregada, detectar pico de potencia máxima (MPPT eólico)
- Proteger contra sobrevoltaje/sobrevelocidad
- Recolectar datos para Machine Learning (predicción de generación)

---

## 1. Arquitectura del Sistema de Potencia

```
AEROGENERADOR → RECTIFICADOR 3-fase → DC/DC Buck-Boost → BATERÍA 12V
PANELES SOLAR → MPPT Solar         ↗                    ↓
                                                    INVERSOR → HELADERA
                                                         ↓
                                                    ESP32 (telemetría)
```

---

## 2. Electrónica de Potencia - Componentes Clave

### 2.1 Rectificador Trifásico
- 6× diodos Schottky MBR20200CT (20A 200V)
- Capacitor filtro 10000µF 50V
- Fusible 30A entrada

**Voltaje salida**: V_DC ≈ 1.35 × V_AC_línea

### 2.2 DC/DC Buck-Boost (Regulación 14V)
**Módulo recomendado**: LTC3780 (5-32V in, 1-30V out, 10A)
- Ajustar salida a 14.0-14.4V
- Eficiencia objetivo: >85%
- Disipador si corriente >5A

### 2.3 Resistencia de Frenado (Dump Load)
- Resistencia 1Ω 300W (cerámica/rejilla)
- Relé/MOSFET IRF3205 controlado por ESP32
- Activar si: SOC>90% o RPM>600 o V>16V

### 2.4 MPPT Solar
**Recomendado**: Victron SmartSolar 75/15 o EPSolar Tracer 2210A
- Conexión: Paneles → MPPT → Batería
- Telemetría vía RS485 o Bluetooth

### 2.5 Medición de Potencia
- **Voltaje**: Divisor resistivo (ya en ESP32)
- **Corriente**: ACS758-50A (sensor Hall)
- **Cálculo**: P = V × I

---

## 3. Dimensionamiento

### 3.1 Heladera (Carga Principal)
- Consumo: 0.8-1.5 kWh/día
- Potencia pico arranque: 300-600W
- **Inversor necesario**: 500W continuo, 1000W pico, onda senoidal pura

### 3.2 Baterías
- Energía 2 días autonomía: 2.4 kWh
- **Capacidad**: 400Ah (plomo-ácido) o 200Ah (LiFePO4)
- **Configuración inicial**: 2× AGM 12V 100Ah paralelo

### 3.3 Solar
- Potencia necesaria: 375Wp (considerando 4h sol pico/día)
- **Configuración**: 2× paneles 200W (400Wp total)

### 3.4 Eólico
- Fórmula: P = 0.5 × ρ × A × v³ × Cp
- Turbina 1.2m diámetro, viento 6m/s: ~50W reales
- **Selección**: Turbina genérica 400W (potencia real 100-150W)

---

## 4. Plan de Pruebas - Resumen Ejecutivo

### Fase 0: Laboratorio (1 semana)
1. Calibrar sensores (voltaje ±0.05V, corriente ±0.1A)
2. Validar DC/DC (eficiencia >85%)
3. Probar dump load y protecciones
4. Integración completa en banco de pruebas

### Fase 1: Instalación Campo (1 día)
1. Montar aerogenerador y paneles
2. Instalar electrónica en gabinete
3. Conectar baterías y verificar voltajes
4. Puesta en marcha con carga de prueba

### Fase 2: Campaña 1 Día (baseline)
- Mediciones cada 10 minutos
- Pruebas escalonadas de carga (0W → 50W → 150W → 300W)
- Eventos controlados (dump load, desconexión fuentes)
- Exportar CSV telemetría + bitácora manual

### Fase 3: Campaña 1 Semana (dataset ML)
- Operación continua con checklist diario
- Exportar telemetría cada hora (backend → CSV)
- Consumir API clima cada hora (OpenWeather)
- Fusionar datos: telemetría + clima por timestamp
- 2 eventos controlados durante semana

### Fase 4: Validación Potencia Máxima
- Graficar curva P vs RPM
- Identificar RPM_cut_in, RPM_nominal, RPM_max_safe
- Actualizar umbrales en firmware
- Validar protecciones

---

## 5. Protecciones Esenciales

| Condición | Umbral | Acción |
|-----------|--------|--------|
| Sobrevoltaje | >16.0V | Activar dump load + desconectar carga |
| Sobrecorriente | >1.2× I_nominal | Abrir relé carga |
| Temperatura alta | >50°C batería | Reducir corriente / ventilador |
| Descarga profunda | <11.5V | Desconectar inversor |
| RPM excesivo | >600 RPM | Activar freno |

---

## 6. Datos para Machine Learning

### Features (Entrada)
- Voltajes (generador, batería, cargas)
- Corrientes (solar, eólica, consumo)
- RPM, frecuencia eléctrica
- Temperatura (si disponible)
- Datos API clima: viento, radiación, temperatura, humedad
- Hora del día, día de semana

### Labels (Salida a Predecir)
- Potencia entregada (W)
- SOC batería (%)
- Eficiencia (P_real / P_teórica)

### Formato Dataset
- CSV con timestamps ISO8601
- Columnas: timestamp, v_bat, i_solar, i_eolica, rpm, wind_speed_api, temp_api, potencia_W, soc_bat
- Guardar en `X:\PREDICCION DE CLIMA\datasets\`

---

## 7. Próximos Pasos Inmediatos

1. 🔲 Adquirir componentes faltantes (ver lista sección 2)
2. 🔲 Armar banco de pruebas en laboratorio
3. 🔲 Implementar protecciones en firmware
4. 🔲 Crear scripts de exportación telemetría (backend)
5. 🔲 Crear script consumo API clima
6. 🔲 Planificar instalación en campo (fecha, equipo, permisos)
7. 🔲 Preparar bitácora de campo y planillas de registro

---

**Documento complementario a**: `PLAN_MAESTRO_SISTEMA_HIBRIDO.md`
**Última actualización**: 2025-11-05
