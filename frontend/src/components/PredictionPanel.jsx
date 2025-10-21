import React from 'react';
import { 
  TrendingUp, 
  Battery, 
  Clock, 
  AlertTriangle,
  CheckCircle2 
} from 'lucide-react';
import DataSourceBadge from './DataSourceBadge';

const PredictionPanel = ({ predictionData, autonomy }) => {
  if (!predictionData) {
    return (
      <div className="card">
        <div className="animate-pulse">
          <div className="h-40 bg-gray-200 rounded"></div>
        </div>
      </div>
    );
  }

  const {
    total_solar_24h_wh = 0,
    total_wind_24h_wh = 0,
    total_consumption_24h_wh = 0,
    energy_deficit_hours = [],
  } = predictionData || {};

  const totalGeneration = Number(total_solar_24h_wh || 0) + Number(total_wind_24h_wh || 0);
  const balance = totalGeneration - Number(total_consumption_24h_wh || 0);
  const balancePercentage = totalGeneration > 0 ? (balance / totalGeneration * 100).toFixed(1) : '0.0';
  
  // Validar autonomy
  const safeAutonomy = autonomy !== null && autonomy !== undefined && !isNaN(autonomy) && isFinite(autonomy) 
    ? Number(autonomy) 
    : 0;

  return (
    <div className="space-y-6">
      {/* Resumen de Predicción 24h */}
      <div className="card bg-gradient-to-br from-purple-50 to-blue-50">
        <div className="flex items-center justify-between mb-4">
          <h3 className="card-title flex items-center mb-0">
            <TrendingUp className="w-5 h-5 mr-2" />
            Predicción IA - Próximas 24 Horas
          </h3>
          <div className="flex gap-2">
            <DataSourceBadge 
              source="api" 
              details="Pronóstico de OpenWeather API"
            />
            <DataSourceBadge 
              source="ia" 
              details="Análisis y predicción por IA"
            />
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
          <div className="p-4 bg-white rounded-lg shadow-sm">
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm font-medium text-gray-600">Generación Total</span>
              <span className="text-green-600">
                <TrendingUp className="w-4 h-4" />
              </span>
            </div>
            <p className="text-2xl font-bold text-gray-900">
              {(totalGeneration / 1000).toFixed(1)} kWh
            </p>
            <div className="flex items-center mt-2 space-x-2 text-xs">
              <span className="text-yellow-600">☀️ {(total_solar_24h_wh / 1000).toFixed(1)} kWh</span>
              <span className="text-blue-600">🌬️ {(total_wind_24h_wh / 1000).toFixed(1)} kWh</span>
            </div>
          </div>

          <div className="p-4 bg-white rounded-lg shadow-sm">
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm font-medium text-gray-600">Consumo Previsto</span>
              <span className="text-orange-600">
                <Battery className="w-4 h-4" />
              </span>
            </div>
            <p className="text-2xl font-bold text-gray-900">
              {(total_consumption_24h_wh / 1000).toFixed(1)} kWh
            </p>
            <p className="text-xs text-gray-500 mt-2">
              Promedio: {(total_consumption_24h_wh / 24).toFixed(0)} W/h
            </p>
          </div>

          <div className="p-4 bg-white rounded-lg shadow-sm">
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm font-medium text-gray-600">Balance Energético</span>
              <span className={balance > 0 ? 'text-green-600' : 'text-red-600'}>
                {balance > 0 ? <CheckCircle2 className="w-4 h-4" /> : <AlertTriangle className="w-4 h-4" />}
              </span>
            </div>
            <p className={`text-2xl font-bold ${balance > 0 ? 'text-green-600' : 'text-red-600'}`}>
              {balance > 0 ? '+' : ''}{(balance / 1000).toFixed(1)} kWh
            </p>
            <p className="text-xs text-gray-500 mt-2">
              {balance > 0 ? 'Excedente' : 'Déficit'} ({balancePercentage}%)
            </p>
          </div>
        </div>

        {/* Alertas de Déficit */}
        {energy_deficit_hours.length > 0 && (
          <div className="p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
            <div className="flex items-start">
              <AlertTriangle className="w-5 h-5 text-yellow-600 mt-0.5 mr-3" />
              <div>
                <h4 className="font-semibold text-yellow-900">
                  Déficit Energético Previsto
                </h4>
                <p className="text-sm text-yellow-800 mt-1">
                  Se prevé déficit energético en {energy_deficit_hours.length} horas de las próximas 24h.
                </p>
                <p className="text-xs text-yellow-700 mt-2">
                  💡 Considere reducir el consumo no esencial o activar fuentes de respaldo.
                </p>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Autonomía */}
      <div className="card">
        <h3 className="card-title flex items-center">
          <Clock className="w-5 h-5 mr-2" />
          Autonomía de Batería
        </h3>

        <div className="flex items-center justify-between p-6 bg-gradient-to-r from-green-50 to-emerald-50 rounded-lg border border-green-200">
          <div>
            <p className="text-sm font-medium text-gray-600 mb-1">
              Tiempo restante con consumo actual
            </p>
            <p className="text-4xl font-bold text-gray-900">
              {safeAutonomy > 0 && safeAutonomy < 1000
                ? `${safeAutonomy.toFixed(1)} h` 
                : safeAutonomy >= 1000 ? '∞' : '0 h'}
            </p>
            <p className="text-xs text-gray-500 mt-2">
              {safeAutonomy > 24 
                ? 'Más de un día de autonomía'
                : safeAutonomy > 12
                ? 'Autonomía suficiente'
                : safeAutonomy > 4
                ? 'Autonomía moderada'
                : 'Autonomía baja'}
            </p>
          </div>
          <div className="relative">
            <svg className="w-24 h-24" viewBox="0 0 100 100">
              <circle
                cx="50"
                cy="50"
                r="40"
                fill="none"
                stroke="#e5e7eb"
                strokeWidth="8"
              />
              <circle
                cx="50"
                cy="50"
                r="40"
                fill="none"
                stroke={safeAutonomy > 12 ? '#10b981' : safeAutonomy > 4 ? '#f59e0b' : '#ef4444'}
                strokeWidth="8"
                strokeDasharray={`${Math.min((safeAutonomy / 24) * 251, 251)} 251`}
                strokeLinecap="round"
                transform="rotate(-90 50 50)"
              />
              <text
                x="50"
                y="50"
                textAnchor="middle"
                dy="0.3em"
                className="text-xl font-bold"
                fill={safeAutonomy > 12 ? '#10b981' : safeAutonomy > 4 ? '#f59e0b' : '#ef4444'}
              >
                {safeAutonomy > 0 && safeAutonomy < 100 ? Math.round(safeAutonomy) : safeAutonomy >= 100 ? '∞' : '0'}
              </text>
            </svg>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PredictionPanel;
