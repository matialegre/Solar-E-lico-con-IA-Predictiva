import React, { useState, useEffect } from 'react';
import { Power, Wifi, WifiOff, Zap, Battery } from 'lucide-react';

const ESP32Monitor = () => {
  const [esp32Data, setEsp32Data] = useState(null);
  const [connected, setConnected] = useState(false);
  const [loading, setLoading] = useState(false);
  const [lastUpdate, setLastUpdate] = useState(null);

  // Cargar datos del ESP32
  const loadESP32Data = async () => {
    try {
      const response = await fetch('/api/esp32/devices');
      const data = await response.json();
      
      if (data.devices && data.devices.length > 0) {
        const esp = data.devices[0];
        setEsp32Data(esp);
        setConnected(esp.status === 'online');
        setLastUpdate(new Date());
      }
    } catch (error) {
      console.error('Error cargando datos ESP32:', error);
      setConnected(false);
    }
  };

  // Cargar datos iniciales y actualizar cada 0.5 segundos (tiempo real)
  useEffect(() => {
    loadESP32Data();
    const interval = setInterval(loadESP32Data, 500);  // 500ms = 0.5s
    return () => clearInterval(interval);
  }, []);

  // Enviar comando al ESP32
  const sendCommand = async (command, parameter) => {
    setLoading(true);
    try {
      const response = await fetch('http://190.211.201.217:11113/api/esp32/command/ESP32_INVERSOR_001', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ command, parameter })
      });
      
      const result = await response.json();
      console.log('Comando enviado:', result);
      
      // Esperar confirmación ACK
      if (result.command_id) {
        await waitForAck(result.command_id);
      }
      
      // Recargar datos
      setTimeout(loadESP32Data, 500);
    } catch (error) {
      console.error('Error enviando comando:', error);
    } finally {
      setLoading(false);
    }
  };

  // Esperar confirmación ACK
  const waitForAck = async (commandId) => {
    for (let i = 0; i < 10; i++) {
      try {
        const response = await fetch(`http://190.211.201.217:11113/api/esp32/command/ESP32_INVERSOR_001/status/${commandId}`);
        const status = await response.json();
        
        if (status.status === 'acked') {
          console.log('✅ Comando confirmado');
          return true;
        }
        
        await new Promise(resolve => setTimeout(resolve, 1000));
      } catch (error) {
        console.error('Error verificando ACK:', error);
      }
    }
    console.log('⏱️ Timeout esperando ACK');
    return false;
  };

  // Obtener estado del relé
  const getRelayState = (relayName) => {
    if (!esp32Data) return false;
    // relays está en el nivel superior, NO dentro de telemetry
    return esp32Data.relays?.[relayName] || false;
  };

  // Obtener valor ADC
  const getADCValue = (adcName) => {
    if (!esp32Data) {
      return '0.000';
    }
    
    // raw_adc está en el nivel superior, NO dentro de telemetry
    const rawAdc = esp32Data.raw_adc;
    
    if (!rawAdc) {
      return '0.000';
    }
    
    const value = rawAdc[adcName];
    
    if (value === undefined || value === null) {
      return '0.000';
    }
    
    return Number(value).toFixed(3);
  };

  return (
    <div className="bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 rounded-xl shadow-2xl overflow-hidden border border-slate-700">
      {/* Header */}
      <div className="bg-gradient-to-r from-blue-600 to-purple-600 px-6 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <Zap className="w-8 h-8 text-yellow-300" />
            <div>
              <h2 className="text-2xl font-bold text-white">Monitor ESP32</h2>
              <p className="text-blue-100 text-sm">Inversor Híbrido - Tiempo Real</p>
            </div>
          </div>
          
          {/* Estado de conexión */}
          <div className="flex items-center space-x-2">
            {connected ? (
              <>
                <Wifi className="w-6 h-6 text-green-400 animate-pulse" />
                <span className="text-green-300 font-semibold">CONECTADO</span>
              </>
            ) : (
              <>
                <WifiOff className="w-6 h-6 text-red-400" />
                <span className="text-red-300 font-semibold">DESCONECTADO</span>
              </>
            )}
          </div>
        </div>
      </div>

      <div className="p-6 space-y-6">
        {/* Información del dispositivo */}
        {/* Info del dispositivo */}
        <div className="grid grid-cols-4 gap-4 mb-6">
          <div className="bg-slate-800 rounded-lg p-3">
            <p className="text-slate-400 text-xs mb-1">Device ID</p>
            <p className="text-white text-sm font-mono">{esp32Data?.device_id || '-'}</p>
          </div>
          
          <div className="bg-slate-800 rounded-lg p-3">
            <p className="text-slate-400 text-xs mb-1">Contador</p>
            <p className="text-green-400 text-2xl font-bold font-mono">
              {esp32Data?.contador || 0}
            </p>
          </div>
          
          <div className="bg-slate-800 rounded-lg p-3">
            <p className="text-slate-400 text-xs mb-1">Última actualización</p>
            <p className="text-white text-sm">
              {lastUpdate ? lastUpdate.toLocaleTimeString() : '-'}
            </p>
          </div>
          
          <div className="bg-slate-800 rounded-lg p-3">
            <p className="text-slate-400 text-xs mb-1">RSSI</p>
            <p className="text-white text-sm font-mono">
              {esp32Data?.heartbeat?.rssi || '-'} dBm
            </p>
          </div>
        </div>

        {/* Control de Relés */}
        <div>
          <h3 className="text-lg font-semibold text-white mb-4 flex items-center">
            <Power className="w-5 h-5 mr-2 text-yellow-400" />
            Control de Relés
          </h3>
          
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {/* Relé Solar */}
            <div className="bg-slate-800 rounded-lg p-4">
              <div className="flex items-center justify-between mb-3">
                <span className="text-white font-medium">☀️ Solar</span>
                <div className={`w-3 h-3 rounded-full ${getRelayState('solar') ? 'bg-green-500 animate-pulse' : 'bg-gray-600'}`} />
              </div>
              <div className="space-y-2">
                <button
                  onClick={() => sendCommand('solar', 'on')}
                  disabled={loading || getRelayState('solar')}
                  className={`w-full py-2 rounded-lg font-semibold transition ${
                    getRelayState('solar')
                      ? 'bg-green-600 text-white cursor-not-allowed'
                      : 'bg-green-500 hover:bg-green-600 text-white'
                  }`}
                >
                  ON
                </button>
                <button
                  onClick={() => sendCommand('solar', 'off')}
                  disabled={loading || !getRelayState('solar')}
                  className={`w-full py-2 rounded-lg font-semibold transition ${
                    !getRelayState('solar')
                      ? 'bg-red-600 text-white cursor-not-allowed'
                      : 'bg-red-500 hover:bg-red-600 text-white'
                  }`}
                >
                  OFF
                </button>
              </div>
            </div>

            {/* Relé Eólica */}
            <div className="bg-slate-800 rounded-lg p-4">
              <div className="flex items-center justify-between mb-3">
                <span className="text-white font-medium">💨 Eólica</span>
                <div className={`w-3 h-3 rounded-full ${getRelayState('wind') ? 'bg-green-500 animate-pulse' : 'bg-gray-600'}`} />
              </div>
              <div className="space-y-2">
                <button
                  onClick={() => sendCommand('eolica', 'on')}
                  disabled={loading || getRelayState('wind')}
                  className={`w-full py-2 rounded-lg font-semibold transition ${
                    getRelayState('wind')
                      ? 'bg-green-600 text-white cursor-not-allowed'
                      : 'bg-green-500 hover:bg-green-600 text-white'
                  }`}
                >
                  ON
                </button>
                <button
                  onClick={() => sendCommand('eolica', 'off')}
                  disabled={loading || !getRelayState('wind')}
                  className={`w-full py-2 rounded-lg font-semibold transition ${
                    !getRelayState('wind')
                      ? 'bg-red-600 text-white cursor-not-allowed'
                      : 'bg-red-500 hover:bg-red-600 text-white'
                  }`}
                >
                  OFF
                </button>
              </div>
            </div>

            {/* Relé Red */}
            <div className="bg-slate-800 rounded-lg p-4">
              <div className="flex items-center justify-between mb-3">
                <span className="text-white font-medium">🔌 Red</span>
                <div className={`w-3 h-3 rounded-full ${getRelayState('grid') ? 'bg-green-500 animate-pulse' : 'bg-gray-600'}`} />
              </div>
              <div className="space-y-2">
                <button
                  onClick={() => sendCommand('red', 'on')}
                  disabled={loading || getRelayState('grid')}
                  className={`w-full py-2 rounded-lg font-semibold transition ${
                    getRelayState('grid')
                      ? 'bg-green-600 text-white cursor-not-allowed'
                      : 'bg-green-500 hover:bg-green-600 text-white'
                  }`}
                >
                  ON
                </button>
                <button
                  onClick={() => sendCommand('red', 'off')}
                  disabled={loading || !getRelayState('grid')}
                  className={`w-full py-2 rounded-lg font-semibold transition ${
                    !getRelayState('grid')
                      ? 'bg-red-600 text-white cursor-not-allowed'
                      : 'bg-red-500 hover:bg-red-600 text-white'
                  }`}
                >
                  OFF
                </button>
              </div>
            </div>

            {/* Relé Carga */}
            <div className="bg-slate-800 rounded-lg p-4">
              <div className="flex items-center justify-between mb-3">
                <span className="text-white font-medium">⚡ Carga</span>
                <div className={`w-3 h-3 rounded-full ${getRelayState('load') ? 'bg-green-500 animate-pulse' : 'bg-gray-600'}`} />
              </div>
              <div className="space-y-2">
                <button
                  onClick={() => sendCommand('carga', 'on')}
                  disabled={loading || getRelayState('load')}
                  className={`w-full py-2 rounded-lg font-semibold transition ${
                    getRelayState('load')
                      ? 'bg-green-600 text-white cursor-not-allowed'
                      : 'bg-green-500 hover:bg-green-600 text-white'
                  }`}
                >
                  ON
                </button>
                <button
                  onClick={() => sendCommand('carga', 'off')}
                  disabled={loading || !getRelayState('load')}
                  className={`w-full py-2 rounded-lg font-semibold transition ${
                    !getRelayState('load')
                      ? 'bg-red-600 text-white cursor-not-allowed'
                      : 'bg-red-500 hover:bg-red-600 text-white'
                  }`}
                >
                  OFF
                </button>
              </div>
            </div>
          </div>
        </div>

        {/* Mediciones ADC */}
        <div>
          <h3 className="text-lg font-semibold text-white mb-4 flex items-center">
            <Battery className="w-5 h-5 mr-2 text-blue-400" />
            Mediciones ADC (0-3.3V)
          </h3>
          
          {/* Indicador de RPM/Frecuencia - Turbina (SIEMPRE VISIBLE) */}
          <div className="mb-6 bg-gradient-to-r from-purple-900/50 to-pink-900/50 rounded-lg p-4 border border-purple-700">
            <div className="flex items-center justify-between">
              <div className="flex-1">
                <div className="flex items-center gap-2 mb-1">
                  <p className="text-slate-400 text-sm">RPM Turbina Eólica</p>
                  {esp32Data?.telemetry?.turbine_rpm > 0 && (
                    <span className="px-2 py-0.5 bg-green-500/20 text-green-400 text-xs rounded-full border border-green-500/50">
                      ✓ ACTIVO
                    </span>
                  )}
                  {(!esp32Data?.telemetry?.turbine_rpm || esp32Data?.telemetry?.turbine_rpm === 0) && (
                    <span className="px-2 py-0.5 bg-gray-500/20 text-gray-400 text-xs rounded-full border border-gray-500/50">
                      ○ SIN SEÑAL
                    </span>
                  )}
                </div>
                <p className="text-3xl font-bold text-purple-400 font-mono">
                  {Math.round(esp32Data?.telemetry?.turbine_rpm || esp32Data?.telemetry?.rpm || 0)} <span className="text-lg">RPM</span>
                </p>
              </div>
              <div className="text-right">
                <p className="text-slate-400 text-sm">Frecuencia Eléctrica</p>
                <p className="text-2xl font-bold text-pink-400 font-mono">
                  {(esp32Data?.telemetry?.frequency_hz || 0).toFixed(2)} <span className="text-sm">Hz</span>
                </p>
              </div>
            </div>
          </div>

          {/* Grid de 2x2 (4 ADC reales del hardware) */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {/* GPIO34 - Batería */}
            <div className="bg-slate-800 rounded-lg p-4 border-l-4 border-blue-500">
              <p className="text-slate-400 text-xs mb-1">GPIO34 (ADC1)</p>
              <p className="text-lg font-semibold text-white mb-1">🔋 Batería</p>
              <p className="text-3xl font-bold text-blue-400 font-mono">
                {getADCValue('adc1_bat1')}
                <span className="text-sm ml-1">V</span>
              </p>
            </div>

            {/* GPIO35 - Eólica DC */}
            <div className="bg-slate-800 rounded-lg p-4 border-l-4 border-cyan-500">
              <p className="text-slate-400 text-xs mb-1">GPIO35 (ADC2)</p>
              <p className="text-lg font-semibold text-white mb-1">💨 Eólica</p>
              <p className="text-3xl font-bold text-cyan-400 font-mono">
                {getADCValue('adc2_eolica')}
                <span className="text-sm ml-1">V</span>
              </p>
            </div>

            {/* GPIO36 - Solar */}
            <div className="bg-slate-800 rounded-lg p-4 border-l-4 border-yellow-500">
              <p className="text-slate-400 text-xs mb-1">GPIO36 (ADC5)</p>
              <p className="text-lg font-semibold text-white mb-1">☀️ Solar</p>
              <p className="text-3xl font-bold text-yellow-400 font-mono">
                {getADCValue('adc5_solar')}
                <span className="text-sm ml-1">V</span>
              </p>
            </div>

            {/* GPIO39 - Carga */}
            <div className="bg-slate-800 rounded-lg p-4 border-l-4 border-green-500">
              <p className="text-slate-400 text-xs mb-1">GPIO39 (ADC6)</p>
              <p className="text-lg font-semibold text-white mb-1">⚡ Carga</p>
              <p className="text-3xl font-bold text-green-400 font-mono">
                {getADCValue('adc6_load')}
                <span className="text-sm ml-1">V</span>
              </p>
            </div>
          </div>
        </div>

        {/* Indicador de carga */}
        {loading && (
          <div className="text-center py-2">
            <div className="inline-block animate-spin rounded-full h-6 w-6 border-b-2 border-blue-500"></div>
            <p className="text-slate-400 text-sm mt-2">Enviando comando...</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default ESP32Monitor;
