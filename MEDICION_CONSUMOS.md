# 📊 Medición de Consumos - Casa de Prueba

## Objetivo
Medir el consumo real de la casa antes de instalar el sistema para dimensionarlo correctamente.

---

## 🔌 Método 1: Lectura de Medidor de Luz

### Paso a Paso:
1. **Registrar lectura del medidor ahora:**
   - Fecha/Hora: ________________
   - Lectura: ________ kWh

2. **Registrar lectura 24 horas después:**
   - Fecha/Hora: ________________
   - Lectura: ________ kWh

3. **Calcular consumo diario:**
   - Consumo = Lectura Final - Lectura Inicial
   - Consumo promedio: ________ kWh/día
   - Consumo promedio: ________ W (kWh/día × 1000 ÷ 24)

### Repetir durante 7 días:

| Día | Fecha | Lectura | Consumo (kWh) | Promedio (W) |
|-----|-------|---------|---------------|--------------|
| 1   |       |         |               |              |
| 2   |       |         |               |              |
| 3   |       |         |               |              |
| 4   |       |         |               |              |
| 5   |       |         |               |              |
| 6   |       |         |               |              |
| 7   |       |         |               |              |
| **Promedio** | | | | |

---

## 💡 Método 2: Inventario de Electrodomésticos

### Electrodomésticos Principales

| Aparato | Potencia (W) | Horas/día | Consumo (Wh/día) | Notas |
|---------|--------------|-----------|------------------|-------|
| **HELADERA** | 150 | 24 | 3,600 | Compresor cicla 50% |
| Freezer | 200 | 24 | 4,800 | Si hay |
| **TV** | 80 | 6 | 480 | |
| **Iluminación LED** | 60 | 5 | 300 | Total de la casa |
| Cargadores (celular, laptop) | 30 | 3 | 90 | |
| Microondas | 1,000 | 0.25 | 250 | 15 min/día |
| Lavarropas | 500 | 1 | 500 | 3 veces/semana |
| Calefón eléctrico | 1,500 | 0 | 0 | **NO usar** con solar |
| Aire acondicionado | 1,200 | 0 | 0 | Verano solamente |
| Ventilador | 50 | 8 | 400 | Verano |
| Computadora | 150 | 4 | 600 | |
| Router WiFi | 10 | 24 | 240 | |
| Licuadora/Multiprocesadora | 400 | 0.1 | 40 | 6 min/día |
| Otros (standby) | 20 | 24 | 480 | Varios |
| **TOTAL ESTIMADO** | | | **~11,780 Wh/día** | **~490 W promedio** |

---

## 📈 Perfil de Consumo por Hora

Estimación de consumo hora por hora (llenar basándose en rutina):

| Hora | Aparatos encendidos | W estimados |
|------|---------------------|-------------|
| 00:00-01:00 | Heladera, router, standby | 80 |
| 01:00-02:00 | Heladera, router, standby | 80 |
| 02:00-03:00 | Heladera, router, standby | 80 |
| 03:00-04:00 | Heladera, router, standby | 80 |
| 04:00-05:00 | Heladera, router, standby | 80 |
| 05:00-06:00 | Heladera, router, standby | 80 |
| 06:00-07:00 | **+Luz, cafetera** | 350 |
| 07:00-08:00 | **+TV, desayuno** | 450 |
| 08:00-09:00 | **+Computadora** | 600 |
| 09:00-10:00 | Heladera, router, standby | 200 |
| 10:00-11:00 | Heladera, router, standby | 200 |
| 11:00-12:00 | Heladera, router, standby | 200 |
| 12:00-13:00 | **+Microondas, cocina** | 800 |
| 13:00-14:00 | **+TV, almuerzo** | 350 |
| 14:00-15:00 | Heladera, router, standby | 200 |
| 15:00-16:00 | Heladera, router, standby | 200 |
| 16:00-17:00 | Heladera, router, standby | 200 |
| 17:00-18:00 | **+Computadora** | 600 |
| 18:00-19:00 | **+Luces, TV** | 450 |
| 19:00-20:00 | **+Cocina** | 700 |
| 20:00-21:00 | **+TV, cena** | 650 |
| 21:00-22:00 | **+Luces, TV** | 550 |
| 22:00-23:00 | **+Luces, TV** | 450 |
| 23:00-00:00 | Heladera, router, standby | 200 |

**Promedio estimado:** ~330 W

---

## 🔍 Método 3: Medidor de Consumo Enchufable

### Opción Económica:
Comprar un **medidor de consumo enchufable** (~$8,000 pesos)

**Marcas recomendadas:**
- Kill A Watt
- Sonoff POW
- Tuya Smart Plug con medición

### Qué medir:
1. **Heladera** - 24 horas completas
2. **TV principal** - Tiempo que se usa
3. **Computadora** - Tiempo que se usa
4. **Consumo standby total** - Noche completa

---

## 📊 Análisis de Resultados

### Después de 7 días de medición:

**Consumo promedio diario:** __________ kWh/día
**Consumo promedio horario:** __________ W
**Pico máximo detectado:** __________ W
**Consumo nocturno (00-06):** __________ W

### Comparación con Diseño:
- Diseño actual usa: **650W promedio**
- Consumo real medido: __________ W
- Diferencia: __________ W (___%)

### Ajustes Necesarios:
- [ ] Sistema actual es suficiente
- [ ] Necesita MÁS capacidad: _____ W adicionales
- [ ] Necesita MENOS capacidad: Ahorrar $______
- [ ] Necesita cambios en hábitos de consumo

---

## 💡 Recomendaciones para Reducir Consumo

### Cambios Fáciles (Sin costo):
- [ ] Apagar TV cuando no se usa (modo standby consume)
- [ ] Desenchufar cargadores cuando no se usan
- [ ] Usar luz natural durante el día
- [ ] Reducir temperatura heladera a nivel medio
- [ ] Lavar ropa con agua fría

### Cambios con Inversión Baja:
- [ ] Cambiar todas las luces a LED (~$15,000)
- [ ] Zapatillas con interruptor para cortar standby (~$3,000)
- [ ] Timer para calefón (solo cuando se usa) (~$5,000)

### Potencial de Ahorro:
- Cambio a LED: -200 Wh/día
- Eliminar standby: -150 Wh/día
- Uso eficiente heladera: -500 Wh/día
- **Total ahorro posible: -850 Wh/día (-35%)**

---

## 🎯 Conclusiones

Al completar esta medición, sabrás:
1. ✅ Consumo real de tu casa
2. ✅ Si el sistema diseñado es correcto
3. ✅ Cuánto podés ahorrar optimizando
4. ✅ Qué electrodomésticos consumen más
5. ✅ Cuándo hay picos de consumo (para IA)

**Próximo paso:** Ajustar el dimensionamiento del sistema con datos reales.

---

*Completar esta planilla ANTES de comprar componentes*
