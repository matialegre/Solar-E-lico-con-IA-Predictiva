import React, { useState, useEffect } from 'react';
import { Cloud, Sun, Droplets, Wind, Zap, TrendingUp, Calendar } from 'lucide-react';
import { getForecast5Days } from '../api/api';

const WeatherForecast = () => {
  const [forecast, setForecast] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadForecast();
    const interval = setInterval(loadForecast, 600000); // Actualizar cada 10 min
    return () => clearInterval(interval);
  }, []);

  const loadForecast = async () => {
    try {
      const data = await getForecast5Days();
      setForecast(data);
      setLoading(false);
    } catch (error) {
      console.error('Error loading forecast:', error);
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="card">
        <div className="animate-pulse">
          <div className="h-64 bg-gray-200 rounded"></div>
        </div>
      </div>
    );
  }

  if (!forecast || !forecast.success) {
    return null;
  }

  const getDayName = (dateStr) => {
    const date = new Date(dateStr);
    const days = ['Dom', 'Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb'];
    return days[date.getDay()];
  };

  const getWeatherIcon = (condition) => {
    const lower = condition.toLowerCase();
    if (lower.includes('despejado') || lower.includes('clear')) return '☀️';
    if (lower.includes('nube') || lower.includes('cloud')) return '☁️';
    if (lower.includes('lluvia') || lower.includes('rain')) return '🌧️';
    if (lower.includes('tormenta') || lower.includes('storm')) return '⛈️';
    return '🌤️';
  };

  const totalSolarProduction = forecast.forecast.reduce((sum, day) => 
    sum + day.estimated_solar_wh_per_kw, 0
  );

  return (
    <div className="space-y-6">
      {/* Header con resumen - MÁS GRANDE Y DESTACADO */}
      <div className="card bg-gradient-to-br from-blue-600 via-purple-600 to-pink-600 text-white shadow-2xl">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h2 className="text-4xl font-bold flex items-center mb-3">
              <Calendar className="w-10 h-10 mr-3" />
              Pronóstico Meteorológico
            </h2>
            <p className="text-blue-100 text-lg">📍 {forecast.location}</p>
            <p className="text-blue-200 text-sm mt-1">Predicción con datos reales de OpenWeatherMap</p>
          </div>
          <div className="text-right bg-white bg-opacity-20 p-6 rounded-xl">
            <p className="text-sm text-blue-100 mb-2">⚡ Producción Solar Total</p>
            <p className="text-5xl font-bold mb-2">{(totalSolarProduction / 1000).toFixed(1)}</p>
            <p className="text-xl text-blue-200">kWh</p>
            <p className="text-xs text-blue-200 mt-2">Próximos 5 días (por kW instalado)</p>
          </div>
        </div>
      </div>

      {/* Cards de pronóstico por día - SOLO 4 DÍAS */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        {forecast.forecast.slice(0, 4).map((day, index) => (
          <div 
            key={day.date}
            className={`card hover:shadow-2xl transition-all transform hover:-translate-y-2 ${
              index === 0 ? 'bg-gradient-to-br from-yellow-100 to-orange-100 border-4 border-yellow-500 shadow-xl scale-105' : 'bg-gradient-to-br from-white to-gray-50'
            }`}
          >
            {/* Día */}
            <div className="text-center mb-3">
              <p className="text-sm font-medium text-gray-600">
                {index === 0 ? 'HOY' : getDayName(day.date)}
              </p>
              <p className="text-xs text-gray-500">{day.date.substring(5)}</p>
            </div>

            {/* Icono del clima */}
            <div className="text-center mb-3">
              <span className="text-4xl">{getWeatherIcon(day.condition)}</span>
              <p className="text-xs text-gray-600 mt-1 capitalize">{day.condition}</p>
            </div>

            {/* Temperatura */}
            <div className="text-center mb-3">
              <p className="text-2xl font-bold text-gray-800">{day.temp_avg}°C</p>
              <div className="flex justify-center items-center space-x-2 text-xs text-gray-500">
                <span className="text-red-500">↑ {day.temp_max}°</span>
                <span className="text-blue-500">↓ {day.temp_min}°</span>
              </div>
            </div>

            {/* Radiación Solar */}
            <div className="bg-gradient-to-r from-yellow-100 to-orange-100 rounded-lg p-3 mb-2">
              <div className="flex items-center justify-between mb-1">
                <div className="flex items-center">
                  <Sun className="w-4 h-4 text-yellow-600 mr-1" />
                  <span className="text-xs font-medium text-gray-700">Solar</span>
                </div>
                <Zap className="w-4 h-4 text-orange-500" />
              </div>
              <p className="text-lg font-bold text-orange-600">
                {day.solar_radiation_kwh_m2} kWh/m²
              </p>
              <p className="text-xs text-gray-600 mt-1">
                ≈ {(day.estimated_solar_wh_per_kw / 1000).toFixed(1)} kWh/kW
              </p>
            </div>

            {/* Detalles adicionales */}
            <div className="space-y-2 text-xs">
              <div className="flex items-center justify-between text-gray-600">
                <span className="flex items-center">
                  <Cloud className="w-3 h-3 mr-1" />
                  Nubes
                </span>
                <span className="font-medium">{day.clouds_percent}%</span>
              </div>
              <div className="flex items-center justify-between text-gray-600">
                <span className="flex items-center">
                  <Wind className="w-3 h-3 mr-1" />
                  Viento
                </span>
                <span className="font-medium">{day.wind_speed} m/s</span>
              </div>
              <div className="flex items-center justify-between text-gray-600">
                <span className="flex items-center">
                  <Droplets className="w-3 h-3 mr-1" />
                  Humedad
                </span>
                <span className="font-medium">{day.humidity}%</span>
              </div>
              {day.rain_mm > 0 && (
                <div className="flex items-center justify-between text-blue-600">
                  <span className="flex items-center">
                    🌧️ Lluvia
                  </span>
                  <span className="font-medium">{day.rain_mm} mm</span>
                </div>
              )}
            </div>
          </div>
        ))}
      </div>

      {/* Gráfico de producción solar */}
      <div className="card bg-gradient-to-br from-yellow-50 to-orange-50">
        <h4 className="font-bold text-gray-800 mb-4 flex items-center">
          <TrendingUp className="w-5 h-5 mr-2 text-orange-600" />
          Estimación de Producción Solar
        </h4>
        
        <div className="space-y-3">
          {forecast.forecast.map((day, index) => {
            const maxProduction = Math.max(...forecast.forecast.map(d => d.estimated_solar_wh_per_kw));
            const barWidth = (day.estimated_solar_wh_per_kw / maxProduction) * 100;
            
            return (
              <div key={day.date}>
                <div className="flex items-center justify-between mb-1">
                  <span className="text-sm font-medium text-gray-700">
                    {index === 0 ? 'HOY' : getDayName(day.date)}
                  </span>
                  <span className="text-sm font-bold text-orange-600">
                    {(day.estimated_solar_wh_per_kw / 1000).toFixed(2)} kWh/kW
                  </span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-6 overflow-hidden">
                  <div
                    className="bg-gradient-to-r from-yellow-400 to-orange-500 h-6 rounded-full flex items-center justify-end pr-2 transition-all duration-500"
                    style={{ width: `${barWidth}%` }}
                  >
                    {barWidth > 20 && (
                      <span className="text-xs text-white font-bold">
                        ☀️ {day.solar_radiation_kwh_m2} kWh/m²
                      </span>
                    )}
                  </div>
                </div>
              </div>
            );
          })}
        </div>

        <div className="mt-4 p-3 bg-white rounded-lg border border-orange-200">
          <p className="text-xs text-gray-600">
            <strong>💡 Nota:</strong> Estos valores son estimaciones basadas en condiciones climáticas.
            La producción real depende de la orientación, inclinación, temperatura y eficiencia de los paneles.
          </p>
        </div>
      </div>
    </div>
  );
};

export default WeatherForecast;
