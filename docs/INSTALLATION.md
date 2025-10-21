# 📦 Guía de Instalación Completa

## Requisitos Previos

### Software
- Python 3.8+
- Node.js 16+
- Git
- PlatformIO (para ESP32)

### Hardware (Opcional)
- ESP32 DevKit
- Sensores de voltaje/corriente
- Módulo de relés
- Sistema de energía renovable

## 1️⃣ Clonar el Repositorio

```bash
git clone <repository-url>
cd PREDICCION_DE_CLIMA
```

## 2️⃣ Configurar Backend

### Instalar dependencias

```bash
cd backend
pip install -r requirements.txt
```

### Configurar variables de entorno

```bash
cp ../.env.example .env
```

Editar `.env`:
```env
DATABASE_URL=sqlite:///./inversor.db
OPENWEATHER_API_KEY=tu_api_key_aqui
LATITUDE=40.4168
LONGITUDE=-3.7038
BATTERY_CAPACITY_WH=5000
```

### Obtener API Key de OpenWeatherMap

1. Registrarse en: https://openweathermap.org/api
2. Crear API key gratuita
3. Copiarla en `.env`

### Inicializar base de datos

```bash
python -c "from database import init_db; init_db()"
```

### Iniciar servidor

```bash
python main.py
```

El servidor estará en: http://localhost:8000

Documentación API: http://localhost:8000/docs

## 3️⃣ Configurar Frontend

### Instalar dependencias

```bash
cd ../frontend
npm install
```

### Configurar API URL

```bash
cp .env.example .env
```

Editar `.env`:
```env
REACT_APP_API_URL=http://localhost:8000
```

### Iniciar aplicación

```bash
npm start
```

La aplicación estará en: http://localhost:3000

## 4️⃣ Modo Simulación (Sin Hardware)

Para probar el sistema sin hardware físico:

### Terminal 1 - Backend
```bash
cd backend
python main.py
```

### Terminal 2 - Simulador
```bash
cd backend
python simulator.py --interval 10
```

### Terminal 3 - Frontend
```bash
cd frontend
npm start
```

Ahora verás datos simulados en el dashboard.

## 5️⃣ Configurar ESP32 (Producción)

### Instalar PlatformIO

```bash
pip install platformio
```

### Configurar WiFi

Editar `firmware/include/config.h`:
```cpp
#define WIFI_SSID "TU_WIFI"
#define WIFI_PASSWORD "TU_PASSWORD"
#define SERVER_URL "http://IP_SERVIDOR:8000"
```

### Compilar y subir

```bash
cd firmware
pio run --target upload
pio device monitor
```

## 6️⃣ Arquitectura de Despliegue

### Desarrollo Local
```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  Frontend   │────▶│   Backend   │◀────│  Simulator  │
│ localhost:  │     │ localhost:  │     │   Python    │
│    3000     │     │    8000     │     │             │
└─────────────┘     └─────────────┘     └─────────────┘
```

### Producción con Hardware
```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  Frontend   │────▶│   Backend   │◀────│    ESP32    │
│   (Build)   │     │  + SQLite   │     │  + Sensores │
└─────────────┘     └─────────────┘     └─────────────┘
```

## 7️⃣ Verificación de Instalación

### Backend
```bash
curl http://localhost:8000/api/system/status
```

Respuesta esperada:
```json
{
  "status": "online",
  "version": "1.0.0",
  "auto_mode": true
}
```

### Frontend
Abrir http://localhost:3000 en navegador

### Simulador
Verificar logs:
```
✓ [10:30:45] Solar: 1245W | Viento: 567W | Batería: 75.3% | Consumo: 450W
```

## 8️⃣ Troubleshooting

### Error: Puerto 8000 en uso
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:8000 | xargs kill -9
```

### Error: ModuleNotFoundError
```bash
pip install -r backend/requirements.txt --upgrade
```

### Error: npm dependencies
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### Base de datos corrupta
```bash
cd backend
rm inversor.db
python -c "from database import init_db; init_db()"
```

## 9️⃣ Despliegue en Producción

### Backend (Ubuntu Server)

```bash
# Instalar dependencias
sudo apt update
sudo apt install python3-pip nginx

# Instalar aplicación
cd /opt
git clone <repo>
cd PREDICCION_DE_CLIMA/backend
pip3 install -r requirements.txt

# Crear servicio systemd
sudo nano /etc/systemd/system/inversor.service
```

```ini
[Unit]
Description=Inversor Inteligente Backend
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/PREDICCION_DE_CLIMA/backend
ExecStart=/usr/bin/python3 main.py
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# Iniciar servicio
sudo systemctl enable inversor
sudo systemctl start inversor
```

### Frontend (Build para producción)

```bash
cd frontend
npm run build

# Servir con nginx
sudo cp -r build/* /var/www/html/
```

## 🎉 ¡Instalación Completa!

Ahora deberías tener:
- ✅ Backend corriendo en puerto 8000
- ✅ Frontend accesible en navegador
- ✅ Simulador generando datos (o ESP32 conectado)
- ✅ Dashboard mostrando métricas en tiempo real

## 📚 Próximos Pasos

1. Revisar la documentación de la API
2. Personalizar umbrales de alertas
3. Entrenar modelo de IA con datos reales
4. Configurar notificaciones
5. Conectar hardware físico

## 🆘 Soporte

Si encuentras problemas:
1. Revisar logs del servidor
2. Verificar configuración de red
3. Comprobar versiones de dependencias
4. Consultar la documentación
