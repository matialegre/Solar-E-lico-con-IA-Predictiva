# 📐 Anexo - Cálculos Eléctricos Detallados

## 1. Dimensionamiento de Cables

**Fórmula caída de voltaje**:
```
ΔV = (2 × L × I × ρ) / S

Donde:
L = longitud cable (m)
I = corriente (A)
ρ = resistividad cobre (0.0172 Ω·mm²/m)
S = sección cable (mm²)
```

**Ejemplo**: Aerogenerador a 10m del gabinete, corriente máxima 20A, caída aceptable 3%:
```
ΔV_max = 14V × 0.03 = 0.42V
S = (2 × 10 × 20 × 0.0172) / 0.42 = 16.4 mm²
→ Usar cable 25 mm² (AWG 4) para margen
```

**Tabla secciones recomendadas**:
| Tramo | Distancia | Corriente | Sección mínima |
|-------|-----------|-----------|----------------|
| Aerogenerador → Rectificador | 10m | 20A | 25 mm² (AWG 4) |
| Paneles → MPPT | 5m | 15A | 16 mm² (AWG 6) |
| Batería → Inversor | 2m | 50A | 50 mm² (AWG 1) |
| DC/DC → Batería | 1m | 30A | 35 mm² (AWG 2) |

---

## 2. Cálculo de Eficiencia del Sistema

**Eficiencia global**:
```
η_total = η_rectificador × η_DC/DC × η_batería × η_inversor

Valores típicos:
η_rectificador = 0.95 (diodos Schottky)
η_DC/DC = 0.90 (buck-boost)
η_batería = 0.85 (carga/descarga)
η_inversor = 0.90 (onda pura)

η_total = 0.95 × 0.90 × 0.85 × 0.90 = 0.65 (65%)
```

**Implicación**: Si aerogenerador genera 100W, solo ~65W llegan a la carga AC.

---

## 3. Balance Energético Diario

**Generación estimada**:
```
E_solar = 400Wp × 4h × 0.8 = 1.28 kWh/día
E_eólica = 100W × 6h × 0.7 = 0.42 kWh/día
E_total_generada = 1.70 kWh/día
```

**Consumo**:
```
E_heladera = 1.2 kWh/día
E_luces = 0.2 kWh/día
E_otros = 0.1 kWh/día
E_total_consumida = 1.5 kWh/día
```

**Balance**: +0.2 kWh/día (excedente 13%) → Sistema dimensionado correctamente ✅

---

## 4. Potencia Eólica Teórica

**Fórmula Betz**:
```
P = 0.5 × ρ × A × v³ × Cp

Donde:
ρ = 1.225 kg/m³ (densidad aire nivel mar)
A = π × r² (área barrido)
v = velocidad viento (m/s)
Cp = 0.35-0.45 (coeficiente potencia turbinas pequeñas)
```

**Ejemplo turbina 1.2m diámetro**:
```
A = π × 0.6² = 1.13 m²

Viento 4 m/s: P = 0.5 × 1.225 × 1.13 × 64 × 0.4 = 17.7 W
Viento 6 m/s: P = 0.5 × 1.225 × 1.13 × 216 × 0.4 = 59.5 W
Viento 8 m/s: P = 0.5 × 1.225 × 1.13 × 512 × 0.4 = 141 W
Viento 10 m/s: P = 0.5 × 1.225 × 1.13 × 1000 × 0.4 = 276 W
```

**Nota**: Potencia real será 60-80% de teórica (pérdidas mecánicas y eléctricas).

---

**Complementa**: `PLAN_ELECTRONICA_POTENCIA_DETALLADO.md`
