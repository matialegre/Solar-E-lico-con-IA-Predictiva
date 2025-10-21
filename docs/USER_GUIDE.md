# 📖 Guía de Usuario

## Introducción

El Sistema Inversor Inteligente Híbrido te permite monitorear y controlar tu sistema de energía renovable con la ayuda de inteligencia artificial.

## 🎯 Características Principales

### ✅ Monitoreo en Tiempo Real
- Generación solar y eólica actual
- Estado de batería (voltaje, corriente, SoC)
- Consumo del hogar
- Balance energético instantáneo

### 🤖 Inteligencia Artificial
- Predicción de generación para 24 horas
- Estimación de consumo futuro
- Cálculo de autonomía
- Detección de déficit energético

### 🎛️ Control Inteligente
- Modo automático con IA
- Control manual de fuentes
- Priorización inteligente
- Protecciones de batería

### 📊 Visualización
- Gráficos históricos
- Predicciones futuras
- Clima en tiempo real
- Alertas y notificaciones

---

## 🚀 Inicio Rápido

### Primer Uso

1. **Iniciar el sistema**:
   - Windows: Doble clic en `start_all.bat`
   - Linux/Mac: Ejecutar scripts individuales

2. **Abrir dashboard**:
   - Navegador: http://localhost:3000

3. **Verificar conexión**:
   - LED verde "Conectado" en la esquina superior
   - Datos actualizándose cada 30 segundos

### Configuración Inicial

1. **Configurar ubicación**:
   - Editar `.env` → `LATITUDE` y `LONGITUDE`
   - Reiniciar backend

2. **Configurar capacidades**:
   ```env
   BATTERY_CAPACITY_WH=5000    # Capacidad batería (Wh)
   MAX_SOLAR_POWER_W=3000      # Máxima potencia solar (W)
   MAX_WIND_POWER_W=2000       # Máxima potencia eólica (W)
   ```

3. **Obtener API Key de clima**:
   - Registrarse en openweathermap.org
   - Copiar API key en `.env`

---

## 📊 Panel de Control (Dashboard)

### Métricas Principales

#### 1. Generación Solar ☀️
- **Valor**: Potencia actual en Watts
- **Porcentaje**: % de capacidad máxima
- **Color**: 
  - Amarillo: Generando
  - Gris: Sin generación (noche)

#### 2. Generación Eólica 🌬️
- **Valor**: Potencia actual en Watts
- **Indicador**: Viento disponible
- **Variabilidad**: Puede cambiar rápidamente

#### 3. Batería 🔋
- **SoC**: Estado de carga (%)
- **Estado**: Cargando/Descargando
- **Potencia**: W positivos (carga) o negativos (descarga)
- **Colores**:
  - Verde: >50%
  - Amarillo: 20-50%
  - Rojo: <20% ⚠️

#### 4. Consumo Actual ⚡
- **Valor**: Potencia consumida (W)
- **Comparación**: % respecto a generación

#### 5. Balance Energético
- **Excedente**: Verde (+W)
- **Déficit**: Rojo (-W)

### Gráficos

#### Histórico 24h
- Línea amarilla: Solar
- Línea azul: Eólica
- Línea roja: Consumo

**Uso**: Identificar patrones diarios

#### Estado de Batería
- Evolución del SoC durante el día
- Identifica momentos de carga/descarga

#### Predicción IA
- Barras de predicción 24h
- Comparar con histórico para validar

---

## 🎛️ Modos de Operación

### Modo Automático (Recomendado) 🤖

**¿Cuándo usar?**
- Operación normal del día a día
- Confiar en las decisiones de IA
- Optimización automática

**Comportamiento**:
1. La IA analiza:
   - Estado actual
   - Clima
   - Predicciones
   - Histórico

2. Decide automáticamente:
   - Qué fuente usar
   - Si cargar batería
   - Cuándo alertar

3. Prioriza:
   - Renovables primero
   - Batería cuando es necesario
   - Red solo en emergencias

**Activar**:
- Toggle "Modo Automático IA" en panel de control

### Modo Manual 🎮

**¿Cuándo usar?**
- Mantenimiento del sistema
- Pruebas de componentes
- Situaciones específicas
- Emergencias

**Controles Disponibles**:
- ☀️ **Solar**: Activar/Desactivar
- 🌬️ **Eólica**: Activar/Desactivar
- 🔋 **Batería**: Activar/Desactivar
- ⚡ **Red**: Conectar/Desconectar

**⚠️ Advertencia**: En modo manual, las protecciones automáticas siguen activas en el ESP32.

---

## 📈 Predicciones y Autonomía

### Predicción 24 Horas

**Panel de predicción muestra**:
- Generación total esperada (kWh)
- Consumo previsto (kWh)
- Balance energético
- Horas con posible déficit

**Interpretación**:

✅ **Balance Positivo** (+X kWh)
- Generación > Consumo
- Batería se cargará
- Sistema estable

⚠️ **Balance Negativo** (-X kWh)
- Generación < Consumo
- Batería se descargará
- Planificar reducción de consumo

### Cálculo de Autonomía

**Autonomía = Energía Disponible / Consumo Actual**

Ejemplo:
```
Batería: 75% SoC de 5000Wh = 3750Wh disponibles
Consumo: 500W
Autonomía = 3750 / 500 = 7.5 horas
```

**Indicadores**:
- 🟢 Verde: >12h (muy buena)
- 🟡 Amarillo: 4-12h (moderada)
- 🔴 Rojo: <4h (baja)

---

## 🚨 Alertas

### Tipos de Alertas

#### 🔴 Críticas
- **Batería Crítica** (<20%)
  - Acción: Activar fuente alternativa inmediatamente
  - Reducir consumo no esencial
  
#### 🟡 Advertencias
- **Batería Baja** (20-30%)
  - Acción: Preparar generador o reducir consumo
  
- **Autonomía Reducida** (<2h)
  - Acción: Minimizar uso de energía

#### 🔵 Informativas
- **Déficit Previsto**
  - Acción: Planificar uso eficiente
  
- **Exceso de Generación**
  - Acción: Posible uso de cargas diferibles

### Gestión de Alertas

1. **Leer mensaje**: Descripción del problema
2. **Ver acción sugerida**: 💡 Recomendación
3. **Tomar acción**: Manual o automática
4. **Resolver**: La alerta desaparecerá cuando se solucione

---

## 🌤️ Widget de Clima

### Información Mostrada

- **Temperatura**: Actual en °C
- **Condiciones**: Descripción textual
- **Viento**: Velocidad en m/s
- **Humedad**: % relativa
- **Nubosidad**: % cobertura
- **Presión**: hPa
- **Radiación Solar**: W/m² (cuando disponible)

### Impacto en Energía

- **☁️ Nublado**: Reduce generación solar 30-75%
- **🌧️ Lluvia**: Reduce generación solar >75%
- **💨 Viento Fuerte**: Aumenta generación eólica
- **☀️ Despejado**: Máxima generación solar

---

## 💡 Consejos de Uso

### Optimizar Autonomía

1. **Usar electrodomésticos de alta potencia durante el día**
   - Lavadora, secadora, horno
   - Aprovechar generación solar

2. **Reducir consumo nocturno**
   - Apagar standby
   - Luces LED eficientes

3. **Cargar dispositivos con excedente**
   - Cuando balance es positivo
   - Durante picos de generación

### Interpretar Tendencias

**Gráfico de Batería Descendente** 📉
- Consumo > Generación
- Verificar clima
- Reducir carga si es necesario

**Gráfico de Batería Estable** ➡️
- Balance equilibrado
- Operación óptima

**Gráfico de Batería Ascendente** 📈
- Exceso de generación
- Buen momento para cargas extras

### Mantenimiento Preventivo

**Diario**:
- Revisar alertas
- Verificar autonomía
- Comprobar conectividad

**Semanal**:
- Analizar gráficos de tendencia
- Verificar precisión de predicciones
- Revisar histórico de alertas

**Mensual**:
- Calibrar sensores si es necesario
- Verificar conexiones físicas
- Actualizar firmware

---

## ❓ Preguntas Frecuentes

### ¿Por qué la predicción no coincide con la realidad?

**Razones**:
- Cambios climáticos repentinos
- Modelo en entrenamiento (primeros días)
- Datos meteorológicos imprecisos

**Solución**:
- El sistema mejora con más datos históricos
- Verificar API key de clima
- Después de 1-2 semanas será más preciso

### ¿Qué hacer si la batería está siempre baja?

**Diagnóstico**:
1. Verificar capacidad real vs configurada
2. Revisar consumo promedio
3. Verificar generación solar/eólica

**Acciones**:
- Reducir consumo base
- Agregar más paneles/turbinas
- Considerar batería de mayor capacidad

### ¿El sistema funciona sin internet?

**Con ESP32**:
- ❌ No puede enviar datos al servidor
- ✅ Protecciones locales siguen activas
- ✅ Relés funcionan según última configuración

**Backend**:
- ❌ No obtiene datos meteorológicos actualizados
- ✅ Usa últimos datos en cache
- ✅ Funcionalidad básica disponible

### ¿Puedo controlar desde mi teléfono?

**Actualmente**:
- ✅ Abrir http://IP_SERVIDOR:3000 en móvil
- ✅ Dashboard responsive

**Futuro**:
- App móvil nativa
- Notificaciones push
- Control offline

---

## 📞 Soporte

### Recursos
- 📘 Documentación: `docs/`
- 🔧 API Reference: `docs/API_REFERENCE.md`
- 🏗️ Arquitectura: `docs/ARCHITECTURE.md`
- 💻 Instalación: `docs/INSTALLATION.md`

### Logs para Debugging
- Backend: Console o archivo log
- ESP32: Serial Monitor (115200 baud)
- Frontend: Browser DevTools (F12)

### Reportar Problemas
1. Describir el problema
2. Incluir logs relevantes
3. Mencionar configuración
4. Pasos para reproducir
