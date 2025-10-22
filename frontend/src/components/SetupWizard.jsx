import React, { useState } from 'react';
import { MapPin, Zap, Sun, Wind, Battery, ChevronRight, ChevronLeft, CheckCircle } from 'lucide-react';
import api from '../api/api';

const SetupWizard = ({ onComplete }) => {
  const [step, setStep] = useState(1);
  const [config, setConfig] = useState({
    // Ubicación
    latitude: -38.7183,
    longitude: -62.2663,
    location_name: 'Bahía Blanca, Buenos Aires',
    
    // Modo
    mode: null, // 'demand' o 'resources'
    
    // Modo 1: Demanda
    target_power_w: 3000,
    
    // Modo 2: Recursos existentes
    solar_panel_w: 0,
    solar_panel_area_m2: 0,
    wind_turbine_w: 0,
    wind_turbine_diameter_m: 0,
    battery_capacity_wh: 0
  });
  
  const [recommendation, setRecommendation] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleLocationSelect = (lat, lng, name) => {
    setConfig({ ...config, latitude: lat, longitude: lng, location_name: name });
  };

  const handleModeSelect = (mode) => {
    setConfig({ ...config, mode });
    setStep(3);
  };

  const handleSubmit = async () => {
    setLoading(true);
    try {
      const endpoint = config.mode === 'demand' 
        ? '/api/recommendation/by-demand'
        : '/api/recommendation/by-resources';
      
      const response = await api.post(endpoint, config);
      setRecommendation(response.data);
      setStep(4);
    } catch (error) {
      console.error('Error getting recommendation:', error);
      alert('Error al obtener recomendación');
    } finally {
      setLoading(false);
    }
  };

  const handleSaveConfig = async () => {
    try {
      // Guardar configuración completa
      const fullConfig = {
        ...config,
        recommendation,
        configured: true,
        timestamp: new Date().toISOString()
      };
      
      await api.post('/api/configuracion/usuario', fullConfig);
      
      // Guardar en localStorage también
      localStorage.setItem('system_config', JSON.stringify(fullConfig));
      
      alert('✅ Configuración guardada exitosamente');
      
      if (onComplete) onComplete();
    } catch (error) {
      console.error('Error saving config:', error);
      alert('Error al guardar configuración');
    }
  };

  return (
    <div className="max-w-4xl mx-auto">
      {/* Progress Bar */}
      <div className="mb-8">
        <div className="flex items-center justify-between mb-2">
          {[1, 2, 3, 4].map((s) => (
            <div key={s} className="flex items-center flex-1">
              <div className={`w-8 h-8 rounded-full flex items-center justify-center ${
                step >= s ? 'bg-blue-600 text-white' : 'bg-gray-300 text-gray-600'
              }`}>
                {step > s ? <CheckCircle className="w-5 h-5" /> : s}
              </div>
              {s < 4 && <div className={`flex-1 h-1 mx-2 ${step > s ? 'bg-blue-600' : 'bg-gray-300'}`} />}
            </div>
          ))}
        </div>
        <div className="flex justify-between text-xs text-gray-600">
          <span>Ubicación</span>
          <span>Modo</span>
          <span>Datos</span>
          <span>Resultado</span>
        </div>
      </div>

      {/* Step 1: Ubicación */}
      {step === 1 && (
        <div className="card">
          <h2 className="text-2xl font-bold mb-4 flex items-center">
            <MapPin className="w-6 h-6 mr-2 text-blue-600" />
            Paso 1: Ubicación del Sistema
          </h2>
          <p className="text-gray-600 mb-6">
            Hacé click en el mapa para elegir dónde está instalado tu sistema
          </p>
          
          <div className="mb-4 p-4 bg-blue-50 rounded">
            <p className="font-semibold">📍 Ubicación seleccionada:</p>
            <p className="text-sm">Latitud: {config.latitude.toFixed(4)}°</p>
            <p className="text-sm">Longitud: {config.longitude.toFixed(4)}°</p>
            <div className="mt-2">
              <label className="text-sm font-semibold">Nombre del lugar:</label>
              <input
                type="text"
                value={config.location_name}
                onChange={(e) => setConfig({...config, location_name: e.target.value})}
                className="w-full p-2 border rounded mt-1"
                placeholder="Ej: Bahía Blanca, Buenos Aires"
              />
            </div>
          </div>

          {/* Mapa interactivo simple */}
          <div className="bg-gray-100 h-96 rounded-lg border-2 border-gray-300 overflow-hidden mb-4 relative">
            <iframe
              src={`https://www.openstreetmap.org/export/embed.html?bbox=${config.longitude-0.5}%2C${config.latitude-0.5}%2C${config.longitude+0.5}%2C${config.latitude+0.5}&layer=mapnik&marker=${config.latitude}%2C${config.longitude}`}
              width="100%"
              height="100%"
              frameBorder="0"
              className="rounded-lg"
            />
            <div className="absolute bottom-4 left-4 bg-white p-3 rounded-lg shadow-lg">
              <p className="text-xs text-gray-600 mb-2">📍 Ajusta la ubicación manualmente:</p>
              <div className="grid grid-cols-2 gap-2">
                <div>
                  <label className="text-xs">Latitud:</label>
                  <input
                    type="number"
                    step="0.0001"
                    value={config.latitude}
                    onChange={(e) => setConfig({...config, latitude: parseFloat(e.target.value)})}
                    className="w-full p-1 text-sm border rounded"
                  />
                </div>
                <div>
                  <label className="text-xs">Longitud:</label>
                  <input
                    type="number"
                    step="0.0001"
                    value={config.longitude}
                    onChange={(e) => setConfig({...config, longitude: parseFloat(e.target.value)})}
                    className="w-full p-1 text-sm border rounded"
                  />
                </div>
              </div>
            </div>
          </div>

          <button
            onClick={() => setStep(2)}
            className="btn btn-primary w-full flex items-center justify-center"
          >
            Continuar
            <ChevronRight className="w-5 h-5 ml-2" />
          </button>
        </div>
      )}

      {/* Step 2: Elegir Modo */}
      {step === 2 && (
        <div className="card">
          <h2 className="text-2xl font-bold mb-4 flex items-center">
            <Zap className="w-6 h-6 mr-2 text-yellow-600" />
            Paso 2: Elegí el Modo
          </h2>
          <p className="text-gray-600 mb-6">
            ¿Qué querés calcular?
          </p>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Modo 1: Por Demanda */}
            <button
              onClick={() => handleModeSelect('demand')}
              className="p-6 border-2 border-gray-300 rounded-lg hover:border-blue-600 hover:bg-blue-50 transition text-left"
            >
              <div className="flex items-center mb-4">
                <Zap className="w-8 h-8 text-yellow-600 mr-3" />
                <h3 className="text-xl font-bold">Modo 1: Por Demanda</h3>
              </div>
              <p className="text-gray-600 mb-4">
                Tengo <strong>X watts de consumo</strong> y quiero saber qué equipamiento necesito
              </p>
              <ul className="text-sm space-y-2 text-gray-700">
                <li>✓ Ingresás tu consumo en watts</li>
                <li>✓ Te recomendamos paneles, molino, batería</li>
                <li>✓ Basado en clima de tu zona</li>
              </ul>
            </button>

            {/* Modo 2: Por Recursos */}
            <button
              onClick={() => handleModeSelect('resources')}
              className="p-6 border-2 border-gray-300 rounded-lg hover:border-green-600 hover:bg-green-50 transition text-left"
            >
              <div className="flex items-center mb-4">
                <Sun className="w-8 h-8 text-orange-600 mr-3" />
                <h3 className="text-xl font-bold">Modo 2: Por Recursos</h3>
              </div>
              <p className="text-gray-600 mb-4">
                Tengo <strong>estos paneles/molino</strong> y quiero saber cuánta potencia puedo generar
              </p>
              <ul className="text-sm space-y-2 text-gray-700">
                <li>✓ Ingresás tus equipos actuales</li>
                <li>✓ Te decimos cuánto podés generar</li>
                <li>✓ Optimización según clima real</li>
              </ul>
            </button>
          </div>

          <button
            onClick={() => setStep(1)}
            className="btn btn-secondary mt-6 flex items-center"
          >
            <ChevronLeft className="w-5 h-5 mr-2" />
            Volver
          </button>
        </div>
      )}

      {/* Step 3: Ingresar Datos */}
      {step === 3 && config.mode === 'demand' && (
        <div className="card">
          <h2 className="text-2xl font-bold mb-4 flex items-center">
            <Zap className="w-6 h-6 mr-2 text-yellow-600" />
            Paso 3: Ingresá tu Demanda
          </h2>
          
          <div className="space-y-4">
            <div>
              <label className="block font-semibold mb-2">Potencia que necesitás (Watts)</label>
              <input
                type="number"
                value={config.target_power_w}
                onChange={(e) => setConfig({...config, target_power_w: parseInt(e.target.value)})}
                className="w-full p-3 border rounded"
                placeholder="3000"
              />
              <p className="text-sm text-gray-600 mt-1">
                Ejemplo: 3000W para heladera, luces, TV, etc.
              </p>
            </div>
          </div>

          <div className="flex gap-4 mt-6">
            <button
              onClick={() => setStep(2)}
              className="btn btn-secondary flex items-center"
            >
              <ChevronLeft className="w-5 h-5 mr-2" />
              Volver
            </button>
            <button
              onClick={handleSubmit}
              disabled={loading}
              className="btn btn-primary flex-1 flex items-center justify-center"
            >
              {loading ? 'Calculando...' : 'Calcular Recomendación'}
              <ChevronRight className="w-5 h-5 ml-2" />
            </button>
          </div>
        </div>
      )}

      {step === 3 && config.mode === 'resources' && (
        <div className="card">
          <h2 className="text-2xl font-bold mb-4 flex items-center">
            <Sun className="w-6 h-6 mr-2 text-orange-600" />
            Paso 3: Ingresá tus Recursos
          </h2>
          
          <div className="space-y-6">
            <div className="p-4 bg-orange-50 rounded">
              <h3 className="font-bold mb-3 flex items-center">
                <Sun className="w-5 h-5 mr-2" />
                Panel Solar
              </h3>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm mb-1">Potencia (W)</label>
                  <input
                    type="number"
                    value={config.solar_panel_w}
                    onChange={(e) => setConfig({...config, solar_panel_w: parseInt(e.target.value)})}
                    className="w-full p-2 border rounded"
                  />
                </div>
                <div>
                  <label className="block text-sm mb-1">Área (m²)</label>
                  <input
                    type="number"
                    step="0.1"
                    value={config.solar_panel_area_m2}
                    onChange={(e) => setConfig({...config, solar_panel_area_m2: parseFloat(e.target.value)})}
                    className="w-full p-2 border rounded"
                  />
                </div>
              </div>
            </div>

            <div className="p-4 bg-blue-50 rounded">
              <h3 className="font-bold mb-3 flex items-center">
                <Wind className="w-5 h-5 mr-2" />
                Turbina Eólica
              </h3>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm mb-1">Potencia (W)</label>
                  <input
                    type="number"
                    value={config.wind_turbine_w}
                    onChange={(e) => setConfig({...config, wind_turbine_w: parseInt(e.target.value)})}
                    className="w-full p-2 border rounded"
                  />
                </div>
                <div>
                  <label className="block text-sm mb-1">Diámetro (m)</label>
                  <input
                    type="number"
                    step="0.1"
                    value={config.wind_turbine_diameter_m}
                    onChange={(e) => setConfig({...config, wind_turbine_diameter_m: parseFloat(e.target.value)})}
                    className="w-full p-2 border rounded"
                  />
                </div>
              </div>
            </div>

            <div className="p-4 bg-green-50 rounded">
              <h3 className="font-bold mb-3 flex items-center">
                <Battery className="w-5 h-5 mr-2" />
                Batería
              </h3>
              <div>
                <label className="block text-sm mb-1">Capacidad (Wh)</label>
                <input
                  type="number"
                  value={config.battery_capacity_wh}
                  onChange={(e) => setConfig({...config, battery_capacity_wh: parseInt(e.target.value)})}
                  className="w-full p-2 border rounded"
                />
              </div>
            </div>
          </div>

          <div className="flex gap-4 mt-6">
            <button
              onClick={() => setStep(2)}
              className="btn btn-secondary flex items-center"
            >
              <ChevronLeft className="w-5 h-5 mr-2" />
              Volver
            </button>
            <button
              onClick={handleSubmit}
              disabled={loading}
              className="btn btn-primary flex-1 flex items-center justify-center"
            >
              {loading ? 'Calculando...' : 'Calcular Potencial'}
              <ChevronRight className="w-5 h-5 ml-2" />
            </button>
          </div>
        </div>
      )}

      {/* Step 4: Resultado */}
      {step === 4 && recommendation && (
        <div className="card">
          <h2 className="text-2xl font-bold mb-4 flex items-center text-green-600">
            <CheckCircle className="w-6 h-6 mr-2" />
            ¡Recomendación Lista!
          </h2>

          <div className="space-y-4 mb-6">
            {config.mode === 'demand' && (
              <>
                <div className="p-4 bg-orange-50 rounded">
                  <h3 className="font-bold mb-2">☀️ Panel Solar Recomendado</h3>
                  <p>{recommendation.solar?.power_w}W ({recommendation.solar?.area_m2}m²)</p>
                </div>
                <div className="p-4 bg-blue-50 rounded">
                  <h3 className="font-bold mb-2">💨 Turbina Eólica Recomendada</h3>
                  <p>{recommendation.wind?.power_w}W (Diámetro: {recommendation.wind?.diameter_m}m)</p>
                </div>
                <div className="p-4 bg-green-50 rounded">
                  <h3 className="font-bold mb-2">🔋 Batería Recomendada</h3>
                  <p>{recommendation.battery?.capacity_wh}Wh ({recommendation.battery?.voltage}V)</p>
                </div>
              </>
            )}

            {config.mode === 'resources' && (
              <>
                <div className="p-4 bg-yellow-50 rounded">
                  <h3 className="font-bold mb-2">⚡ Potencia Máxima Estimada</h3>
                  <p className="text-2xl font-bold text-yellow-600">{recommendation.max_power_w}W</p>
                </div>
                <div className="p-4 bg-blue-50 rounded">
                  <h3 className="font-bold mb-2">📊 Generación Promedio Diaria</h3>
                  <p>{recommendation.daily_generation_kwh} kWh/día</p>
                </div>
              </>
            )}
          </div>

          <button
            onClick={handleSaveConfig}
            className="btn btn-primary w-full"
          >
            Guardar Configuración
          </button>
        </div>
      )}
    </div>
  );
};

export default SetupWizard;
