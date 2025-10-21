import React from 'react';
import { 
  Sun, 
  Wind, 
  Battery, 
  Zap, 
  TrendingUp,
  Activity,
  TrendingDown
} from 'lucide-react';
import DataSourceBadge from './DataSourceBadge';

const MetricCard = ({ icon: Icon, label, value, unit, color, subValue, trend }) => {
  return (
    <div className="metric-card">
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <div className={`p-3 rounded-lg bg-${color}-100`}>
            <Icon className={`w-6 h-6 text-${color}-600`} />
          </div>
          <div>
            <p className="metric-label">{label}</p>
            <div className="flex items-baseline">
              <span className="metric-value">{value}</span>
              <span className="metric-unit">{unit}</span>
            </div>
            {subValue && (
              <p className="text-xs text-gray-500 mt-1">{subValue}</p>
            )}
          </div>
        </div>
        {trend && (
          <div className={`flex items-center text-${trend > 0 ? 'green' : 'red'}-600`}>
            <TrendingUp className={`w-4 h-4 ${trend < 0 ? 'transform rotate-180' : ''}`} />
            <span className="text-sm font-medium ml-1">{Math.abs(trend)}%</span>
          </div>
        )}
      </div>
    </div>
  );
};

const EnergyMetrics = ({ energyData }) => {
  if (!energyData) {
    return (
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div className="metric-card animate-pulse">
          <div className="h-20 bg-gray-200 rounded"></div>
        </div>
      </div>
    );
  }

  const {
    solar_power_w = 0,
    wind_power_w = 0,
    total_generation_w = 0,
    battery_soc_percent = 0,
    battery_power_w = 0,
    load_power_w = 0,
  } = energyData;

  return (
    <div>
      {/* Header con indicador de fuente */}
      <div className="bg-orange-50 border-l-4 border-orange-400 p-3 rounded-lg mb-4 flex items-center justify-between">
        <div className="flex items-center">
          <span className="text-sm font-medium text-orange-900 mr-2">Datos de Generación y Batería:</span>
          <DataSourceBadge 
            source="simulado" 
            details="Datos simulados - Conecta ESP32 con sensores para datos reales"
          />
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <MetricCard
          icon={Sun}
          label="Generación Solar"
          value={Math.round(solar_power_w)}
          unit="W"
          color="yellow"
          subValue={`${((solar_power_w / 3000) * 100).toFixed(1)}% de capacidad`}
        />
      
      <MetricCard
        icon={Wind}
        label="Generación Eólica"
        value={Math.round(wind_power_w)}
        unit="W"
        color="blue"
        subValue={`${((wind_power_w / 2000) * 100).toFixed(1)}% de capacidad`}
      />
      
      <MetricCard
        icon={Battery}
        label="Batería"
        value={battery_soc_percent.toFixed(1)}
        unit="%"
        color={battery_soc_percent > 50 ? 'green' : battery_soc_percent > 20 ? 'yellow' : 'red'}
        subValue={`${battery_power_w > 0 ? 'Cargando' : 'Descargando'} (${Math.abs(battery_power_w).toFixed(0)}W)`}
      />
      
      <MetricCard
        icon={Activity}
        label="Generación Total"
        value={Math.round(total_generation_w)}
        unit="W"
        color="green"
        subValue="Solar + Eólica"
      />
      
      <MetricCard
        icon={Zap}
        label="Consumo Actual"
        subValue={`${Math.round(load_power_w)} W consumo`}
        color="orange"
      />
      
      <MetricCard
        icon={TrendingUp}
        label="Balance Energético"
        value={Math.round(total_generation_w - load_power_w)}
        unit="W"
        color={total_generation_w - load_power_w > 0 ? 'green' : 'red'}
        subValue={total_generation_w - load_power_w > 0 ? 'Excedente' : 'Déficit'}
      />
      </div>
    </div>
  );
};

export default EnergyMetrics;
