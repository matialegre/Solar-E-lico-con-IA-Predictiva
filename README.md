# 🔋 Sistema Inversor Inteligente Híbrido

Sistema de gestión energética híbrido (Solar + Eólico + Batería) con Inteligencia Artificial predictiva basada en datos meteorológicos en tiempo real.

## 🔧 Configuración Personalizada (NUEVO)

**¡El sistema SE ADAPTA a tu casa!**

```cmd
CONFIGURAR_SISTEMA.bat
```

El asistente interactivo te preguntará:
- ✅ **Tu ubicación** → Obtiene datos climáticos REALES de tu zona
- ✅ **Tu consumo** → Dimensiona el sistema exacto que necesitas
- ✅ **Tu presupuesto** → Recomienda paneles, turbinas y batería

**Beneficios:**
- 📊 Sistema dimensionado específicamente para ti
- 💨 Considera viento y sol de TU zona (vía API)
- 🔋 Batería correctamente calculada
- 💰 Presupuesto real basado en tu consumo
- 📋 Guarda configuración en `configuracion_usuario.json`

**Documentación:** [GUIA_CONFIGURACION.md](GUIA_CONFIGURACION.md)

---

## 🏠 Instalación en Casa de Prueba

**¿Primera vez instalando? Empezá por acá:**

1. 🔧 **[CONFIGURAR_SISTEMA.bat](GUIA_CONFIGURACION.md)** - Dimensiona TU sistema
2. 📋 **[Guía de Instalación Casa Prueba](INSTALACION_CASA_PRUEBA.md)** - Plan completo 8 semanas
3. 📊 **[Medición de Consumos](MEDICION_CONSUMOS.md)** - Medir consumo real antes de comprar
4. ✅ **[Checklist de Implementación](CHECKLIST_IMPLEMENTACION.md)** - Paso a paso semanal

**Presupuesto estimado:** ~$1,967,000 ARS (~USD 2,100)
**Timeline:** 8 semanas desde cero hasta sistema completo funcionando, controlado mediante IA predictiva y módulo IoT (ESP32).

## 🏗️ Arquitectura

```
├── backend/          # FastAPI + IA Predictiva
├── frontend/         # React + Tailwind Dashboard
├── firmware/         # ESP32 con FreeRTOS
├── database/         # Scripts SQL y migraciones
└── simulator/        # Simulador sin hardware
```

## 🚀 Características

- ✅ **IA Predictiva**: Predicción de energía disponible 24h con datos meteorológicos
- ✅ **Control Automático**: Decisiones inteligentes de priorización de fuentes
- ✅ **Dashboard Real-Time**: Visualización en tiempo real de todas las métricas
- ✅ **IoT ESP32**: Firmware con FreeRTOS para lectura de sensores
- ✅ **API Clima**: Integración con OpenWeatherMap
- ✅ **Modo Simulación**: Pruebas sin hardware físico
- ✅ **Notificaciones**: Alertas de déficit energético

## 📦 Instalación

### Backend
```bash
cd backend
pip install -r requirements.txt
python -m uvicorn main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm start
```

### Firmware ESP32
1. Instalar PlatformIO
2. Abrir proyecto en `firmware/`
3. Configurar WiFi en `config.h`
4. Compilar y subir

## 🔧 Configuración

### Variables de Entorno (.env)
```
DATABASE_URL=sqlite:///./inversor.db
OPENWEATHER_API_KEY=tu_api_key
MQTT_BROKER=localhost
MQTT_PORT=1883
LATITUDE=40.4168
LONGITUDE=-3.7038
```

## 🎮 Uso

1. **Iniciar Backend**: `python main.py`
2. **Iniciar Frontend**: `npm start`
3. **Modo Simulación**: Activar desde dashboard o `python simulator/simulator.py`

## 📊 API Endpoints

- `GET /api/energy/current` - Estado actual del sistema
- `GET /api/energy/history` - Histórico de energía
- `GET /api/predictions/24h` - Predicciones 24 horas
- `POST /api/control/manual` - Control manual de fuentes
- `POST /api/control/auto` - Activar/desactivar modo automático

## 🧠 IA Predictiva

El sistema utiliza:
- **Random Forest Regressor** para predicción de generación solar/eólica
- **Datos meteorológicos** de OpenWeatherMap
- **Históricos** de consumo y generación
- **Cálculo de autonomía** basado en consumo actual

## 📱 Hardware Soportado

- ESP32 (recomendado)
- Raspberry Pi
- Sensores de voltaje/corriente (ACS712, INA219)
- Relés para conmutación

## 📄 Licencia

MIT License

## 👥 Autor

Sistema desarrollado para gestión inteligente de energía renovable
