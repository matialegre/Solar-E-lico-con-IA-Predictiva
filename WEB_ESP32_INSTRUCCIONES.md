# 🌐 WEB LOCAL DEL ESP32 - INSTRUCCIONES

## ✅ LO QUE SE AGREGÓ:

---

## 📁 **1. ARCHIVOS NUEVOS:**

### **Backend:**
- ✅ `nasa_power_service.py` - Servicio NASA POWER API
- ✅ Endpoint: `GET /api/climate/historical` - Datos históricos reales

### **Firmware:**
- ✅ `web_server.h` - Servidor web local del ESP32
- Dashboard HTML en tiempo real

### **Modificaciones:**
- ✅ `recommendation_service.py` - Ahora usa datos NASA POWER
- ✅ `inversor_hibrido.ino` - Incluye servidor web
- ✅ `main.py` - Endpoint datos climáticos

---

## 🌐 **2. WEB LOCAL DEL ESP32**

### **¿Qué muestra?**

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃         🔌 ESP32 Inversor Híbrido             ┃
┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
┃  ● ONLINE    ESP32_INVERSOR_001               ┃
┃  🌐 Conectado al servidor                     ┃
┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
┃                                                ┃
┃  🔋 Batería          ☀️ Solar                 ┃
┃   Voltaje: 48.5V      Corriente: 12.5A        ┃
┃   SOC: 85%            Potencia: 612W           ┃
┃   Temp: 25.0°C        Irradiancia: 850 W/m²   ┃
┃                                                ┃
┃  💨 Eólica           ⚡ Consumo                ┃
┃   Corriente: 8.2A     Corriente: 15.3A        ┃
┃   Potencia: 402W      Potencia: 750W          ┃
┃   Viento: 6.5 m/s     Balance: +264W          ┃
┃                                                ┃
┃  🔌 Estado de Relés:                          ┃
┃   ☀️ SOLAR: ON   💨 EÓLICA: ON                ┃
┃   🔌 RED: OFF    ⚡ CARGA: ON                  ┃
┃                                                ┃
┃            [🔄 Actualizar Datos]               ┃
┃                                                ┃
┃  Última actualización: 16:45:23               ┃
┃  IP Local: 192.168.0.122                      ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
```

### **Características:**
- ✅ **Se actualiza solo cada 2 segundos**
- ✅ **Muestra todos los ADCs** en tiempo real
- ✅ **Estado de relés** (ON/OFF con colores)
- ✅ **Estado de conexión** con el servidor
- ✅ **Balance de potencia** (generación - consumo)
- ✅ **Responsive** (funciona en móvil)

---

## 🔧 **3. CÓMO USAR:**

### **Paso 1: Agregar librería AsyncWebServer**

**Para Arduino IDE:**
```
1. Sketch → Include Library → Manage Libraries
2. Buscar: "ESPAsyncWebServer"
3. Instalar: ESPAsyncWebServer by me-no-dev
4. También instalar: AsyncTCP by me-no-dev
```

**O copiar esta librería:**
```
Arduino/libraries/ESPAsyncWebServer/
Arduino/libraries/AsyncTCP/
```

### **Paso 2: Compilar y subir firmware**

```
1. Abrir: inversor_hibrido.ino
2. Verificar que incluya: #include "web_server.h"
3. Compilar
4. Subir al ESP32
```

### **Paso 3: Acceder a la web local**

```
1. Conectar ESP32
2. Abrir Monitor Serie
3. Ver mensaje:
   ================================================
   🌐 Servidor web iniciado
      Acceso local: http://192.168.0.122
      Dashboard en tiempo real disponible
   ================================================

4. Abrir en navegador: http://192.168.0.122
```

---

## 🎯 **4. MODELO DE APRENDIZAJE NASA POWER**

### **¿Qué hace?**

1. **Obtiene datos históricos** de 5 años de la ubicación
2. **Calcula promedios** de:
   - Radiación solar (kWh/m²/día)
   - Velocidad del viento (m/s)
   - Horas de sol pico

3. **Genera patrones estacionales:**
   - Verano (Dic-Feb)
   - Otoño (Mar-May)
   - Invierno (Jun-Ago)
   - Primavera (Sep-Nov)

4. **Identifica mejores/peores meses**

### **Endpoint:**
```
GET /api/climate/historical?latitude=-38.7183&longitude=-62.2663&years=5
```

### **Respuesta:**
```json
{
  "status": "success",
  "source": "NASA POWER",
  "location": {
    "latitude": -38.7183,
    "longitude": -62.2663
  },
  "period": {
    "start": "2020-01-01",
    "end": "2025-01-01",
    "years": 5
  },
  "averages": {
    "solar_irradiance_kwh_m2_day": 5.5,
    "solar_irradiance_w_m2": 850,
    "wind_speed_ms": 6.5,
    "sun_hours_day": 5.5
  },
  "monthly": {
    "solar_kwh_m2_day": {
      "1": 7.2, "2": 6.8, "3": 5.5, ...
    },
    "wind_ms": {
      "1": 7.5, "2": 7.2, "3": 6.8, ...
    }
  },
  "seasonal": {
    "summer": {
      "solar_kwh_m2_day": 7.0,
      "wind_ms": 7.3
    },
    "winter": {
      "solar_kwh_m2_day": 3.5,
      "wind_ms": 5.8
    }
  },
  "best_month_solar": 1,
  "worst_month_solar": 6
}
```

---

## 🚀 **5. FLUJO COMPLETO AHORA:**

```
1. ESP32 se enciende
   ↓
2. Conecta al WiFi
   ↓
3. Inicia servidor web local (puerto 80)
   ↓
4. Se registra en servidor remoto
   ↓
5. Monitor Serie muestra:
   ✅ CONEXIÓN EXITOSA CON EL SERVIDOR
   🌐 Servidor web iniciado
      Acceso local: http://192.168.0.122
   ↓
6. Desde tu navegador local:
   http://192.168.0.122
   → Ves ADCs, relés, estado EN TIEMPO REAL
   ↓
7. Desde argentina.ngrok.pro:
   http://190.211.201.217:11113
   → Ves panel ESP32 + wizard + todo el dashboard
   ↓
8. Wizard usa datos NASA POWER REALES
   → Recomendación basada en clima histórico de la zona
```

---

## 📋 **6. PARA INSTALAR LIBRERÍAS:**

### **Método 1: Desde GitHub**
```bash
cd Arduino/libraries/
git clone https://github.com/me-no-dev/ESPAsyncWebServer.git
git clone https://github.com/me-no-dev/AsyncTCP.git
```

### **Método 2: Descargar ZIP**
1. https://github.com/me-no-dev/ESPAsyncWebServer/archive/master.zip
2. https://github.com/me-no-dev/AsyncTCP/archive/master.zip
3. Sketch → Include Library → Add .ZIP Library

---

## ✅ **RESUMEN:**

```
✅ Servidor web local en ESP32 (puerto 80)
✅ Dashboard HTML con datos en tiempo real
✅ Se actualiza solo cada 2 segundos
✅ Muestra ADCs, relés, conexión servidor
✅ NASA POWER API integrada (5 años histórico)
✅ Recomendaciones basadas en clima real
✅ Patrones estacionales calculados
✅ Todo funcionando en paralelo
```

---

**¡EL SISTEMA ESTÁ COMPLETÍSIMO!** 🎉
