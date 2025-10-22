import React, { useState, useEffect } from 'react';
import { Activity, Zap, Wind, Battery, Thermometer, Sun, Gauge } from 'lucide-react';
import api from '../api/api';

const ESP32LiveData = () => {
  const [devices, setDevices] = useState([]);
  const [telemetry, setTelemetry] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadData();
    const interval = setInterval(loadData, 2000); // Actualizar cada 2 seg
    return () => clearInterval(interval);
  }, []);

  const loadData = async () => {
    try {
      // Cargar dispositivos
      const devicesResponse = await api.get('/api/esp32/devices');
      setDevices(devicesResponse.data.devices || []);
      
      // Si hay dispositivos, cargar su telemetría desde dashboard
      if (devicesResponse.data.devices.length > 0) {
        const dashResponse = await api.get('/api/dashboard');
        setTelemetry(dashResponse.data);
      }
      
      setLoading(false);
    } catch (error) {
      console.error('Error loading ESP32 live data:', error);
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="card bg-gray-800 border-2 border-gray-700 animate-pulse">
        <div className="h-96 bg-gray-700 rounded"></div>
      </div>
    );
  }

  const device = devices[0];
  const isOnline = device?.status === 'online';

  if (!device) {
    return (
      <div className="card bg-gray-800 border-2 border-gray-700 text-center py-12">
        <Activity className="w-12 h-12 mx-auto mb-3 text-gray-500" />
        <p className="text-gray-400">Esperando ESP32...</p>
      </div>
    );
  }

  return (
    <div className="card bg-gradient-to-br from-gray-800 to-gray-900 border-2 border-blue-500">
      {/* Header */}
      <div className="flex items-center justify-between mb-4 pb-3 border-b border-gray-700">
        <h3 className="text-xl font-bold text-white flex items-center">
          <Activity className={`w-6 h-6 mr-2 ${isOnline ? 'text-green-400 animate-pulse' : 'text-red-400'}`} />
          📡 Datos en Vivo ESP32
        </h3>
        <div className={`px-2 py-1 rounded text-xs font-bold ${
          isOnline ? 'bg-green-500 text-white' : 'bg-red-500 text-white'
        }`}>
          {isOnline ? '● ONLINE' : '● OFFLINE'}
        </div>
      </div>

      {/* Device Info */}
      <div className="mb-4 p-3 bg-gray-700/50 rounded-lg">
        <p className="text-xs text-gray-400">Device ID</p>
        <p className="text-sm font-mono text-white">{device.device_id}</p>
        {device.ip_local && (
          <>
            <p className="text-xs text-gray-400 mt-2">IP Local</p>
            <p className="text-sm font-mono text-blue-300">{device.ip_local}</p>
          </>
        )}
      </div>

      {/* Telemetry Data */}
      {telemetry && (
        <div className="space-y-2">
          {/* Batería */}
          <div className="p-3 bg-blue-500/10 border border-blue-500/30 rounded-lg">
            <div className="flex items-center justify-between mb-1">
              <div className="flex items-center">
                <Battery className="w-4 h-4 mr-2 text-blue-400" />
                <span className="text-sm text-blue-300">Batería</span>
              </div>
              <span className="text-lg font-bold text-white">
                {telemetry.battery?.soc?.toFixed(1) || 0}%
              </span>
            </div>
            <div className="text-xs text-gray-400">
              {telemetry.battery?.voltage?.toFixed(2) || 0}V | {telemetry.battery?.current?.toFixed(1) || 0}A
            </div>
          </div>

          {/* Solar */}
          <div className="p-3 bg-yellow-500/10 border border-yellow-500/30 rounded-lg">
            <div className="flex items-center justify-between mb-1">
              <div className="flex items-center">
                <Sun className="w-4 h-4 mr-2 text-yellow-400" />
                <span className="text-sm text-yellow-300">Solar</span>
              </div>
              <span className="text-lg font-bold text-white">
                {telemetry.solar?.power?.toFixed(0) || 0}W
              </span>
            </div>
            <div className="text-xs text-gray-400">
              {telemetry.solar?.voltage?.toFixed(1) || 0}V | {telemetry.solar?.current?.toFixed(1) || 0}A
            </div>
          </div>

          {/* Eólica */}
          <div className="p-3 bg-green-500/10 border border-green-500/30 rounded-lg">
            <div className="flex items-center justify-between mb-1">
              <div className="flex items-center">
                <Wind className="w-4 h-4 mr-2 text-green-400" />
                <span className="text-sm text-green-300">Eólica</span>
              </div>
              <span className="text-lg font-bold text-white">
                {telemetry.wind?.power?.toFixed(0) || 0}W
              </span>
            </div>
            <div className="text-xs text-gray-400">
              {telemetry.wind?.wind_speed?.toFixed(1) || 0} m/s
            </div>
          </div>

          {/* Consumo */}
          <div className="p-3 bg-red-500/10 border border-red-500/30 rounded-lg">
            <div className="flex items-center justify-between mb-1">
              <div className="flex items-center">
                <Zap className="w-4 h-4 mr-2 text-red-400" />
                <span className="text-sm text-red-300">Consumo</span>
              </div>
              <span className="text-lg font-bold text-white">
                {telemetry.load_power?.toFixed(0) || 0}W
              </span>
            </div>
          </div>

          {/* Temperatura */}
          {telemetry.temperature && (
            <div className="p-3 bg-purple-500/10 border border-purple-500/30 rounded-lg">
              <div className="flex items-center justify-between">
                <div className="flex items-center">
                  <Thermometer className="w-4 h-4 mr-2 text-purple-400" />
                  <span className="text-sm text-purple-300">Temperatura</span>
                </div>
                <span className="text-lg font-bold text-white">
                  {telemetry.temperature?.toFixed(1) || 0}°C
                </span>
              </div>
            </div>
          )}

          {/* Balance */}
          <div className="p-3 bg-gray-700/50 rounded-lg border border-gray-600">
            <div className="flex items-center justify-between">
              <div className="flex items-center">
                <Gauge className="w-4 h-4 mr-2 text-gray-400" />
                <span className="text-sm text-gray-300">Balance</span>
              </div>
              <span className={`text-lg font-bold ${
                (telemetry.solar?.power || 0) + (telemetry.wind?.power || 0) - (telemetry.load_power || 0) >= 0
                  ? 'text-green-400'
                  : 'text-red-400'
              }`}>
                {((telemetry.solar?.power || 0) + (telemetry.wind?.power || 0) - (telemetry.load_power || 0)).toFixed(0)}W
              </span>
            </div>
          </div>
        </div>
      )}

      {/* Heartbeat info */}
      {device.heartbeat && (
        <div className="mt-4 p-2 bg-gray-700/30 rounded text-xs text-gray-400">
          <div className="flex justify-between">
            <span>Uptime:</span>
            <span className="text-gray-300">{Math.floor(device.heartbeat.uptime / 60)}min</span>
          </div>
          <div className="flex justify-between mt-1">
            <span>WiFi RSSI:</span>
            <span className="text-gray-300">{device.heartbeat.rssi} dBm</span>
          </div>
          <div className="flex justify-between mt-1">
            <span>Free Heap:</span>
            <span className="text-gray-300">{Math.floor(device.heartbeat.free_heap / 1024)} KB</span>
          </div>
        </div>
      )}

      {/* Update indicator */}
      <div className="mt-3 text-center">
        <div className="inline-flex items-center text-xs text-gray-500">
          <div className="w-2 h-2 bg-green-400 rounded-full mr-2 animate-pulse"></div>
          Actualiza cada 2 seg
        </div>
      </div>
    </div>
  );
};

export default ESP32LiveData;
