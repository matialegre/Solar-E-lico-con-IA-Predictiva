import React, { useState, useEffect } from 'react';
import { Cloud, Sun, Droplets, Wind, Zap, Calendar, CloudRain } from 'lucide-react';
import { getForecast5Days } from '../api/api';

const WeatherForecastSimple = () => {
  const [forecast, setForecast] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadForecast();
    const interval = setInterval(loadForecast, 600000);
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
      <div className="card bg-gradient-to-br from-blue-500 to-purple-600 text-white">
        <div className="animate-pulse h-64"></div>
      </div>
    );
  }

  if (!forecast || !forecast.success) {
    return null;
  }

  const getDayName = (dateStr) => {
    const date = new Date(dateStr);
    const days = ['Domingo', 'Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado'];
    return days[date.getDay()];
  };

  const getWeatherIcon = (condition, clouds) => {
    const lower = condition.toLowerCase();
    if (lower.includes('despejado') || lower.includes('clear')) return <Sun className="w-16 h-16 text-yellow-300" />;
    if (lower.includes('lluvia') || lower.includes('rain')) return <CloudRain className="w-16 h-16 text-blue-300" />;
    if (clouds > 70) return <Cloud className="w-16 h-16 text-gray-300" />;
    return <Sun className="w-16 h-16 text-yellow-200" />;
  };

  const totalSolarProduction = forecast.forecast.slice(0, 4).reduce((sum, day) => 
    sum + day.estimated_solar_wh_per_kw, 0
  );

  return (
    <div className="space-y-8">
      {/* Header Principal - SUPER DESTACADO */}
      <div className="bg-gradient-to-br from-blue-500 via-purple-600 to-pink-600 rounded-3xl shadow-2xl p-12 text-white border-4 border-white border-opacity-30">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h2 className="text-6xl font-black mb-4 flex items-center drop-shadow-lg">
              <Calendar className="w-12 h-12 mr-4" />
              Pronóstico del Clima
            </h2>
            <p className="text-3xl text-white font-bold drop-shadow-md">📍 {forecast.location}</p>
            <p className="text-lg text-blue-200 mt-2">Predicción para paneles solares</p>
          </div>
          <div className="text-right bg-white bg-opacity-20 backdrop-blur-sm p-8 rounded-2xl">
            <p className="text-sm text-blue-100 mb-2 uppercase tracking-wide">Producción Total</p>
            <div className="flex items-baseline justify-end">
              <p className="text-6xl font-bold">{(totalSolarProduction / 1000).toFixed(1)}</p>
              <p className="text-2xl ml-2">kWh</p>
            </div>
            <p className="text-sm text-blue-200 mt-2">Próximos 4 días (por kW instalado)</p>
          </div>
        </div>
      </div>

      {/* Pronóstico de 4 días - CARDS GRANDES */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
        {forecast.forecast.slice(0, 4).map((day, index) => {
          const isToday = index === 0;
          
          return (
            <div 
              key={day.date}
              className={`
                rounded-2xl shadow-xl overflow-hidden transform transition-all duration-300
                ${isToday 
                  ? 'bg-gradient-to-br from-orange-400 to-red-500 scale-105 shadow-2xl' 
                  : 'bg-white hover:scale-105 hover:shadow-2xl'
                }
              `}
            >
              {/* Header del día */}
              <div className={`p-6 ${isToday ? 'bg-black bg-opacity-20' : 'bg-gradient-to-r from-blue-500 to-purple-500'} text-white`}>
                <p className="text-2xl font-bold text-center">
                  {isToday ? '🔆 HOY' : getDayName(day.date)}
                </p>
                <p className="text-center text-sm opacity-90 mt-1">{day.date}</p>
              </div>

              {/* Contenido */}
              <div className="p-6">
                {/* Icono del clima */}
                <div className="flex justify-center mb-4">
                  {getWeatherIcon(day.condition, day.clouds_percent)}
                </div>

                {/* Condición */}
                <p className={`text-center text-lg font-semibold mb-4 capitalize ${isToday ? 'text-white' : 'text-gray-800'}`}>
                  {day.condition}
                </p>

                {/* Temperatura */}
                <div className="text-center mb-6">
                  <p className={`text-5xl font-bold ${isToday ? 'text-white' : 'text-gray-900'}`}>
                    {day.temp_avg}°
                  </p>
                  <div className="flex justify-center items-center gap-4 mt-2">
                    <span className={`text-sm ${isToday ? 'text-orange-200' : 'text-red-500'}`}>
                      ↑ {day.temp_max}°
                    </span>
                    <span className={`text-sm ${isToday ? 'text-blue-200' : 'text-blue-500'}`}>
                      ↓ {day.temp_min}°
                    </span>
                  </div>
                </div>

                {/* Producción Solar - DESTACADO */}
                <div className={`
                  rounded-xl p-4 mb-4
                  ${isToday 
                    ? 'bg-yellow-400 bg-opacity-30 border-2 border-yellow-200' 
                    : 'bg-gradient-to-br from-yellow-100 to-orange-100 border-2 border-yellow-400'
                  }
                `}>
                  <div className="flex items-center justify-between mb-2">
                    <div className="flex items-center gap-2">
                      <Sun className={`w-5 h-5 ${isToday ? 'text-yellow-200' : 'text-yellow-600'}`} />
                      <span className={`font-bold ${isToday ? 'text-white' : 'text-gray-800'}`}>
                        Radiación Solar
                      </span>
                    </div>
                    <Zap className={`w-5 h-5 ${isToday ? 'text-yellow-200' : 'text-orange-500'}`} />
                  </div>
                  <p className={`text-3xl font-bold ${isToday ? 'text-white' : 'text-orange-600'}`}>
                    {day.solar_radiation_kwh_m2}
                  </p>
                  <p className={`text-sm ${isToday ? 'text-yellow-100' : 'text-gray-600'}`}>
                    kWh/m² por día
                  </p>
                  <div className={`mt-3 pt-3 border-t ${isToday ? 'border-yellow-300' : 'border-yellow-400'}`}>
                    <p className={`text-xs ${isToday ? 'text-yellow-100' : 'text-gray-600'} mb-1`}>
                      Producción estimada:
                    </p>
                    <p className={`text-2xl font-bold ${isToday ? 'text-white' : 'text-green-600'}`}>
                      {(day.estimated_solar_wh_per_kw / 1000).toFixed(2)} kWh
                    </p>
                    <p className={`text-xs ${isToday ? 'text-yellow-100' : 'text-gray-500'}`}>
                      por kW de paneles
                    </p>
                  </div>
                </div>

                {/* Detalles adicionales */}
                <div className="space-y-2">
                  <div className={`flex items-center justify-between p-2 rounded ${isToday ? 'bg-white bg-opacity-20' : 'bg-gray-50'}`}>
                    <span className={`flex items-center text-sm ${isToday ? 'text-white' : 'text-gray-700'}`}>
                      <Cloud className="w-4 h-4 mr-2" />
                      Nubes
                    </span>
                    <span className={`font-bold ${isToday ? 'text-white' : 'text-gray-900'}`}>
                      {day.clouds_percent}%
                    </span>
                  </div>
                  <div className={`flex items-center justify-between p-2 rounded ${isToday ? 'bg-white bg-opacity-20' : 'bg-gray-50'}`}>
                    <span className={`flex items-center text-sm ${isToday ? 'text-white' : 'text-gray-700'}`}>
                      <Wind className="w-4 h-4 mr-2" />
                      Viento
                    </span>
                    <span className={`font-bold ${isToday ? 'text-white' : 'text-gray-900'}`}>
                      {day.wind_speed} m/s
                    </span>
                  </div>
                  <div className={`flex items-center justify-between p-2 rounded ${isToday ? 'bg-white bg-opacity-20' : 'bg-gray-50'}`}>
                    <span className={`flex items-center text-sm ${isToday ? 'text-white' : 'text-gray-700'}`}>
                      <Droplets className="w-4 h-4 mr-2" />
                      Humedad
                    </span>
                    <span className={`font-bold ${isToday ? 'text-white' : 'text-gray-900'}`}>
                      {day.humidity}%
                    </span>
                  </div>
                  {day.rain_mm > 0 && (
                    <div className={`flex items-center justify-between p-2 rounded ${isToday ? 'bg-blue-500 bg-opacity-30' : 'bg-blue-50'}`}>
                      <span className={`flex items-center text-sm ${isToday ? 'text-white' : 'text-blue-700'}`}>
                        <CloudRain className="w-4 h-4 mr-2" />
                        Lluvia
                      </span>
                      <span className={`font-bold ${isToday ? 'text-white' : 'text-blue-900'}`}>
                        {day.rain_mm} mm
                      </span>
                    </div>
                  )}
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Nota informativa */}
      <div className="bg-blue-50 border-l-4 border-blue-500 p-6 rounded-lg">
        <p className="text-sm text-gray-700">
          <strong>💡 Nota:</strong> La producción solar estimada considera un sistema de 1kW con eficiencia del 17%, 
          orientación óptima y condiciones meteorológicas previstas. Los valores reales pueden variar según la 
          instalación específica, sombras y temperatura de los paneles.
        </p>
      </div>
    </div>
  );
};

export default WeatherForecastSimple;
