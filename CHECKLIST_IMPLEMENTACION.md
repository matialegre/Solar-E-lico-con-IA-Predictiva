# ✅ Checklist de Implementación - Casa de Prueba

## 📅 SEMANA 1: Preparación

### Lunes - Relevamiento
- [ ] Medir consumos de la casa (usar `MEDICION_CONSUMOS.md`)
- [ ] Tomar fotos del techo (orientación, espacio disponible)
- [ ] Tomar fotos del patio/jardín (para torre eólica)
- [ ] Identificar lugar para gabinete (garaje/lavadero)
- [ ] Revisar tablero eléctrico actual
- [ ] Verificar que hay toma a tierra

### Martes - Compras Fase 1
- [ ] ESP32-WROOM-32 DevKit v1 (x1) - $8,000
- [ ] ACS712 30A (x3) - $10,500
- [ ] Shunt 100A 75mV (x1) - $15,000
- [ ] DS18B20 (x2) - $5,000
- [ ] LDR GL5528 (x1) - $500
- [ ] Módulo relés 4 canales (x1) - $15,000
- [ ] Fuente 5V 2A (x1) - $8,000
- [ ] Cables, resistencias, borneras - $10,000
- [ ] Protoboard/PCB - $8,000
- **TOTAL: ~$80,000**

### Miércoles - Armado de Prototipo
- [ ] Armar circuito ESP32 en protoboard
- [ ] Conectar sensores de corriente
- [ ] Conectar sensores de temperatura
- [ ] Probar con fuente de alimentación
- [ ] Verificar lecturas en monitor serial

### Jueves - Software
- [ ] Instalar Python 3.10+
- [ ] Instalar Node.js 18+
- [ ] Clonar repositorio o copiar archivos
- [ ] Instalar dependencias backend (`pip install -r requirements.txt`)
- [ ] Instalar dependencias frontend (`npm install`)
- [ ] Configurar archivo `.env` con tu ubicación
- [ ] Probar que levanta el backend (puerto 8801)
- [ ] Probar que levanta el frontend (puerto 3002)

### Viernes - Pruebas de Sistema
- [ ] Cargar código en ESP32 (si ya está listo)
- [ ] Probar comunicación ESP32 → Backend
- [ ] Verificar que se ven datos en dashboard
- [ ] Probar todos los sensores
- [ ] Documentar problemas encontrados

---

## 📅 SEMANA 2: Cotizaciones

### Lunes - Cotizar Paneles Solares
Pedir cotización a mínimo 3 proveedores:
- [ ] Proveedor 1: ________________ - Precio: $_______
- [ ] Proveedor 2: ________________ - Precio: $_______
- [ ] Proveedor 3: ________________ - Precio: $_______

**Especificaciones a pedir:**
- 3 paneles de 300W policristalinos
- Estructura de montaje para techo
- Garantía mínima 10 años
- Certificación IRAM

### Martes - Cotizar Controlador MPPT
- [ ] Controlador MPPT 30A para 48V
- [ ] Marca recomendada: Epever, Renogy, Victron
- [ ] Verificar que tenga pantalla LCD
- [ ] Cotización: $_______

### Miércoles - Cotizar Batería
- [ ] Batería LiFePO4 48V 100Ah (4.8 kWh)
- [ ] Con BMS incluido
- [ ] Garantía mínima 5 años / 3000 ciclos
- [ ] Cotización: $_______

### Jueves - Cotizar Inversor
- [ ] Inversor onda pura 2000W
- [ ] Entrada 48V DC
- [ ] Salida 220V AC 50Hz
- [ ] Protecciones: sobrecarga, cortocircuito, temperatura
- [ ] Cotización: $_______

### Viernes - Decisión de Compra
- [ ] Revisar todas las cotizaciones
- [ ] Calcular inversión total Fase 2
- [ ] Decidir si arrancar con solar o esperar
- [ ] Planificar presupuesto

---

## 📅 SEMANA 3-4: Instalación Solar (si se compró)

### Preparación Techo
- [ ] Limpiar área del techo
- [ ] Marcar ubicación de estructura
- [ ] Verificar que soporta el peso (~60kg)
- [ ] Revisar impermeabilización

### Instalación Estructura
- [ ] Instalar rieles de aluminio
- [ ] Fijar con tornillos y sellador
- [ ] Verificar orientación NORTE
- [ ] Verificar ángulo 38° (latitud de Bahía Blanca)
- [ ] Probar que está firme

### Montaje Paneles
- [ ] Montar panel 1
- [ ] Montar panel 2
- [ ] Montar panel 3
- [ ] Conectar en SERIE (para 48V)
- [ ] Verificar polaridad (+/-)
- [ ] Medir voltaje en circuito abierto (~60-70V)

### Cableado
- [ ] Pasar cable solar desde techo a interior
- [ ] Usar cable 6mm² rojo y negro
- [ ] Proteger cable con canaleta
- [ ] Dejar margen para conexiones
- [ ] NO conectar aún al controlador

### Instalación Controlador MPPT
- [ ] Ubicar en lugar seco, ventilado
- [ ] Conectar cables de paneles a MPPT (entrada solar)
- [ ] TODAVÍA NO conectar batería
- [ ] Verificar que pantalla enciende (si tiene)
- [ ] Leer manual del controlador

---

## 📅 SEMANA 5-6: Batería e Inversor

### Preparación Gabinete
- [ ] Limpiar área para gabinete
- [ ] Asegurar ventilación adecuada
- [ ] Instalar estantes si es necesario
- [ ] Tener extintor ABC cerca

### Instalación Batería
- [ ] Ubicar batería en lugar seco
- [ ] NO cerca de fuentes de calor
- [ ] Conexión a tierra obligatoria
- [ ] Conectar BMS si viene separado
- [ ] Verificar voltaje de batería (~52V cuando cargada)

### Conexión Controlador MPPT → Batería
- [ ] **IMPORTANTE:** Conectar batería PRIMERO
- [ ] Usar cable 16mm² corto (max 1m)
- [ ] Poner fusible 30A entre batería y MPPT
- [ ] Apretar bien las borneras
- [ ] Verificar que MPPT enciende correctamente
- [ ] Esperar que empiece a cargar (si hay sol)

### Instalación Inversor
- [ ] Ubicar cerca de batería
- [ ] Conectar cables de batería a inversor
- [ ] **Verificar polaridad: ROJO+ NEGRO-**
- [ ] Fusible 80A entre batería e inversor
- [ ] Conectar tierra
- [ ] NO encender todavía

### Modificación Tablero Eléctrico
**⚠️ REQUIERE ELECTRICISTA MATRICULADO**
- [ ] Agregar entrada desde inversor
- [ ] Instalar contactor automático (red ↔ inversor)
- [ ] Instalar disyuntor 30mA
- [ ] Instalar interruptor termomagnético
- [ ] Identificar circuitos a alimentar con solar
- [ ] Probar switcheo red ↔ inversor

### Primera Prueba Completa
- [ ] Verificar que batería está cargada (>90%)
- [ ] Encender inversor
- [ ] Verificar voltaje salida 220V AC
- [ ] Probar con carga pequeña (lámpara 60W)
- [ ] Verificar que funciona
- [ ] Probar con más carga (TV, laptop)
- [ ] Monitorear consumo y generación

---

## 📅 SEMANA 7: Integración y Calibración

### Conexión ESP32 al Sistema
- [ ] Conectar sensores de corriente en líneas correctas
- [ ] Conectar sensores de temperatura en paneles
- [ ] Conectar LDR para radiación solar
- [ ] Alimentar ESP32 con fuente 5V
- [ ] Verificar lecturas en dashboard

### Configuración Relés
- [ ] Conectar relés a ESP32 (GPIO 16, 17, 18, 19)
- [ ] Programar lógica de control
- [ ] Probar activación manual desde dashboard
- [ ] Probar modo automático

### Calibración Sensores
- [ ] Calibrar sensores de corriente con pinza amperométrica
- [ ] Calibrar voltaje con multímetro
- [ ] Ajustar factores de corrección en código
- [ ] Verificar precisión ±5%

### Puesta en Marcha
- [ ] Sistema funcionando 100% solar
- [ ] Red como backup automático
- [ ] Datos llegando al dashboard
- [ ] IA empezando a aprender patrones

---

## 📅 SEMANA 8: Monitoreo y Ajustes

### Recopilación de Datos
- [ ] Dejar sistema operando 24/7
- [ ] Revisar dashboard diariamente
- [ ] Anotar problemas o anomalías
- [ ] Capturar screenshots de métricas

### Análisis Semanal
- [ ] Calcular energía solar generada total
- [ ] Calcular consumo total de la casa
- [ ] Calcular % de autonomía lograda
- [ ] Comparar con predicciones

### Ajustes Finos
- [ ] Ajustar ángulo de paneles si es necesario
- [ ] Optimizar consumos de la casa
- [ ] Calibrar IA con datos reales
- [ ] Documentar lecciones aprendidas

---

## 🎯 Objetivos Medibles - Primer Mes

- [ ] **Uptime:** >90% del tiempo funcionando
- [ ] **Autonomía:** >40% de energía de paneles
- [ ] **Ahorro:** Reducir factura en $10,000+
- [ ] **Datos:** Mínimo 30 días de datos limpios
- [ ] **IA:** Predicciones con >70% precisión

---

## 📞 Contactos de Emergencia

### Electricista Matriculado
- Nombre: _______________________
- Tel: _________________________
- Matrícula: ____________________

### Proveedor Paneles
- Empresa: _____________________
- Tel: _________________________
- Garantía: ____________________

### Proveedor Batería
- Empresa: _____________________
- Tel: _________________________
- Garantía: ____________________

### Soporte Técnico ESP32/Software
- GitHub Issues
- Email: _______________________

---

## 🚨 En Caso de Problema

### Batería no carga
1. Verificar fusible entre MPPT y batería
2. Verificar cables bien conectados
3. Verificar voltaje de paneles (>48V)
4. Verificar configuración MPPT (debe ser 48V)

### Inversor no enciende
1. Verificar batería tiene carga (>48V)
2. Verificar fusible entre batería e inversor
3. Verificar conexión a tierra
4. Revisar manual del inversor

### ESP32 no envía datos
1. Verificar conexión WiFi
2. Verificar backend está corriendo
3. Verificar IP correcta en código
4. Revisar logs de consola

### Peligro eléctrico
1. **Cortar alimentación inmediatamente**
2. No tocar cables si hay chispa/humo
3. Usar extintor ABC si hay fuego
4. Llamar electricista

---

## 📈 Seguimiento Mensual

### Mes 1
- Fecha inicio: __________
- kWh generados: __________
- kWh consumidos: __________
- % autonomía: __________
- Problemas: __________

### Mes 2
- kWh generados: __________
- kWh consumidos: __________
- % autonomía: __________
- Mejoras: __________

### Mes 3
- kWh generados: __________
- kWh consumidos: __________
- % autonomía: __________
- Lecciones: __________

---

**¡Éxitos con la instalación!** 🚀⚡☀️

*Ir tildando items a medida que se completan*
