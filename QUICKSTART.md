# ⚡ Inicio Rápido - 5 Minutos

## 🎯 Objetivo
Tener el sistema funcionando en **modo simulación** en menos de 5 minutos.

## 📋 Pre-requisitos
- ✅ Python 3.8+
- ✅ Node.js 16+
- ✅ 10 GB de espacio libre

## 🚀 Pasos

### 1. Descargar/Clonar el Proyecto
```bash
# Si tienes Git
git clone <repository-url>
cd PREDICCION_DE_CLIMA

# O descargar y extraer ZIP
```

### 2. Configurar Variables de Entorno
```bash
# Copiar archivo de ejemplo
copy .env.example .env

# Editar .env (opcional para empezar)
# Por defecto funciona en modo simulación
```

### 3. Opción A: Inicio Automático (Windows)

**Doble clic en:**
```
start_all.bat
```

Esto abrirá 3 ventanas:
- Backend (servidor)
- Simulador (datos falsos)
- Frontend (dashboard)

### 3. Opción B: Inicio Manual

**Terminal 1 - Backend:**
```bash
cd backend
pip install -r requirements.txt
python main.py
```

**Terminal 2 - Simulador:**
```bash
cd backend
python simulator.py
```

**Terminal 3 - Frontend:**
```bash
cd frontend
npm install
npm start
```

### 4. Abrir Dashboard

Navegar a: **http://localhost:3000**

## ✅ Verificación

Deberías ver:
- ✅ Métricas actualizándose cada 10 segundos
- ✅ Gráficos con datos simulados
- ✅ Estado "Conectado" en verde
- ✅ Panel de clima (datos simulados)
- ✅ Predicciones de IA

## 🎮 Probar el Sistema

1. **Ver datos en tiempo real**: Los valores cambian automáticamente
2. **Activar modo manual**: Toggle en "Modo Automático IA"
3. **Controlar fuentes**: Botones de Solar, Eólica, etc.
4. **Ver predicciones**: Panel de predicción 24h
5. **Verificar alertas**: Panel de alertas (si las hay)

## 🔧 URLs Útiles

| Servicio | URL |
|----------|-----|
| Dashboard | http://localhost:3000 |
| API Backend | http://localhost:8000 |
| API Docs | http://localhost:8000/docs |
| ReDoc | http://localhost:8000/redoc |

## 🐛 Solución de Problemas Rápida

### Error: Puerto en uso
```bash
# Matar proceso en puerto 8000
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Error: Módulo no encontrado
```bash
# Backend
cd backend
pip install -r requirements.txt --upgrade

# Frontend
cd frontend
rm -rf node_modules
npm install
```

### No aparecen datos
1. Verificar que simulador esté corriendo
2. Abrir http://localhost:8000/api/system/status
3. Debe responder: `{"status": "online"}`

## 📚 Siguiente Paso

Una vez funcionando, consulta:
- 📖 **USER_GUIDE.md** - Cómo usar el sistema
- 🏗️ **ARCHITECTURE.md** - Entender la arquitectura
- 🔧 **INSTALLATION.md** - Configuración avanzada
- 🔌 **firmware/README.md** - Conectar hardware real

## 🎉 ¡Listo!

Ahora tienes un sistema completo de gestión de energía renovable con IA funcionando en tu computadora.

---

**Tiempo estimado**: 5-10 minutos  
**Dificultad**: ⭐⭐☆☆☆ (Fácil)
