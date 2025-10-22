import React, { useState, useEffect } from 'react';
import { Cpu, Wifi, WifiOff, CheckCircle, XCircle, Activity, Clock, Zap } from 'lucide-react';
import api from '../api/api';

const ESP32Status = () => {
  const [devices, setDevices] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadDevices();
    const interval = setInterval(loadDevices, 3000); // Actualizar cada 3 seg (más frecuente)
    return () => clearInterval(interval);
  }, []);

  const loadDevices = async () => {
    try {
      const response = await api.get('/api/esp32/devices');
      console.log('📡 ESP32 Devices Response:', response.data);
      setDevices(response.data.devices || []);
      setLoading(false);
    } catch (error) {
      console.error('❌ Error loading ESP32 devices:', error);
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="card animate-pulse">
        <div className="h-32 bg-gray-200 rounded"></div>
      </div>
    );
  }

  return (
    <div className="card bg-gradient-to-br from-blue-50 to-indigo-50 border-2 border-blue-200">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-2xl font-bold text-gray-800 flex items-center">
          <Cpu className="w-8 h-8 mr-3 text-blue-600" />
          🔌 Estado de Conexión ESP32
        </h3>
        <div className={`px-3 py-1 rounded-full text-sm font-bold ${
          devices.length > 0 && devices[0]?.status === 'online' 
            ? 'bg-green-500 text-white animate-pulse' 
            : 'bg-red-500 text-white'
        }`}>
          {devices.length > 0 && devices[0]?.status === 'online' ? '● ONLINE' : '● OFFLINE'}
        </div>
      </div>

      {devices.length === 0 ? (
        <div className="text-center py-12 bg-yellow-50 border-2 border-yellow-300 rounded-lg">
          <WifiOff className="w-16 h-16 mx-auto mb-4 text-yellow-600" />
          <p className="text-xl font-bold text-gray-800 mb-2">⚠️ Esperando Conexión del ESP32</p>
          <p className="text-gray-700 mb-4">
            1. Conectá el ESP32 a la corriente<br/>
            2. El ESP32 se conectará automáticamente al WiFi<br/>
            3. Aparecerá aquí cuando se registre en el servidor
          </p>
          <div className="inline-flex items-center px-4 py-2 bg-blue-100 text-blue-800 rounded-lg text-sm">
            <Activity className="w-4 h-4 mr-2 animate-pulse" />
            Esperando dispositivo...
          </div>
        </div>
      ) : (
        <div className="space-y-4">
          {devices.map((device) => {
            const isOnline = device.status === 'online';
            const lastSeenDate = new Date(device.last_seen);
            const secondsAgo = Math.floor((Date.now() - lastSeenDate.getTime()) / 1000);
            const lastSeenMinutes = Math.floor(secondsAgo / 60);
            
            return (
              <div 
                key={device.device_id}
                className={`p-4 rounded-lg border-2 ${
                  isOnline 
                    ? 'bg-green-50 border-green-200' 
                    : 'bg-red-50 border-red-200'
                }`}
              >
                <div className="flex items-start justify-between mb-3">
                  <div className="flex items-center">
                    {isOnline ? (
                      <>
                        <CheckCircle className="w-6 h-6 text-green-600 mr-3 animate-pulse" />
                        <div>
                          <h4 className="text-xl font-bold text-gray-800">
                            {device.device_id}
                          </h4>
                          <p className="text-sm">
                            <span className="text-green-600 font-bold">✅ CONECTADO AL SERVIDOR</span>
                          </p>
                          {/* DATOS EN TIEMPO REAL */}
                          {device.telemetry && (
                            <div className="mt-2 grid grid-cols-2 gap-2 text-xs">
                              <div className="bg-blue-100 px-2 py-1 rounded">
                                🔋 {device.telemetry.battery_soc?.toFixed(0) || 0}% | {device.telemetry.battery_voltage?.toFixed(1) || 0}V
                              </div>
                              <div className="bg-yellow-100 px-2 py-1 rounded">
                                ☀️ {device.telemetry.solar_power?.toFixed(0) || 0}W
                              </div>
                              <div className="bg-green-100 px-2 py-1 rounded">
                                💨 {device.telemetry.wind_power?.toFixed(0) || 0}W
                              </div>
                              <div className="bg-red-100 px-2 py-1 rounded">
                                ⚡ {device.telemetry.load_power?.toFixed(0) || 0}W
                              </div>
                            </div>
                          )}
                        </div>
                      </>
                    ) : (
                      <>
                        <XCircle className="w-6 h-6 text-red-600 mr-3" />
                        <div>
                          <h4 className="text-xl font-bold text-gray-800">{device.device_id}</h4>
                          <p className="text-sm text-red-600 font-bold">❌ Desconectado</p>
                          <p className="text-xs text-gray-600 mt-1">Última conexión hace {lastSeenMinutes} min</p>
                        </div>
                      </>
                    )}
                  </div>
                  <div className="flex items-center text-sm bg-white px-3 py-1 rounded-full">
                    <Clock className="w-4 h-4 mr-1" />
                    {isOnline ? (
                      <span className="text-green-600 font-bold">Ahora</span>
                    ) : (
                      `Hace ${lastSeenMinutes} min`
                    )}
                  </div>
                </div>

                {device.telemetry && (
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mt-3">
                    <div className="bg-white p-2 rounded">
                      <div className="flex items-center text-xs text-gray-600 mb-1">
                        <Zap className="w-3 h-3 mr-1" />
                        Voltaje
                      </div>
                      <div className="font-bold text-sm">{device.telemetry.battery_voltage?.toFixed(1) || '0.0'}V</div>
                    </div>
                    <div className="bg-white p-2 rounded">
                      <div className="flex items-center text-xs text-gray-600 mb-1">
                        <Activity className="w-3 h-3 mr-1" />
                        SOC
                      </div>
                      <div className="font-bold text-sm">{device.telemetry.battery_soc?.toFixed(0) || '0'}%</div>
                    </div>
                    <div className="bg-white p-2 rounded">
                      <div className="text-xs text-gray-600 mb-1">Solar</div>
                      <div className="font-bold text-sm">{device.telemetry.solar_power?.toFixed(0) || '0'}W</div>
                    </div>
                    <div className="bg-white p-2 rounded">
                      <div className="text-xs text-gray-600 mb-1">Eólica</div>
                      <div className="font-bold text-sm">{device.telemetry.wind_power?.toFixed(0) || '0'}W</div>
                    </div>
                  </div>
                )}

                {device.relays && (
                  <div className="mt-3 flex gap-2 flex-wrap">
                    {['solar', 'wind', 'grid', 'load'].map((relay) => (
                      <span 
                        key={relay}
                        className={`text-xs px-2 py-1 rounded ${
                          device.relays[relay] 
                            ? 'bg-green-600 text-white' 
                            : 'bg-gray-300 text-gray-600'
                        }`}
                      >
                        {relay === 'solar' && '☀️ Solar'}
                        {relay === 'wind' && '💨 Eólica'}
                        {relay === 'grid' && '🔌 Red'}
                        {relay === 'load' && '⚡ Carga'}
                      </span>
                    ))}
                  </div>
                )}
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
};

export default ESP32Status;
