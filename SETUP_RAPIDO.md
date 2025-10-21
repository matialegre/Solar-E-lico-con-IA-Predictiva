# ⚡ Setup Rápido con tu ngrok

## Ya tienes ngrok corriendo ✅

Tu URL: `https://argentina.ngrok.pro`

## 🚀 Solo 3 pasos

### 1. Iniciar el sistema
```cmd
start_simple.bat
```

Esto inicia:
- Backend en puerto 8000
- Simulador
- Frontend en puerto 3000

### 2. Configurar Frontend

Edita `frontend\.env`:

```env
REACT_APP_API_URL=https://argentina.ngrok.pro
```

**⚠️ IMPORTANTE**: Asegúrate que tu ngrok esté apuntando al puerto 8000:
```cmd
ngrok http 8000 --region=sa
```

### 3. Reiniciar Frontend

```cmd
# Ctrl+C en la ventana del Frontend
# Luego:
cd frontend
npm start
```

## ✅ ¡Listo!

Ahora puedes compartir:
- `https://argentina.ngrok.pro` → Para usar la API
- `https://argentina.ngrok.pro/docs` → Para ver documentación
- Frontend local: `http://localhost:3000`

## 📝 Notas

Si quieres exponer el frontend también:
```cmd
# En otra terminal
ngrok http 3000 --region=sa
```

Y obtendrás otra URL para el dashboard.

---

**Resumen**: 
1. `start_simple.bat` 
2. Editar `frontend\.env` con tu URL de ngrok
3. Reiniciar frontend
