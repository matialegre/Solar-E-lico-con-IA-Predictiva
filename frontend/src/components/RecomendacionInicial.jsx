import React, { useState, useEffect } from 'react';
import { Sun, Wind, Battery, Zap, CheckCircle, AlertTriangle, Settings, ExternalLink } from 'lucide-react';
import axios from 'axios';
import DataSourceBadge from './DataSourceBadge';

const RecomendacionInicial = () => {
  const [config, setConfig] = useState(null);
  const [loading, setLoading] = useState(true);
  const [showConfig, setShowConfig] = useState(false);

  useEffect(() => {
    loadConfig();
  }, []);

  const loadConfig = async () => {
    try {
      const response = await axios.get(`${process.env.REACT_APP_API_URL}/api/configuracion/usuario`);
      setConfig(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Error cargando configuración:', error);
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="bg-white rounded-xl shadow-lg p-6 animate-pulse">
        <div className="h-8 bg-gray-200 rounded w-3/4 mb-4"></div>
        <div className="h-4 bg-gray-200 rounded w-full mb-2"></div>
        <div className="h-4 bg-gray-200 rounded w-2/3"></div>
      </div>
    );
  }

  // Sin configuración - Mostrar llamado a acción
  if (!config || !config.configurado) {
    return (
      <div className="bg-gradient-to-br from-indigo-500 to-purple-600 rounded-2xl shadow-2xl p-8 text-white">
        <div className="flex items-start justify-between mb-6">
          <div>
            <h2 className="text-3xl font-bold mb-2">¡Bienvenido al Sistema Híbrido! 🚀</h2>
            <p className="text-indigo-100 text-lg">
              Para comenzar, necesitamos dimensionar el sistema según TU casa.
            </p>
          </div>
          <AlertTriangle className="w-12 h-12 text-yellow-300" />
        </div>

        <div className="bg-white bg-opacity-10 rounded-xl p-6 mb-6 backdrop-blur-sm">
          <h3 className="text-xl font-bold mb-4">El sistema te preguntará:</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="flex items-start">
              <CheckCircle className="w-5 h-5 mr-2 flex-shrink-0 mt-0.5" />
              <div>
                <p className="font-bold">Tu ubicación</p>
                <p className="text-sm text-indigo-100">Latitud, longitud → Datos climáticos REALES de tu zona</p>
              </div>
            </div>
            <div className="flex items-start">
              <CheckCircle className="w-5 h-5 mr-2 flex-shrink-0 mt-0.5" />
              <div>
                <p className="font-bold">Tu consumo</p>
                <p className="text-sm text-indigo-100">kWh/día o estimación por electrodomésticos</p>
              </div>
            </div>
            <div className="flex items-start">
              <CheckCircle className="w-5 h-5 mr-2 flex-shrink-0 mt-0.5" />
              <div>
                <p className="font-bold">Viento de tu zona</p>
                <p className="text-sm text-indigo-100">Obtenido de OpenWeather API</p>
              </div>
            </div>
            <div className="flex items-start">
              <CheckCircle className="w-5 h-5 mr-2 flex-shrink-0 mt-0.5" />
              <div>
                <p className="font-bold">Recomendación exacta</p>
                <p className="text-sm text-indigo-100">Paneles, turbina, batería dimensionados</p>
              </div>
            </div>
          </div>
        </div>

        <div className="flex flex-col sm:flex-row gap-4">
          <button
            onClick={() => window.open('x:\\PREDICCION DE CLIMA\\CONFIGURAR_SISTEMA.bat', '_blank')}
            className="flex-1 bg-white text-indigo-600 px-6 py-4 rounded-xl font-bold hover:bg-indigo-50 transition-all flex items-center justify-center"
          >
            <Settings className="w-5 h-5 mr-2" />
            Configurar Mi Sistema Ahora
          </button>
          <button
            onClick={() => setShowConfig(true)}
            className="flex-1 bg-indigo-700 bg-opacity-50 px-6 py-4 rounded-xl font-bold hover:bg-opacity-70 transition-all flex items-center justify-center"
          >
            Ver Dashboard sin Configurar
          </button>
        </div>

        <div className="mt-6 text-center text-sm text-indigo-100">
          <p>💡 <strong>Tip:</strong> Ejecuta <code className="bg-black bg-opacity-30 px-2 py-1 rounded">CONFIGURAR_SISTEMA.bat</code> desde la carpeta del proyecto</p>
        </div>
      </div>
    );
  }

  // Con configuración - Mostrar resumen
  const cfg = config.configuracion;
  const modo = cfg.modo || 'recomendacion';
  const paneles = cfg.paneles_solares || cfg.sistema_recomendado?.paneles || cfg.componentes?.paneles;
  const turbina = cfg.turbina_eolica || cfg.sistema_recomendado?.turbina || cfg.componentes?.turbina;
  const bateria = cfg.bateria || cfg.sistema_recomendado?.bateria || cfg.componentes?.bateria;
  const inversor = cfg.inversor || cfg.sistema_recomendado?.inversor;
  const consumo = cfg.consumo;
  const capacidad = cfg.capacidad_sistema;
  const ubicacion = cfg.ubicacion;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-gradient-to-br from-green-500 to-emerald-600 rounded-2xl shadow-xl p-6 text-white">
        <div className="flex items-start justify-between mb-4">
          <div>
            <h2 className="text-3xl font-bold mb-2">Tu Sistema Configurado ✅</h2>
            <p className="text-green-100">
              {ubicacion?.ciudad || 'Sistema personalizado'} ({ubicacion?.latitud}, {ubicacion?.longitud})
            </p>
          </div>
          <button
            onClick={() => window.open('x:\\PREDICCION DE CLIMA\\CONFIGURAR_SISTEMA.bat', '_blank')}
            className="bg-white bg-opacity-20 hover:bg-opacity-30 px-4 py-2 rounded-lg text-sm font-medium transition-all flex items-center"
          >
            <Settings className="w-4 h-4 mr-2" />
            Reconfigurar
          </button>
        </div>

        {/* Clima de la zona */}
        {ubicacion?.clima_historico && (
          <div className="bg-white bg-opacity-10 rounded-lg p-4 backdrop-blur-sm mb-4">
            <div className="flex items-center mb-2">
              <DataSourceBadge 
                source="api" 
                details="Datos históricos de OpenWeather API"
              />
              <span className="ml-2 text-sm font-medium">Datos Climáticos de Tu Zona</span>
            </div>
            <div className="grid grid-cols-3 gap-4 mt-3">
              <div>
                <p className="text-xs text-green-100">Viento Promedio</p>
                <p className="text-lg font-bold">{ubicacion.clima_historico.viento_promedio_ms} m/s</p>
              </div>
              <div>
                <p className="text-xs text-green-100">Viento Máximo</p>
                <p className="text-lg font-bold">{ubicacion.clima_historico.viento_maximo_ms} m/s</p>
              </div>
              <div>
                <p className="text-xs text-green-100">Temperatura</p>
                <p className="text-lg font-bold">{ubicacion.clima_historico.temperatura_promedio_c}°C</p>
              </div>
            </div>
          </div>
        )}

        {/* Resumen del sistema */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div className="bg-white bg-opacity-10 rounded-lg p-4 backdrop-blur-sm">
            <Sun className="w-8 h-8 mb-2" />
            <p className="text-sm text-green-100 mb-1">Paneles Solares</p>
            <p className="text-2xl font-bold">{paneles?.cantidad || 0}x {paneles?.potencia_unitaria || paneles?.potencia_por_panel_w || 300}W</p>
            <p className="text-xs text-green-100 mt-1">{(paneles?.potencia_total || paneles?.potencia_total_w || 0) / 1000} kW</p>
          </div>

          <div className="bg-white bg-opacity-10 rounded-lg p-4 backdrop-blur-sm">
            <Wind className="w-8 h-8 mb-2" />
            <p className="text-sm text-green-100 mb-1">Turbina Eólica</p>
            <p className="text-2xl font-bold">{turbina?.cantidad || 0}x {turbina?.potencia_unitaria || turbina?.potencia_nominal_w || 1000}W</p>
            <p className="text-xs text-green-100 mt-1">{((turbina?.cantidad || 0) * (turbina?.potencia_unitaria || turbina?.potencia_nominal_w || 1000)) / 1000} kW</p>
          </div>

          <div className="bg-white bg-opacity-10 rounded-lg p-4 backdrop-blur-sm">
            <Battery className="w-8 h-8 mb-2" />
            <p className="text-sm text-green-100 mb-1">Batería</p>
            <p className="text-2xl font-bold">{bateria?.voltaje || bateria?.voltaje_nominal || 48}V {bateria?.capacidad_ah || 100}Ah</p>
            <p className="text-xs text-green-100 mt-1">{bateria?.capacidad_kwh || 4.8} kWh</p>
          </div>

          <div className="bg-white bg-opacity-10 rounded-lg p-4 backdrop-blur-sm">
            <Zap className="w-8 h-8 mb-2" />
            <p className="text-sm text-green-100 mb-1">Inversor</p>
            <p className="text-2xl font-bold">{(inversor?.potencia_continua || inversor?.potencia_continua_w || 2000) / 1000} kW</p>
            <p className="text-xs text-green-100 mt-1">Continua</p>
          </div>
        </div>
      </div>

      {/* Balance energético */}
      {cfg.sistema_recomendado && (
        <div className="bg-white rounded-xl shadow-lg p-6">
          <h3 className="text-xl font-bold text-gray-900 mb-4 flex items-center">
            Balance Energético Estimado
            <DataSourceBadge 
              source="ia" 
              details="Calculado por algoritmo de dimensionamiento"
            />
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="text-center p-4 bg-gray-50 rounded-lg">
              <p className="text-sm text-gray-600 mb-1">Consumo Diario</p>
              <p className="text-3xl font-bold text-gray-900">{consumo?.promedio_diario_kwh || 0} kWh</p>
            </div>
            <div className="text-center p-4 bg-green-50 rounded-lg">
              <p className="text-sm text-gray-600 mb-1">Generación Estimada</p>
              <p className="text-3xl font-bold text-green-600">
                {cfg.sistema_recomendado.generacion_total_dia_kwh || 0} kWh
              </p>
            </div>
            <div className="text-center p-4 bg-blue-50 rounded-lg">
              <p className="text-sm text-gray-600 mb-1">Cobertura</p>
              <p className="text-3xl font-bold text-blue-600">
                {cfg.sistema_recomendado.cobertura_porcentaje || 0}%
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Nota sobre datos simulados */}
      <div className="bg-gradient-to-r from-orange-50 to-yellow-50 border-l-4 border-orange-400 rounded-lg p-4">
        <div className="flex items-start">
          <AlertTriangle className="w-5 h-5 text-orange-600 mr-3 flex-shrink-0 mt-0.5" />
          <div>
            <p className="text-sm font-bold text-orange-900 mb-2">Sobre los Datos del Dashboard:</p>
            <div className="space-y-1 text-xs text-orange-800">
              <p>• <DataSourceBadge source="api" /> = Datos REALES de OpenWeather API (clima, pronóstico)</p>
              <p>• <DataSourceBadge source="ia" /> = Procesado por IA/ML (predicciones, patrones, recomendaciones)</p>
              <p>• <DataSourceBadge source="simulado" /> = Datos SIMULADOS (batería, paneles, turbina - sin ESP32 conectado)</p>
            </div>
            <p className="text-xs text-orange-700 mt-3 font-medium">
              💡 Para datos reales de generación y batería, conecta el ESP32 con sensores reales.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default RecomendacionInicial;
