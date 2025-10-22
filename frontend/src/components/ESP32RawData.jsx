import React, { useState, useEffect } from 'react';
import { Activity, Zap } from 'lucide-react';
import api from '../api/api';

const ESP32RawData = () => {
  const [devices, setDevices] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadData();
    const interval = setInterval(loadData, 1000); // Actualizar cada 1 seg
    return () => clearInterval(interval);
  }, []);

  const loadData = async () => {
    try {
      const response = await api.get('/api/esp32/devices');
      setDevices(response.data.devices || []);
      setLoading(false);
    } catch (error) {
      console.error('Error loading ESP32 raw data:', error);
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="card bg-gray-800 border-2 border-gray-700 animate-pulse">
        <div className="h-64 bg-gray-700 rounded"></div>
      </div>
    );
  }

  const device = devices[0];
  if (!device) return null;

  const rawData = device.raw_adc || {};

  return (
    <div className="card bg-gradient-to-br from-gray-900 to-black border-2 border-yellow-500">
      <div className="flex items-center justify-between mb-4 pb-3 border-b border-gray-700">
        <h3 className="text-xl font-bold text-white flex items-center">
          <Zap className="w-6 h-6 mr-2 text-yellow-400" />
          📊 ADCs RAW (Valores Reales 0-3.3V)
        </h3>
        <div className="px-2 py-1 rounded text-xs font-bold bg-yellow-500 text-black">
          ⚡ TIEMPO REAL
        </div>
      </div>

      <div className="space-y-3">
        {/* ADC 1 - Voltaje Batería 1 */}
        <div className="p-3 bg-gray-800/50 border border-gray-700 rounded-lg">
          <div className="flex justify-between items-center mb-2">
            <span className="text-sm text-gray-300">📍 ADC1_CH6 (GPIO34) - Batería 1</span>
            <span className="text-lg font-mono font-bold text-yellow-400">
              {rawData.adc1_bat1?.toFixed(3) || '0.000'}V
            </span>
          </div>
          <div className="w-full bg-gray-700 h-2 rounded-full overflow-hidden">
            <div 
              className="h-full bg-gradient-to-r from-yellow-500 to-green-500 transition-all duration-300"
              style={{ width: `${((rawData.adc1_bat1 || 0) / 3.3) * 100}%` }}
            />
          </div>
          <div className="text-xs text-gray-500 mt-1">
            ADC raw: {rawData.adc1_bat1_raw || 0} / 4095 ({(((rawData.adc1_bat1_raw || 0) / 4095) * 100).toFixed(1)}%)
          </div>
        </div>

        {/* ADC 2 - Voltaje Batería 2 */}
        <div className="p-3 bg-gray-800/50 border border-gray-700 rounded-lg">
          <div className="flex justify-between items-center mb-2">
            <span className="text-sm text-gray-300">📍 ADC1_CH7 (GPIO35) - Batería 2</span>
            <span className="text-lg font-mono font-bold text-yellow-400">
              {rawData.adc2_bat2?.toFixed(3) || '0.000'}V
            </span>
          </div>
          <div className="w-full bg-gray-700 h-2 rounded-full overflow-hidden">
            <div 
              className="h-full bg-gradient-to-r from-yellow-500 to-green-500 transition-all duration-300"
              style={{ width: `${((rawData.adc2_bat2 || 0) / 3.3) * 100}%` }}
            />
          </div>
          <div className="text-xs text-gray-500 mt-1">
            ADC raw: {rawData.adc2_bat2_raw || 0} / 4095
          </div>
        </div>

        {/* ADC 3 - Voltaje Batería 3 */}
        <div className="p-3 bg-gray-800/50 border border-gray-700 rounded-lg">
          <div className="flex justify-between items-center mb-2">
            <span className="text-sm text-gray-300">📍 ADC1_CH4 (GPIO32) - Batería 3</span>
            <span className="text-lg font-mono font-bold text-yellow-400">
              {rawData.adc3_bat3?.toFixed(3) || '0.000'}V
            </span>
          </div>
          <div className="w-full bg-gray-700 h-2 rounded-full overflow-hidden">
            <div 
              className="h-full bg-gradient-to-r from-yellow-500 to-green-500 transition-all duration-300"
              style={{ width: `${((rawData.adc3_bat3 || 0) / 3.3) * 100}%` }}
            />
          </div>
          <div className="text-xs text-gray-500 mt-1">
            ADC raw: {rawData.adc3_bat3_raw || 0} / 4095
          </div>
        </div>

        {/* ADC 4 - Corriente Solar */}
        <div className="p-3 bg-yellow-900/20 border border-yellow-700 rounded-lg">
          <div className="flex justify-between items-center mb-2">
            <span className="text-sm text-yellow-300">☀️ ADC1_CH5 (GPIO33) - Solar</span>
            <span className="text-lg font-mono font-bold text-yellow-400">
              {rawData.adc4_solar?.toFixed(3) || '0.000'}V
            </span>
          </div>
          <div className="w-full bg-gray-700 h-2 rounded-full overflow-hidden">
            <div 
              className="h-full bg-yellow-500 transition-all duration-300"
              style={{ width: `${((rawData.adc4_solar || 0) / 3.3) * 100}%` }}
            />
          </div>
          <div className="text-xs text-gray-500 mt-1">
            ADC raw: {rawData.adc4_solar_raw || 0} / 4095
          </div>
        </div>

        {/* ADC 5 - Corriente Eólica */}
        <div className="p-3 bg-green-900/20 border border-green-700 rounded-lg">
          <div className="flex justify-between items-center mb-2">
            <span className="text-sm text-green-300">💨 ADC1_CH0 (GPIO36) - Eólica</span>
            <span className="text-lg font-mono font-bold text-green-400">
              {rawData.adc5_wind?.toFixed(3) || '0.000'}V
            </span>
          </div>
          <div className="w-full bg-gray-700 h-2 rounded-full overflow-hidden">
            <div 
              className="h-full bg-green-500 transition-all duration-300"
              style={{ width: `${((rawData.adc5_wind || 0) / 3.3) * 100}%` }}
            />
          </div>
          <div className="text-xs text-gray-500 mt-1">
            ADC raw: {rawData.adc5_wind_raw || 0} / 4095
          </div>
        </div>

        {/* ADC 6 - Corriente Consumo */}
        <div className="p-3 bg-red-900/20 border border-red-700 rounded-lg">
          <div className="flex justify-between items-center mb-2">
            <span className="text-sm text-red-300">⚡ ADC1_CH3 (GPIO39) - Consumo</span>
            <span className="text-lg font-mono font-bold text-red-400">
              {rawData.adc6_load?.toFixed(3) || '0.000'}V
            </span>
          </div>
          <div className="w-full bg-gray-700 h-2 rounded-full overflow-hidden">
            <div 
              className="h-full bg-red-500 transition-all duration-300"
              style={{ width: `${((rawData.adc6_load || 0) / 3.3) * 100}%` }}
            />
          </div>
          <div className="text-xs text-gray-500 mt-1">
            ADC raw: {rawData.adc6_load_raw || 0} / 4095
          </div>
        </div>

        {/* ADC 7 - LDR (Radiación) */}
        <div className="p-3 bg-orange-900/20 border border-orange-700 rounded-lg">
          <div className="flex justify-between items-center mb-2">
            <span className="text-sm text-orange-300">🌞 ADC2_CH8 (GPIO25) - LDR</span>
            <span className="text-lg font-mono font-bold text-orange-400">
              {rawData.adc7_ldr?.toFixed(3) || '0.000'}V
            </span>
          </div>
          <div className="w-full bg-gray-700 h-2 rounded-full overflow-hidden">
            <div 
              className="h-full bg-orange-500 transition-all duration-300"
              style={{ width: `${((rawData.adc7_ldr || 0) / 3.3) * 100}%` }}
            />
          </div>
          <div className="text-xs text-gray-500 mt-1">
            ADC raw: {rawData.adc7_ldr_raw || 0} / 4095
          </div>
        </div>
      </div>

      {/* Nota técnica */}
      <div className="mt-4 p-3 bg-blue-900/20 border border-blue-700 rounded-lg">
        <div className="text-xs text-blue-300">
          <p className="font-bold mb-1">📝 Especificaciones Técnicas:</p>
          <ul className="list-disc list-inside space-y-1 text-gray-400">
            <li>ADC ESP32: 12-bit (0-4095)</li>
            <li>Rango voltaje: 0 - 3.3V</li>
            <li>Resolución: 0.8 mV por step</li>
            <li>Actualización: Cada 1 segundo</li>
            <li>Divisores resistivos: 100kΩ / 10kΩ (factor 11x)</li>
          </ul>
        </div>
      </div>

      {/* Actualización */}
      <div className="mt-3 text-center">
        <div className="inline-flex items-center text-xs text-gray-500">
          <div className="w-2 h-2 bg-yellow-400 rounded-full mr-2 animate-pulse"></div>
          Actualiza cada 1 seg
        </div>
      </div>
    </div>
  );
};

export default ESP32RawData;
