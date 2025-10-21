/**
 * Dashboard con navegación por tabs
 * Organiza todo el contenido de forma clara
 */

import React, { useState } from 'react';
import { Home, Activity, Settings, Info, Zap } from 'lucide-react';

// Importar todos los componentes
import EnergyMetrics from '../components/EnergyMetrics';
import EnergyCharts from '../components/EnergyCharts';
import WeatherWidget from '../components/WeatherWidget';
import PredictionPanel from '../components/PredictionPanel';
import ControlPanel from '../components/ControlPanel';
import AlertsPanel from '../components/AlertsPanel';
import BatteryProtection from '../components/BatteryProtection';
import WindProtection from '../components/WindProtection';
import EfficiencyMonitor from '../components/EfficiencyMonitor';
import PatternLearning from '../components/PatternLearning';
import SmartStrategy from '../components/SmartStrategy';
import SystemStatus from '../components/SystemStatus';
import SystemCalculator from '../components/SystemCalculator';
import MarketingInfo from '../components/MarketingInfo';
import HardwareInfo from '../components/HardwareInfo';
import LocationMap from '../components/LocationMap';

export default function DashboardTabs({ 
  dashboardData, 
  historyData, 
  predictionData,
  autoMode,
  onAutoModeChange 
}) {
  const [activeTab, setActiveTab] = useState('dashboard');

  const tabs = [
    { id: 'dashboard', name: 'Dashboard', icon: Home },
    { id: 'monitoring', name: 'Monitoreo', icon: Activity },
    { id: 'config', name: 'Configuración', icon: Settings },
    { id: 'info', name: 'Información', icon: Info },
  ];

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      {/* Sistema de Estado siempre visible */}
      <div className="bg-gray-800 border-b border-gray-700 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <SystemStatus />
        </div>
      </div>

      {/* Tabs Navigation */}
      <div className="bg-gray-800 border-b border-gray-700">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <nav className="flex space-x-8">
            {tabs.map((tab) => {
              const Icon = tab.icon;
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`
                    flex items-center gap-2 px-3 py-4 border-b-2 font-medium text-sm
                    transition-colors
                    ${activeTab === tab.id
                      ? 'border-blue-500 text-blue-400'
                      : 'border-transparent text-gray-400 hover:text-gray-300 hover:border-gray-300'
                    }
                  `}
                >
                  <Icon className="w-5 h-5" />
                  {tab.name}
                </button>
              );
            })}
          </nav>
        </div>
      </div>

      {/* Tab Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* TAB 1: DASHBOARD PRINCIPAL */}
        {activeTab === 'dashboard' && (
          <div className="space-y-8">
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
              {/* Columna Principal */}
              <div className="lg:col-span-2 space-y-8">
                {/* Métricas de Energía */}
                <EnergyMetrics energyData={dashboardData?.energy_status} />

                {/* Pronóstico IA */}
                <PredictionPanel predictionData={predictionData} />

                {/* Gráficos */}
                <EnergyCharts 
                  dashboardData={dashboardData}
                  historyData={historyData}
                  predictionData={predictionData}
                />

                {/* Estrategia Inteligente */}
                <SmartStrategy />
              </div>

              {/* Columna Lateral */}
              <div className="space-y-8">
                {/* Clima */}
                <WeatherWidget weather={dashboardData?.weather} />

                {/* Mapa */}
                <LocationMap 
                  latitude={-38.7183} 
                  longitude={-62.2663}
                  location="Bahía Blanca, Buenos Aires, Argentina"
                />

                {/* Control Panel */}
                <ControlPanel
                  autoMode={autoMode}
                  onAutoModeChange={onAutoModeChange}
                />

                {/* Alertas */}
                <AlertsPanel alerts={dashboardData?.alerts} />
              </div>
            </div>
          </div>
        )}

        {/* TAB 2: MONITOREO AVANZADO */}
        {activeTab === 'monitoring' && (
          <div className="space-y-8">
            <h2 className="text-3xl font-bold mb-6">📊 Monitoreo Avanzado</h2>
            
            {/* Protección Batería */}
            <BatteryProtection energyData={dashboardData?.energy_status} />

            {/* Protección Eólica */}
            <WindProtection />

            {/* Monitor de Eficiencia */}
            <EfficiencyMonitor />

            {/* Aprendizaje de Patrones */}
            <PatternLearning />

            {/* Gráficos Históricos Completos */}
            <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
              <h3 className="text-xl font-bold mb-4">Histórico Extendido</h3>
              <EnergyCharts 
                dashboardData={dashboardData}
                historyData={historyData}
                predictionData={predictionData}
              />
            </div>
          </div>
        )}

        {/* TAB 3: CONFIGURACIÓN */}
        {activeTab === 'config' && (
          <div className="space-y-8">
            <h2 className="text-3xl font-bold mb-6">⚙️ Configuración del Sistema</h2>
            
            {/* Dimensionamiento */}
            <div className="bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg p-6 text-center mb-8">
              <h3 className="text-2xl font-bold mb-4">🧮 Dimensionamiento Completo</h3>
              <p className="mb-4">Calcula el sistema ideal para tu ubicación</p>
              <button
                onClick={() => window.location.href = '/dimensionamiento'}
                className="px-6 py-3 bg-white text-blue-600 font-bold rounded-lg hover:bg-gray-100"
              >
                Ir a Dimensionamiento →
              </button>
            </div>

            {/* Dispositivos ESP32 */}
            <div className="bg-gradient-to-r from-green-600 to-teal-600 rounded-lg p-6 text-center mb-8">
              <h3 className="text-2xl font-bold mb-4">📡 Dispositivos ESP32</h3>
              <p className="mb-4">Gestiona tus dispositivos conectados</p>
              <button
                onClick={() => window.location.href = '/dispositivos'}
                className="px-6 py-3 bg-white text-green-600 font-bold rounded-lg hover:bg-gray-100"
              >
                Ver Dispositivos →
              </button>
            </div>

            {/* Calculadora de Sistema */}
            <SystemCalculator />

            {/* Mapa de Ubicación */}
            <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
              <h3 className="text-xl font-bold mb-4">📍 Ubicación del Sistema</h3>
              <LocationMap 
                latitude={-38.7183} 
                longitude={-62.2663}
                location="Bahía Blanca, Buenos Aires, Argentina"
              />
            </div>
          </div>
        )}

        {/* TAB 4: INFORMACIÓN */}
        {activeTab === 'info' && (
          <div className="space-y-8">
            <h2 className="text-3xl font-bold mb-6">📚 Información del Sistema</h2>
            
            {/* Marketing */}
            <MarketingInfo />

            {/* Hardware */}
            <HardwareInfo />

            {/* Documentación */}
            <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
              <h3 className="text-2xl font-bold mb-4">📖 Documentación</h3>
              <div className="grid md:grid-cols-2 gap-4">
                <a 
                  href="/docs/firmware" 
                  className="p-4 bg-gray-700 rounded hover:bg-gray-600 transition-colors"
                >
                  <h4 className="font-bold mb-2">🔧 Guía Firmware ESP32</h4>
                  <p className="text-sm text-gray-400">Instalación y configuración</p>
                </a>
                <a 
                  href="/docs/api" 
                  className="p-4 bg-gray-700 rounded hover:bg-gray-600 transition-colors"
                >
                  <h4 className="font-bold mb-2">📡 API Reference</h4>
                  <p className="text-sm text-gray-400">Endpoints y ejemplos</p>
                </a>
                <a 
                  href="/docs/hardware" 
                  className="p-4 bg-gray-700 rounded hover:bg-gray-600 transition-colors"
                >
                  <h4 className="font-bold mb-2">⚡ Conexiones Eléctricas</h4>
                  <p className="text-sm text-gray-400">Diagramas y esquemas</p>
                </a>
                <a 
                  href="/docs/troubleshooting" 
                  className="p-4 bg-gray-700 rounded hover:bg-gray-600 transition-colors"
                >
                  <h4 className="font-bold mb-2">🔍 Troubleshooting</h4>
                  <p className="text-sm text-gray-400">Solución de problemas</p>
                </a>
              </div>
            </div>

            {/* Sobre el Sistema */}
            <div className="bg-gradient-to-r from-purple-600 to-pink-600 rounded-lg p-8 text-center">
              <Zap className="w-16 h-16 mx-auto mb-4" />
              <h3 className="text-3xl font-bold mb-4">Sistema Inversor Híbrido</h3>
              <p className="text-lg mb-4">
                Solar + Eólico con Inteligencia Artificial
              </p>
              <div className="flex justify-center gap-8 text-sm">
                <div>
                  <p className="font-bold">Versión</p>
                  <p>1.0.0</p>
                </div>
                <div>
                  <p className="font-bold">Backend</p>
                  <p>FastAPI + Python</p>
                </div>
                <div>
                  <p className="font-bold">Frontend</p>
                  <p>React 18</p>
                </div>
                <div>
                  <p className="font-bold">Firmware</p>
                  <p>ESP32 Arduino</p>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
