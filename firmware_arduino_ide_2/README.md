# 🔋 Firmware Arduino IDE 2.0

Firmware ESP32 sin librerías Adafruit - Solo ADC interno + OpAmps.

---

## 🚀 Inicio Rápido

1. **Abrir:** `File → Open → inversor_hibrido/inversor_hibrido.ino`
2. **Editar:** Pestaña `config.h` con tu WiFi
3. **Seleccionar:** `Tools → Board → ESP32 Dev Module`
4. **Subir:** Click → Upload

---

## 📋 Hardware

- ESP32 Dev Kit / WROOM-32
- ADC interno 12-bit
- Shunts + OpAmps (LM358)
- Divisores resistivos

**Pines usados:**
- GPIO 34,35,32: Voltajes (ADC1)
- GPIO 33,36,39: Corrientes (ADC1)
- GPIO 25: LDR (ADC2)
- GPIO 26: Anemómetro

---

## ⚙️ Configuración

Editar `config.h`:
```cpp
#define WIFI_SSID "TU_WIFI"
#define WIFI_PASSWORD "TU_PASSWORD"
#define SERVER_URL "http://190.211.201.217:11113"
```

---

## 📡 Comunicación

- **POST** telemetría cada 5 seg
- **GET** comandos cada 10 seg
- Sin MQTT, solo HTTP

---

Ver documentación completa en `/docs`
