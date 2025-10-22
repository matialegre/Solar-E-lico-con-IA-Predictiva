/**
 * Página de dimensionamiento de sistema
 * Wizard con 2 opciones: desde consumo o desde recursos
 */

import React, { useState } from 'react';
import { Calculator, Zap, Wind, Battery, DollarSign, ArrowRight, ArrowLeft, Check } from 'lucide-react';
import axios from 'axios';
import EquationDisplay from '../components/EquationDisplay';

const API_URL = process.env.REACT_APP_API_URL || 'http://190.211.201.217:11112';

export default function DimensionamientoPage() {
  const [step, setStep] = useState(1);
  const [opcion, setOpcion] = useState(null);
  const [loading, setLoading] = useState(false);
  const [resultado, setResultado] = useState(null);

  // Form data Opción 1
  const [formOpcion1, setFormOpcion1] = useState({
    latitude: -38.7183,
    longitude: -62.2663,
    consumo_diario_kwh: 15.6,
    dias_autonomia: 2,
    voltaje_sistema: 48
  });

  // Form data Opción 2
  const [formOpcion2, setFormOpcion2] = useState({
    latitude: -38.7183,
    longitude: -62.2663,
    potencia_solar_w: 3000,
    area_solar_m2: 15.0,
    potencia_eolica_w: 2000,
    diametro_turbina_m: 2.5
  });

  const calcularOpcion1 = async () => {
    try {
      setLoading(true);
      const response = await axios.post(`${API_URL}/api/dimensionamiento/opcion1`, formOpcion1);
      setResultado(response.data);
      setStep(3);
    } catch (error) {
      console.error('Error calculando:', error);
      alert('Error al calcular dimensionamiento');
    } finally {
      setLoading(false);
    }
  };

  const calcularOpcion2 = async () => {
    try {
      setLoading(true);
      const response = await axios.post(`${API_URL}/api/dimensionamiento/opcion2`, formOpcion2);
      setResultado(response.data);
      setStep(3);
    } catch (error) {
      console.error('Error calculando:', error);
      alert('Error al calcular dimensionamiento');
    } finally {
      setLoading(false);
    }
  };

  const resetWizard = () => {
    setStep(1);
    setOpcion(null);
    setResultado(null);
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white p-6">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold mb-2">🧮 Dimensionamiento de Sistema</h1>
          <p className="text-gray-400">
            Calcula el sistema solar + eólico ideal para tus necesidades
          </p>
        </div>

        {/* Progress Steps */}
        <div className="flex items-center justify-center gap-4 mb-8">
          {[1, 2, 3].map((num) => (
            <React.Fragment key={num}>
              <div className={`flex items-center justify-center w-12 h-12 rounded-full border-2 font-bold ${
                step >= num ? 'bg-blue-600 border-blue-600' : 'bg-gray-800 border-gray-700'
              }`}>
                {step > num ? <Check className="w-6 h-6" /> : num}
              </div>
              {num < 3 && (
                <div className={`h-1 w-16 ${step > num ? 'bg-blue-600' : 'bg-gray-700'}`} />
              )}
            </React.Fragment>
          ))}
        </div>

        {/* Step Content */}
        {step === 1 && (
          <div className="max-w-4xl mx-auto">
            <h2 className="text-2xl font-bold text-center mb-8">
              Elige cómo quieres calcular tu sistema
            </h2>
            
            <div className="grid md:grid-cols-2 gap-6">
              {/* Opción 1 */}
              <button
                onClick={() => { setOpcion(1); setStep(2); }}
                className="bg-gray-800 hover:bg-gray-750 p-8 rounded-lg border-2 border-gray-700 hover:border-blue-500 transition-all text-left group"
              >
                <div className="flex items-start gap-4">
                  <Zap className="w-12 h-12 text-yellow-400 flex-shrink-0 group-hover:scale-110 transition-transform" />
                  <div>
                    <h3 className="text-xl font-bold mb-2">Opción 1: Desde Consumo</h3>
                    <p className="text-gray-400 mb-4">
                      Tengo X consumo diario, ¿qué sistema necesito?
                    </p>
                    <ul className="text-sm text-gray-500 space-y-1">
                      <li>✓ Ingresas tu consumo en kWh/día</li>
                      <li>✓ Sistema calcula paneles y turbinas necesarias</li>
                      <li>✓ Dimensiona batería automáticamente</li>
                      <li>✓ Muestra ecuaciones y costos</li>
                    </ul>
                  </div>
                </div>
              </button>

              {/* Opción 2 */}
              <button
                onClick={() => { setOpcion(2); setStep(2); }}
                className="bg-gray-800 hover:bg-gray-750 p-8 rounded-lg border-2 border-gray-700 hover:border-green-500 transition-all text-left group"
              >
                <div className="flex items-start gap-4">
                  <Wind className="w-12 h-12 text-green-400 flex-shrink-0 group-hover:scale-110 transition-transform" />
                  <div>
                    <h3 className="text-xl font-bold mb-2">Opción 2: Desde Recursos</h3>
                    <p className="text-gray-400 mb-4">
                      Tengo estos recursos, ¿qué puedo generar?
                    </p>
                    <ul className="text-sm text-gray-500 space-y-1">
                      <li>✓ Ingresas paneles y turbinas que tienes</li>
                      <li>✓ Sistema calcula generación máxima</li>
                      <li>✓ Te dice el consumo máximo soportable</li>
                      <li>✓ Recomienda batería ideal</li>
                    </ul>
                  </div>
                </div>
              </button>
            </div>
          </div>
        )}

        {step === 2 && opcion === 1 && (
          <div className="max-w-2xl mx-auto bg-gray-800 rounded-lg p-8 border border-gray-700">
            <h2 className="text-2xl font-bold mb-6 flex items-center gap-2">
              <Zap className="w-6 h-6 text-yellow-400" />
              Opción 1: Desde Consumo
            </h2>

            <div className="space-y-6">
              <div className="grid md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm text-gray-400 mb-2">Latitud</label>
                  <input
                    type="number"
                    step="0.0001"
                    value={formOpcion1.latitude}
                    onChange={(e) => setFormOpcion1({ ...formOpcion1, latitude: parseFloat(e.target.value) || 0 })}
                    className="w-full px-4 py-2 bg-gray-900 border border-gray-700 rounded focus:border-blue-500 focus:outline-none"
                  />
                </div>
                <div>
                  <label className="block text-sm text-gray-400 mb-2">Longitud</label>
                  <input
                    type="number"
                    step="0.0001"
                    value={formOpcion1.longitude}
                    onChange={(e) => setFormOpcion1({ ...formOpcion1, longitude: parseFloat(e.target.value) || 0 })}
                    className="w-full px-4 py-2 bg-gray-900 border border-gray-700 rounded focus:border-blue-500 focus:outline-none"
                  />
                </div>
              </div>

              <div>
                <label className="block text-sm text-gray-400 mb-2">
                  Consumo Diario (kWh/día)
                </label>
                <input
                  type="number"
                  step="0.1"
                  value={formOpcion1.consumo_diario_kwh}
                  onChange={(e) => setFormOpcion1({ ...formOpcion1, consumo_diario_kwh: parseFloat(e.target.value) || 0 })}
                  className="w-full px-4 py-2 bg-gray-900 border border-gray-700 rounded focus:border-blue-500 focus:outline-none text-xl font-bold"
                />
                <p className="text-xs text-gray-500 mt-1">
                  Ejemplo: 15.6 kWh/día = 468 kWh/mes
                </p>
              </div>

              <div className="grid md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm text-gray-400 mb-2">
                    Días de Autonomía
                  </label>
                  <input
                    type="number"
                    value={formOpcion1.dias_autonomia}
                    onChange={(e) => setFormOpcion1({ ...formOpcion1, dias_autonomia: parseInt(e.target.value) || 0 })}
                    className="w-full px-4 py-2 bg-gray-900 border border-gray-700 rounded focus:border-blue-500 focus:outline-none"
                  />
                </div>
                <div>
                  <label className="block text-sm text-gray-400 mb-2">
                    Voltaje Sistema (V)
                  </label>
                  <select
                    value={formOpcion1.voltaje_sistema}
                    onChange={(e) => setFormOpcion1({ ...formOpcion1, voltaje_sistema: parseInt(e.target.value) })}
                    className="w-full px-4 py-2 bg-gray-900 border border-gray-700 rounded focus:border-blue-500 focus:outline-none"
                  >
                    <option value={12}>12V</option>
                    <option value={24}>24V</option>
                    <option value={48}>48V</option>
                  </select>
                </div>
              </div>
            </div>

            <div className="flex gap-4 mt-8">
              <button
                onClick={() => setStep(1)}
                className="flex-1 py-3 bg-gray-700 hover:bg-gray-600 rounded-lg font-bold flex items-center justify-center gap-2"
              >
                <ArrowLeft className="w-5 h-5" />
                Volver
              </button>
              <button
                onClick={calcularOpcion1}
                disabled={loading}
                className="flex-1 py-3 bg-blue-600 hover:bg-blue-700 rounded-lg font-bold flex items-center justify-center gap-2 disabled:opacity-50"
              >
                {loading ? 'Calculando...' : 'Calcular Sistema'}
                <Calculator className="w-5 h-5" />
              </button>
            </div>
          </div>
        )}

        {step === 2 && opcion === 2 && (
          <div className="max-w-2xl mx-auto bg-gray-800 rounded-lg p-8 border border-gray-700">
            <h2 className="text-2xl font-bold mb-6 flex items-center gap-2">
              <Wind className="w-6 h-6 text-green-400" />
              Opción 2: Desde Recursos
            </h2>

            <div className="space-y-6">
              <div className="grid md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm text-gray-400 mb-2">Latitud</label>
                  <input
                    type="number"
                    step="0.0001"
                    value={formOpcion2.latitude}
                    onChange={(e) => setFormOpcion2({ ...formOpcion2, latitude: parseFloat(e.target.value) || 0 })}
                    className="w-full px-4 py-2 bg-gray-900 border border-gray-700 rounded focus:border-blue-500 focus:outline-none"
                  />
                </div>
                <div>
                  <label className="block text-sm text-gray-400 mb-2">Longitud</label>
                  <input
                    type="number"
                    step="0.0001"
                    value={formOpcion2.longitude}
                    onChange={(e) => setFormOpcion2({ ...formOpcion2, longitude: parseFloat(e.target.value) || 0 })}
                    className="w-full px-4 py-2 bg-gray-900 border border-gray-700 rounded focus:border-blue-500 focus:outline-none"
                  />
                </div>
              </div>

              <div className="p-4 bg-yellow-500/10 border border-yellow-500/30 rounded">
                <p className="text-yellow-400 font-bold mb-2">☀️ Sistema Solar</p>
                <div className="grid md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm text-gray-400 mb-2">Potencia (W)</label>
                    <input
                      type="number"
                      value={formOpcion2.potencia_solar_w}
                      onChange={(e) => setFormOpcion2({ ...formOpcion2, potencia_solar_w: parseFloat(e.target.value) || 0 })}
                      className="w-full px-4 py-2 bg-gray-900 border border-gray-700 rounded focus:border-yellow-500 focus:outline-none"
                      placeholder="Ej: 3000"
                    />
                  </div>
                  <div>
                    <label className="block text-sm text-gray-400 mb-2">Área (m²)</label>
                    <input
                      type="number"
                      step="0.1"
                      value={formOpcion2.area_solar_m2}
                      onChange={(e) => setFormOpcion2({ ...formOpcion2, area_solar_m2: parseFloat(e.target.value) || 0 })}
                      className="w-full px-4 py-2 bg-gray-900 border border-gray-700 rounded focus:border-yellow-500 focus:outline-none"
                      placeholder="Ej: 15"
                    />
                  </div>
                </div>
              </div>

              <div className="p-4 bg-blue-500/10 border border-blue-500/30 rounded">
                <p className="text-blue-400 font-bold mb-2">💨 Sistema Eólico</p>
                <div className="grid md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm text-gray-400 mb-2">Potencia (W)</label>
                    <input
                      type="number"
                      value={formOpcion2.potencia_eolica_w}
                      onChange={(e) => setFormOpcion2({ ...formOpcion2, potencia_eolica_w: parseFloat(e.target.value) || 0 })}
                      className="w-full px-4 py-2 bg-gray-900 border border-gray-700 rounded focus:border-blue-500 focus:outline-none"
                      placeholder="Ej: 2000"
                    />
                  </div>
                  <div>
                    <label className="block text-sm text-gray-400 mb-2">Diámetro (m)</label>
                    <input
                      type="number"
                      step="0.1"
                      value={formOpcion2.diametro_turbina_m}
                      onChange={(e) => setFormOpcion2({ ...formOpcion2, diametro_turbina_m: parseFloat(e.target.value) || 0 })}
                      className="w-full px-4 py-2 bg-gray-900 border border-gray-700 rounded focus:border-blue-500 focus:outline-none"
                      placeholder="Ej: 2.5"
                    />
                  </div>
                </div>
              </div>
            </div>

            <div className="flex gap-4 mt-8">
              <button
                onClick={() => setStep(1)}
                className="flex-1 py-3 bg-gray-700 hover:bg-gray-600 rounded-lg font-bold flex items-center justify-center gap-2"
              >
                <ArrowLeft className="w-5 h-5" />
                Volver
              </button>
              <button
                onClick={calcularOpcion2}
                disabled={loading}
                className="flex-1 py-3 bg-green-600 hover:bg-green-700 rounded-lg font-bold flex items-center justify-center gap-2 disabled:opacity-50"
              >
                {loading ? 'Calculando...' : 'Calcular Generación'}
                <Calculator className="w-5 h-5" />
              </button>
            </div>
          </div>
        )}

        {step === 3 && resultado && (
          <div className="space-y-6">
            {/* Resumen */}
            <div className="bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg p-8 text-center">
              <h2 className="text-3xl font-bold mb-4">
                {resultado.tipo === 'opcion1_desde_consumo' 
                  ? '✅ Sistema Dimensionado'
                  : '✅ Potencia Calculada'
                }
              </h2>
              <div className="grid md:grid-cols-3 gap-6">
                <div>
                  <p className="text-blue-100 mb-1">Generación Diaria</p>
                  <p className="text-4xl font-bold">
                    {resultado.tipo === 'opcion1_desde_consumo'
                      ? resultado.resumen.generacion_total_diaria_kwh.toFixed(1)
                      : resultado.resultado.generacion_total_kwh_dia.toFixed(1)
                    } kWh
                  </p>
                </div>
                <div>
                  <p className="text-blue-100 mb-1">Cobertura</p>
                  <p className="text-4xl font-bold">
                    {resultado.tipo === 'opcion1_desde_consumo'
                      ? resultado.resumen.cobertura_porcentaje.toFixed(0)
                      : '100'
                    }%
                  </p>
                </div>
                <div>
                  <p className="text-blue-100 mb-1">
                    {resultado.tipo === 'opcion1_desde_consumo' ? 'Inversión' : 'Consumo Máximo'}
                  </p>
                  <p className="text-4xl font-bold">
                    {resultado.tipo === 'opcion1_desde_consumo'
                      ? `$${resultado.resumen.costo_total_usd.toLocaleString()}`
                      : `${resultado.resultado.consumo_maximo_soportable_kwh_dia.toFixed(1)} kWh`
                    }
                  </p>
                </div>
              </div>
            </div>

            {/* Sistema Solar */}
            {resultado.sistema_solar && (
              <div className="bg-gray-800 rounded-lg p-6 border border-yellow-500">
                <h3 className="text-2xl font-bold mb-4 flex items-center gap-2">
                  <Zap className="w-6 h-6 text-yellow-400" />
                  Sistema Solar
                </h3>
                
                <EquationDisplay calculos={resultado.sistema_solar.calculos} />
                
                <div className="mt-6 grid md:grid-cols-2 gap-4">
                  <div className="p-4 bg-gray-900 rounded">
                    <p className="text-gray-400 text-sm mb-2">Paneles Recomendados</p>
                    <p className="text-2xl font-bold">
                      {resultado.sistema_solar.resultado.paneles.cantidad} x {resultado.sistema_solar.resultado.paneles.potencia_unitaria_w}W
                    </p>
                    <p className="text-sm text-gray-500">
                      Total: {resultado.sistema_solar.resultado.paneles.potencia_total_w}W
                    </p>
                  </div>
                  <div className="p-4 bg-gray-900 rounded">
                    <p className="text-gray-400 text-sm mb-2">Generación Diaria</p>
                    <p className="text-2xl font-bold text-yellow-400">
                      {resultado.sistema_solar.resultado.generacion.diaria_kwh.toFixed(2)} kWh
                    </p>
                    <p className="text-sm text-gray-500">
                      {resultado.sistema_solar.resultado.generacion.anual_kwh.toFixed(0)} kWh/año
                    </p>
                  </div>
                </div>
              </div>
            )}

            {/* Sistema Eólico */}
            {resultado.sistema_eolico && (
              <div className="bg-gray-800 rounded-lg p-6 border border-blue-500">
                <h3 className="text-2xl font-bold mb-4 flex items-center gap-2">
                  <Wind className="w-6 h-6 text-blue-400" />
                  Sistema Eólico
                </h3>
                
                <EquationDisplay calculos={resultado.sistema_eolico.calculos} />
                
                <div className="mt-6 grid md:grid-cols-2 gap-4">
                  <div className="p-4 bg-gray-900 rounded">
                    <p className="text-gray-400 text-sm mb-2">Turbinas Recomendadas</p>
                    <p className="text-2xl font-bold">
                      {resultado.sistema_eolico.resultado.turbinas.cantidad} x {resultado.sistema_eolico.resultado.turbinas.potencia_unitaria_w}W
                    </p>
                    <p className="text-sm text-gray-500">
                      Diámetro: {resultado.sistema_eolico.resultado.turbinas.diametro_m}m
                    </p>
                  </div>
                  <div className="p-4 bg-gray-900 rounded">
                    <p className="text-gray-400 text-sm mb-2">Generación Diaria</p>
                    <p className="text-2xl font-bold text-blue-400">
                      {resultado.sistema_eolico.resultado.generacion.diaria_kwh.toFixed(2)} kWh
                    </p>
                    <p className="text-sm text-gray-500">
                      {resultado.sistema_eolico.resultado.generacion.anual_kwh.toFixed(0)} kWh/año
                    </p>
                  </div>
                </div>
              </div>
            )}

            {/* Sistema Batería */}
            {resultado.sistema_bateria && (
              <div className="bg-gray-800 rounded-lg p-6 border border-green-500">
                <h3 className="text-2xl font-bold mb-4 flex items-center gap-2">
                  <Battery className="w-6 h-6 text-green-400" />
                  Sistema de Almacenamiento
                </h3>
                
                <EquationDisplay calculos={resultado.sistema_bateria.calculos} />
                
                <div className="mt-6 grid md:grid-cols-3 gap-4">
                  <div className="p-4 bg-gray-900 rounded">
                    <p className="text-gray-400 text-sm mb-2">Configuración</p>
                    <p className="text-2xl font-bold">
                      {resultado.sistema_bateria.resultado.baterias.total_baterias} baterías
                    </p>
                    <p className="text-sm text-gray-500">
                      {resultado.sistema_bateria.resultado.baterias.configuracion_serie}S × {resultado.sistema_bateria.resultado.baterias.configuracion_paralelo}P
                    </p>
                  </div>
                  <div className="p-4 bg-gray-900 rounded">
                    <p className="text-gray-400 text-sm mb-2">Capacidad Total</p>
                    <p className="text-2xl font-bold text-green-400">
                      {resultado.sistema_bateria.resultado.baterias.capacidad_total_kwh.toFixed(1)} kWh
                    </p>
                    <p className="text-sm text-gray-500">
                      {resultado.sistema_bateria.resultado.baterias.voltaje_total}V
                    </p>
                  </div>
                  <div className="p-4 bg-gray-900 rounded">
                    <p className="text-gray-400 text-sm mb-2">Autonomía</p>
                    <p className="text-2xl font-bold">
                      {resultado.sistema_bateria.resultado.autonomia.dias} días
                    </p>
                    <p className="text-sm text-gray-500">
                      DoD {resultado.sistema_bateria.resultado.autonomia.profundidad_descarga}%
                    </p>
                  </div>
                </div>
              </div>
            )}

            {/* Costos */}
            {resultado.tipo === 'opcion1_desde_consumo' && (
              <div className="bg-gray-800 rounded-lg p-6 border border-purple-500">
                <h3 className="text-2xl font-bold mb-4 flex items-center gap-2">
                  <DollarSign className="w-6 h-6 text-purple-400" />
                  Análisis Económico
                </h3>
                
                <div className="grid md:grid-cols-2 gap-6">
                  <div>
                    <h4 className="font-bold mb-3">Inversión Inicial</h4>
                    <div className="space-y-2 text-sm">
                      <div className="flex justify-between">
                        <span className="text-gray-400">Sistema Solar:</span>
                        <span className="font-bold">${resultado.sistema_solar.resultado.costo.total_estimado_usd.toLocaleString()}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-gray-400">Sistema Eólico:</span>
                        <span className="font-bold">${resultado.sistema_eolico.resultado.costo.total_estimado_usd.toLocaleString()}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-gray-400">Baterías:</span>
                        <span className="font-bold">${resultado.sistema_bateria.resultado.costo.total_estimado_usd.toLocaleString()}</span>
                      </div>
                      <div className="flex justify-between pt-2 border-t border-gray-700">
                        <span className="text-gray-400 font-bold">Total:</span>
                        <span className="font-bold text-xl text-purple-400">${resultado.resumen.costo_total_usd.toLocaleString()}</span>
                      </div>
                    </div>
                  </div>
                  
                  <div>
                    <h4 className="font-bold mb-3">Retorno de Inversión</h4>
                    <div className="space-y-4">
                      <div className="p-4 bg-gray-900 rounded">
                        <p className="text-gray-400 text-sm mb-1">Payback Period</p>
                        <p className="text-3xl font-bold text-green-400">
                          {resultado.resumen.payback_years} años
                        </p>
                      </div>
                      <div className="p-4 bg-gray-900 rounded">
                        <p className="text-gray-400 text-sm mb-1">ROI Anual</p>
                        <p className="text-3xl font-bold text-blue-400">
                          {resultado.resumen.roi_anual_porcentaje}%
                        </p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* Botones */}
            <div className="flex gap-4">
              <button
                onClick={resetWizard}
                className="flex-1 py-3 bg-gray-700 hover:bg-gray-600 rounded-lg font-bold"
              >
                Nuevo Cálculo
              </button>
              <button
                onClick={() => window.print()}
                className="flex-1 py-3 bg-blue-600 hover:bg-blue-700 rounded-lg font-bold"
              >
                Imprimir Reporte
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
