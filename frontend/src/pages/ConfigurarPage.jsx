/**
 * Página de configuración de dispositivo ESP32
 * Permite configurar ubicación con mapa interactivo
 */

import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { MapPin, Save, ArrowLeft, Loader } from 'lucide-react';
import axios from 'axios';
import MapSelector from '../components/MapSelector';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export default function ConfigurarPage() {
  const { deviceId } = useParams();
  const navigate = useNavigate();
  
  const [device, setDevice] = useState(null);
  const [config, setConfig] = useState({
    latitude: -38.7183,
    longitude: -62.2663,
    battery_capacity_wh: 5000,
    solar_area_m2: 16.0,
    wind_power_w: 2000,
    proteccion_activa: true,
    aprendizaje_activo: false
  });
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [climaData, setClimaData] = useState(null);
  const [loadingClima, setLoadingClima] = useState(false);

  useEffect(() => {
    fetchDevice();
  }, [deviceId]);

  const fetchDevice = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`${API_URL}/api/esp32/devices/${deviceId}`);
      setDevice(response.data);
      
      // Cargar configuración actual
      const configResponse = await axios.get(`${API_URL}/api/esp32/config/${deviceId}`);
      setConfig(configResponse.data);
      
      // Cargar datos climáticos
      fetchClimaData(configResponse.data.latitude, configResponse.data.longitude);
    } catch (error) {
      console.error('Error cargando dispositivo:', error);
      alert('Error al cargar dispositivo');
      navigate('/dispositivos');
    } finally {
      setLoading(false);
    }
  };

  const fetchClimaData = async (lat, lon) => {
    try {
      setLoadingClima(true);
      const response = await axios.get(`${API_URL}/api/dimensionamiento/clima/${lat}/${lon}`);
      setClimaData(response.data);
    } catch (error) {
      console.error('Error cargando clima:', error);
    } finally {
      setLoadingClima(false);
    }
  };

  const handleLocationChange = (lat, lon) => {
    setConfig({ ...config, latitude: lat, longitude: lon });
    fetchClimaData(lat, lon);
  };

  const handleSave = async () => {
    try {
      setSaving(true);
      await axios.post(`${API_URL}/api/esp32/config/${deviceId}`, config);
      alert('✅ Configuración guardada correctamente');
      navigate('/dispositivos');
    } catch (error) {
      console.error('Error guardando configuración:', error);
      alert('❌ Error al guardar configuración');
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-900 text-white flex items-center justify-center">
        <div className="text-center">
          <Loader className="w-12 h-12 text-blue-400 animate-spin mx-auto mb-4" />
          <p className="text-gray-400">Cargando configuración...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-900 text-white p-6">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="flex items-center gap-4 mb-6">
          <button
            onClick={() => navigate('/dispositivos')}
            className="p-2 bg-gray-800 hover:bg-gray-700 rounded-lg transition-colors"
          >
            <ArrowLeft className="w-5 h-5" />
          </button>
          <div>
            <h1 className="text-3xl font-bold">⚙️ Configurar Dispositivo</h1>
            <p className="text-gray-400">{deviceId}</p>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Mapa */}
          <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
            <h2 className="text-xl font-bold mb-4 flex items-center gap-2">
              <MapPin className="w-5 h-5 text-blue-400" />
              Ubicación Geográfica
            </h2>
            
            <p className="text-sm text-gray-400 mb-4">
              Arrastra el marcador en el mapa para establecer la ubicación del dispositivo.
            </p>

            <MapSelector
              initialLat={config.latitude}
              initialLon={config.longitude}
              onChange={handleLocationChange}
            />

            <div className="mt-4 p-4 bg-gray-900 rounded">
              <div className="grid grid-cols-2 gap-4 text-sm">
                <div>
                  <p className="text-gray-400">Latitud</p>
                  <p className="font-mono text-lg">{config.latitude.toFixed(4)}°</p>
                </div>
                <div>
                  <p className="text-gray-400">Longitud</p>
                  <p className="font-mono text-lg">{config.longitude.toFixed(4)}°</p>
                </div>
              </div>
            </div>
          </div>

          {/* Configuración */}
          <div className="space-y-6">
            {/* Datos Climáticos */}
            <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
              <h2 className="text-xl font-bold mb-4">🌤️ Datos Climáticos Históricos</h2>
              
              {loadingClima ? (
                <div className="text-center py-4">
                  <Loader className="w-8 h-8 text-blue-400 animate-spin mx-auto" />
                </div>
              ) : climaData ? (
                <div className="space-y-4">
                  <div className="p-4 bg-yellow-500/10 border border-yellow-500/30 rounded">
                    <p className="text-sm text-yellow-400 font-bold mb-2">
                      ☀️ Irradiancia Solar Promedio
                    </p>
                    <p className="text-2xl font-bold">
                      {climaData.solar.annual_avg_kwh_m2_day.toFixed(2)} kWh/m²/día
                    </p>
                    <p className="text-xs text-gray-400 mt-1">
                      Promedio de {climaData.historical_data.years_analyzed} años ({climaData.historical_data.period})
                    </p>
                  </div>

                  <div className="p-4 bg-blue-500/10 border border-blue-500/30 rounded">
                    <p className="text-sm text-blue-400 font-bold mb-2">
                      💨 Velocidad Viento Promedio
                    </p>
                    <p className="text-2xl font-bold">
                      {climaData.wind.annual_avg_ms.toFixed(1)} m/s
                    </p>
                    <p className="text-xs text-gray-400 mt-1">
                      Datos de NASA POWER API
                    </p>
                  </div>

                  <div className="p-4 bg-gray-900 rounded">
                    <p className="text-sm text-gray-400 mb-2">
                      🌡️ Temperatura Promedio
                    </p>
                    <p className="text-xl font-bold">
                      {climaData.temperature.annual_avg_c.toFixed(1)}°C
                    </p>
                  </div>
                </div>
              ) : (
                <p className="text-gray-400 text-sm">
                  Selecciona una ubicación en el mapa para ver datos climáticos
                </p>
              )}
            </div>

            {/* Configuración del Sistema */}
            <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
              <h2 className="text-xl font-bold mb-4">🔋 Configuración del Sistema</h2>
              
              <div className="space-y-4">
                <div>
                  <label className="block text-sm text-gray-400 mb-2">
                    Capacidad Batería (Wh)
                  </label>
                  <input
                    type="number"
                    value={config.battery_capacity_wh}
                    onChange={(e) => setConfig({ ...config, battery_capacity_wh: parseFloat(e.target.value) })}
                    className="w-full px-4 py-2 bg-gray-900 border border-gray-700 rounded focus:border-blue-500 focus:outline-none"
                  />
                </div>

                <div>
                  <label className="block text-sm text-gray-400 mb-2">
                    Área Solar (m²)
                  </label>
                  <input
                    type="number"
                    step="0.1"
                    value={config.solar_area_m2}
                    onChange={(e) => setConfig({ ...config, solar_area_m2: parseFloat(e.target.value) })}
                    className="w-full px-4 py-2 bg-gray-900 border border-gray-700 rounded focus:border-blue-500 focus:outline-none"
                  />
                </div>

                <div>
                  <label className="block text-sm text-gray-400 mb-2">
                    Potencia Eólica (W)
                  </label>
                  <input
                    type="number"
                    value={config.wind_power_w}
                    onChange={(e) => setConfig({ ...config, wind_power_w: parseFloat(e.target.value) })}
                    className="w-full px-4 py-2 bg-gray-900 border border-gray-700 rounded focus:border-blue-500 focus:outline-none"
                  />
                </div>

                <div className="flex items-center gap-3 pt-2">
                  <input
                    type="checkbox"
                    id="proteccion"
                    checked={config.proteccion_activa}
                    onChange={(e) => setConfig({ ...config, proteccion_activa: e.target.checked })}
                    className="w-4 h-4"
                  />
                  <label htmlFor="proteccion" className="text-sm">
                    Protección contra embalamiento activa
                  </label>
                </div>

                <div className="flex items-center gap-3">
                  <input
                    type="checkbox"
                    id="aprendizaje"
                    checked={config.aprendizaje_activo}
                    onChange={(e) => setConfig({ ...config, aprendizaje_activo: e.target.checked })}
                    className="w-4 h-4"
                  />
                  <label htmlFor="aprendizaje" className="text-sm">
                    Aprendizaje automático de patrones
                  </label>
                </div>
              </div>
            </div>

            {/* Botón Guardar */}
            <button
              onClick={handleSave}
              disabled={saving}
              className="w-full py-3 bg-blue-600 hover:bg-blue-700 rounded-lg font-bold flex items-center justify-center gap-2 transition-colors disabled:opacity-50"
            >
              {saving ? (
                <>
                  <Loader className="w-5 h-5 animate-spin" />
                  Guardando...
                </>
              ) : (
                <>
                  <Save className="w-5 h-5" />
                  Guardar Configuración
                </>
              )}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
