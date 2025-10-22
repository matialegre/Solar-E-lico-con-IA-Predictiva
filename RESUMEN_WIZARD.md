# ✅ WIZARD DE CONFIGURACIÓN CREADO

## 🎯 LO QUE SE CREÓ:

### **1. Frontend:**
- ✅ **`SetupWizard.jsx`** - Wizard completo con 4 pasos
  - Paso 1: Elegir ubicación en mapa
  - Paso 2: Elegir modo (Demanda o Recursos)
  - Paso 3: Ingresar datos
  - Paso 4: Ver recomendación

### **2. Backend:**
- ✅ **`recommendation_service.py`** - Servicio de cálculos
  - `calculate_by_demand()` - Recomienda equipamiento según watts necesarios
  - `calculate_by_resources()` - Calcula potencial según equipos existentes
  
- ✅ **Endpoints en `main.py`:**
  - `POST /api/recommendation/by-demand`
  - `POST /api/recommendation/by-resources`

---

## 🔧 CÓMO AGREGAR AL DASHBOARD:

### **Opción 1: Botón en el Dashboard Principal**

Agregar en `App.jsx`:

```jsx
import SetupWizard from './components/SetupWizard';

// Dentro del componente:
const [showWizard, setShowWizard] = useState(false);

// En el render:
{showWizard ? (
  <SetupWizard onComplete={() => setShowWizard(false)} />
) : (
  // ... dashboard normal
)}

// Botón para abrir:
<button onClick={() => setShowWizard(true)} className="btn btn-primary">
  ⚙️ Configurar Sistema
</button>
```

### **Opción 2: Ruta Separada**

En `AppRouter.jsx`:

```jsx
import SetupWizard from './components/SetupWizard';

<Route path="/setup" element={<SetupWizard />} />
```

Acceso: `http://190.211.201.217:11113/setup`

---

## 📊 FLUJO COMPLETO:

```
1. Usuario abre wizard
   ↓
2. Elige ubicación en mapa (lat/long)
   ↓
3. Elige modo:
   - Modo 1: "Tengo 3000W de demanda" → Recomienda paneles/molino/batería
   - Modo 2: "Tengo panel de 1000W" → Calcula cuánto puedo generar
   ↓
4. Ingresa datos específicos
   ↓
5. Backend calcula con:
   - Clima promedio de la zona
   - Eficiencias realistas
   - Autonomía de 2 días
   ↓
6. Muestra recomendación con costos estimados
   ↓
7. Guarda configuración
```

---

## 🎨 PERSONALIZACIÓN:

### **Cambiar valores por defecto:**
```javascript
// En SetupWizard.jsx, línea 7:
const [config, setConfig] = useState({
  latitude: -38.7183,  // ← Cambiar aquí
  longitude: -62.2663,
  target_power_w: 3000 // ← Cambiar demanda por defecto
});
```

### **Integrar mapa real:**
Reemplazar el placeholder en Paso 1 con `LocationMap` interactivo

---

## ⚡ SIGUIENTE PASO:

¿Querés que:
1. **Integre el wizard en el dashboard actual** (botón para abrirlo)
2. **Cree ruta separada** (/setup)
3. **Haga el mapa interactivo** primero
4. **Otra cosa?**
