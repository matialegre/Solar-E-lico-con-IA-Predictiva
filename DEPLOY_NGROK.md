# 🌐 Despliegue con ngrok - Guía Completa

## ¿Qué es ngrok?

**ngrok** crea un túnel seguro que expone tu servidor local a Internet con una URL pública.

## 📋 Requisitos Previos

### 1. Instalar ngrok

**Opción A - Descarga directa:**
```bash
# Descargar desde:
https://ngrok.com/download

# Descomprimir y agregar al PATH
```

**Opción B - Con Chocolatey:**
```cmd
choco install ngrok
```

### 2. Crear cuenta en ngrok (gratis)
```
https://dashboard.ngrok.com/signup
```

### 3. Autenticar ngrok
```bash
# Obtener tu authtoken desde:
https://dashboard.ngrok.com/get-started/your-authtoken

# Configurar:
ngrok config add-authtoken TU_TOKEN_AQUI
```

## 🚀 Métodos de Inicio

### Método 1: Script Completo (Recomendado)

**Inicia TODO el sistema + ngrok:**

```cmd
start_with_ngrok.bat
```

Este script:
- ✅ Inicia Backend (puerto 8000)
- ✅ Inicia Simulador
- ✅ Inicia Frontend (puerto 3000)
- ✅ Crea tunnel ngrok para Backend
- ✅ Crea tunnel ngrok para Frontend

### Método 2: Solo Tunnels ngrok

Si ya tienes el sistema corriendo:

```cmd
start_ngrok_only.bat
```

### Método 3: Manual

```bash
# Terminal 1 - Backend
cd backend
python main.py

# Terminal 2 - Simulador
cd backend
python simulator.py

# Terminal 3 - Frontend
cd frontend
npm start

# Terminal 4 - ngrok Backend
ngrok http 8000 --region=sa

# Terminal 5 - ngrok Frontend
ngrok http 3000 --region=sa
```

## 🔧 Configuración

### Paso 1: Obtener URLs de ngrok

Después de ejecutar ngrok, verás algo así:

```
Session Status                online
Forwarding                    https://abc123.ngrok.io -> http://localhost:8000
```

**Copia la URL**: `https://abc123.ngrok.io`

### Paso 2: Configurar Frontend

Edita `frontend/.env`:

```env
# Cambiar de:
REACT_APP_API_URL=http://localhost:8000

# A:
REACT_APP_API_URL=https://abc123.ngrok.io
```

### Paso 3: Reiniciar Frontend

```cmd
# Ctrl+C en la ventana del frontend
# Luego:
npm start
```

## 🌐 URLs Públicas

Después de configurar, tendrás:

| Servicio | URL Pública |
|----------|-------------|
| **Backend API** | https://abc123.ngrok.io |
| **API Docs** | https://abc123.ngrok.io/docs |
| **Frontend** | https://xyz789.ngrok.io |

## 📊 Monitoreo de ngrok

### Web Interface

Abre en tu navegador:

```
http://127.0.0.1:4040  (Backend)
http://127.0.0.1:4041  (Frontend)
```

Verás:
- ✅ Requests en tiempo real
- ✅ Headers HTTP
- ✅ Payloads
- ✅ Tiempos de respuesta
- ✅ Replay de requests

## 🔐 Seguridad

### Proteger con Contraseña (Plan Gratis)

```cmd
ngrok http 8000 --region=sa --basic-auth="usuario:password"
```

### Configuración Permanente

Crear `ngrok.yml`:

```yaml
version: "2"
authtoken: TU_TOKEN
region: sa
tunnels:
  backend:
    proto: http
    addr: 8000
    basic_auth:
      - "usuario:password"
  frontend:
    proto: http
    addr: 3000
```

Iniciar con:
```cmd
ngrok start --all
```

## 🌍 Regiones Disponibles

```cmd
--region=us     # Estados Unidos
--region=eu     # Europa
--region=ap     # Asia Pacífico
--region=au     # Australia
--region=sa     # Sudamérica (el más cercano para Argentina)
--region=jp     # Japón
--region=in     # India
```

## 📱 Compartir con Otros

Una vez que tengas las URLs públicas:

1. **Backend API**: `https://abc123.ngrok.io`
   - Comparte con desarrolladores
   - Para integración con apps
   - Testing de API

2. **Frontend**: `https://xyz789.ngrok.io`
   - Comparte con usuarios finales
   - Para demos
   - Testing en dispositivos móviles

## ⚠️ Limitaciones Plan Gratuito

- ✅ 1 usuario
- ✅ 40 conexiones/minuto
- ✅ 1 tunnel activo a la vez (con cuenta)
- ⚠️ URLs cambian al reiniciar ngrok
- ⚠️ 8 horas máximo por sesión

### Solución: Plan Pago

- Plan Personal ($8/mes):
  - 3 tunnels simultáneos
  - URLs personalizadas (ej: `miapp.ngrok.io`)
  - Sin límite de tiempo

## 🐛 Troubleshooting

### Error: "Failed to establish a connection"

```bash
# Verificar que el servicio local esté corriendo
curl http://localhost:8000/api/system/status
```

### Error: "Account limit exceeded"

Estás usando múltiples tunnels sin autenticación:

```bash
# Autenticarte con token
ngrok config add-authtoken TU_TOKEN
```

### Frontend no se conecta al Backend

Verificar en `frontend/.env`:
```env
REACT_APP_API_URL=https://URL_CORRECTA_NGROK.ngrok.io
```

NO incluir barra final `/`

### CORS Error

Agregar en `backend/main.py` (ya está configurado):

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción: lista específica
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## 📈 Uso Avanzado

### Inspeccionar Tráfico

```bash
# En la interfaz web (http://127.0.0.1:4040)
# Puedes:
- Ver todos los requests
- Replay requests
- Ver response bodies
- Analizar performance
```

### Logs Detallados

```bash
ngrok http 8000 --region=sa --log=stdout --log-level=debug
```

### Guardar Logs

```bash
ngrok http 8000 --region=sa --log=ngrok.log
```

## 🎯 Casos de Uso

### 1. Demo para Clientes
```cmd
start_with_ngrok.bat
```
Comparte la URL del frontend con el cliente.

### 2. Testing en Móvil
Abre la URL de ngrok en tu teléfono para probar el dashboard responsive.

### 3. Webhook Development
Usa la URL de ngrok como endpoint para webhooks externos.

### 4. Colaboración Remota
Comparte la URL con tu equipo para testing conjunto.

## 🔄 Flujo Completo de Despliegue

```mermaid
1. Ejecutar start_with_ngrok.bat
2. Esperar que abran 5 ventanas
3. Copiar URL de ngrok del Backend
4. Actualizar frontend/.env
5. Reiniciar frontend
6. Compartir URL del Frontend
7. ¡Listo para usar!
```

## 📞 Soporte ngrok

- Documentación: https://ngrok.com/docs
- Dashboard: https://dashboard.ngrok.com
- Status: https://status.ngrok.com

---

## 🎉 ¡Listo!

Ahora tu Sistema Inversor Inteligente está accesible desde cualquier lugar del mundo.

**Comandos rápidos:**
```cmd
# Inicio completo con ngrok
start_with_ngrok.bat

# Solo tunnels (si ya está corriendo)
start_ngrok_only.bat

# Ver dashboard ngrok
# http://127.0.0.1:4040
```

---

**URLs después de configurar:**
- 🌐 Frontend Público: https://XXXXX.ngrok.io
- 🔌 Backend API Público: https://YYYYY.ngrok.io
- 📚 API Docs: https://YYYYY.ngrok.io/docs
