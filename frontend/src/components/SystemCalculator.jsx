import React, { useState, useEffect } from 'react';
import { Sun, Wind, Battery, Zap, TrendingUp, MapPin, Award, AlertCircle } from 'lucide-react';
import api from '../api/api';

const SystemCalculator = () => {
  const [calc, setCalc] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadCalculations();
  }, []);

  const loadCalculations = async () => {
    try {
      const response = await api.get('/api/system/calculate');
      setCalc(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Error loading system calculations:', error);
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="card">
        <div className="animate-pulse h-64">
          <div className="h-6 bg-gray-200 rounded mb-4 w-1/3"></div>
          <div className="h-4 bg-gray-200 rounded mb-2"></div>
          <div className="h-4 bg-gray-200 rounded mb-2 w-5/6"></div>
        </div>
      </div>
    );
  }

  if (!calc) return null;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-gradient-to-br from-indigo-600 via-purple-600 to-pink-600 rounded-2xl shadow-xl p-6 text-white">
        <h2 className="text-3xl font-bold mb-2 flex items-center">
          <Zap className="w-8 h-8 mr-3" />
          Dimensionamiento del Sistema
        </h2>
        <p className="text-sm opacity-90">
          Cálculo personalizado basado en tu consumo y ubicación geográfica
        </p>
      </div>

      {/* Consumo Actual */}
      <div className="bg-white rounded-xl shadow-lg p-6 border-l-4 border-orange-500">
        <h3 className="text-xl font-bold text-gray-900 mb-4 flex items-center">
          <TrendingUp className="w-6 h-6 mr-2 text-orange-500" />
          Tu Consumo
        </h3>
        <div className="grid grid-cols-3 gap-4">
          <div className="text-center">
            <p className="text-sm text-gray-600 mb-1">Potencia Promedio</p>
            <p className="text-3xl font-bold text-gray-900">{calc.consumption.average_power_w}</p>
            <p className="text-xs text-gray-500">Watts</p>
          </div>
          <div className="text-center">
            <p className="text-sm text-gray-600 mb-1">Consumo Diario</p>
            <p className="text-3xl font-bold text-gray-900">{(calc.consumption.daily_consumption_wh / 1000).toFixed(1)}</p>
            <p className="text-xs text-gray-500">kWh/día</p>
          </div>
          <div className="text-center">
            <p className="text-sm text-gray-600 mb-1">Consumo Mensual</p>
            <p className="text-3xl font-bold text-gray-900">{calc.consumption.monthly_consumption_kwh}</p>
            <p className="text-xs text-gray-500">kWh/mes</p>
          </div>
        </div>
      </div>

      {/* Requerimientos */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Solar */}
        <div className="bg-gradient-to-br from-yellow-50 to-orange-50 rounded-xl shadow-lg p-6 border-2 border-yellow-400">
          <h3 className="text-xl font-bold text-gray-900 mb-4 flex items-center">
            <Sun className="w-6 h-6 mr-2 text-yellow-600" />
            Sistema Solar Recomendado
          </h3>
          <div className="space-y-4">
            <div className="flex justify-between items-center p-3 bg-white rounded-lg">
              <span className="text-sm font-medium text-gray-700">Paneles necesarios</span>
              <span className="text-2xl font-bold text-yellow-600">{calc.solar.panels_needed}</span>
            </div>
            <div className="flex justify-between items-center p-3 bg-white rounded-lg">
              <span className="text-sm font-medium text-gray-700">Potencia por panel</span>
              <span className="text-lg font-bold text-gray-900">{calc.solar.panel_wattage_w} W</span>
            </div>
            <div className="flex justify-between items-center p-3 bg-yellow-100 rounded-lg">
              <span className="text-sm font-bold text-gray-800">Capacidad Total</span>
              <span className="text-2xl font-black text-yellow-700">{calc.solar.total_capacity_w} W</span>
            </div>
            <div className="border-t pt-3">
              <p className="text-xs text-gray-600 mb-2">Generación diaria estimada:</p>
              <p className="text-3xl font-black text-green-600">{calc.solar.daily_generation_kwh} kWh</p>
              <p className="text-sm text-gray-600 mt-1">
                Cubre el <strong>{calc.solar.coverage_percent}%</strong> del consumo
              </p>
            </div>
          </div>
        </div>

        {/* Eólica */}
        <div className="bg-gradient-to-br from-blue-50 to-cyan-50 rounded-xl shadow-lg p-6 border-2 border-blue-400">
          <h3 className="text-xl font-bold text-gray-900 mb-4 flex items-center">
            <Wind className="w-6 h-6 mr-2 text-blue-600" />
            Sistema Eólico Recomendado
          </h3>
          <div className="space-y-4">
            <div className="flex justify-between items-center p-3 bg-white rounded-lg">
              <span className="text-sm font-medium text-gray-700">Turbinas necesarias</span>
              <span className="text-2xl font-bold text-blue-600">{calc.wind.turbines_needed}</span>
            </div>
            <div className="flex justify-between items-center p-3 bg-white rounded-lg">
              <span className="text-sm font-medium text-gray-700">Potencia por turbina</span>
              <span className="text-lg font-bold text-gray-900">{calc.wind.turbine_wattage_w} W</span>
            </div>
            <div className="flex justify-between items-center p-3 bg-blue-100 rounded-lg">
              <span className="text-sm font-bold text-gray-800">Capacidad Total</span>
              <span className="text-2xl font-black text-blue-700">{calc.wind.total_capacity_w} W</span>
            </div>
            <div className="border-t pt-3">
              <p className="text-xs text-gray-600 mb-2">Generación diaria estimada:</p>
              <p className="text-3xl font-black text-green-600">{calc.wind.daily_generation_kwh} kWh</p>
              <p className="text-sm text-gray-600 mt-1">
                Cubre el <strong>{calc.wind.coverage_percent}%</strong> del consumo
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Batería */}
      <div className="bg-white rounded-xl shadow-lg p-6 border-l-4 border-green-500">
        <h3 className="text-xl font-bold text-gray-900 mb-4 flex items-center">
          <Battery className="w-6 h-6 mr-2 text-green-600" />
          Sistema de Almacenamiento
        </h3>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="text-center p-3 bg-gray-50 rounded-lg">
            <p className="text-xs text-gray-600 mb-1">Capacidad Actual</p>
            <p className="text-2xl font-bold text-gray-900">{(calc.battery.current_capacity_wh / 1000).toFixed(1)}</p>
            <p className="text-xs text-gray-500">kWh</p>
          </div>
          <div className="text-center p-3 bg-green-100 rounded-lg">
            <p className="text-xs text-gray-600 mb-1">Recomendada</p>
            <p className="text-2xl font-bold text-green-700">{calc.battery.recommended_capacity_kwh}</p>
            <p className="text-xs text-gray-500">kWh</p>
          </div>
          <div className="text-center p-3 bg-gray-50 rounded-lg">
            <p className="text-xs text-gray-600 mb-1">Voltaje</p>
            <p className="text-2xl font-bold text-gray-900">{calc.battery.system_voltage_v}</p>
            <p className="text-xs text-gray-500">V</p>
          </div>
          <div className="text-center p-3 bg-gray-50 rounded-lg">
            <p className="text-xs text-gray-600 mb-1">Autonomía</p>
            <p className="text-2xl font-bold text-gray-900">{calc.battery.autonomy_days}</p>
            <p className="text-xs text-gray-500">días</p>
          </div>
        </div>
        {calc.battery.needs_upgrade && (
          <div className="mt-4 bg-yellow-50 border border-yellow-300 rounded-lg p-3 flex items-center">
            <AlertCircle className="w-5 h-5 text-yellow-600 mr-2" />
            <p className="text-sm text-yellow-800">
              Se recomienda ampliar la capacidad de batería a <strong>{calc.battery.recommended_capacity_kwh} kWh</strong> para mayor autonomía
            </p>
          </div>
        )}
      </div>

      {/* Resumen de Generación */}
      <div className="bg-gradient-to-br from-green-500 to-emerald-600 rounded-xl shadow-lg p-6 text-white">
        <h3 className="text-2xl font-bold mb-4 flex items-center">
          <Award className="w-8 h-8 mr-3" />
          Balance Energético
        </h3>
        <div className="grid grid-cols-2 md:grid-cols-3 gap-6">
          <div>
            <p className="text-sm opacity-90 mb-1">Generación Total Diaria</p>
            <p className="text-4xl font-black">{calc.generation.total_daily_kwh} kWh</p>
            <p className="text-xs opacity-75 mt-1">
              {calc.generation.solar_percent}% Solar + {calc.generation.wind_percent}% Eólica
            </p>
          </div>
          <div>
            <p className="text-sm opacity-90 mb-1">Balance Energético</p>
            <p className={`text-4xl font-black ${calc.generation.balance_wh >= 0 ? '' : 'text-red-300'}`}>
              {calc.generation.balance_percent > 0 ? '+' : ''}{calc.generation.balance_percent}%
            </p>
            <p className="text-xs opacity-75 mt-1">
              {calc.generation.is_sufficient ? '✅ Sistema suficiente' : '⚠️ Aumentar capacidad'}
            </p>
          </div>
          <div>
            <p className="text-sm opacity-90 mb-1">Excedente/Déficit</p>
            <p className={`text-3xl font-bold ${calc.generation.balance_wh >= 0 ? '' : 'text-red-300'}`}>
              {(calc.generation.balance_wh / 1000).toFixed(2)} kWh
            </p>
            <p className="text-xs opacity-75 mt-1">Por día</p>
          </div>
        </div>
      </div>

      {/* Optimización por Ubicación */}
      <div className="bg-white rounded-xl shadow-lg p-6 border-l-4 border-purple-500">
        <h3 className="text-xl font-bold text-gray-900 mb-4 flex items-center">
          <MapPin className="w-6 h-6 mr-2 text-purple-600" />
          Optimización para tu Ubicación
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <p className="text-sm text-gray-600 mb-3">
              📍 Latitud: <strong>{calc.location.latitude.toFixed(4)}°</strong> ({calc.optimization.hemisphere})
            </p>
            <p className="text-sm text-gray-600 mb-3">
              🌍 Zona climática: <strong className="capitalize">{calc.optimization.latitude_zone}</strong>
            </p>
            <p className="text-sm text-gray-600 mb-3">
              📐 Ángulo óptimo paneles: <strong>{calc.optimization.optimal_panel_angle_degrees}°</strong>
            </p>
          </div>
          <div>
            <div className="bg-purple-50 rounded-lg p-4">
              <p className="text-sm text-gray-700 mb-2">
                ☀️ Potencial solar: <strong className="text-yellow-600 capitalize">{calc.optimization.solar_potential_rating}</strong>
              </p>
              <p className="text-sm text-gray-700 mb-3">
                💨 Potencial eólico: <strong className="text-blue-600 capitalize">{calc.optimization.wind_potential_rating}</strong>
              </p>
              <p className="text-sm font-bold text-purple-800 bg-purple-100 rounded p-2">
                ✨ {calc.optimization.recommendation_text}
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SystemCalculator;
