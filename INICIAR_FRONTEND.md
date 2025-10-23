# 🚀 INICIAR FRONTEND

## Paso 1: Abrir terminal en carpeta frontend

```cmd
cd X:\PREDICCION DE CLIMA\frontend
```

## Paso 2: Instalar dependencias (solo primera vez)

```cmd
npm install
```

## Paso 3: Iniciar desarrollo

```cmd
npm start
```

El navegador se abrirá automáticamente en `http://localhost:3000`

---

## ✅ Si funciona correctamente

Deberías ver el dashboard con:
- Datos del ESP32 en tiempo real
- Gráficos de energía
- Estado de batería
- Controles de relés

---

## 🔧 Si hay errores

### Error: `npm: command not found`

Necesitas instalar Node.js:
1. Descarga desde: https://nodejs.org/
2. Instala versión LTS
3. Reinicia terminal
4. Intenta de nuevo

### Error: Puerto 3000 ocupado

```cmd
# Usar otro puerto
set PORT=3001 && npm start
```

### Error: CORS o no conecta con backend

Verifica en `frontend/src/api/config.js` que la URL sea:
```javascript
const API_URL = 'http://190.211.201.217:11113';
```

---

## 🎨 Acceder al frontend

Una vez iniciado:
- **Local:** http://localhost:3000
- **Red local:** http://192.168.0.122:3000
- **IP pública:** http://190.211.201.217:3000

---

## 🛑 Detener frontend

Presiona `Ctrl+C` en la terminal donde está corriendo.
