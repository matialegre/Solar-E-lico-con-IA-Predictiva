# 🏠 Instalación Sistema Híbrido en Casa - Proyecto Piloto

## 📋 Resumen del Proyecto

**Objetivo:** Instalar y probar el sistema híbrido solar + eólico con IA en una casa real (Bahía Blanca, Argentina)

**Tipo de instalación:** Prueba piloto / Prototipo funcional

**Ubicación:** Casa particular - Primera implementación real

---

## 🎯 Especificaciones del Sistema para Casa de Prueba

### Consumo Estimado
- **Consumo promedio:** 650W (15.6 kWh/día)
- **Pico de consumo:** ~1500W (heladera + microondas + iluminación)
- **Consumo mensual:** ~468 kWh/mes

### Sistema Dimensionado
Basado en cálculos del sistema:

#### ☀️ Paneles Solares
- **Cantidad:** 3 paneles de 300W
- **Potencia total:** 900W (0.9 kW)
- **Generación diaria:** ~4.5 kWh/día
- **Cobertura:** 29% del consumo

#### 💨 Turbina Eólica
- **Cantidad:** 1 turbina de 1000W
- **Potencia nominal:** 1 kW
- **Generación diaria:** ~3.5 kWh/día
- **Cobertura:** 22% del consumo

#### 🔋 Batería
- **Tipo:** LiFePO4 48V
- **Capacidad:** 100Ah (4.8 kWh)
- **Autonomía:** ~7 horas con consumo promedio
- **DoD recomendado:** 80%

#### ⚡ Inversor
- **Tipo:** Inversor de onda pura
- **Potencia:** 2000W continua, 4000W pico
- **Entrada:** 48V DC
- **Salida:** 220V AC 50Hz

---

## 💰 Presupuesto Estimado (Pesos Argentinos - Octubre 2024)

| Componente | Especificación | Cantidad | Precio Unit. | Total |
|-----------|----------------|----------|--------------|-------|
| **GENERACIÓN SOLAR** |
| Panel solar | 300W policristalino | 3 | $80,000 | $240,000 |
| Estructura montaje | Aluminio, techo | 1 | $50,000 | $50,000 |
| **GENERACIÓN EÓLICA** |
| Turbina eólica | 1000W, 48V | 1 | $450,000 | $450,000 |
| Torre/mástil | 6 metros, anclajes | 1 | $120,000 | $120,000 |
| **ALMACENAMIENTO** |
| Batería LiFePO4 | 48V 100Ah | 1 | $380,000 | $380,000 |
| BMS (Battery Management) | Protección batería | 1 | $35,000 | $35,000 |
| **CONVERSIÓN** |
| Inversor | 2000W onda pura 48V | 1 | $180,000 | $180,000 |
| Controlador MPPT | Solar 30A | 1 | $65,000 | $65,000 |
| Controlador eólico | 1000W | 1 | $55,000 | $55,000 |
| **PROTECCIÓN EÓLICA** |
| Resistencia frenado | 10Ω 2000W cerámica | 1 | $25,000 | $25,000 |
| Disipador/ventilación | Para resistencia | 1 | $15,000 | $15,000 |
| **CONTROL & MONITOREO** |
| ESP32 DevKit | Microcontrolador | 1 | $8,000 | $8,000 |
| Sensores corriente | ACS712 30A | 3 | $3,500 | $10,500 |
| Shunt corriente | 100A 75mV | 1 | $15,000 | $15,000 |
| Sensor temperatura | DS18B20 | 2 | $2,500 | $5,000 |
| LDR | Radiación solar | 1 | $500 | $500 |
| **CABLEADO & PROTECCIÓN** |
| Cable solar | 6mm² x 50m | 1 | $45,000 | $45,000 |
| Cable batería | 16mm² x 10m | 1 | $35,000 | $35,000 |
| Fusibles/portafusibles | Varios | 1 lote | $18,000 | $18,000 |
| Cajas estancas | IP65 | 3 | $8,000 | $24,000 |
| Relés | 30A 250VAC | 4 | $5,500 | $22,000 |
| **INSTALACIÓN** |
| Mano de obra | Eléctrico + montaje | 3 días | $60,000 | $180,000 |
| Materiales varios | Conectores, borneras | - | - | $35,000 |
| **TOTAL ESTIMADO** | | | | **$1,967,000** |

**≈ USD 2,100** (al cambio de ~$950/USD)

---

## 📦 Lista de Compras (Orden de Prioridad)

### Fase 1: Control y Monitoreo (Empezar por acá)
- [ ] ESP32-WROOM-32 DevKit v1
- [ ] Sensores de corriente ACS712 (x3)
- [ ] Shunt de corriente 100A
- [ ] Sensores de temperatura DS18B20 (x2)
- [ ] Fotoresistencia LDR
- [ ] Módulo relés 4 canales
- [ ] Fuente 5V 2A
- [ ] Resistencias, cables, protoboard

**Costo Fase 1:** ~$85,000 (~USD 90)

### Fase 2: Energía Solar (Primera fuente)
- [ ] 3 paneles solares 300W
- [ ] Estructura de montaje
- [ ] Controlador MPPT 30A
- [ ] Cable solar 6mm²
- [ ] Fusibles y protecciones

**Costo Fase 2:** ~$450,000 (~USD 475)

### Fase 3: Almacenamiento
- [ ] Batería LiFePO4 48V 100Ah
- [ ] BMS
- [ ] Cable batería 16mm²

**Costo Fase 3:** ~$450,000 (~USD 475)

### Fase 4: Conversión AC
- [ ] Inversor 2000W onda pura
- [ ] Tablero eléctrico modificado

**Costo Fase 4:** ~$200,000 (~USD 210)

### Fase 5: Energía Eólica (Última, opcional)
- [ ] Turbina eólica 1000W
- [ ] Torre/mástil 6m
- [ ] Controlador eólico
- [ ] Resistencia de frenado
- [ ] Sistema de protección

**Costo Fase 5:** ~$665,000 (~USD 700)

---

## 🛠️ Plan de Implementación (8 Semanas)

### Semana 1-2: Preparación y Diseño
- [x] Relevamiento de consumos reales de la casa
- [x] Diseño del sistema (COMPLETADO)
- [ ] Compra Fase 1 (control y monitoreo)
- [ ] Armado y prueba de ESP32 + sensores
- [ ] Instalación de software (backend + frontend)

### Semana 3-4: Sistema Solar
- [ ] Compra Fase 2 (paneles + MPPT)
- [ ] Instalación de estructura en techo
- [ ] Montaje de paneles solares
- [ ] Cableado DC
- [ ] Pruebas de generación

### Semana 5-6: Batería e Inversor
- [ ] Compra Fases 3 y 4
- [ ] Instalación de batería en lugar seguro
- [ ] Conexión BMS y protecciones
- [ ] Instalación inversor
- [ ] Modificación tablero eléctrico
- [ ] Pruebas de sistema completo

### Semana 7-8: Eólica y Optimización
- [ ] Compra Fase 5 (opcional)
- [ ] Instalación torre eólica
- [ ] Montaje turbina
- [ ] Sistema de protección contra embalamiento
- [ ] Integración completa
- [ ] Calibración IA y aprendizaje

---

## ⚙️ Instalación Física

### 1. Ubicación de Componentes

```
TECHO:
├── Paneles solares (3x 300W) - Orientación Norte
│   └── Ángulo: 38° (igual a latitud)
└── Estructura de montaje aluminio

PATIO/JARDÍN:
├── Torre eólica 6m
│   ├── Base de hormigón 0.5m³
│   ├── Vientos/tensores (4)
│   └── Turbina 1000W en la punta
└── Anclajes cada 3m

INTERIOR (Garaje/Lavadero):
├── Gabinete principal (60x80cm)
│   ├── Batería LiFePO4 48V 100Ah
│   ├── BMS
│   ├── Inversor 2000W
│   ├── Controlador MPPT solar
│   ├── Controlador eólico
│   └── Resistencia de frenado (CON VENTILACIÓN)
│
├── Caja de control (30x40cm)
│   ├── ESP32 + sensores
│   ├── Módulo relés (4 canales)
│   ├── Fusibles y protecciones
│   └── Display opcional
│
└── Tablero eléctrico modificado
    ├── Entrada RED (backup)
    ├── Entrada INVERSOR (principal)
    └── Contactor automático
```

### 2. Conexiones Eléctricas

#### Paneles Solares → MPPT → Batería
```
Panel 1 ─┐
Panel 2 ─┼─→ [Serie] → MPPT → BMS → Batería 48V
Panel 3 ─┘
```

#### Turbina Eólica → Controlador → Batería
```
Turbina → Controlador Eólico → BMS → Batería 48V
                    │
                    └──→ Resistencia Frenado (protección)
```

#### Batería → Inversor → Casa
```
Batería 48V → Inversor 2000W → 220VAC → Tablero → Casa
```

---

## 📊 Monitoreo y Control

### Dashboard Web Accesible
- **Local:** http://192.168.1.X:3002
- **Internet:** http://tu-ngrok-url.ngrok.io (opcional)

### Funciones del Sistema
1. **Monitoreo en tiempo real:**
   - Generación solar instantánea
   - Generación eólica instantánea
   - Estado de batería (%)
   - Consumo de la casa
   - Balance energético

2. **IA Predictiva:**
   - Aprende patrones de consumo
   - Predice próximas horas
   - Recomienda cuándo cargar batería
   - Detecta electrodomésticos (heladera, microondas, etc.)

3. **Protección Eólica:**
   - Monitoreo de velocidad de viento
   - Protección contra embalamiento
   - Activación automática de resistencia
   - Control manual de emergencia

4. **Pronóstico Meteorológico:**
   - 4 días adelante
   - Estimación solar y eólica
   - Optimización automática

---

## ⚠️ Seguridad y Normativas

### Normas a Cumplir
- [ ] **AEA 90364** - Instalaciones eléctricas en inmuebles
- [ ] **Conexión a tierra** obligatoria (PAT < 40Ω)
- [ ] **Fusibles y protecciones** en todas las líneas
- [ ] **Certificación eléctrica** por matriculado
- [ ] **Seguro hogar** actualizado (informar modificación)

### Medidas de Seguridad
- [ ] Fusibles antes de batería
- [ ] Interruptor termomagnético principal
- [ ] Disyuntor diferencial 30mA
- [ ] Cajas estancas IP65 en exterior
- [ ] Ventilación forzada en gabinete
- [ ] Extintores ABC cercanos
- [ ] Señalización de tensiones

---

## 📈 Objetivos de la Prueba Piloto

### Semana 1-4:
- [x] Sistema funcionando básico
- [ ] Generación solar operativa
- [ ] Monitoreo en tiempo real OK
- [ ] IA aprendiendo patrones

### Mes 2-3:
- [ ] Sistema completo (solar + batería + inversor)
- [ ] 50% autonomía energética
- [ ] Datos de 30 días recolectados
- [ ] Patrones de consumo identificados

### Mes 4-6:
- [ ] Sistema híbrido completo (+ eólica)
- [ ] 70% autonomía energética
- [ ] IA optimizada
- [ ] ROI calculado con datos reales

---

## 🎓 Aprendizajes Esperados

### Técnicos
- Rendimiento real vs teórico de paneles
- Generación eólica en Bahía Blanca
- Eficiencia del sistema completo
- Desgaste de baterías LiFePO4
- Problemas y soluciones encontrados

### Económicos
- Ahorro real en factura eléctrica
- Tiempo de recuperación de inversión
- Costos de mantenimiento
- Vida útil de componentes

### IA y Software
- Precisión de predicciones
- Calidad del aprendizaje de patrones
- Efectividad de protección eólica
- Usabilidad del dashboard

---

## 📝 Próximos Pasos

1. **ESTA SEMANA:**
   - [ ] Comprar ESP32 + sensores (Fase 1)
   - [ ] Medir consumos reales de la casa
   - [ ] Definir ubicación exacta de componentes
   - [ ] Revisar instalación eléctrica actual

2. **PRÓXIMAS 2 SEMANAS:**
   - [ ] Armar prototipo de control con ESP32
   - [ ] Probar software completo
   - [ ] Cotizar paneles solares (mínimo 3 proveedores)
   - [ ] Contactar electricista matriculado

3. **MES 1:**
   - [ ] Instalar paneles + MPPT
   - [ ] Primera generación solar
   - [ ] Recopilar datos

---

## 📞 Contactos Útiles

### Proveedores Argentina
- **Paneles Solares:**
  - Energe (CABA)
  - Sustentator (Buenos Aires)
  - Termosolar (La Plata)

- **Turbinas Eólicas:**
  - INVAP (Bariloche)
  - Genneia (Buenos Aires)
  - Proveedores chinos (AliExpress, Alibaba)

- **Baterías LiFePO4:**
  - Litio Argentina
  - EVE Battery (importadas)
  - BYD (distribuidores oficiales)

- **Componentes Electrónicos:**
  - ElectroComponentes
  - Robomart (ESP32, sensores)
  - MercadoLibre

### Asesoramiento
- Colegio de Ingenieros de Bahía Blanca
- INTI (Instituto Nacional de Tecnología Industrial)

---

## 📊 KPIs a Medir

| Métrica | Objetivo | Actual | Estado |
|---------|----------|--------|--------|
| Autonomía % | 70% | 0% | 🔴 No iniciado |
| Ahorro mensual | $50,000 | $0 | 🔴 No iniciado |
| Uptime sistema | >95% | - | 🔴 No iniciado |
| Precisión IA | >80% | - | 🔴 No iniciado |
| ROI (meses) | <36 | - | 🔴 No iniciado |

---

## 🚀 ¡VAMOS A HACERLO!

Este es el plan para la **PRIMERA INSTALACIÓN REAL** del sistema. 

**Ventajas de empezar con casa propia:**
✅ Control total del experimento
✅ Iteración rápida si hay problemas
✅ Datos reales para optimizar
✅ Aprendizaje sin presión de cliente
✅ Prueba de concepto completa
✅ Base para escalar a más casas

**Una vez que esto funcione bien durante 3-6 meses, tenemos:**
- Sistema probado y optimizado
- Datos reales de rendimiento
- Costos reales conocidos
- Problemas resueltos
- Referencias para futuros clientes

---

**Fecha de inicio prevista:** A definir
**Fecha objetivo finalización Fase 1:** +2 semanas
**Fecha objetivo sistema completo:** +8 semanas

---

*Documento vivo - Actualizar con progreso real*
