import React, { useState, useEffect, useCallback } from 'react';
import Header from './components/Header';
import EnergyMetrics from './components/EnergyMetrics';
import EnergyCharts from './components/EnergyCharts';
import ControlPanel from './components/ControlPanel';
import AlertsPanel from './components/AlertsPanel';
import WeatherWidget from './components/WeatherWidget';
import PredictionPanel from './components/PredictionPanel';
import ESP32Status from './components/ESP32Status';
import ESP32LiveData from './components/ESP32LiveData';
import ESP32RawData from './components/ESP32RawData';
import SetupWizard from './components/SetupWizard';
import ProjectInfo from './components/ProjectInfo';
import HardwareTest from './components/HardwareTest';
import LoadingScreen from './components/LoadingScreen';
import SystemCalculator from './components/SystemCalculator';
import PatternLearning from './components/PatternLearning';
import WindProtection from './components/WindProtection';
import BatteryProtection from './components/BatteryProtection';
import RecomendacionInicial from './components/RecomendacionInicial';
import EfficiencyMonitor from './components/EfficiencyMonitor';
import SmartStrategy from './components/SmartStrategy';
import SystemStatus from './components/SystemStatus';
import LocationMap from './components/LocationMap';
import WeatherForecastFixed from './components/WeatherForecastFixed';
import MarketingInfo from './components/MarketingInfo';
import HardwareInfo from './components/HardwareInfo';
import {
  getDashboardData,
  getEnergyHistory,
  getPredictions24h,
  getSystemStatus,
  createWebSocket,
} from './api/api';
import { RefreshCw } from 'lucide-react';

function App() {
  const [dashboardData, setDashboardData] = useState(null);
  const [historyData, setHistoryData] = useState(null);
  const [predictionData, setPredictionData] = useState(null);
  const [systemStatus, setSystemStatus] = useState(null);
  const [loading, setLoading] = useState(true);
  const [connected, setConnected] = useState(false);
  const [autoMode, setAutoMode] = useState(true);
  const [ws, setWs] = useState(null);

  // Cargar datos del dashboard
  const loadDashboardData = useCallback(async () => {
    try {
      const data = await getDashboardData();
      setDashboardData(data);
      setAutoMode(data.auto_mode);
      setConnected(true);
    } catch (error) {
      console.error('Error cargando dashboard:', error);
      setConnected(false);
    }
  }, []);

  // Cargar histórico
  const loadHistoryData = useCallback(async () => {
    try {
      const data = await getEnergyHistory(24);
      setHistoryData(data);
    } catch (error) {
      console.error('Error cargando histórico:', error);
    }
  }, []);

  // Cargar predicciones
  const loadPredictions = useCallback(async () => {
    try {
      const data = await getPredictions24h();
      setPredictionData(data);
    } catch (error) {
      console.error('Error cargando predicciones:', error);
    }
  }, []);

  // Cargar estado del sistema
  const loadSystemStatus = useCallback(async () => {
    try {
      const data = await getSystemStatus();
      setSystemStatus(data);
    } catch (error) {
      console.error('Error cargando estado del sistema:', error);
    }
  }, []);

  // Cargar todos los datos
  const loadAllData = useCallback(async () => {
    setLoading(true);
    await Promise.all([
      loadDashboardData(),
      loadHistoryData(),
      loadPredictions(),
      loadSystemStatus(),
    ]);
    setLoading(false);
  }, [loadDashboardData, loadHistoryData, loadPredictions, loadSystemStatus]);

  // Cargar datos iniciales
  useEffect(() => {
    loadAllData();
  }, [loadAllData]);

  // Actualizar periódicamente
  useEffect(() => {
    const interval = setInterval(() => {
      loadDashboardData();
      loadHistoryData();
    }, 30000); // Cada 30 segundos

    return () => clearInterval(interval);
  }, [loadDashboardData, loadHistoryData]);

  // Actualizar predicciones cada 5 minutos
  useEffect(() => {
    const interval = setInterval(() => {
      loadPredictions();
    }, 300000); // Cada 5 minutos

    return () => clearInterval(interval);
  }, [loadPredictions]);

  const handleRefresh = () => {
    loadAllData();
  };

  const handleAutoModeChange = (newMode) => {
    setAutoMode(newMode);
    loadDashboardData();
  };

  if (loading) {
    return <LoadingScreen />;
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-900 via-purple-900 to-pink-900">
      <Header systemStatus={systemStatus} connected={connected} />

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Panel ESP32 */}
        <div className="mb-8">
          <ESP32Status />
        </div>

        {/* Botón de actualizar */}
        <div className="flex justify-end mb-4">
          <button
            onClick={handleRefresh}
            className="btn btn-secondary flex items-center"
          >
            <RefreshCw className="w-4 h-4 mr-2" />
            Actualizar
          </button>
        </div>

        {/* Métricas principales */}
        <div className="mb-8">
          <EnergyMetrics energyData={dashboardData?.energy_status} />
        </div>

        {/* ====== PRONÓSTICO DEL CLIMA ====== */}
        <div className="mb-8">
          <WeatherForecastFixed />
        </div>

        {/* Recomendación/Configuración Inicial */}
        <div className="mb-8">
          <RecomendacionInicial />
        </div>

        {/* Grid de dos columnas */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-8">
          {/* Columna izquierda - 2/3 */}
          <div className="lg:col-span-2 space-y-8">
            {/* Gráficos */}
            <EnergyCharts
              historyData={historyData}
              predictionData={predictionData}
            />

            {/* Protección de Batería */}
            <div>
              <BatteryProtection energyData={dashboardData?.energy_status} />
            </div>

            {/* Pronóstico IA */}
            <div>
              <PredictionPanel predictionData={predictionData} />
            </div>

            {/* Dimensionamiento del Sistema */}
            <div>
              <SystemCalculator />
            </div>

            {/* Aprendizaje de Patrones */}
            <div>
              <PatternLearning />
            </div>

            {/* Protección Eólica */}
            <div>
              <WindProtection />
            </div>

            {/* Monitor de Eficiencia */}
            <div>
              <EfficiencyMonitor />
            </div>

            {/* Estrategia Inteligente */}
            <div>
              <SmartStrategy />
            </div>

            {/* Información de Marketing */}
            <div>
              <MarketingInfo />
            </div>

            {/* Información de Hardware */}
            <div>
              <HardwareInfo />
            </div>

            {/* Columna derecha - 1/3 */}
          </div>
          <div className="space-y-8">
            {/* Datos en Vivo ESP32 */}
            <ESP32LiveData />

            {/* Datos RAW ADCs */}
            <ESP32RawData />

            {/* Clima */}
            <WeatherWidget weather={dashboardData?.weather} />

            {/* Mapa de ubicación */}
            <LocationMap 
              latitude={-38.7183} 
              longitude={-62.2663}
              location="Bahía Blanca, Buenos Aires, Argentina"
            />

            {/* Panel de control */}
            <ControlPanel
              autoMode={autoMode}
              onAutoModeChange={handleAutoModeChange}
            />

            {/* Alertas */}
            <AlertsPanel alerts={dashboardData?.alerts} />
          </div>
        </div>
      </main>

      {/* RecomendacionInicial siempre visible */}
      <RecomendacionInicial />
      
      {/* Panel de Estado del Sistema - DESHABILITADO TEMPORALMENTE */}
      {/* <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
        <SystemStatus />
      </div> */}
      
      {/* Contenido principal */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
          <div className="flex items-center justify-between">
            <p className="text-sm text-gray-500">
              Sistema Inversor Inteligente Híbrido con IA Meteorológica
            </p>
            <p className="text-xs text-gray-400">
              &copy; 2024 - Desarrollado con React + FastAPI
            </p>
          </div>
        </div>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200 mt-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center justify-between">
            <p className="text-sm text-gray-500">
              Sistema Inversor Inteligente Híbrido con IA Meteorológica
            </p>
            <p className="text-xs text-gray-400">
              &copy; 2024 - Desarrollado con React + FastAPI
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;
