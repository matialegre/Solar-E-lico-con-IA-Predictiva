# 🔧 Solución Error 404 - URLs Duplicadas `/api/api/`

## 🔍 Problema:
El frontend está haciendo peticiones a:
```
http://localhost:3002/api/api/dashboard  ❌ (duplicado)
```

En lugar de:
```
http://localhost:8801/api/dashboard  ✅ (correcto)
```

---

## ⚠️ Causa:
React compiló el bundle JavaScript con el valor **VIEJO** de `.env`:
```env
REACT_APP_API_URL=/api  ❌ (viejo)
```

Y aunque lo cambiastes a:
```env
REACT_APP_API_URL=http://localhost:8801  ✅ (nuevo)
```

**El navegador y Node todavía tienen el código viejo en caché.**

---

## ✅ Solución Rápida:

### **Opción 1: Usar el script automático** (MÁS FÁCIL)

1. **Ejecutar:**
   ```cmd
   LIMPIAR_Y_REINICIAR.bat
   ```

2. **Esperar** a que ambos servidores arranquen (verás mensajes en las ventanas)

3. **En el navegador:**
   - Presionar `Ctrl + Shift + R` (Windows/Linux)
   - O `Cmd + Shift + R` (Mac)
   - Esto hace un "hard refresh" y limpia caché del navegador

---

### **Opción 2: Manual** (si la Opción 1 no funciona)

#### Paso 1: Detener TODO
```cmd
DETENER_TODO.bat
```

#### Paso 2: Limpiar caché de npm
```cmd
cd frontend
rmdir /s /q node_modules\.cache
rmdir /s /q build
```

#### Paso 3: Verificar .env
Abrir `frontend/.env` y verificar que diga:
```env
REACT_APP_API_URL=http://localhost:8801
PORT=3002
```

#### Paso 4: Reiniciar
```cmd
cd ..
INICIAR_TODO.bat
```

#### Paso 5: Limpiar navegador
En el navegador:
1. Abrir DevTools (F12)
2. Click derecho en el botón de recargar
3. Seleccionar "Vaciar caché y recargar de forma forzada"

**O simplemente:**
- `Ctrl + Shift + R`

---

## 🎯 Verificación:

### Una vez reiniciado, deberías ver:

**En la consola del navegador (F12):**
```
✅ WebSocket conectado
```

**Y NO deberías ver:**
```
❌ :3002/api/api/dashboard (404)
```

**Deberías ver peticiones a:**
```
✅ http://localhost:8801/api/dashboard (200)
✅ http://localhost:8801/api/energy/history (200)
✅ http://localhost:8801/api/predictions/24h (200)
```

---

## 🚀 Después de Reiniciar:

1. **Backend debería estar en:** `http://localhost:8801`
2. **Frontend debería estar en:** `http://localhost:3002`
3. **WebSocket debería conectar a:** `ws://localhost:8801/api/ws`

---

## 📊 Cómo Verificar que Funciona:

### En el navegador, abre DevTools (F12) y verifica:

**Network tab:**
- Las peticiones van a `localhost:8801` ✅
- NO van a `localhost:3002/api/api/` ❌

**Console tab:**
- `✅ WebSocket conectado`
- NO hay errores 404

**En la página:**
- Dashboard se carga con datos
- Gráficos aparecen
- Protección de batería visible
- Todo funciona

---

## 🆘 Si AÚN no funciona:

### 1. Verificar que backend esté corriendo:
Abrir en navegador: http://localhost:8801/docs

Deberías ver la documentación de la API (Swagger UI)

### 2. Verificar puerto del backend:
```cmd
netstat -ano | findstr :8801
```
Debería mostrar que el puerto 8801 está en uso

### 3. Verificar .env del backend:
Archivo: `backend/.env`
```env
PORT=8801  ✅ (debe ser 8801)
```

### 4. Cerrar TODAS las ventanas de terminal/PowerShell
A veces quedan procesos zombie:
```cmd
taskkill /F /IM node.exe
taskkill /F /IM python.exe
```

Luego reiniciar con `INICIAR_TODO.bat`

---

## 💡 Para el Futuro:

### Cambios en archivos `.env` requieren:
1. ✅ Detener servidores
2. ✅ Limpiar caché (especialmente frontend)
3. ✅ Reiniciar servidores
4. ✅ Hard refresh en navegador (Ctrl+Shift+R)

### Variables de entorno en React:
- Solo las que empiezan con `REACT_APP_` son visibles
- Se compilan en el bundle cuando se inicia `npm start`
- Cambiarlas requiere reiniciar el servidor de desarrollo

---

**¡Con esto debería funcionar todo!** 🎉

Si después de seguir estos pasos aún hay problemas, puede ser:
- Firewall bloqueando el puerto 8801
- Antivirus bloqueando las conexiones
- Otro proceso usando el puerto 8801
