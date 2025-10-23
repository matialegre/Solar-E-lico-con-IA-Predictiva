import React, { useState, useEffect } from 'react';
import { Power, Zap, Wind, Battery, Home, AlertTriangle } from 'lucide-react';

const ESP32Control = () => {
  const [espData, setEspData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [commandStatus, setCommandStatus] = useState('');

  const DEVICE_ID = 'ESP32_INVERSOR_001';
  const API_BASE = 'http://190.211.201.217:11113';

  // Obtener estado del ESP cada 2 segundos
  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch(`${API_BASE}/api/esp32/estado/${DEVICE_ID}`);
        const data = await response.json();
        if (data.status === 'success') {
          setEspData(data);
        }
      } catch (error) {
        console.error('Error al obtener datos del ESP:', error);
      }
    };

    fetchData();
    const interval = setInterval(fetchData, 2000);
    return () => clearInterval(interval);
  }, []);

  // Enviar comando a relé
  const sendCommand = async (command, parameter) => {
    setLoading(true);
    setCommandStatus('Enviando...');
    
    try {
      const response = await fetch(`${API_BASE}/api/esp32/command/${DEVICE_ID}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ command, parameter })
      });
      
      const data = await response.json();
      if (data.status === 'success') {
        setCommandStatus(`✅ Comando ${command} (${parameter}) enviado`);
      } else {
        setCommandStatus(`❌ Error: ${data.message}`);
      }
    } catch (error) {
      setCommandStatus(`❌ Error de conexión: ${error.message}`);
    }
    
    setLoading(false);
    setTimeout(() => setCommandStatus(''), 3000);
  };

  const RelayButton = ({ name, command, state, icon: Icon, color }) => (
    <div className="bg-gray-800 p-4 rounded-lg">
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center gap-2">
          <Icon className={`w-5 h-5 ${color}`} />
          <span className="font-semibold">{name}</span>
        </div>
        <div className={`w-3 h-3 rounded-full ${state ? 'bg-green-500' : 'bg-red-500'}`} />
      </div>
      <div className="flex gap-2">
        <button
          onClick={() => sendCommand(command, 'on')}
          disabled={loading}
          className="flex-1 bg-green-600 hover:bg-green-700 disabled:bg-gray-600 text-white py-2 px-4 rounded transition"
        >
          ON
        </button>
        <button
          onClick={() => sendCommand(command, 'off')}
          disabled={loading}
          className="flex-1 bg-red-600 hover:bg-red-700 disabled:bg-gray-600 text-white py-2 px-4 rounded transition"
        >
          OFF
        </button>
      </div>
    </div>
  );

  const ADCDisplay = ({ label, voltage, gpio, filtered }) => (
    <div className="bg-gray-800 p-3 rounded">
      <div className="text-sm text-gray-400 mb-1">{label}</div>
      <div className="text-2xl font-bold text-cyan-400">{voltage?.toFixed(3) || '0.000'} V</div>
      {filtered !== undefined && (
        <div className="text-sm text-gray-300 mt-1">
          DC Filtrado: <span className="text-yellow-400">{filtered?.toFixed(3) || '0.000'} V</span>
        </div>
      )}
      <div className="text-xs text-gray-500 mt-1">{gpio}</div>
    </div>
  );

  if (!espData) {
    return (
      <div className="bg-gray-900 rounded-lg shadow-xl p-6">
        <h2 className="text-2xl font-bold text-white mb-4">🔌 Control ESP32</h2>
        <div className="text-gray-400">Conectando con ESP32...</div>
      </div>
    );
  }

  const { telemetry, relays, raw_adc, last_seen } = espData;

  return (
    <div className="bg-gray-900 rounded-lg shadow-xl p-6 space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold text-white">🔌 Control ESP32</h2>
        <div className="flex items-center gap-2">
          <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse" />
          <span className="text-sm text-gray-400">
            {new Date(last_seen).toLocaleTimeString()}
          </span>
        </div>
      </div>

      {/* Status mensaje */}
      {commandStatus && (
        <div className="bg-blue-900/50 border border-blue-500 rounded-lg p-3 text-white">
          {commandStatus}
        </div>
      )}

      {/* Control de Relés */}
      <div>
        <h3 className="text-lg font-semibold text-white mb-3">⚡ Control de Relés</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <RelayButton
            name="Panel Solar"
            command="solar"
            state={relays?.solar}
            icon={Zap}
            color="text-yellow-400"
          />
          <RelayButton
            name="Eólica"
            command="eolica"
            state={relays?.wind}
            icon={Wind}
            color="text-blue-400"
          />
          <RelayButton
            name="Red Backup"
            command="red"
            state={relays?.grid}
            icon={Power}
            color="text-red-400"
          />
          <RelayButton
            name="Carga"
            command="carga"
            state={relays?.load}
            icon={Home}
            color="text-green-400"
          />
        </div>
      </div>

      {/* Lecturas ADC (0-3.3V) */}
      <div>
        <h3 className="text-lg font-semibold text-white mb-3">📊 Voltajes ADC (0–3.3V)</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <ADCDisplay
            label="Batería"
            voltage={raw_adc?.adc1_bat1}
            gpio="GPIO34"
          />
          <ADCDisplay
            label="Corriente Solar"
            voltage={raw_adc?.adc4_solar}
            gpio="GPIO36"
          />
          <ADCDisplay
            label="Corriente Eólica"
            voltage={raw_adc?.adc5_wind}
            filtered={telemetry?.v_wind_v_dc}
            gpio="GPIO35"
          />
          <ADCDisplay
            label="Corriente Carga"
            voltage={raw_adc?.adc6_load}
            gpio="GPIO39"
          />
        </div>
      </div>

      {/* Stage 1 Voltages */}
      <div>
        <h3 className="text-lg font-semibold text-white mb-3">🔬 Stage 1 (Procesado)</h3>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="bg-gray-800 p-3 rounded">
            <div className="text-sm text-gray-400">V_Bat</div>
            <div className="text-xl font-bold text-green-400">
              {telemetry?.v_bat_v?.toFixed(3) || '0.000'} V
            </div>
          </div>
          <div className="bg-gray-800 p-3 rounded">
            <div className="text-sm text-gray-400">V_Solar</div>
            <div className="text-xl font-bold text-yellow-400">
              {telemetry?.v_solar_v?.toFixed(3) || '0.000'} V
            </div>
          </div>
          <div className="bg-gray-800 p-3 rounded">
            <div className="text-sm text-gray-400">V_Wind DC</div>
            <div className="text-xl font-bold text-blue-400">
              {telemetry?.v_wind_v_dc?.toFixed(3) || '0.000'} V
            </div>
          </div>
          <div className="bg-gray-800 p-3 rounded">
            <div className="text-sm text-gray-400">V_Load</div>
            <div className="text-xl font-bold text-red-400">
              {telemetry?.v_load_v?.toFixed(3) || '0.000'} V
            </div>
          </div>
        </div>
      </div>

      {/* Botón de emergencia */}
      <div className="border-t border-gray-700 pt-4">
        <button
          onClick={() => sendCommand('apagar_todo', '')}
          disabled={loading}
          className="w-full bg-red-600 hover:bg-red-700 disabled:bg-gray-600 text-white py-3 px-6 rounded-lg font-bold flex items-center justify-center gap-2 transition"
        >
          <AlertTriangle className="w-5 h-5" />
          APAGAR TODO (EMERGENCIA)
        </button>
      </div>
    </div>
  );
};

export default ESP32Control;
