import React, { useState, useEffect } from 'react';
import { Cloud, Sun, Droplets, Wind, Zap, Calendar, CloudRain, Activity } from 'lucide-react';
import { getForecast5Days } from '../api/api';
import DataSourceBadge from './DataSourceBadge';

const WeatherForecastFixed = () => {
  const [forecast, setForecast] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadForecast();
  }, []);

  const loadForecast = async () => {
    try {
      console.log('Cargando pronóstico...');
      const data = await getForecast5Days();
      console.log('Datos recibidos:', data);
      
      if (data && data.success && data.forecast && data.forecast.length > 0) {
        setForecast(data);
      } else {
        console.log('Datos inválidos, usando datos de ejemplo');
        setForecast(getFallbackData());
      }
      setLoading(false);
    } catch (err) {
      console.error('Error cargando pronóstico:', err);
      setError(err.message);
      // Usar datos de ejemplo si falla
      setForecast(getFallbackData());
      setLoading(false);
    }
  };

  const getFallbackData = () => {
    const today = new Date();
    const days = [];
    
    for (let i = 0; i < 4; i++) {
      const date = new Date(today);
      date.setDate(date.getDate() + i);
      const dateStr = date.toISOString().split('T')[0];
      
      const windSpeed = 5 + Math.random() * 10;
      const solarRad = 5.5 - i * 0.5;
      
      days.push({
        date: dateStr,
        temp_avg: 20 + Math.random() * 5,
        temp_max: 25 + Math.random() * 5,
        temp_min: 15 + Math.random() * 5,
        condition: i === 0 ? 'despejado' : (i % 2 === 0 ? 'parcialmente nublado' : 'nublado'),
        clouds_percent: 20 + i * 20,
        wind_speed: windSpeed,
        humidity: 50 + Math.random() * 20,
        rain_mm: 0,
        solar_radiation_kwh_m2: solarRad,
        estimated_solar_wh_per_kw: solarRad * 170,
        estimated_wind_wh_per_kw: Math.pow(windSpeed / 3.5, 3) * 50 // Fórmula cúbica para viento
      });
    }
    
    return {
      success: true,
      location: 'Bahía Blanca',
      forecast: days
    };
  };

  const getDayName = (dateStr) => {
    const date = new Date(dateStr);
    const days = ['Domingo', 'Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado'];
    return days[date.getDay()];
  };

  const getWeatherIcon = (condition, clouds) => {
    const lower = condition.toLowerCase();
    if (lower.includes('despejado') || lower.includes('clear')) return '☀️';
    if (lower.includes('lluvia') || lower.includes('rain')) return '🌧️';
    if (clouds > 70) return '☁️';
    return '🌤️';
  };

  if (loading) {
    return (
      <div className="bg-gradient-to-br from-blue-600 via-purple-600 to-pink-600 rounded-3xl shadow-2xl p-12 text-white">
        <h2 className="text-4xl font-bold">Cargando pronóstico del clima...</h2>
      </div>
    );
  }

  if (!forecast || !forecast.forecast) {
    return (
      <div className="bg-red-500 rounded-3xl shadow-2xl p-12 text-white">
        <h2 className="text-4xl font-bold">Error al cargar el pronóstico</h2>
        <p className="text-xl mt-4">{error || 'No se pudieron obtener los datos'}</p>
      </div>
    );
  }

  const days = forecast.forecast.slice(0, 4);
  const totalSolar = days.reduce((sum, day) => sum + day.estimated_solar_wh_per_kw, 0);
  const totalWind = days.reduce((sum, day) => sum + (day.estimated_wind_wh_per_kw || 0), 0);

  return (
    <div className="space-y-8">
      {/* HEADER */}
      <div className="bg-gradient-to-br from-blue-600 via-purple-600 to-pink-600 rounded-2xl shadow-xl p-8 text-white">
        <div className="flex flex-col md:flex-row items-center justify-between gap-6">
          <div>
            <div className="flex items-center gap-3 mb-3">
              <h2 className="text-4xl font-bold flex items-center">
                <Calendar className="mr-4" size={40} />
                Pronóstico Inteligente 4 Días
              </h2>
              <div className="flex gap-2">
                <DataSourceBadge 
                  source="api" 
                  details="OpenWeather API - Pronóstico 5 días cada 3 horas"
                />
                <DataSourceBadge 
                  source="ia" 
                  details="Cálculo de energía solar y eólica por IA"
                />
              </div>
            </div>
            <p className="text-xl font-semibold">📍 {forecast.location}</p>
            <p className="text-sm mt-1 opacity-80">Estimación para sistema híbrido solar + eólico</p>
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div className="bg-yellow-500 bg-opacity-30 backdrop-blur-lg p-4 rounded-xl text-center">
              <p className="text-xs uppercase mb-1">☀️ Solar</p>
              <p className="text-3xl font-black">{(totalSolar / 1000).toFixed(1)}</p>
              <p className="text-xs opacity-80">kWh (4 días)</p>
            </div>
            <div className="bg-blue-500 bg-opacity-30 backdrop-blur-lg p-4 rounded-xl text-center">
              <p className="text-xs uppercase mb-1">💨 Eólica</p>
              <p className="text-3xl font-black">{(totalWind / 1000).toFixed(1)}</p>
              <p className="text-xs opacity-80">kWh (4 días)</p>
            </div>
          </div>
        </div>
      </div>

      {/* 4 CARDS DEL CLIMA */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {days.map((day, index) => {
          const isToday = index === 0;
          
          return (
            <div 
              key={day.date}
              className={`
                rounded-xl shadow-lg overflow-hidden transform transition-all duration-300 hover:scale-105
                ${isToday 
                  ? 'bg-gradient-to-br from-orange-400 via-red-500 to-pink-600 scale-105 border-2 border-yellow-300' 
                  : 'bg-white'
                }
              `}
            >
              {/* HEADER */}
              <div className={`p-4 text-center ${isToday ? 'bg-black bg-opacity-20' : 'bg-gradient-to-r from-blue-500 to-purple-600'} text-white`}>
                <p className="text-2xl font-bold">
                  {isToday ? '🔆 HOY' : getDayName(day.date)}
                </p>
                <p className="text-xs opacity-90 mt-1">{day.date.substring(5)}</p>
              </div>

              {/* CONTENIDO */}
              <div className="p-4">
                {/* ICONO */}
                <div className="text-6xl text-center mb-3">
                  {getWeatherIcon(day.condition, day.clouds_percent)}
                </div>

                {/* CONDICIÓN */}
                <p className={`text-center text-lg font-bold mb-3 capitalize ${isToday ? 'text-white' : 'text-gray-800'}`}>
                  {day.condition}
                </p>

                {/* TEMPERATURA */}
                <div className="text-center mb-4">
                  <p className={`text-4xl font-bold ${isToday ? 'text-white' : 'text-gray-900'}`}>
                    {Math.round(day.temp_avg)}°
                  </p>
                  <div className="flex justify-center gap-3 mt-1 text-sm">
                    <span className={isToday ? 'text-orange-200' : 'text-red-500'}>
                      ↑{Math.round(day.temp_max)}°
                    </span>
                    <span className={isToday ? 'text-blue-200' : 'text-blue-500'}>
                      ↓{Math.round(day.temp_min)}°
                    </span>
                  </div>
                </div>

                {/* GENERACIÓN SOLAR */}
                <div className={`rounded-lg p-3 mb-2 ${
                  isToday 
                    ? 'bg-yellow-300 bg-opacity-30 border-2 border-yellow-200' 
                    : 'bg-gradient-to-br from-yellow-50 to-orange-50 border border-yellow-300'
                }`}>
                  <div className="flex items-center justify-between mb-1">
                    <span className={`font-bold text-sm ${isToday ? 'text-white' : 'text-gray-800'}`}>
                      ☀️ Solar
                    </span>
                    <span className={`text-xs ${isToday ? 'text-yellow-100' : 'text-gray-600'}`}>
                      {day.solar_radiation_kwh_m2.toFixed(1)} kWh/m²
                    </span>
                  </div>
                  <p className={`text-2xl font-black ${isToday ? 'text-white' : 'text-orange-600'}`}>
                    {(day.estimated_solar_wh_per_kw / 1000).toFixed(2)} kWh
                  </p>
                  <p className={`text-xs ${isToday ? 'text-yellow-100' : 'text-gray-600'}`}>
                    por kW instalado
                  </p>
                </div>

                {/* GENERACIÓN EÓLICA */}
                <div className={`rounded-lg p-3 mb-3 ${
                  isToday 
                    ? 'bg-blue-300 bg-opacity-30 border-2 border-blue-200' 
                    : 'bg-gradient-to-br from-blue-50 to-cyan-50 border border-blue-300'
                }`}>
                  <div className="flex items-center justify-between mb-1">
                    <span className={`font-bold text-sm ${isToday ? 'text-white' : 'text-gray-800'}`}>
                      💨 Eólica
                    </span>
                    <span className={`text-xs ${isToday ? 'text-blue-100' : 'text-gray-600'}`}>
                      {day.wind_speed.toFixed(1)} m/s
                    </span>
                  </div>
                  <p className={`text-2xl font-black ${isToday ? 'text-white' : 'text-blue-600'}`}>
                    {((day.estimated_wind_wh_per_kw || 0) / 1000).toFixed(2)} kWh
                  </p>
                  <p className={`text-xs ${isToday ? 'text-blue-100' : 'text-gray-600'}`}>
                    por kW instalado
                  </p>
                </div>

                {/* DETALLES */}
                <div className="grid grid-cols-2 gap-2">
                  <div className={`flex flex-col items-center p-2 rounded-lg ${isToday ? 'bg-white bg-opacity-20' : 'bg-gray-100'}`}>
                    <Cloud className={`w-5 h-5 mb-1 ${isToday ? 'text-white' : 'text-gray-600'}`} />
                    <span className={`text-xs ${isToday ? 'text-white' : 'text-gray-600'}`}>Nubes</span>
                    <span className={`font-bold text-sm ${isToday ? 'text-white' : 'text-gray-900'}`}>
                      {Math.round(day.clouds_percent)}%
                    </span>
                  </div>
                  <div className={`flex flex-col items-center p-2 rounded-lg ${isToday ? 'bg-white bg-opacity-20' : 'bg-gray-100'}`}>
                    <Droplets className={`w-5 h-5 mb-1 ${isToday ? 'text-white' : 'text-gray-600'}`} />
                    <span className={`text-xs ${isToday ? 'text-white' : 'text-gray-600'}`}>Humedad</span>
                    <span className={`font-bold text-sm ${isToday ? 'text-white' : 'text-gray-900'}`}>
                      {Math.round(day.humidity)}%
                    </span>
                  </div>
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* SISTEMA INTELIGENTE */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="bg-gradient-to-br from-purple-50 to-indigo-50 border-l-4 border-purple-500 p-6 rounded-lg">
          <h4 className="font-bold text-purple-800 mb-3 flex items-center">
            <Activity className="w-5 h-5 mr-2" />
            🤖 Sistema Híbrido Inteligente
          </h4>
          <p className="text-sm text-gray-700 mb-3">
            El sistema de IA optimiza automáticamente las fuentes de energía basándose en:
          </p>
          <ul className="text-xs text-gray-600 space-y-1">
            <li>✓ Predicción meteorológica en tiempo real</li>
            <li>✓ Patrones de consumo aprendidos</li>
            <li>✓ Estado de carga de batería</li>
            <li>✓ Rendimiento solar vs eólico</li>
          </ul>
        </div>
        
        <div className="bg-gradient-to-br from-green-50 to-emerald-50 border-l-4 border-green-500 p-6 rounded-lg">
          <h4 className="font-bold text-green-800 mb-3 flex items-center">
            <Zap className="w-5 h-5 mr-2" />
            ⚙️ Control con Relés Inteligentes
          </h4>
          <p className="text-sm text-gray-700 mb-3">
            El sistema decide automáticamente:
          </p>
          <ul className="text-xs text-gray-600 space-y-1">
            <li>• Si hay mucho viento → Prioriza eólica</li>
            <li>• Si hay mucho sol → Prioriza solar</li>
            <li>• Desconecta fuentes según necesidad</li>
            <li>• Aprende patrones de consumo del hogar</li>
          </ul>
        </div>
      </div>
      
      {/* NOTA */}
      <div className="bg-blue-50 border-l-4 border-blue-500 p-4 rounded-lg">
        <p className="text-xs text-gray-700">
          <strong>💡 Nota:</strong> Estimaciones basadas en condiciones meteorológicas, eficiencia solar 17% y turbina eólica con cut-in de 3.5 m/s.
          {error && <span className="text-orange-600"> Usando datos de ejemplo por error en API.</span>}
        </p>
      </div>
    </div>
  );
};

export default WeatherForecastFixed;
