# 📘 SISTEMA INVERSOR HÍBRIDO - MANUAL TÉCNICO COMPLETO
## Parte 3: Cálculos y Ecuaciones

---

# 9. DIMENSIONAMIENTO SOLAR

## 9.1 Conceptos Básicos

### Horas Sol Pico (HSP):
```
HSP = Irradiancia diaria total (kWh/m²/día)

Ejemplo:
Bahía Blanca: 4.3 kWh/m²/día promedio anual
→ HSP = 4.3 horas
```

### Eficiencia del Sistema:
```
η_sistema = η_panel × η_inversor × η_cables × η_controlador

Típico:
η_panel = 0.17 (17%)
η_inversor = 0.95 (95%)
η_cables = 0.98 (98%)
η_controlador = 0.97 (97%)

η_sistema = 0.17 × 0.95 × 0.98 × 0.97 = 0.154 (15.4%)

Simplificado: η_sistema = 0.85 (85%)
```

## 9.2 Ecuaciones de Dimensionamiento

### Opción 1: Desde Consumo → Sistema Necesario

**Paso 1: Energía Solar Necesaria**
```
E_solar = Consumo_diario × % cobertura_solar

Ejemplo:
Consumo = 15.6 kWh/día
Cobertura solar = 60% (resto eólico)

E_solar = 15.6 × 0.60 = 9.36 kWh/día
```

**Paso 2: Potencia Pico Necesaria**
```
P_pico = E_solar / (HSP × η_sistema)

Ejemplo:
P_pico = 9.36 / (4.3 × 0.85)
P_pico = 9.36 / 3.655
P_pico = 2,562 W = 2.56 kW
```

**Paso 3: Número de Paneles**
```
N_paneles = ceil(P_pico / P_panel)

Ejemplo con panel 400W:
N_paneles = ceil(2562 / 400)
N_paneles = 7 paneles
```

**Paso 4: Potencia Total Real**
```
P_total = N_paneles × P_panel

Ejemplo:
P_total = 7 × 400W = 2,800W
```

**Paso 5: Generación Diaria Estimada**
```
E_diaria = (P_total / 1000) × HSP × η_sistema

Ejemplo:
E_diaria = (2800 / 1000) × 4.3 × 0.85
E_diaria = 2.8 × 4.3 × 0.85
E_diaria = 10.2 kWh/día
```

**Paso 6: Área Total Necesaria**
```
Área_total = N_paneles × Área_panel

Ejemplo con paneles de 1.65 m²:
Área_total = 7 × 1.65 = 11.55 m²
```

## 9.3 Ángulo e Inclinación

### Ángulo Óptimo:
```
α_óptimo = |Latitud| ± 15°

Para Bahía Blanca (Lat: -38.72°):
α_óptimo = 38.7° ± 15°

Verano: 38.7° - 15° = 23.7°
Invierno: 38.7° + 15° = 53.7°
Fijo anual: 38.7°
```

### Orientación:
```
Hemisferio Sur: Orientación al NORTE
Hemisferio Norte: Orientación al SUR

Desviación máxima aceptable: ±20°
Pérdida por 10° de desviación: ~1.5%
```

## 9.4 Factores de Corrección

### Por Temperatura:
```
P_real = P_nominal × [1 - 0.005 × (T_panel - 25)]

Ejemplo:
Panel 400W a 45°C en verano:
P_real = 400 × [1 - 0.005 × (45 - 25)]
P_real = 400 × [1 - 0.005 × 20]
P_real = 400 × 0.90 = 360W (10% pérdida)
```

### Por Suciedad:
```
Factor_suciedad = 0.95 (5% pérdida)

Con limpieza semestral: 0.95
Con limpieza mensual: 0.98
Sin limpieza: 0.85-0.90
```

### Por Sombreado:
```
Factor_sombra = (100 - %sombreado) / 100

10% sombreado → Factor = 0.90
20% sombreado → Factor = 0.80

⚠️ Sombra en serie reduce TODO el string
```

---

# 10. DIMENSIONAMIENTO EÓLICO

## 10.1 Ecuaciones Fundamentales

### Potencia del Viento Disponible:
```
P_viento = 0.5 × ρ × A × v³

Donde:
ρ = densidad aire (kg/m³)
A = área barrido (m²)
v = velocidad viento (m/s)

Densidad aire al nivel del mar: 1.225 kg/m³
```

### Área de Barrido:
```
A = π × r²

Donde:
r = radio de las palas (m)
D = diámetro = 2r

Ejemplo turbina 1.8m diámetro:
A = π × (0.9)² = 2.54 m²
```

### Límite de Betz:
```
P_max_teórica = P_viento × 0.593

El límite de Betz establece que MÁXIMO
se puede extraer el 59.3% de la energía del viento.

Esto es una ley física fundamental.
```

### Potencia Real Aprovechable:
```
P_real = P_viento × η_turbina

η_turbina típica: 0.30 - 0.40 (30-40%)
η_turbina buena: 0.35 - 0.45 (35-45%)
η_turbina excelente: 0.40 - 0.50 (40-50%)

Promedio usado: η = 0.35 (35%)
```

## 10.2 Ejemplo de Cálculo Completo

**Datos:**
- Turbina 2000W
- Diámetro: 2.5m
- Viento promedio: 5.2 m/s

**Paso 1: Área de Barrido**
```
r = D / 2 = 2.5 / 2 = 1.25m
A = π × (1.25)² = 4.91 m²
```

**Paso 2: Potencia del Viento**
```
P_viento = 0.5 × 1.225 × 4.91 × (5.2)³
P_viento = 0.5 × 1.225 × 4.91 × 140.61
P_viento = 422 W
```

**Paso 3: Límite de Betz**
```
P_max_teórica = 422 × 0.593 = 250 W
```

**Paso 4: Potencia Real (35% eficiencia)**
```
P_real = 422 × 0.35 = 148 W
```

**Paso 5: Generación Diaria**
```
E_diaria = (P_real × 24) / 1000
E_diaria = (148 × 24) / 1000
E_diaria = 3.55 kWh/día
```

## 10.3 Velocidad de Viento y Altura

### Perfil de Viento (Ley Potencial):
```
v₂ = v₁ × (h₂ / h₁)^α

Donde:
α = coeficiente (típico 0.14 - 0.20)
h₁ = altura de medición
h₂ = altura del rotor
v₁ = velocidad a h₁
v₂ = velocidad a h₂

Ejemplo:
Viento a 10m: 4.5 m/s
Altura turbina: 15m
α = 0.14

v₂ = 4.5 × (15/10)^0.14
v₂ = 4.5 × 1.057
v₂ = 4.76 m/s
```

## 10.4 Curva de Potencia

### Velocidades Características:
```
v_cut-in: Velocidad de arranque (3-4 m/s)
v_nominal: Velocidad nominal (12-14 m/s)
v_cut-out: Velocidad de corte (25-30 m/s)

Ejemplo turbina típica:
v_cut-in = 3.5 m/s
v_nominal = 12 m/s
v_cut-out = 25 m/s
```

### Distribución de Weibull:
```
P(v) = (k/c) × (v/c)^(k-1) × e^(-(v/c)^k)

Donde:
k = factor de forma (1.5 - 3.0)
c = factor de escala (relacionado con v_media)
v = velocidad del viento

Para estimación rápida:
c ≈ 1.13 × v_media
```

---

# 11. DIMENSIONAMIENTO DE BATERÍA

## 11.1 Ecuaciones Básicas

### Capacidad Necesaria:
```
C_batería = (Consumo_diario × Días_autonomía) / DoD

Donde:
DoD = Profundidad de Descarga (Depth of Discharge)

Para LiFePO4: DoD = 0.80 (80%)
Para Plomo-ácido: DoD = 0.50 (50%)
```

### Ejemplo Completo:
```
Consumo: 15.6 kWh/día
Autonomía: 2 días
Batería: LiFePO4 (DoD = 80%)

C_batería = (15.6 × 2) / 0.80
C_batería = 31.2 / 0.80
C_batería = 39 kWh
```

## 11.2 Conversión a Ah

### Capacidad en Amperios-Hora:
```
C_Ah = (C_kWh × 1000) / V_sistema

Ejemplo sistema 48V:
C_Ah = (39 × 1000) / 48
C_Ah = 812.5 Ah
```

## 11.3 Configuración Serie/Paralelo

### Baterías en Serie (Voltaje):
```
N_serie = V_sistema / V_batería

Ejemplo:
Sistema 48V con baterías 12V:
N_serie = 48 / 12 = 4 baterías en serie
```

### Baterías en Paralelo (Capacidad):
```
N_paralelo = C_Ah_necesaria / C_Ah_batería

Ejemplo:
Necesaria: 812.5 Ah
Batería: 200 Ah cada una
N_paralelo = 812.5 / 200 = 4.06
N_paralelo = 5 (redondear arriba)
```

### Configuración Total:
```
Total_baterías = N_serie × N_paralelo

Ejemplo:
Total = 4 × 5 = 20 baterías
Configuración: 4S5P (4 serie, 5 paralelo)

Voltaje final: 48V
Capacidad final: 1000 Ah
Energía total: 48V × 1000Ah = 48 kWh
```

## 11.4 Ciclos de Vida vs DoD

### Relación DoD - Ciclos:
```
LiFePO4:
DoD 80%: ~5,000 ciclos
DoD 50%: ~8,000 ciclos
DoD 30%: ~12,000 ciclos

Plomo-ácido:
DoD 50%: ~1,200 ciclos
DoD 30%: ~2,500 ciclos
DoD 20%: ~4,000 ciclos
```

### Años de Vida Estimados:
```
Años = (Ciclos × DoD) / (Consumo_diario / C_batería × 365)

Ejemplo:
Batería LiFePO4 48kWh, DoD 80%:
Consumo: 15.6 kWh/día
Ciclos: 5,000

Años = (5000 × 0.80) / (15.6 / 48 × 365)
Años = 4000 / (0.325 × 365)
Años = 4000 / 118.6
Años ≈ 34 años

(En práctica: 10-15 años por degradación química)
```

---

# 12. CARGAS INDUCTIVAS

## 12.1 Clasificación de Cargas

### Cargas Resistivas (FP ≈ 1.0):
```
Potencia Activa (W) = Potencia Aparente (VA)

Ejemplos:
- Luces incandescentes
- Calefactores
- Hornos eléctricos
- Pavas eléctricas

Factor de potencia: 0.95 - 1.00
Factor de arranque: 1.0 - 1.2x
```

### Cargas Inductivas (FP < 1.0):
```
Potencia Activa (W) < Potencia Aparente (VA)

Ejemplos:
- Heladeras
- Aires acondicionados
- Lavarropas
- Bombas de agua
- Motores

Factor de potencia: 0.60 - 0.85
Factor de arranque: 3.0 - 7.0x
```

## 12.2 Factor de Potencia

### Definición:
```
FP = P_activa / P_aparente = cos(φ)

Donde:
P_activa (W): Potencia útil
P_aparente (VA): Potencia total
φ: Ángulo de desfase
```

### Cálculo de Corriente:
```
Para cargas resistivas:
I = P / V

Para cargas inductivas:
I = S / V = P / (V × FP)

Ejemplo:
Heladera 400W, FP = 0.70, 220V

I = 400 / (220 × 0.70)
I = 400 / 154
I = 2.60 A

Pero la potencia aparente es:
S = 400 / 0.70 = 571 VA
```

## 12.3 Pico de Arranque

### Factor de Arranque:
```
P_pico = P_nominal × Factor_arranque

Heladera 400W:
Factor = 4.0
P_pico = 400 × 4.0 = 1,600W

Duración: 1-3 segundos
```

### Tabla de Factores Típicos:
```
Electrodoméstico          Factor    Duración
────────────────────────────────────────────
Luces LED                 1.0x      0s
Luces incandescentes      1.2x      0.1s
TV LCD                    1.5x      0.5s
Heladera                  4.0x      2s
Freezer                   4.0x      2s
Lavarropas                5.0x      3s
Aire acondicionado        3.5x      2.5s
Bomba agua                4.5x      2s
Soldadora                 3.0x      1s
Taladro                   3.0x      1s
```

## 12.4 Dimensionamiento Inversor

### Regla Práctica:
```
P_inversor_continuo >= P_cargas_resistivas + P_cargas_inductivas

P_inversor_pico >= max(P_picos_individuales) × 1.2

Margen de seguridad: 20%
```

### Ejemplo Real:
```
Cargas:
- Luces: 300W (resistiva)
- Heladera: 400W (inductiva, pico 1,600W)
- Lavarropas: 500W (inductiva, pico 2,500W)
- TV: 150W (resistiva)

Consumo nominal total: 1,350W

Pico máximo (si arrancan juntos):
300 + 1,600 + 2,500 + 150 = 4,550W

Inversor necesario:
Continuo: 1,350W × 1.3 = 1,755W → 2,000W
Pico: 4,550W × 1.2 = 5,460W → 6,000W

Inversor recomendado: 2,000W continuo / 6,000W pico
```

### Estrategia de Arranque Secuencial:
```
Para evitar inversor muy grande:

1. Arrancar heladera (pico 1,600W)
2. Esperar 5 segundos
3. Arrancar lavarropas (pico 2,500W)

Pico máximo real: 2,500W (no simultáneo)

Inversor necesario:
Continuo: 1,755W → 2,000W
Pico: 2,500W × 1.2 = 3,000W

Inversor recomendado: 2,000W / 3,000W ✅
(Más económico)
```

---

**FIN PARTE 3**

*Continúa en MANUAL_COMPLETO_PARTE_4.md*
