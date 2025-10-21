import React from 'react';
import { Globe, Brain, Activity } from 'lucide-react';

const DataSourceBadge = ({ source, details }) => {
  const getSourceConfig = () => {
    switch (source) {
      case 'api':
        return {
          icon: Globe,
          label: 'API Real',
          color: 'bg-blue-100 text-blue-700 border-blue-300',
          tooltip: 'Datos obtenidos de OpenWeather API en tiempo real'
        };
      case 'ia':
        return {
          icon: Brain,
          label: 'IA/ML',
          color: 'bg-purple-100 text-purple-700 border-purple-300',
          tooltip: 'Procesado por Inteligencia Artificial'
        };
      case 'simulado':
        return {
          icon: Activity,
          label: 'Simulado',
          color: 'bg-orange-100 text-orange-700 border-orange-300',
          tooltip: 'Datos simulados (sin ESP32 conectado)'
        };
      default:
        return {
          icon: Activity,
          label: 'N/A',
          color: 'bg-gray-100 text-gray-700 border-gray-300',
          tooltip: 'Fuente desconocida'
        };
    }
  };

  const config = getSourceConfig();
  const Icon = config.icon;

  return (
    <div className="inline-flex items-center group relative">
      <span className={`inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium border ${config.color}`}>
        <Icon className="w-3 h-3 mr-1" />
        {config.label}
      </span>
      
      {/* Tooltip */}
      <div className="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 px-3 py-2 bg-gray-900 text-white text-xs rounded-lg opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none whitespace-nowrap z-50">
        <div className="font-bold mb-1">{config.tooltip}</div>
        {details && <div className="text-gray-300">{details}</div>}
        <div className="absolute top-full left-1/2 transform -translate-x-1/2 -mt-1">
          <div className="border-4 border-transparent border-t-gray-900"></div>
        </div>
      </div>
    </div>
  );
};

export default DataSourceBadge;
