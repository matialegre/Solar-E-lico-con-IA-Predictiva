import React, { useState, useEffect } from 'react';
import { Zap, Activity, AlertCircle, CheckCircle, Power, ToggleLeft, ToggleRight } from 'lucide-react';
import api from '../api/api';

const HardwareTest = () => {
  const [testData, setTestData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [relayControl, setRelayControl] = useState({
    solar: false,
    wind: false,
    grid: false,
    load: false
  });
  const [thresholds, setThresholds] = useState({
    max_wind_speed: 25.0,
    max_wind_power: 2000,
    max_voltage: 65.0,
    brake_enabled: true
  });

  useEffect(() => {
    loadTestData();
    const interval = setInterval(loadTestData, 1000); // Actualizar cada segundo
    return () => clearInterval(interval);
  }, []);

  const loadTestData = async () => {
    try {
      const response = await api.get('/api/hardware/test');
      setTestData(response.data);
      setRelayControl(response.data.relays);
      if (response.data.thresholds) {
        setThresholds(response.data.thresholds);
      }
      setLoading(false);
    } catch (error) {
      console.error('Error loading hardware test:', error);
      setLoading(false);
    }
  };

  const toggleRelay = async (relayName) => {
    try {
      const newState = !relayControl[relayName];
      await api.post('/api/hardware/relay', {
        relay: relayName,
        state: newState
      });
      setRelayControl({...relayControl, [relayName]: newState});
    } catch (error) {
      console.error('Error toggling relay:', error);
      alert('Error al controlar relé');
    }
  };

  const saveThresholds = async () => {
    try {
      await api.post('/api/hardware/thresholds', thresholds);
      alert('✅ Umbrales de protección guardados correctamente');
    } catch (error) {
      console.error('Error saving thresholds:', error);
      alert('Error al guardar umbrales');
    }
  };

  if (loading) {
    return (
      <div className="card animate-pulse">
        <div className="h-96 bg-gray-200 rounded"></div>
      </div>
    );
  }

  const pinConfig = [
    { type: 'ADC', pin: 'GPIO34', name: 'Voltaje Batería 1', adc: 'ADC1_CH6' },
    { type: 'ADC', pin: 'GPIO35', name: 'Voltaje Batería 2', adc: 'ADC1_CH7' },
    { type: 'ADC', pin: 'GPIO32', name: 'Voltaje Batería 3', adc: 'ADC1_CH4' },
    { type: 'ADC', pin: 'GPIO33', name: 'Corriente Solar', adc: 'ADC1_CH5' },
    { type: 'ADC', pin: 'GPIO36', name: 'Corriente Eólica', adc: 'ADC1_CH0' },
    { type: 'ADC', pin: 'GPIO39', name: 'Corriente Consumo', adc: 'ADC1_CH3' },
    { type: 'ADC', pin: 'GPIO25', name: 'Irradiancia (LDR)', adc: 'ADC2_CH8' },
    { type: 'ADC', pin: 'GPIO26', name: 'Velocidad Viento', adc: 'GPIO' },
  ];

  const relayPins = [
    { pin: 'GPIO16', name: 'Relé Solar', key: 'solar' },
    { pin: 'GPIO17', name: 'Relé Eólica', key: 'wind' },
    { pin: 'GPIO18', name: 'Relé Red', key: 'grid' },
    { pin: 'GPIO19', name: 'Relé Carga', key: 'load' },
    { pin: 'GPIO23', name: 'Relé Freno', key: 'brake' }
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="card bg-gradient-to-br from-yellow-50 to-orange-50 border-l-4 border-yellow-500">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-2xl font-bold text-gray-800 flex items-center">
              <Activity className="w-7 h-7 mr-3 text-yellow-600" />
              🔧 Prueba de Hardware ESP32
            </h2>
            <p className="text-gray-600 mt-1">
              Monitoreo en tiempo real de ADCs y control de relés
            </p>
          </div>
          <AlertCircle className="w-12 h-12 text-yellow-500 opacity-50" />
        </div>
      </div>

      {/* Estado de Conexión */}
      <div className="card">
        <div className="flex items-center justify-between p-4 bg-green-50 rounded-lg">
          <div className="flex items-center">
            <CheckCircle className="w-6 h-6 text-green-600 mr-3 animate-pulse" />
            <div>
              <h3 className="font-bold text-gray-800">ESP32 Conectado</h3>
              <p className="text-sm text-gray-600">Datos actualizándose cada 1 segundo</p>
            </div>
          </div>
          <div className="text-right">
            <p className="text-xs text-gray-500">Última actualización:</p>
            <p className="font-mono text-sm font-bold">{new Date().toLocaleTimeString()}</p>
          </div>
        </div>
      </div>

      {/* ADCs - Configuración de Pines */}
      <div className="card">
        <h3 className="text-xl font-bold text-gray-800 mb-4 flex items-center">
          <Zap className="w-6 h-6 mr-2 text-blue-600" />
          Pines ADC Configurados
        </h3>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead className="bg-blue-100">
              <tr>
                <th className="p-3 text-left font-bold">Pin GPIO</th>
                <th className="p-3 text-left font-bold">Canal ADC</th>
                <th className="p-3 text-left font-bold">Función</th>
                <th className="p-3 text-left font-bold">Valor RAW</th>
                <th className="p-3 text-left font-bold">Convertido</th>
                <th className="p-3 text-left font-bold">Estado</th>
              </tr>
            </thead>
            <tbody className="divide-y">
              {testData?.adcs?.map((adc, idx) => (
                <tr key={idx} className="hover:bg-gray-50">
                  <td className="p-3">
                    <span className="font-mono font-bold text-blue-600">{adc.pin}</span>
                  </td>
                  <td className="p-3">
                    <span className="text-xs bg-purple-100 px-2 py-1 rounded">{adc.channel}</span>
                  </td>
                  <td className="p-3 font-semibold">{adc.function}</td>
                  <td className="p-3">
                    <span className="font-mono bg-gray-100 px-2 py-1 rounded">
                      {adc.raw_value}
                    </span>
                  </td>
                  <td className="p-3">
                    <span className="font-bold text-green-600">{adc.converted_value}</span>
                  </td>
                  <td className="p-3">
                    {adc.is_connected ? (
                      <span className="text-xs bg-green-100 text-green-800 px-2 py-1 rounded font-bold">
                        ✓ OK
                      </span>
                    ) : (
                      <span className="text-xs bg-red-100 text-red-800 px-2 py-1 rounded font-bold">
                        ✗ Desconectado
                      </span>
                    )}
                  </td>
                </tr>
              )) || (
                <tr>
                  <td colSpan="6" className="p-4 text-center text-gray-500">
                    Esperando datos del ESP32...
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>

      {/* Control de Relés */}
      <div className="card">
        <h3 className="text-xl font-bold text-gray-800 mb-4 flex items-center">
          <Power className="w-6 h-6 mr-2 text-red-600" />
          Control de Relés (Salidas Digitales)
        </h3>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-4">
          {relayPins.map((relay) => {
            const isOn = relayControl[relay.key];
            return (
              <div 
                key={relay.key}
                className={`p-4 rounded-lg border-2 transition ${
                  isOn 
                    ? 'bg-green-50 border-green-500' 
                    : 'bg-gray-50 border-gray-300'
                }`}
              >
                <div className="flex justify-between items-start mb-3">
                  <div>
                    <h4 className="font-bold text-gray-800">{relay.name}</h4>
                    <p className="text-xs text-gray-600">Pin: <span className="font-mono">{relay.pin}</span></p>
                  </div>
                  {isOn ? (
                    <ToggleRight className="w-8 h-8 text-green-600" />
                  ) : (
                    <ToggleLeft className="w-8 h-8 text-gray-400" />
                  )}
                </div>
                
                <button
                  onClick={() => toggleRelay(relay.key)}
                  className={`w-full py-2 rounded-lg font-bold transition ${
                    isOn
                      ? 'bg-green-600 text-white hover:bg-green-700'
                      : 'bg-gray-300 text-gray-700 hover:bg-gray-400'
                  }`}
                >
                  {isOn ? '✓ ENCENDIDO' : '✗ APAGADO'}
                </button>
              </div>
            );
          })}
        </div>

        <div className="p-4 bg-yellow-50 border border-yellow-300 rounded-lg">
          <div className="flex items-start">
            <AlertCircle className="w-5 h-5 text-yellow-600 mr-2 flex-shrink-0 mt-0.5" />
            <div className="text-sm text-yellow-800">
              <p className="font-bold mb-1">⚠️ ADVERTENCIA:</p>
              <p>Solo usar para pruebas. El control manual puede interferir con la estrategia automática del sistema.</p>
            </div>
          </div>
        </div>
      </div>

      {/* Tabla de Referencia Rápida */}
      <div className="card">
        <h3 className="text-xl font-bold text-gray-800 mb-4">📋 Referencia Rápida de Pines</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* ADC Inputs */}
          <div>
            <h4 className="font-bold text-blue-600 mb-3">🔌 ENTRADAS ANALÓGICAS (ADC)</h4>
            <div className="space-y-2">
              {pinConfig.map((pin, idx) => (
                <div key={idx} className="flex justify-between text-sm p-2 bg-blue-50 rounded">
                  <span className="font-mono font-bold">{pin.pin}</span>
                  <span className="text-gray-600">{pin.name}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Digital Outputs */}
          <div>
            <h4 className="font-bold text-red-600 mb-3">⚡ SALIDAS DIGITALES (Relés)</h4>
            <div className="space-y-2">
              {relayPins.map((pin, idx) => (
                <div key={idx} className="flex justify-between text-sm p-2 bg-red-50 rounded">
                  <span className="font-mono font-bold">{pin.pin}</span>
                  <span className="text-gray-600">{pin.name}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Protección Eólica - Umbrales */}
      <div className="card bg-gradient-to-br from-red-50 to-orange-50 border-2 border-red-300">
        <h3 className="text-xl font-bold text-gray-800 mb-4 flex items-center">
          <AlertCircle className="w-6 h-6 mr-2 text-red-600" />
          ⚠️ Protección contra Embalamiento Eólico
        </h3>
        
        <div className="mb-4 p-4 bg-red-100 border border-red-300 rounded-lg">
          <p className="text-sm text-red-800 font-semibold mb-2">
            🔴 IMPORTANTE: Configura los umbrales de seguridad para tu generador eólico
          </p>
          <p className="text-xs text-red-700">
            Cuando se superen estos valores, el sistema activará automáticamente el freno de emergencia (GPIO23)
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
          {/* Velocidad máxima del viento */}
          <div className="p-4 bg-white rounded-lg">
            <label className="block font-bold text-gray-800 mb-2">
              💨 Velocidad Máxima del Viento
            </label>
            <div className="flex items-center gap-2">
              <input
                type="number"
                step="0.5"
                value={thresholds.max_wind_speed}
                onChange={(e) => setThresholds({...thresholds, max_wind_speed: parseFloat(e.target.value)})}
                className="flex-1 p-2 border-2 border-gray-300 rounded font-bold text-lg"
              />
              <span className="font-bold text-gray-600">m/s</span>
            </div>
            <p className="text-xs text-gray-600 mt-1">
              Recomendado: 20-30 m/s según turbina
            </p>
          </div>

          {/* Potencia máxima */}
          <div className="p-4 bg-white rounded-lg">
            <label className="block font-bold text-gray-800 mb-2">
              ⚡ Potencia Máxima Eólica
            </label>
            <div className="flex items-center gap-2">
              <input
                type="number"
                step="100"
                value={thresholds.max_wind_power}
                onChange={(e) => setThresholds({...thresholds, max_wind_power: parseInt(e.target.value)})}
                className="flex-1 p-2 border-2 border-gray-300 rounded font-bold text-lg"
              />
              <span className="font-bold text-gray-600">W</span>
            </div>
            <p className="text-xs text-gray-600 mt-1">
              Potencia nominal de tu turbina
            </p>
          </div>

          {/* Voltaje máximo */}
          <div className="p-4 bg-white rounded-lg">
            <label className="block font-bold text-gray-800 mb-2">
              🔌 Voltaje Máximo (Rectificado)
            </label>
            <div className="flex items-center gap-2">
              <input
                type="number"
                step="1"
                value={thresholds.max_voltage}
                onChange={(e) => setThresholds({...thresholds, max_voltage: parseFloat(e.target.value)})}
                className="flex-1 p-2 border-2 border-gray-300 rounded font-bold text-lg"
              />
              <span className="font-bold text-gray-600">V</span>
            </div>
            <p className="text-xs text-gray-600 mt-1">
              Para batería 48V: 58-65V máximo
            </p>
          </div>

          {/* Activar/Desactivar protección */}
          <div className="p-4 bg-white rounded-lg flex items-center justify-center">
            <div className="text-center">
              <label className="block font-bold text-gray-800 mb-3">
                🛡️ Protección Automática
              </label>
              <button
                onClick={() => setThresholds({...thresholds, brake_enabled: !thresholds.brake_enabled})}
                className={`px-6 py-3 rounded-lg font-bold transition text-lg ${
                  thresholds.brake_enabled
                    ? 'bg-green-600 text-white hover:bg-green-700'
                    : 'bg-gray-400 text-gray-700 hover:bg-gray-500'
                }`}
              >
                {thresholds.brake_enabled ? '✓ ACTIVADA' : '✗ DESACTIVADA'}
              </button>
            </div>
          </div>
        </div>

        <button
          onClick={saveThresholds}
          className="w-full py-3 bg-red-600 text-white font-bold rounded-lg hover:bg-red-700 transition text-lg"
        >
          💾 Guardar Umbrales de Protección
        </button>

        {/* Estado actual */}
        {testData && (
          <div className="mt-4 p-4 bg-white rounded-lg border-2 border-gray-200">
            <h4 className="font-bold text-gray-800 mb-3">📊 Estado Actual del Generador:</h4>
            <div className="grid grid-cols-3 gap-4 text-center">
              <div>
                <p className="text-xs text-gray-600">Velocidad Viento</p>
                <p className="text-xl font-bold text-blue-600">
                  {testData.current_wind_speed || 0} m/s
                </p>
                <p className="text-xs text-gray-500">
                  Máx: {thresholds.max_wind_speed} m/s
                </p>
              </div>
              <div>
                <p className="text-xs text-gray-600">Potencia Eólica</p>
                <p className="text-xl font-bold text-green-600">
                  {testData.current_wind_power || 0} W
                </p>
                <p className="text-xs text-gray-500">
                  Máx: {thresholds.max_wind_power} W
                </p>
              </div>
              <div>
                <p className="text-xs text-gray-600">Voltaje</p>
                <p className="text-xl font-bold text-purple-600">
                  {testData.current_voltage || 0} V
                </p>
                <p className="text-xs text-gray-500">
                  Máx: {thresholds.max_voltage} V
                </p>
              </div>
            </div>
            
            {/* Advertencia si se supera */}
            {(testData.current_wind_speed > thresholds.max_wind_speed || 
              testData.current_wind_power > thresholds.max_wind_power) && (
              <div className="mt-3 p-3 bg-red-100 border-2 border-red-500 rounded-lg animate-pulse">
                <p className="text-red-800 font-bold text-center">
                  🚨 ¡UMBRAL SUPERADO! Freno activándose...
                </p>
              </div>
            )}
          </div>
        )}
      </div>

      {/* Calibración */}
      <div className="card bg-gradient-to-br from-purple-50 to-pink-50">
        <h3 className="text-xl font-bold text-gray-800 mb-4">🔧 Factores de Calibración</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
          <div className="p-3 bg-white rounded-lg">
            <p className="text-gray-600">Voltaje (0-60V)</p>
            <p className="font-mono font-bold text-purple-600">Factor: 0.01465</p>
            <p className="text-xs text-gray-500">Divisor 100kΩ/10kΩ</p>
          </div>
          <div className="p-3 bg-white rounded-lg">
            <p className="text-gray-600">Corriente (±300A)</p>
            <p className="font-mono font-bold text-purple-600">Factor: 0.0732</p>
            <p className="text-xs text-gray-500">Shunt 75mV + OpAmp 44x</p>
          </div>
          <div className="p-3 bg-white rounded-lg">
            <p className="text-gray-600">Irradiancia (0-1200 W/m²)</p>
            <p className="font-mono font-bold text-purple-600">Factor: 0.293</p>
            <p className="text-xs text-gray-500">LDR GL5528</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default HardwareTest;
