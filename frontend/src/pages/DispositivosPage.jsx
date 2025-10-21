/**
 * Página de gestión de dispositivos ESP32
 * Muestra todos los ESP32 conectados con su estado
 */

import React, { useState, useEffect } from 'react';
import { Activity, Wifi, WifiOff, MapPin, Settings, Trash2, RefreshCw } from 'lucide-react';
import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export default function DispositivosPage() {
  const [devices, setDevices] = useState([]);
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState({ total: 0, online: 0, offline: 0 });

  const fetchDevices = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`${API_URL}/api/esp32/devices`);
      setDevices(response.data.devices || []);
      setStats({
        total: response.data.total || 0,
        online: response.data.online || 0,
        offline: response.data.offline || 0
      });
    } catch (error) {
      console.error('Error cargando dispositivos:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDevices();
    // Actualizar cada 5 segundos
    const interval = setInterval(fetchDevices, 5000);
    return () => clearInterval(interval);
  }, []);

  const handleDelete = async (deviceId) => {
    if (!window.confirm(`¿Eliminar dispositivo ${deviceId}?`)) return;
    
    try {
      await axios.delete(`${API_URL}/api/esp32/devices/${deviceId}`);
      fetchDevices();
    } catch (error) {
      console.error('Error eliminando dispositivo:', error);
      alert('Error al eliminar dispositivo');
    }
  };

  const formatUptime = (seconds) => {
    if (!seconds) return 'N/A';
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    return `${hours}h ${minutes}m`;
  };

  const formatDate = (isoString) => {
    if (!isoString) return 'N/A';
    const date = new Date(isoString);
    return date.toLocaleString('es-AR');
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white p-6">
      {/* Header */}
      <div className="max-w-7xl mx-auto mb-8">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h1 className="text-3xl font-bold mb-2">📡 Dispositivos ESP32</h1>
            <p className="text-gray-400">Gestión y monitoreo de dispositivos conectados</p>
          </div>
          <button
            onClick={fetchDevices}
            disabled={loading}
            className="px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg flex items-center gap-2 transition-colors disabled:opacity-50"
          >
            <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
            Actualizar
          </button>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
          <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
            <div className="flex items-center gap-3">
              <Activity className="w-8 h-8 text-blue-400" />
              <div>
                <p className="text-gray-400 text-sm">Total Dispositivos</p>
                <p className="text-3xl font-bold">{stats.total}</p>
              </div>
            </div>
          </div>
          
          <div className="bg-gray-800 rounded-lg p-6 border border-green-500">
            <div className="flex items-center gap-3">
              <Wifi className="w-8 h-8 text-green-400" />
              <div>
                <p className="text-gray-400 text-sm">Online</p>
                <p className="text-3xl font-bold text-green-400">{stats.online}</p>
              </div>
            </div>
          </div>
          
          <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
            <div className="flex items-center gap-3">
              <WifiOff className="w-8 h-8 text-gray-400" />
              <div>
                <p className="text-gray-400 text-sm">Offline</p>
                <p className="text-3xl font-bold text-gray-400">{stats.offline}</p>
              </div>
            </div>
          </div>
        </div>

        {/* Devices List */}
        {loading && devices.length === 0 ? (
          <div className="text-center py-12">
            <RefreshCw className="w-12 h-12 text-gray-400 animate-spin mx-auto mb-4" />
            <p className="text-gray-400">Cargando dispositivos...</p>
          </div>
        ) : devices.length === 0 ? (
          <div className="bg-gray-800 rounded-lg p-12 text-center border border-gray-700">
            <Activity className="w-16 h-16 text-gray-600 mx-auto mb-4" />
            <h3 className="text-xl font-bold mb-2">No hay dispositivos registrados</h3>
            <p className="text-gray-400 mb-4">
              Los dispositivos ESP32 aparecerán aquí cuando se conecten al sistema.
            </p>
            <p className="text-sm text-gray-500">
              Asegúrate de que el ESP32 esté configurado correctamente y conectado a la red.
            </p>
          </div>
        ) : (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {devices.map((device) => (
              <div
                key={device.device_id}
                className={`bg-gray-800 rounded-lg p-6 border-2 transition-all ${
                  device.status === 'online'
                    ? 'border-green-500 shadow-lg shadow-green-500/20'
                    : 'border-gray-700'
                }`}
              >
                {/* Header */}
                <div className="flex items-start justify-between mb-4">
                  <div className="flex items-center gap-3">
                    {device.status === 'online' ? (
                      <Wifi className="w-6 h-6 text-green-400" />
                    ) : (
                      <WifiOff className="w-6 h-6 text-gray-400" />
                    )}
                    <div>
                      <h3 className="text-lg font-bold">{device.device_id}</h3>
                      <p className={`text-sm ${device.status === 'online' ? 'text-green-400' : 'text-gray-400'}`}>
                        {device.status === 'online' ? '● Online' : '● Offline'}
                      </p>
                    </div>
                  </div>
                  
                  <div className="flex gap-2">
                    <button
                      onClick={() => window.location.href = `/configurar/${device.device_id}`}
                      className="p-2 bg-blue-600 hover:bg-blue-700 rounded transition-colors"
                      title="Configurar"
                    >
                      <Settings className="w-4 h-4" />
                    </button>
                    <button
                      onClick={() => handleDelete(device.device_id)}
                      className="p-2 bg-red-600 hover:bg-red-700 rounded transition-colors"
                      title="Eliminar"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </div>
                </div>

                {/* Info Grid */}
                <div className="grid grid-cols-2 gap-4 text-sm">
                  <div>
                    <p className="text-gray-400">IP Local</p>
                    <p className="font-mono">{device.ip_local || 'N/A'}</p>
                  </div>
                  
                  <div>
                    <p className="text-gray-400">MAC Address</p>
                    <p className="font-mono text-xs">{device.mac_address || 'N/A'}</p>
                  </div>
                  
                  <div>
                    <p className="text-gray-400">Firmware</p>
                    <p className="font-mono">v{device.firmware_version || 'N/A'}</p>
                  </div>
                  
                  <div>
                    <p className="text-gray-400">Registrado</p>
                    <p className="text-xs">{formatDate(device.registered_at)}</p>
                  </div>
                  
                  <div className="col-span-2">
                    <p className="text-gray-400">Última conexión</p>
                    <p className="text-xs">{formatDate(device.last_seen)}</p>
                  </div>
                </div>

                {/* Location */}
                {device.latitude && device.longitude && (
                  <div className="mt-4 pt-4 border-t border-gray-700">
                    <div className="flex items-center gap-2 text-sm">
                      <MapPin className="w-4 h-4 text-blue-400" />
                      <span className="text-gray-400">Ubicación:</span>
                      <span className="font-mono">
                        {device.latitude.toFixed(4)}, {device.longitude.toFixed(4)}
                      </span>
                    </div>
                  </div>
                )}

                {/* Heartbeat Info */}
                {device.heartbeat && device.status === 'online' && (
                  <div className="mt-4 pt-4 border-t border-gray-700">
                    <div className="grid grid-cols-3 gap-2 text-xs">
                      <div>
                        <p className="text-gray-400">Uptime</p>
                        <p className="font-bold">{formatUptime(device.heartbeat.uptime)}</p>
                      </div>
                      <div>
                        <p className="text-gray-400">Memoria</p>
                        <p className="font-bold">{Math.round(device.heartbeat.free_heap / 1024)} KB</p>
                      </div>
                      <div>
                        <p className="text-gray-400">Señal</p>
                        <p className="font-bold">{device.heartbeat.rssi} dBm</p>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
