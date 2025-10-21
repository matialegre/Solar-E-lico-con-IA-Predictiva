import React, { useState, useEffect } from 'react';
import { Activity, Sun, Wind, TrendingDown, TrendingUp, AlertTriangle, CheckCircle, Wrench } from 'lucide-react';
import axios from 'axios';
import DataSourceBadge from './DataSourceBadge';

const EfficiencyMonitor = () => {
  const [efficiency, setEfficiency] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadEfficiency();
    const interval = setInterval(loadEfficiency, 5000); // Actualizar cada 5 segundos
    return () => clearInterval(interval);
  }, []);

  const loadEfficiency = async () => {
    try {
      // Simular datos - en producción vendrían de sensores reales
      const irradiancia = 600 + Math.random() * 400; // 600-1000 W/m²
      const tempAmbiente = 20 + Math.random() * 15; // 20-35°C
      const potenciaSolar = 700 + Math.random() * 400; // 700-1100 W
      const vientoVel = 6 + Math.random() * 6; // 6-12 m/s
      const potenciaEolica = 300 + Math.random() * 400; // 300-700 W

      const response = await axios.get(
        `${process.env.REACT_APP_API_URL}/api/efficiency/dashboard?` +
        `irradiancia_w_m2=${irradiancia}&` +
        `area_paneles_m2=6&` +
        `potencia_solar_w=${potenciaSolar}&` +
        `temperatura_c=${tempAmbiente}&` +
        `velocidad_viento_ms=${vientoVel}&` +
        `potencia_eolica_w=${potenciaEolica}&` +
        `potencia_nominal_turbina_w=1000`
      );
      
      setEfficiency(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Error loading efficiency:', error);
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

  if (!efficiency) return null;

  const { solar, eolica } = efficiency;

  const getEfficiencyColor = (percent) => {
    if (percent >= 85) return 'text-green-600 bg-green-50 border-green-300';
    if (percent >= 75) return 'text-blue-600 bg-blue-50 border-blue-300';
    if (percent >= 60) return 'text-yellow-600 bg-yellow-50 border-yellow-300';
    return 'text-red-600 bg-red-50 border-red-300';
  };

  const getEfficiencyIcon = (percent) => {
    if (percent >= 85) return <CheckCircle className="w-6 h-6" />;
    if (percent >= 60) return <Activity className="w-6 h-6" />;
    return <AlertTriangle className="w-6 h-6" />;
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-gradient-to-br from-indigo-600 to-purple-600 rounded-2xl shadow-xl p-6 text-white">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h2 className="text-3xl font-bold mb-2 flex items-center">
              <Activity className="w-8 h-8 mr-3" />
              Monitor de Eficiencia Real
            </h2>
            <p className="text-indigo-100">
              Detecta problemas automáticamente comparando generación vs teoría
            </p>
          </div>
          <div className="flex gap-2">
            <DataSourceBadge 
              source="simulado" 
              details="Sensores: LDR (irradiancia) + ACS712 (corriente) + DS18B20 (temperatura)"
            />
            <DataSourceBadge 
              source="ia" 
              details="Algoritmos de diagnóstico automático"
            />
          </div>
        </div>
      </div>

      {/* Alertas Activas */}
      {efficiency.alertas_activas && (
        <div className="bg-red-50 border-l-4 border-red-500 rounded-lg p-4">
          <div className="flex items-start">
            <AlertTriangle className="w-6 h-6 text-red-600 mr-3 flex-shrink-0 mt-0.5" />
            <div>
              <h3 className="font-bold text-red-900 mb-2">⚠️ Alertas de Eficiencia</h3>
              <p className="text-sm text-red-800">
                Se detectaron problemas de eficiencia. Revisa las recomendaciones abajo.
              </p>
            </div>
          </div>
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* EFICIENCIA SOLAR */}
        {solar.status === 'success' && (
          <div className={`rounded-xl shadow-lg p-6 border-2 ${getEfficiencyColor(solar.eficiencia_percent)}`}>
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center">
                <Sun className="w-8 h-8 mr-3" />
                <h3 className="text-xl font-bold">Paneles Solares</h3>
              </div>
              {getEfficiencyIcon(solar.eficiencia_percent)}
            </div>

            {/* Eficiencia Principal */}
            <div className="bg-white rounded-lg p-4 mb-4">
              <p className="text-sm text-gray-600 mb-1">Eficiencia Actual</p>
              <div className="flex items-baseline">
                <span className="text-5xl font-black">{solar.eficiencia_percent}%</span>
                <span className="ml-3 text-lg font-medium text-gray-600">
                  {solar.nivel}
                </span>
              </div>
              
              {/* Barra de progreso */}
              <div className="mt-3 h-3 bg-gray-200 rounded-full overflow-hidden">
                <div 
                  className={`h-full transition-all duration-500 ${
                    solar.eficiencia_percent >= 85 ? 'bg-green-500' :
                    solar.eficiencia_percent >= 75 ? 'bg-blue-500' :
                    solar.eficiencia_percent >= 60 ? 'bg-yellow-500' : 'bg-red-500'
                  }`}
                  style={{ width: `${Math.min(solar.eficiencia_percent, 100)}%` }}
                ></div>
              </div>
            </div>

            {/* Diagnóstico */}
            <div className={`rounded-lg p-3 mb-4 ${
              solar.alerta ? 'bg-red-100 border border-red-300' : 'bg-green-100 border border-green-300'
            }`}>
              <p className="text-sm font-bold mb-1">Diagnóstico:</p>
              <p className="text-sm">{solar.diagnostico}</p>
            </div>

            {/* Mediciones */}
            <div className="bg-white rounded-lg p-4 mb-4">
              <p className="text-xs font-bold text-gray-700 mb-2">📊 Mediciones:</p>
              <div className="grid grid-cols-2 gap-2 text-xs">
                <div>
                  <span className="text-gray-600">Irradiancia:</span>
                  <p className="font-bold">{solar.mediciones.irradiancia_w_m2} W/m²</p>
                </div>
                <div>
                  <span className="text-gray-600">Temperatura:</span>
                  <p className="font-bold">{solar.mediciones.temperatura_c}°C</p>
                </div>
                <div>
                  <span className="text-gray-600">Potencia Teórica:</span>
                  <p className="font-bold">{solar.mediciones.potencia_teorica_w} W</p>
                </div>
                <div>
                  <span className="text-gray-600">Potencia Real:</span>
                  <p className="font-bold">{solar.mediciones.potencia_real_w} W</p>
                </div>
                <div className="col-span-2">
                  <span className="text-gray-600">Pérdida:</span>
                  <p className="font-bold text-red-600">{solar.mediciones.perdida_w} W</p>
                </div>
              </div>
            </div>

            {/* Recomendaciones */}
            {solar.recomendaciones && solar.recomendaciones.length > 0 && (
              <div className="bg-blue-50 rounded-lg p-3 border border-blue-200">
                <p className="text-xs font-bold text-blue-900 mb-2 flex items-center">
                  <Wrench className="w-4 h-4 mr-1" />
                  Recomendaciones:
                </p>
                <ul className="space-y-1">
                  {solar.recomendaciones.map((rec, idx) => (
                    <li key={idx} className="text-xs text-blue-800">• {rec}</li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        )}

        {/* EFICIENCIA EÓLICA */}
        {eolica.status === 'success' && (
          <div className={`rounded-xl shadow-lg p-6 border-2 ${getEfficiencyColor(eolica.eficiencia_percent)}`}>
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center">
                <Wind className="w-8 h-8 mr-3" />
                <h3 className="text-xl font-bold">Turbina Eólica</h3>
              </div>
              {getEfficiencyIcon(eolica.eficiencia_percent)}
            </div>

            {/* Eficiencia Principal */}
            <div className="bg-white rounded-lg p-4 mb-4">
              <p className="text-sm text-gray-600 mb-1">Eficiencia Actual</p>
              <div className="flex items-baseline">
                <span className="text-5xl font-black">{eolica.eficiencia_percent}%</span>
                <span className="ml-3 text-lg font-medium text-gray-600">
                  {eolica.nivel}
                </span>
              </div>
              
              {/* Barra de progreso */}
              <div className="mt-3 h-3 bg-gray-200 rounded-full overflow-hidden">
                <div 
                  className={`h-full transition-all duration-500 ${
                    eolica.eficiencia_percent >= 85 ? 'bg-green-500' :
                    eolica.eficiencia_percent >= 75 ? 'bg-blue-500' :
                    eolica.eficiencia_percent >= 60 ? 'bg-yellow-500' : 'bg-red-500'
                  }`}
                  style={{ width: `${Math.min(eolica.eficiencia_percent, 100)}%` }}
                ></div>
              </div>
            </div>

            {/* Diagnóstico */}
            <div className={`rounded-lg p-3 mb-4 ${
              eolica.alerta ? 'bg-red-100 border border-red-300' : 'bg-green-100 border border-green-300'
            }`}>
              <p className="text-sm font-bold mb-1">Diagnóstico:</p>
              <p className="text-sm">{eolica.diagnostico}</p>
            </div>

            {/* Mediciones */}
            <div className="bg-white rounded-lg p-4 mb-4">
              <p className="text-xs font-bold text-gray-700 mb-2">📊 Mediciones:</p>
              <div className="grid grid-cols-2 gap-2 text-xs">
                <div>
                  <span className="text-gray-600">Viento:</span>
                  <p className="font-bold">{eolica.mediciones.velocidad_viento_ms} m/s</p>
                </div>
                <div>
                  <span className="text-gray-600">Área Barrido:</span>
                  <p className="font-bold">{eolica.mediciones.area_barrido_m2} m²</p>
                </div>
                <div>
                  <span className="text-gray-600">Potencia Teórica:</span>
                  <p className="font-bold">{eolica.mediciones.potencia_teorica_w} W</p>
                </div>
                <div>
                  <span className="text-gray-600">Potencia Real:</span>
                  <p className="font-bold">{eolica.mediciones.potencia_real_w} W</p>
                </div>
                <div className="col-span-2">
                  <span className="text-gray-600">Pérdida:</span>
                  <p className="font-bold text-red-600">{eolica.mediciones.perdida_w} W</p>
                </div>
              </div>
            </div>

            {/* Recomendaciones */}
            {eolica.recomendaciones && eolica.recomendaciones.length > 0 && (
              <div className="bg-blue-50 rounded-lg p-3 border border-blue-200">
                <p className="text-xs font-bold text-blue-900 mb-2 flex items-center">
                  <Wrench className="w-4 h-4 mr-1" />
                  Recomendaciones:
                </p>
                <ul className="space-y-1">
                  {eolica.recomendaciones.map((rec, idx) => (
                    <li key={idx} className="text-xs text-blue-800">• {rec}</li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        )}
      </div>

      {/* Explicación del Sistema */}
      <div className="bg-gradient-to-br from-purple-50 to-pink-50 rounded-xl shadow-lg p-6 border-l-4 border-purple-500">
        <h3 className="text-xl font-bold text-purple-900 mb-4">
          🔬 ¿Cómo Funciona el Monitor de Eficiencia?
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <h4 className="font-bold text-gray-800 mb-2">☀️ Paneles Solares:</h4>
            <ul className="space-y-1 text-sm text-gray-700">
              <li>📡 <strong>LDR:</strong> Mide irradiancia solar (W/m²)</li>
              <li>⚡ <strong>Sensor corriente:</strong> Mide potencia real generada</li>
              <li>🌡️ <strong>Sensor temp:</strong> Factor de corrección (-0.5%/°C)</li>
              <li>🧮 <strong>Compara:</strong> Real vs Teórico</li>
              <li>💡 <strong>Detecta:</strong> Paneles sucios, sombras, daños</li>
            </ul>
          </div>
          <div>
            <h4 className="font-bold text-gray-800 mb-2">💨 Turbina Eólica:</h4>
            <ul className="space-y-1 text-sm text-gray-700">
              <li>💨 <strong>Anemómetro:</strong> Mide velocidad viento (m/s)</li>
              <li>⚡ <strong>Sensor corriente:</strong> Mide potencia real generada</li>
              <li>🔬 <strong>Fórmula Betz:</strong> Potencia teórica del viento</li>
              <li>🧮 <strong>Compara:</strong> Real vs Teórico (límite 59.3%)</li>
              <li>💡 <strong>Detecta:</strong> Fricción, palas sucias/dañadas</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};

export default EfficiencyMonitor;
