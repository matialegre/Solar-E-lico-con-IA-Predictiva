# 🚀 Guía Rápida - Configuración IP Pública

## 🎯 Arquitectura Final

```
┌─────────────────────────────────────────────────────┐
│  INTERNET                                           │
│                                                     │
│  https://argentina.ngrok.pro ────────────┐         │
│                                          │         │
│  http://190.211.201.217:11113 ───────────┼─────┐   │
│                                          │     │   │
└──────────────────────────────────────────┼─────┼───┘
                                           │     │
                                           ▼     ▼
                                    ┌──────────────────┐
                                    │   TU PC          │
                                    │                  │
                                    │  Frontend:3002───┤ Ngrok
                                    │  Backend:11113───┤ IP Pública
                                    └──────────────────┘
```

**Frontend:** Ngrok túnel (https://argentina.ngrok.pro)  
**Backend:** IP pública directa (http://190.211.201.217:11113)

---

## ⚙️ PASOS DE CONFIGURACIÓN

### **1. Configurar Frontend para usar IP pública del backend**

```bash
CONFIGURAR_IP_PUBLICA.bat
```

O manualmente:
```bash
notepad frontend\.env
```

Cambiar:
```env
REACT_APP_API_URL=http://localhost:8801
```

Por:
```env
REACT_APP_API_URL=http://190.211.201.217:11113
```

---

### **2. Verificar puerto abierto en router/firewall**

**Puerto a abrir:** `11113`  
**Protocolo:** TCP  
**Destino:** Tu PC local (ej: 192.168.0.X)

**Verificar:**
```bash
# Desde otra red o PC externo:
curl http://190.211.201.217:11113/api/system/status
```

Si responde → Puerto abierto ✅

---

### **3. Iniciar sistema**

```bash
DETENER.bat
INICIAR.bat
```

---

## 🌐 URLs Finales

| Acceso | URL | Uso |
|--------|-----|-----|
| **Dashboard público** | https://argentina.ngrok.pro | Cualquier persona |
| **API pública** | http://190.211.201.217:11113/docs | ESP32, clientes externos |
| **Dashboard local** | http://localhost:3002 | Solo tu PC |
| **API local** | http://localhost:11113/docs | Solo tu PC |

---

## 🔌 Configuración ESP32

En `firmware/include/config.h`:

```cpp
// Backend con IP pública
#define SERVER_URL "http://190.211.201.217:11113"
#define DEVICE_ID "ESP32_INVERSOR_001"
```

El ESP32 enviará datos directamente a tu IP pública.

---

## ✅ Checklist

- [ ] `frontend\.env` configurado con IP pública
- [ ] Puerto 11113 abierto en router
- [ ] Firewall de Windows permite puerto 11113
- [ ] Backend iniciado con `--host 0.0.0.0`
- [ ] Ngrok apuntando al frontend (3002)

---

## 🔥 Comandos Finales

```bash
# Configurar
CONFIGURAR_IP_PUBLICA.bat

# Iniciar
INICIAR.bat

# Detener
DETENER.bat
```

---

## 🆘 Solución de Problemas

### **Frontend carga pero no hay datos:**
- Verificar que el backend esté corriendo: http://localhost:11113/docs
- Verificar `frontend\.env` tenga la IP correcta

### **Ngrok muestra 404:**
- Verificar que el frontend esté corriendo: http://localhost:3002
- Reiniciar ngrok: `DETENER.bat` → `INICIAR.bat`

### **Backend no accesible desde internet:**
- Verificar puerto 11113 abierto en router
- Verificar IP pública actual: https://www.whatismyip.com
- Verificar firewall Windows: `netsh advfirewall firewall add rule name="Backend" dir=in action=allow protocol=TCP localport=11113`

---

**¡Listo para producción!** 🚀
