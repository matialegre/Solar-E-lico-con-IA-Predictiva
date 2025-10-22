import React, { useState, useEffect } from 'react';
import { Brain, Calendar, Battery, AlertTriangle, CheckCircle, Wind, CloudRain, Sun, TrendingUp } from 'lucide-react';
import api from '../api/api';
import DataSourceBadge from './DataSourceBadge';

const SmartStrategy = () => {
  const [strategy, setStrategy] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadStrategy();
    const interval = setInterval(loadStrategy, 60000); // Actualizar cada minuto
    return () => clearInterval(interval);
  }, []);

  const loadStrategy = async () => {
    try {
      const response = await api.get('/api/strategy/smart');
      setStrategy(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Error loading strategy:', error);
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="card animate-pulse">
        <div className="h-64 bg-gray-200 rounded"></div>
      </div>
    );
  }

  if (!strategy || strategy.status === 'error') {
    return (
      <div className="card bg-red-50 border-l-4 border-red-500">
        <p className="text-red-800">Error cargando estrategia inteligente</p>
      </div>
    );
  }

  const { analisis, estrategia, urgencia } = strategy;

  const getUrgenciaColor = (nivel) => {
    switch (nivel) {
      case 'CRÍTICA': return 'from-red-600 to-orange-600';
      case 'ALTA': return 'from-orange-500 to-yellow-500';
      default: return 'from-green-500 to-emerald-600';
    }
  };

  const getUrgenciaIcon = (nivel) => {
    switch (nivel) {
      case 'CRÍTICA': return <AlertTriangle className="w-8 h-8 animate-pulse" />;
      case 'ALTA': return <AlertTriangle className="w-8 h-8" />;
      default: return <CheckCircle className="w-8 h-8" />;
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className={`bg-gradient-to-br ${getUrgenciaColor(urgencia)} rounded-2xl shadow-xl p-6 text-white`}>
        <div className="flex items-center justify-between mb-4">
          <div>
            <h2 className="text-3xl font-bold mb-2 flex items-center">
              <Brain className="w-8 h-8 mr-3" />
              Estrategia Inteligente de Carga
            </h2>
            <p className="text-white text-opacity-90">
              Decisiones automáticas basadas en pronóstico del clima
            </p>
          </div>
          <div className="flex flex-col items-end gap-2">
            {getUrgenciaIcon(urgencia)}
            <span className="text-sm font-bold bg-white bg-opacity-20 px-3 py-1 rounded-full">
              {urgencia}
            </span>
            <DataSourceBadge 
              source="api" 
              details="OpenWeather API - Pronóstico 4 días"
            />
          </div>
        </div>
      </div>

      {/* Análisis del Clima */}
      <div className="bg-white rounded-xl shadow-lg p-6">
        <h3 className="text-xl font-bold text-gray-900 mb-4 flex items-center">
          <Calendar className="w-6 h-6 mr-2 text-blue-600" />
          Análisis del Pronóstico
        </h3>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Días sin sol */}
          <div className={`rounded-lg p-6 border-2 ${
            analisis.dias_sin_sol > 0 ? 'bg-red-50 border-red-300' : 'bg-green-50 border-green-300'
          }`}>
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center">
                {analisis.dias_sin_sol > 0 ? (
                  <CloudRain className="w-8 h-8 text-red-600 mr-3" />
                ) : (
                  <Sun className="w-8 h-8 text-green-600 mr-3" />
                )}
                <h4 className="text-lg font-bold text-gray-900">
                  {analisis.dias_sin_sol > 0 ? 'Días Sin Sol' : 'Clima Favorable'}
                </h4>
              </div>
              <span className={`text-4xl font-black ${
                analisis.dias_sin_sol > 0 ? 'text-red-600' : 'text-green-600'
              }`}>
                {analisis.dias_sin_sol}
              </span>
            </div>

            {analisis.detalle_sin_sol && analisis.detalle_sin_sol.length > 0 ? (
              <div className="space-y-2">
                <p className="text-sm font-bold text-gray-700 mb-2">Detalles:</p>
                {analisis.detalle_sin_sol.map((dia, idx) => (
                  <div key={idx} className="bg-white rounded p-3 border border-red-200">
                    <div className="flex items-center justify-between">
                      <span className="font-bold text-gray-900">Día {dia.dia}</span>
                      <span className="text-xs text-gray-600">{dia.fecha}</span>
                    </div>
                    <div className="text-sm text-gray-700 mt-1">
                      {dia.razon === 'lluvia' ? (
                        <span>☔ Lluvia: {dia.lluvia_mm.toFixed(1)} mm</span>
                      ) : (
                        <span>☁️ Nubosidad: {dia.nubosidad}%</span>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-sm text-gray-700">
                ☀️ Buenos días solares adelante. Generación solar normal.
              </p>
            )}
          </div>

          {/* Días con viento */}
          <div className={`rounded-lg p-6 border-2 ${
            analisis.dias_con_viento > 0 ? 'bg-blue-50 border-blue-300' : 'bg-gray-50 border-gray-300'
          }`}>
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center">
                <Wind className="w-8 h-8 text-blue-600 mr-3" />
                <h4 className="text-lg font-bold text-gray-900">
                  Días con Buen Viento
                </h4>
              </div>
              <span className={`text-4xl font-black ${
                analisis.dias_con_viento > 0 ? 'text-blue-600' : 'text-gray-400'
              }`}>
                {analisis.dias_con_viento}
              </span>
            </div>

            {analisis.detalle_viento && analisis.detalle_viento.length > 0 ? (
              <div className="space-y-2">
                <p className="text-sm font-bold text-gray-700 mb-2">Detalles:</p>
                {analisis.detalle_viento.map((dia, idx) => (
                  <div key={idx} className="bg-white rounded p-3 border border-blue-200">
                    <div className="flex items-center justify-between">
                      <span className="font-bold text-gray-900">Día {dia.dia}</span>
                      <span className="text-xs text-gray-600">{dia.fecha}</span>
                    </div>
                    <div className="text-sm text-gray-700 mt-1 flex justify-between">
                      <span>💨 Promedio: {dia.viento_promedio.toFixed(1)} m/s</span>
                      <span>🌪️ Máximo: {dia.viento_maximo.toFixed(1)} m/s</span>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-sm text-gray-700">
                Vientos normales esperados. Generación eólica estándar.
              </p>
            )}
          </div>
        </div>
      </div>

      {/* Decisiones Estratégicas */}
      {estrategia.decisiones && estrategia.decisiones.length > 0 && (
        <div className="bg-gradient-to-br from-purple-50 to-indigo-50 rounded-xl shadow-lg p-6 border-l-4 border-purple-500">
          <h3 className="text-xl font-bold text-purple-900 mb-4 flex items-center">
            <TrendingUp className="w-6 h-6 mr-2" />
            Decisiones Recomendadas
          </h3>

          <div className="space-y-4">
            {estrategia.decisiones.map((decision, idx) => {
              const getPrioridadColor = (prioridad) => {
                switch (prioridad) {
                  case 'CRÍTICA': return 'border-red-500 bg-red-50';
                  case 'ALTA': return 'border-orange-500 bg-orange-50';
                  case 'MEDIA': return 'border-yellow-500 bg-yellow-50';
                  default: return 'border-green-500 bg-green-50';
                }
              };

              return (
                <div key={idx} className={`rounded-lg p-4 border-l-4 ${getPrioridadColor(decision.prioridad)}`}>
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <div className="flex items-center mb-2">
                        <Battery className="w-5 h-5 mr-2 text-purple-700" />
                        <span className="font-bold text-gray-900 uppercase text-sm">
                          {decision.accion.replace(/_/g, ' ')}
                        </span>
                        <span className={`ml-3 px-2 py-1 rounded text-xs font-bold ${
                          decision.prioridad === 'CRÍTICA' ? 'bg-red-600 text-white' :
                          decision.prioridad === 'ALTA' ? 'bg-orange-600 text-white' :
                          decision.prioridad === 'MEDIA' ? 'bg-yellow-600 text-white' :
                          'bg-green-600 text-white'
                        }`}>
                          {decision.prioridad}
                        </span>
                      </div>
                      <p className="text-sm text-gray-700">
                        {decision.razon}
                      </p>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* Recomendaciones */}
      {estrategia.recomendaciones && estrategia.recomendaciones.length > 0 && (
        <div className="bg-white rounded-xl shadow-lg p-6">
          <h3 className="text-xl font-bold text-gray-900 mb-4">
            💡 Recomendaciones de Acción
          </h3>
          <div className="space-y-3">
            {estrategia.recomendaciones.map((rec, idx) => (
              <div key={idx} className="flex items-start bg-gradient-to-r from-blue-50 to-indigo-50 rounded-lg p-4 border-l-4 border-blue-500">
                <span className="text-2xl mr-3">
                  {rec.includes('🚨') ? '🚨' : rec.includes('⚠️') ? '⚠️' : rec.includes('💨') ? '💨' : '💡'}
                </span>
                <p className="text-sm text-gray-800 flex-1">
                  {rec}
                </p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Autonomía Necesaria */}
      {estrategia.autonomia_necesaria_dias > 0 && (
        <div className="bg-gradient-to-r from-yellow-50 to-orange-50 rounded-xl shadow-lg p-6 border-2 border-yellow-400">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-xl font-bold text-gray-900 mb-2">
                🔋 Autonomía Necesaria
              </h3>
              <p className="text-gray-700">
                Necesitas batería cargada para <strong>{estrategia.autonomia_necesaria_dias}</strong> día{estrategia.autonomia_necesaria_dias > 1 ? 's' : ''} sin sol
              </p>
            </div>
            <div className="text-center">
              <span className="text-5xl font-black text-orange-600">
                {estrategia.autonomia_necesaria_dias}
              </span>
              <p className="text-sm text-gray-600 mt-1">días</p>
            </div>
          </div>
        </div>
      )}

      {/* Explicación del Sistema */}
      <div className="bg-gradient-to-br from-gray-50 to-slate-50 rounded-xl shadow-lg p-6 border-l-4 border-gray-500">
        <h3 className="text-xl font-bold text-gray-900 mb-4">
          🤖 ¿Cómo Funciona la Estrategia Inteligente?
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm text-gray-700">
          <div>
            <h4 className="font-bold mb-2">📊 Análisis Automático:</h4>
            <ul className="space-y-1 ml-4">
              <li>• Analiza pronóstico 4 días adelante</li>
              <li>• Detecta días con lluvia o nubes</li>
              <li>• Identifica oportunidades de viento</li>
              <li>• Calcula autonomía necesaria</li>
            </ul>
          </div>
          <div>
            <h4 className="font-bold mb-2">⚡ Decisiones Inteligentes:</h4>
            <ul className="space-y-1 ml-4">
              <li>• Aprovechar viento nocturno si mañana llueve</li>
              <li>• Cargar batería antes de días malos</li>
              <li>• Optimizar carga con sol + viento</li>
              <li>• Alertas proactivas de autonomía</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SmartStrategy;
