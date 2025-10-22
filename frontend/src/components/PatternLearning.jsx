import React, { useState, useEffect } from 'react';
import { Brain, TrendingUp, Clock, Zap, AlertTriangle, CheckCircle, Battery } from 'lucide-react';
import api from '../api/api';

const PatternLearning = () => {
  const [patterns, setPatterns] = useState(null);
  const [predictions, setPredictions] = useState(null);
  const [recommendation, setRecommendation] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadAll();
    const interval = setInterval(loadAll, 60000); // Actualizar cada minuto
    return () => clearInterval(interval);
  }, []);

  const loadAll = async () => {
    try {
      const [patternsRes, predictionsRes, recommendationRes] = await Promise.all([
        api.get('/api/patterns/analyze'),
        api.get('/api/patterns/predict?hours=6'),
        api.get('/api/patterns/battery-recommendation')
      ]);
      
      setPatterns(patternsRes.data);
      setPredictions(predictionsRes.data);
      setRecommendation(recommendationRes.data);
      setLoading(false);
    } catch (error) {
      console.error('Error loading patterns:', error);
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="card">
        <div className="animate-pulse h-64"></div>
      </div>
    );
  }

  if (!patterns || patterns.status === 'disabled') {
    return (
      <div className="card bg-yellow-50 border-l-4 border-yellow-500">
        <p className="text-yellow-800">
          ⚠️ El aprendizaje de patrones está deshabilitado. Habilita ENABLE_PATTERN_LEARNING en el backend.
        </p>
      </div>
    );
  }

  if (patterns.status === 'insufficient_data') {
    return (
      <div className="card bg-blue-50 border-l-4 border-blue-500">
        <h3 className="text-xl font-bold text-blue-900 mb-2 flex items-center">
          <Brain className="w-6 h-6 mr-2" />
          Sistema de Aprendizaje Inteligente
        </h3>
        <p className="text-blue-800">
          🤖 Recopilando datos... Se necesitan al menos 24 horas de operación para detectar patrones.
        </p>
        <p className="text-sm text-blue-600 mt-2">
          Registros actuales: <strong>{patterns.records}</strong>
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-gradient-to-br from-purple-600 via-pink-600 to-red-600 rounded-2xl shadow-xl p-6 text-white">
        <h2 className="text-3xl font-bold mb-2 flex items-center">
          <Brain className="w-8 h-8 mr-3" />
          Sistema de Aprendizaje Inteligente
        </h2>
        <p className="text-sm opacity-90">
          Analizando {patterns.days_analyzed.toFixed(0)} días de operación • {patterns.records} registros
        </p>
      </div>

      {/* Recomendación de Carga de Batería */}
      {recommendation && recommendation.status === 'success' && (
        <div className={`rounded-xl shadow-lg p-6 ${
          recommendation.should_charge_now 
            ? 'bg-gradient-to-br from-green-500 to-emerald-600 text-white' 
            : 'bg-white border-2 border-gray-300'
        }`}>
          <h3 className={`text-2xl font-bold mb-3 flex items-center ${recommendation.should_charge_now ? '' : 'text-gray-900'}`}>
            <Battery className="w-7 h-7 mr-2" />
            Recomendación de Carga
          </h3>
          <p className={`text-lg font-semibold mb-4 ${recommendation.should_charge_now ? '' : 'text-gray-800'}`}>
            {recommendation.recommendation}
          </p>
          <div className="grid grid-cols-3 gap-4">
            <div className={`p-3 rounded-lg ${recommendation.should_charge_now ? 'bg-white bg-opacity-20' : 'bg-gray-100'}`}>
              <p className={`text-xs mb-1 ${recommendation.should_charge_now ? 'text-green-100' : 'text-gray-600'}`}>Hora Actual</p>
              <p className={`text-2xl font-bold ${recommendation.should_charge_now ? '' : 'text-gray-900'}`}>{recommendation.current_hour}:00</p>
            </div>
            <div className={`p-3 rounded-lg ${recommendation.should_charge_now ? 'bg-white bg-opacity-20' : 'bg-gray-100'}`}>
              <p className={`text-xs mb-1 ${recommendation.should_charge_now ? 'text-green-100' : 'text-gray-600'}`}>Próximo Pico</p>
              <p className={`text-2xl font-bold ${recommendation.should_charge_now ? '' : 'text-gray-900'}`}>{recommendation.next_peak_hour}:00</p>
            </div>
            <div className={`p-3 rounded-lg ${recommendation.should_charge_now ? 'bg-white bg-opacity-20' : 'bg-gray-100'}`}>
              <p className={`text-xs mb-1 ${recommendation.should_charge_now ? 'text-green-100' : 'text-gray-600'}`}>Tiempo al Pico</p>
              <p className={`text-2xl font-bold ${recommendation.should_charge_now ? '' : 'text-gray-900'}`}>{recommendation.hours_to_peak}h</p>
            </div>
          </div>
        </div>
      )}

      {/* Predicciones */}
      {predictions && predictions.status === 'success' && (
        <div className="bg-white rounded-xl shadow-lg p-6">
          <h3 className="text-xl font-bold text-gray-900 mb-4 flex items-center">
            <TrendingUp className="w-6 h-6 mr-2 text-indigo-600" />
            Predicción de Consumo (Próximas {predictions.hours_ahead} horas)
          </h3>
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
            {predictions.predictions.map((pred, index) => (
              <div 
                key={index}
                className={`p-4 rounded-lg text-center ${
                  pred.confidence > 70 
                    ? 'bg-gradient-to-br from-indigo-500 to-purple-600 text-white' 
                    : 'bg-gray-100'
                }`}
              >
                <p className={`text-xs mb-1 ${pred.confidence > 70 ? 'text-indigo-100' : 'text-gray-600'}`}>
                  {pred.hour}:00
                </p>
                <p className={`text-2xl font-bold ${pred.confidence > 70 ? '' : 'text-gray-900'}`}>
                  {pred.predicted_power_w}
                </p>
                <p className={`text-xs ${pred.confidence > 70 ? 'text-indigo-100' : 'text-gray-500'}`}>
                  Watts
                </p>
                <p className={`text-xs mt-1 truncate ${pred.confidence > 70 ? 'text-indigo-200' : 'text-gray-600'}`}>
                  {pred.device}
                </p>
                {pred.confidence > 0 && (
                  <p className={`text-xs mt-1 ${pred.confidence > 70 ? 'text-green-300' : 'text-green-600'}`}>
                    {pred.confidence}% confianza
                  </p>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Patrones por Hora */}
      <div className="bg-white rounded-xl shadow-lg p-6">
        <h3 className="text-xl font-bold text-gray-900 mb-4 flex items-center">
          <Clock className="w-6 h-6 mr-2 text-blue-600" />
          Patrones de Consumo Aprendidos
        </h3>
        <p className="text-sm text-gray-600 mb-4">
          Promedio de consumo de {patterns.avg_power_w} W • Consumo diario: {(patterns.avg_daily_consumption_wh / 1000).toFixed(1)} kWh
        </p>
        
        {/* Gráfico de barras simple */}
        <div className="space-y-2">
          {patterns.patterns.sort((a, b) => a.hour - b.hour).map((pattern) => {
            const maxPower = Math.max(...patterns.patterns.map(p => p.avg_power_w));
            const widthPercent = (pattern.avg_power_w / maxPower) * 100;
            const isPeak = patterns.peak_hours.includes(pattern.hour);
            const isLow = patterns.low_hours.includes(pattern.hour);
            
            return (
              <div key={pattern.hour} className="flex items-center gap-3">
                <div className="w-16 text-sm font-medium text-gray-700">
                  {String(pattern.hour).padStart(2, '0')}:00
                </div>
                <div className="flex-1">
                  <div 
                    className={`h-8 rounded-r-lg flex items-center px-3 text-sm font-bold text-white transition-all ${
                      isPeak 
                        ? 'bg-gradient-to-r from-red-500 to-orange-500' 
                        : isLow 
                          ? 'bg-gradient-to-r from-green-500 to-emerald-500'
                          : 'bg-gradient-to-r from-blue-500 to-indigo-500'
                    }`}
                    style={{ width: `${widthPercent}%` }}
                  >
                    {pattern.avg_power_w.toFixed(0)} W
                  </div>
                </div>
                <div className="w-32 text-xs text-gray-600 truncate">
                  {pattern.identified_device}
                </div>
                {isPeak && (
                  <div className="flex items-center text-xs text-red-600">
                    <AlertTriangle className="w-4 h-4 mr-1" />
                    Pico
                  </div>
                )}
                {isLow && (
                  <div className="flex items-center text-xs text-green-600">
                    <CheckCircle className="w-4 h-4 mr-1" />
                    Valle
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </div>

      {/* Dispositivos Identificados */}
      <div className="bg-gradient-to-br from-gray-50 to-blue-50 rounded-xl shadow-lg p-6 border border-gray-200">
        <h3 className="text-xl font-bold text-gray-900 mb-4 flex items-center">
          <Zap className="w-6 h-6 mr-2 text-yellow-600" />
          Electrodomésticos Detectados
        </h3>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {[...new Set(patterns.patterns.map(p => p.identified_device))].map(device => {
            const devicePatterns = patterns.patterns.filter(p => p.identified_device === device);
            const avgPower = devicePatterns.reduce((sum, p) => sum + p.avg_power_w, 0) / devicePatterns.length;
            const totalHours = devicePatterns.length;
            
            return (
              <div key={device} className="bg-white rounded-lg p-4 shadow">
                <p className="text-sm font-bold text-gray-800 mb-2 capitalize truncate">
                  {device.replace(/_/g, ' ')}
                </p>
                <p className="text-2xl font-black text-indigo-600">{avgPower.toFixed(0)} W</p>
                <p className="text-xs text-gray-600 mt-1">
                  Activo {totalHours} horas/día
                </p>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};

export default PatternLearning;
