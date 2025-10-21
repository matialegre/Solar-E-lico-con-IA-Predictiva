import React from 'react';
import { 
  Cloud, 
  CloudRain, 
  Sun, 
  Wind, 
  Droplets,
  Gauge,
  Eye
} from 'lucide-react';
import DataSourceBadge from './DataSourceBadge';

const WeatherWidget = ({ weather }) => {
  if (!weather) {
    return (
      <div className="card">
        <div className="animate-pulse">
          <div className="h-20 bg-gray-200 rounded"></div>
        </div>
      </div>
    );
  }

  const getWeatherIcon = (description) => {
    const desc = description.toLowerCase();
    if (desc.includes('rain') || desc.includes('lluvia')) {
      return <CloudRain className="w-12 h-12 text-blue-500" />;
    } else if (desc.includes('cloud') || desc.includes('nube')) {
      return <Cloud className="w-12 h-12 text-gray-500" />;
    } else {
      return <Sun className="w-12 h-12 text-yellow-500" />;
    }
  };

  return (
    <div className="card bg-gradient-to-br from-blue-50 to-cyan-50">
      <div className="flex items-center justify-between mb-4">
        <h3 className="card-title mb-0">
          <Cloud className="w-5 h-5 mr-2" />
          Clima Actual
        </h3>
        <DataSourceBadge 
          source="api" 
          details="OpenWeather API - Actualizado cada 10 minutos"
        />
      </div>
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center space-x-4">
          {getWeatherIcon(weather.description)}
          <div>
            <p className="text-4xl font-bold text-gray-900">
              {weather.temperature_c.toFixed(1)}°C
            </p>
            <p className="text-sm text-gray-600 capitalize">
              {weather.description}
            </p>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="flex items-center space-x-2">
          <Wind className="w-5 h-5 text-blue-600" />
          <div>
            <p className="text-xs text-gray-600">Viento</p>
            <p className="font-semibold text-gray-900">
              {weather.wind_speed_ms.toFixed(1)} m/s
            </p>
          </div>
        </div>

        <div className="flex items-center space-x-2">
          <Droplets className="w-5 h-5 text-blue-600" />
          <div>
            <p className="text-xs text-gray-600">Humedad</p>
            <p className="font-semibold text-gray-900">
              {weather.humidity_percent.toFixed(0)}%
            </p>
          </div>
        </div>

        <div className="flex items-center space-x-2">
          <Cloud className="w-5 h-5 text-gray-600" />
          <div>
            <p className="text-xs text-gray-600">Nubosidad</p>
            <p className="font-semibold text-gray-900">
              {weather.cloud_cover_percent.toFixed(0)}%
            </p>
          </div>
        </div>

        <div className="flex items-center space-x-2">
          <Gauge className="w-5 h-5 text-purple-600" />
          <div>
            <p className="text-xs text-gray-600">Presión</p>
            <p className="font-semibold text-gray-900">
              {weather.pressure_hpa.toFixed(0)} hPa
            </p>
          </div>
        </div>
      </div>

      {weather.solar_radiation_wm2 !== undefined && (
        <div className="mt-4 p-3 bg-yellow-50 rounded-lg border border-yellow-200">
          <div className="flex items-center justify-between">
            <span className="text-sm font-medium text-yellow-800">
              Radiación Solar
            </span>
            <span className="text-lg font-bold text-yellow-900">
              {weather.solar_radiation_wm2.toFixed(0)} W/m²
            </span>
          </div>
        </div>
      )}
    </div>
  );
};

export default WeatherWidget;
