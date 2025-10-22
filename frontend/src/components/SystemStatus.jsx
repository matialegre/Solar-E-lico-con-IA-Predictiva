/**
 * Panel de estado del sistema
 * Muestra estado de todas las APIs y servicios
 */

import React, { useState, useEffect } from 'react';
import { 
  CheckCircle, XCircle, AlertCircle, RefreshCw, 
  Cloud, Satellite, Server, Activity, Brain, Zap
} from 'lucide-react';
import api from '../api/api';

export default function SystemStatus() {
  const [status, setStatus] = useState(null);
  const [forecast, setForecast] = useState(null);
  const [loading, setLoading] = useState(true);
  const [lastUpdate, setLastUpdate] = useState(null);

  const fetchStatus = async () => {
    try {
      const [statusRes, forecastRes] = await Promise.all([
        api.get('/api/status/health'),
        api.get('/api/status/forecast')
      ]);
      
      setStatus(statusRes.data);
      setForecast(forecastRes.data);
      setLastUpdate(new Date());
      setLoading(false);
    } catch (error) {
      console.error('Error fetching status:', error);
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchStatus();
    const interval = setInterval(fetchStatus, 30000); // Actualizar cada 30 seg
    return () => clearInterval(interval);
  }, []);

  const getStatusIcon = (serviceStatus) => {
    switch(serviceStatus) {
      case 'online':
      case 'ready':
        return <CheckCircle className="w-5 h-5 text-green-400" />;
      case 'warning':
      case 'not_trained':
        return <AlertCircle className="w-5 h-5 text-yellow-400" />;
      case 'error':
      case 'offline':
        return <XCircle className="w-5 h-5 text-red-400" />;
      default:
        return <AlertCircle className="w-5 h-5 text-gray-400" />;
    }
  };

  const getServiceIcon = (serviceName) => {
    if (serviceName.includes('OpenWeather')) return <Cloud className="w-5 h-5" />;
    if (serviceName.includes('NASA')) return <Satellite className="w-5 h-5" />;
    if (serviceName.includes('Backend')) return <Server className="w-5 h-5" />;
    if (serviceName.includes('ESP32')) return <Activity className="w-5 h-5" />;
    if (serviceName.includes('Machine')) return <Brain className="w-5 h-5" />;
    return <Zap className="w-5 h-5" />;
  };

  if (loading) {
    return (
      <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
        <div className="flex items-center gap-2 mb-4">
          <RefreshCw className="w-5 h-5 animate-spin" />
          <h3 className="text-lg font-bold">Verificando servicios...</h3>
        </div>
      </div>
    );
  }

  if (!status) {
    return (
      <div className="bg-gray-800 rounded-lg p-6 border border-red-500">
        <div className="flex items-center gap-2">
          <XCircle className="w-5 h-5 text-red-400" />
          <h3 className="text-lg font-bold">Error al verificar estado</h3>
        </div>
      </div>
    );
  }

  const weather = status?.services?.openweather || {};
  const nasa = status?.services?.nasa_power || {};
  const esp32 = status?.services?.esp32 || {};
  const ml = status?.services?.ml || {};

  const healthPercent = status && status.total_services > 0 ? 
    Math.round((status.services_ok / status.total_services) * 100) : 0;

  // Manejar casos donde no hay datos
  if (!status || !status.services) {
    return (
      <div className="card bg-gray-800 border-2 border-gray-700 animate-pulse">
        <div className="h-32 bg-gray-700 rounded"></div>
      </div>
    );
  }

  const healthPercentage = status.summary?.health_percentage || 0;
  const overallStatus = status.summary?.overall_status || 'offline';

  return (
    <div className="space-y-4">
      {/* Header con estado general */}
      <div className={`rounded-lg p-6 border-2 ${
        overallStatus === 'healthy' ? 'bg-green-500/10 border-green-500' :
        overallStatus === 'degraded' ? 'bg-yellow-500/10 border-yellow-500' :
        'bg-red-500/10 border-red-500'
      }`}>
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-2xl font-bold mb-2">Estado del Sistema</h2>
            <p className="text-gray-400">
              {status.summary.online_count} de {status.summary.all_services_count} servicios operativos
            </p>
          </div>
          
          <div className="text-center">
            <div className={`text-5xl font-bold ${
              healthPercentage === 100 ? 'text-green-400' :
              healthPercentage >= 70 ? 'text-yellow-400' :
              'text-red-400'
            }`}>
              {healthPercentage.toFixed(0)}%
            </div>
            <p className="text-sm text-gray-400">Salud del Sistema</p>
          </div>
          
          <button
            onClick={fetchStatus}
            className="px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg flex items-center gap-2"
          >
            <RefreshCw className="w-4 h-4" />
            Actualizar
          </button>
        </div>
      </div>

      {/* Servicios individuales */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {Object.entries(status.services).map(([key, service]) => (
          <div
            key={key}
            className="bg-gray-800 rounded-lg p-4 border border-gray-700 hover:border-gray-600 transition-colors"
          >
            <div className="flex items-start justify-between mb-3">
              <div className="flex items-center gap-2">
                {getServiceIcon(service.name)}
                <h3 className="font-bold">{service.name}</h3>
              </div>
              {getStatusIcon(service.status)}
            </div>

            {service.status === 'online' || service.status === 'ready' ? (
              <div className="space-y-2 text-sm">
                {service.response_time_ms && (
                  <div className="flex justify-between">
                    <span className="text-gray-400">Latencia:</span>
                    <span className="font-mono">{service.response_time_ms}ms</span>
                  </div>
                )}
                
                {service.location && (
                  <div className="flex justify-between">
                    <span className="text-gray-400">Ubicación:</span>
                    <span>{service.location}</span>
                  </div>
                )}
                
                {service.total !== undefined && (
                  <div className="flex justify-between">
                    <span className="text-gray-400">Dispositivos:</span>
                    <span>
                      <span className="text-green-400">{service.online}</span> / {service.total}
                    </span>
                  </div>
                )}
                
                {service.solar_accuracy !== undefined && (
                  <div className="space-y-1">
                    <div className="flex justify-between">
                      <span className="text-gray-400">Precisión Solar:</span>
                      <span className="text-yellow-400">{(service.solar_accuracy * 100).toFixed(1)}%</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-400">Precisión Eólica:</span>
                      <span className="text-blue-400">{(service.wind_accuracy * 100).toFixed(1)}%</span>
                    </div>
                  </div>
                )}
                <p className="text-sm text-gray-400">
                  Ubicación: {forecast?.location || 'Cargando...'}
                </p>
                {forecast?.current_day?.avg_temp && (
                  <p className="text-sm text-gray-400">
                    Temperatura: {forecast.current_day.avg_temp}°C
                  </p>
                )}
              </div>
            ) : (
              <div className="text-sm text-red-400">
                {service.error || service.message || 'Servicio no disponible'}
              </div>
            )}
          </div>
        ))}
      </div>

      {/* Pronóstico 5 días */}
      {forecast && !forecast.error && (
        <div className="bg-gray-800 rounded-lg p-6 border border-blue-500">
          <h3 className="text-xl font-bold mb-4 flex items-center gap-2">
            <Cloud className="w-5 h-5 text-blue-400" />
            Pronóstico 5 Días (Usado por ML)
          </h3>
          
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
            <div className="p-3 bg-gray-900 rounded">
              <p className="text-sm text-gray-400 mb-1">Temp Promedio</p>
              <p className="text-2xl font-bold">{forecast?.summary?.avg_temp?.toFixed(1) || 'N/A'}°C</p>
            </div>
            
            <div className="p-3 bg-gray-900 rounded">
              <p className="text-sm text-gray-400 mb-1">Viento Promedio</p>
              <p className="text-2xl font-bold">{forecast.summary.avg_wind.toFixed(1)} m/s</p>
            </div>
            
            <div className="p-3 bg-gray-900 rounded">
              <p className="text-sm text-gray-400 mb-1">Días Buenos (Solar)</p>
              <p className="text-2xl font-bold text-yellow-400">{forecast.summary.good_solar_days}</p>
            </div>
            
            <div className="p-3 bg-gray-900 rounded">
              <p className="text-sm text-gray-400 mb-1">Días Buenos (Eólico)</p>
              <p className="text-2xl font-bold text-blue-400">{forecast.summary.good_wind_days}</p>
            </div>
          </div>

          <div className="grid grid-cols-5 gap-2">
            {forecast.forecast_days.map((day, idx) => (
              <div key={idx} className="p-3 bg-gray-900 rounded text-center">
                <p className="text-xs text-gray-400 mb-2">{new Date(day.date).toLocaleDateString('es', { month: 'short', day: 'numeric' })}</p>
                <p className="text-sm font-bold mb-1">{day.temp_avg.toFixed(0)}°C</p>
                <p className="text-xs text-blue-400">{day.wind_avg_ms.toFixed(1)} m/s</p>
                <div className="mt-2 flex justify-center gap-1">
                  <div className="relative w-full bg-gray-700 h-2 rounded">
                    <div 
                      className="absolute left-0 top-0 h-full bg-yellow-400 rounded"
                      style={{ width: `${day.solar_factor * 100}%` }}
                      title={`Factor solar: ${(day.solar_factor * 100).toFixed(0)}%`}
                    />
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Última actualización */}
      <div className="text-center text-sm text-gray-500">
        Última actualización: {lastUpdate?.toLocaleTimeString('es')}
      </div>
    </div>
  );
}
