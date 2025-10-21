import React, { useState, useEffect } from 'react';
import { Wind, AlertTriangle, Shield, Zap, Thermometer, Activity, Power } from 'lucide-react';
import axios from 'axios';

const WindProtection = () => {
  const [protection, setProtection] = useState(null);
  const [specs, setSpecs] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadProtectionStatus();
    loadSpecs();
    const interval = setInterval(loadProtectionStatus, 2000); // Actualizar cada 2 segundos
    return () => clearInterval(interval);
  }, []);

  const loadProtectionStatus = async () => {
    try {
      // Simular datos - en producción vendrían del ESP32
      const windSpeed = 8 + Math.random() * 10; // 8-18 m/s
      const voltage = 48 + Math.random() * 8; // 48-56V
      const rpm = 200 + Math.random() * 150; // 200-350 RPM
      
      const response = await axios.get(
        `${process.env.REACT_APP_API_URL}/api/wind/protection/status?wind_speed=${windSpeed}&voltage=${voltage}&rpm=${rpm}`
      );
      setProtection(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Error loading wind protection:', error);
      setLoading(false);
    }
  };

  const loadSpecs = async () => {
    try {
      const response = await axios.get(`${process.env.REACT_APP_API_URL}/api/wind/protection/specs`);
      setSpecs(response.data);
    } catch (error) {
      console.error('Error loading specs:', error);
    }
  };

  const activateBrake = async () => {
    try {
      await axios.post(`${process.env.REACT_APP_API_URL}/api/wind/protection/brake/activate`, null, {
        params: { reason: 'Activación manual desde dashboard' }
      });
      loadProtectionStatus();
    } catch (error) {
      console.error('Error activating brake:', error);
    }
  };

  const deactivateBrake = async () => {
    if (window.confirm('¿Estás seguro? Solo desactiva si las condiciones son seguras.')) {
      try {
        await axios.post(`${process.env.REACT_APP_API_URL}/api/wind/protection/brake/deactivate`);
        loadProtectionStatus();
      } catch (error) {
        console.error('Error deactivating brake:', error);
      }
    }
  };

  if (loading) {
    return (
      <div className="card">
        <div className="animate-pulse h-64"></div>
      </div>
    );
  }

  if (!protection) return null;

  const getDangerColor = (level) => {
    switch (level) {
      case 'critical': return 'red';
      case 'warning': return 'yellow';
      default: return 'green';
    }
  };

  const dangerColor = getDangerColor(protection.danger_level);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className={`bg-gradient-to-br ${
        protection.brake_active 
          ? 'from-red-600 to-orange-600' 
          : protection.danger_level === 'warning'
            ? 'from-yellow-600 to-orange-600'
            : 'from-green-600 to-emerald-600'
      } rounded-2xl shadow-xl p-6 text-white`}>
        <h2 className="text-3xl font-bold mb-2 flex items-center">
          <Shield className="w-8 h-8 mr-3" />
          Protección contra Embalamiento Eólico
        </h2>
        <p className="text-sm opacity-90">
          {protection.brake_active 
            ? '🚨 FRENO DE EMERGENCIA ACTIVO' 
            : protection.danger_level === 'warning'
              ? '⚠️ CONDICIONES DE ADVERTENCIA'
              : '✅ Sistema operando normalmente'}
        </p>
      </div>

      {/* Alertas */}
      {protection.warnings.length > 0 && (
        <div className={`bg-${dangerColor}-50 border-l-4 border-${dangerColor}-500 rounded-lg p-4`}>
          <div className="flex items-start">
            <AlertTriangle className={`w-6 h-6 text-${dangerColor}-600 mr-3 flex-shrink-0`} />
            <div className="flex-1">
              <h4 className={`font-bold text-${dangerColor}-900 mb-2`}>Advertencias del Sistema</h4>
              <ul className="space-y-1">
                {protection.warnings.map((warning, index) => (
                  <li key={index} className={`text-sm text-${dangerColor}-800`}>{warning}</li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      )}

      {/* Acciones Tomadas */}
      {protection.actions_taken.length > 0 && (
        <div className="bg-blue-50 border-l-4 border-blue-500 rounded-lg p-4">
          <h4 className="font-bold text-blue-900 mb-2 flex items-center">
            <Activity className="w-5 h-5 mr-2" />
            Acciones del Sistema
          </h4>
          <ul className="space-y-1">
            {protection.actions_taken.map((action, index) => (
              <li key={index} className="text-sm text-blue-800">{action}</li>
            ))}
          </ul>
        </div>
      )}

      {/* Métricas en Tiempo Real */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className={`bg-white rounded-xl shadow-lg p-4 border-l-4 ${
          protection.metrics.wind_speed_ms >= protection.thresholds.max_wind_speed
            ? 'border-red-500'
            : protection.metrics.wind_speed_ms >= protection.thresholds.warning_wind_speed
              ? 'border-yellow-500'
              : 'border-green-500'
        }`}>
          <div className="flex items-center justify-between mb-2">
            <Wind className={`w-6 h-6 ${
              protection.metrics.wind_speed_ms >= protection.thresholds.max_wind_speed
                ? 'text-red-500'
                : protection.metrics.wind_speed_ms >= protection.thresholds.warning_wind_speed
                  ? 'text-yellow-500'
                  : 'text-green-500'
            }`} />
            <span className="text-xs text-gray-500">Máx: {protection.thresholds.max_wind_speed} m/s</span>
          </div>
          <p className="text-xs text-gray-600 mb-1">Velocidad de Viento</p>
          <p className="text-3xl font-bold text-gray-900">{protection.metrics.wind_speed_ms.toFixed(1)}</p>
          <p className="text-xs text-gray-500">m/s</p>
        </div>

        <div className={`bg-white rounded-xl shadow-lg p-4 border-l-4 ${
          protection.metrics.voltage_v >= protection.thresholds.max_voltage
            ? 'border-red-500'
            : protection.metrics.voltage_v >= protection.thresholds.warning_voltage
              ? 'border-yellow-500'
              : 'border-green-500'
        }`}>
          <div className="flex items-center justify-between mb-2">
            <Zap className={`w-6 h-6 ${
              protection.metrics.voltage_v >= protection.thresholds.max_voltage
                ? 'text-red-500'
                : protection.metrics.voltage_v >= protection.thresholds.warning_voltage
                  ? 'text-yellow-500'
                  : 'text-green-500'
            }`} />
            <span className="text-xs text-gray-500">Máx: {protection.thresholds.max_voltage}V</span>
          </div>
          <p className="text-xs text-gray-600 mb-1">Voltaje</p>
          <p className="text-3xl font-bold text-gray-900">{protection.metrics.voltage_v.toFixed(1)}</p>
          <p className="text-xs text-gray-500">Volts</p>
        </div>

        <div className={`bg-white rounded-xl shadow-lg p-4 border-l-4 ${
          protection.metrics.rpm && protection.metrics.rpm >= protection.thresholds.max_rpm
            ? 'border-red-500'
            : protection.metrics.rpm && protection.metrics.rpm >= protection.thresholds.warning_rpm
              ? 'border-yellow-500'
              : 'border-green-500'
        }`}>
          <div className="flex items-center justify-between mb-2">
            <Activity className={`w-6 h-6 ${
              protection.metrics.rpm && protection.metrics.rpm >= protection.thresholds.max_rpm
                ? 'text-red-500'
                : protection.metrics.rpm && protection.metrics.rpm >= protection.thresholds.warning_rpm
                  ? 'text-yellow-500'
                  : 'text-green-500'
            }`} />
            <span className="text-xs text-gray-500">Máx: {protection.thresholds.max_rpm} RPM</span>
          </div>
          <p className="text-xs text-gray-600 mb-1">Revoluciones</p>
          <p className="text-3xl font-bold text-gray-900">
            {protection.metrics.rpm ? protection.metrics.rpm.toFixed(0) : 'N/A'}
          </p>
          <p className="text-xs text-gray-500">RPM</p>
        </div>

        <div className={`bg-white rounded-xl shadow-lg p-4 border-l-4 ${
          protection.brake_active ? 'border-red-500' : 'border-gray-300'
        }`}>
          <div className="flex items-center justify-between mb-2">
            <Thermometer className={`w-6 h-6 ${protection.brake_active ? 'text-red-500' : 'text-gray-400'}`} />
            <span className="text-xs text-gray-500">Resistencia</span>
          </div>
          <p className="text-xs text-gray-600 mb-1">Potencia de Frenado</p>
          <p className="text-3xl font-bold text-gray-900">{protection.metrics.brake_power_w.toFixed(0)}</p>
          <p className="text-xs text-gray-500">Watts</p>
        </div>
      </div>

      {/* Controles Manuales */}
      <div className="bg-white rounded-xl shadow-lg p-6">
        <h3 className="text-xl font-bold text-gray-900 mb-4 flex items-center">
          <Power className="w-6 h-6 mr-2 text-indigo-600" />
          Control Manual de Freno de Emergencia
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <button
            onClick={activateBrake}
            disabled={protection.brake_active}
            className={`p-4 rounded-lg font-bold text-white transition-all ${
              protection.brake_active
                ? 'bg-gray-400 cursor-not-allowed'
                : 'bg-red-600 hover:bg-red-700 active:scale-95'
            }`}
          >
            🚨 ACTIVAR FRENO DE EMERGENCIA
          </button>
          <button
            onClick={deactivateBrake}
            disabled={!protection.brake_active}
            className={`p-4 rounded-lg font-bold text-white transition-all ${
              !protection.brake_active
                ? 'bg-gray-400 cursor-not-allowed'
                : 'bg-green-600 hover:bg-green-700 active:scale-95'
            }`}
          >
            ✅ DESACTIVAR FRENO (Solo si es seguro)
          </button>
        </div>
        <p className="text-xs text-gray-600 mt-4 text-center">
          ⚠️ El freno se activa automáticamente si se detectan condiciones peligrosas
        </p>
      </div>

      {/* Especificaciones Técnicas */}
      {specs && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="bg-gradient-to-br from-orange-50 to-red-50 rounded-xl shadow-lg p-6 border-2 border-orange-400">
            <h3 className="text-xl font-bold text-gray-900 mb-4 flex items-center">
              <Thermometer className="w-6 h-6 mr-2 text-orange-600" />
              Resistencia de Frenado
            </h3>
            <div className="space-y-3">
              <div className="flex justify-between p-2 bg-white rounded">
                <span className="text-sm text-gray-700">Resistencia:</span>
                <span className="font-bold text-gray-900">{specs.brake_resistor.resistance_ohms} Ω</span>
              </div>
              <div className="flex justify-between p-2 bg-white rounded">
                <span className="text-sm text-gray-700">Potencia máxima:</span>
                <span className="font-bold text-gray-900">{specs.brake_resistor.max_power_watts} W</span>
              </div>
              <div className="flex justify-between p-2 bg-white rounded">
                <span className="text-sm text-gray-700">Corriente máxima:</span>
                <span className="font-bold text-gray-900">{specs.brake_resistor.max_current_amps.toFixed(1)} A</span>
              </div>
              <div className="bg-orange-100 border border-orange-300 rounded p-3 mt-3">
                <p className="text-xs text-orange-800">
                  <strong>Tipo:</strong> {specs.brake_resistor.recommended_type}
                </p>
                <p className="text-xs text-orange-800 mt-1">
                  <strong>⚠️ ADVERTENCIA:</strong> {specs.brake_resistor.safety_note}
                </p>
              </div>
            </div>
          </div>

          <div className="bg-gradient-to-br from-blue-50 to-indigo-50 rounded-xl shadow-lg p-6 border-2 border-blue-400">
            <h3 className="text-xl font-bold text-gray-900 mb-4 flex items-center">
              <Zap className="w-6 h-6 mr-2 text-blue-600" />
              Configuración de Relés
            </h3>
            <div className="space-y-4">
              <div className="bg-white rounded-lg p-3">
                <p className="font-bold text-gray-900 mb-2">
                  {specs.relay_configuration.relay_turbine.name}
                </p>
                <p className="text-xs text-gray-700 mb-1">
                  📍 Pin: <strong>{specs.relay_configuration.relay_turbine.gpio_pin}</strong>
                </p>
                <p className="text-xs text-gray-700 mb-1">
                  ✅ Normal: <strong>{specs.relay_configuration.relay_turbine.normal_state}</strong>
                </p>
                <p className="text-xs text-gray-700">
                  🚨 Protección: <strong>{specs.relay_configuration.relay_turbine.protection_state}</strong>
                </p>
              </div>
              <div className="bg-white rounded-lg p-3">
                <p className="font-bold text-gray-900 mb-2">
                  {specs.relay_configuration.relay_brake.name}
                </p>
                <p className="text-xs text-gray-700 mb-1">
                  📍 Pin: <strong>{specs.relay_configuration.relay_brake.gpio_pin}</strong>
                </p>
                <p className="text-xs text-gray-700 mb-1">
                  ✅ Normal: <strong>{specs.relay_configuration.relay_brake.normal_state}</strong>
                </p>
                <p className="text-xs text-gray-700">
                  🚨 Protección: <strong>{specs.relay_configuration.relay_brake.protection_state}</strong>
                </p>
              </div>
              <div className="bg-red-50 border border-red-300 rounded p-3">
                <p className="text-xs text-red-800">
                  <strong>⚠️ INTERLOCK:</strong> {specs.relay_configuration.interlock}
                </p>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Explicación del Sistema */}
      <div className="bg-gradient-to-br from-purple-50 to-pink-50 rounded-xl shadow-lg p-6 border-l-4 border-purple-500">
        <h3 className="text-xl font-bold text-purple-900 mb-4">
          🛡️ ¿Cómo Funciona la Protección?
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <h4 className="font-bold text-gray-800 mb-2">Cuando hay viento normal:</h4>
            <ul className="space-y-1 text-sm text-gray-700">
              <li>✅ Turbina conectada al sistema</li>
              <li>✅ Generando energía normalmente</li>
              <li>✅ Resistencia de freno APAGADA</li>
              <li>✅ Energía va a batería/consumo</li>
            </ul>
          </div>
          <div>
            <h4 className="font-bold text-gray-800 mb-2">Cuando se embala (viento excesivo):</h4>
            <ul className="space-y-1 text-sm text-gray-700">
              <li>🚨 Sistema detecta sobrevoltaje/RPM alto</li>
              <li>⚡ Turbina se DESCONECTA automáticamente</li>
              <li>🔥 Resistencia de freno se ACTIVA</li>
              <li>💨 Energía se disipa como calor (frena la turbina)</li>
              <li>🛡️ Protege el sistema de daños</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};

export default WindProtection;
