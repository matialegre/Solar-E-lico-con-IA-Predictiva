import React from 'react';
import { DollarSign, Target, Globe, Users, TrendingUp, Package, Award, Zap } from 'lucide-react';

const MarketingInfo = () => {
  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="card bg-gradient-to-br from-green-500 to-blue-600 text-white">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-3xl font-bold flex items-center mb-2">
              <DollarSign className="w-8 h-8 mr-3" />
              Plan de Marketing & Comercialización
            </h2>
            <p className="text-green-100">
              Sistema Inversor Inteligente Híbrido con IA Predictiva
            </p>
          </div>
          <Award className="w-20 h-20 opacity-20" />
        </div>
      </div>

      {/* Propuesta de Valor */}
      <div className="card">
        <h3 className="text-xl font-bold text-gray-800 mb-4 flex items-center">
          <Zap className="w-6 h-6 mr-2 text-yellow-500" />
          Propuesta de Valor Única
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="p-4 bg-gradient-to-br from-yellow-50 to-orange-50 rounded-lg border-l-4 border-yellow-500">
            <div className="text-3xl mb-2">🤖</div>
            <h4 className="font-bold text-gray-800 mb-2">IA Predictiva</h4>
            <p className="text-sm text-gray-600">
              Algoritmos de machine learning que predicen generación y consumo con datos meteorológicos en tiempo real
            </p>
          </div>
          <div className="p-4 bg-gradient-to-br from-green-50 to-blue-50 rounded-lg border-l-4 border-green-500">
            <div className="text-3xl mb-2">⚡</div>
            <h4 className="font-bold text-gray-800 mb-2">Autonomía Inteligente</h4>
            <p className="text-sm text-gray-600">
              Sistema híbrido solar + eólico con gestión automática de batería y optimización de recursos
            </p>
          </div>
          <div className="p-4 bg-gradient-to-br from-purple-50 to-pink-50 rounded-lg border-l-4 border-purple-500">
            <div className="text-3xl mb-2">📱</div>
            <h4 className="font-bold text-gray-800 mb-2">Control Remoto</h4>
            <p className="text-sm text-gray-600">
              Dashboard web completo con monitoreo en tiempo real desde cualquier dispositivo
            </p>
          </div>
        </div>
      </div>

      {/* Mercado Objetivo */}
      <div className="card bg-gradient-to-br from-blue-50 to-indigo-50">
        <h3 className="text-xl font-bold text-gray-800 mb-4 flex items-center">
          <Target className="w-6 h-6 mr-2 text-blue-600" />
          Mercado Objetivo
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <h4 className="font-bold text-blue-800 mb-3">🏡 Segmento Residencial</h4>
            <ul className="space-y-2 text-sm text-gray-700">
              <li className="flex items-start">
                <span className="text-green-500 mr-2">✓</span>
                <span>Casas de campo y zonas rurales sin red eléctrica</span>
              </li>
              <li className="flex items-start">
                <span className="text-green-500 mr-2">✓</span>
                <span>Propietarios con alto consumo eléctrico (>500 kWh/mes)</span>
              </li>
              <li className="flex items-start">
                <span className="text-green-500 mr-2">✓</span>
                <span>Familias con consciencia ambiental y tecnológica</span>
              </li>
              <li className="flex items-start">
                <span className="text-green-500 mr-2">✓</span>
                <span>Barrios privados y countries</span>
              </li>
            </ul>
          </div>
          <div>
            <h4 className="font-bold text-blue-800 mb-3">🏢 Segmento Comercial/Industrial</h4>
            <ul className="space-y-2 text-sm text-gray-700">
              <li className="flex items-start">
                <span className="text-green-500 mr-2">✓</span>
                <span>Estaciones de servicio y comercios rurales</span>
              </li>
              <li className="flex items-start">
                <span className="text-green-500 mr-2">✓</span>
                <span>Campos agrícolas y ganaderos</span>
              </li>
              <li className="flex items-start">
                <span className="text-green-500 mr-2">✓</span>
                <span>Telecomunicaciones (antenas, repetidoras)</span>
              </li>
              <li className="flex items-start">
                <span className="text-green-500 mr-2">✓</span>
                <span>Hoteles, lodges y turismo rural</span>
              </li>
            </ul>
          </div>
        </div>
      </div>

      {/* Canales de Venta */}
      <div className="card">
        <h3 className="text-xl font-bold text-gray-800 mb-4 flex items-center">
          <Globe className="w-6 h-6 mr-2 text-purple-600" />
          Canales de Comercialización
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {/* Online */}
          <div className="p-4 border-2 border-purple-200 rounded-lg hover:shadow-lg transition-shadow">
            <div className="text-2xl mb-2">🌐</div>
            <h4 className="font-bold text-gray-800 mb-2">Venta Online</h4>
            <ul className="text-sm text-gray-600 space-y-1">
              <li>• Mercado Libre Premium</li>
              <li>• Tienda online propia</li>
              <li>• Instagram/Facebook Ads</li>
              <li>• Google Ads (búsquedas)</li>
            </ul>
          </div>

          {/* Distribuidores */}
          <div className="p-4 border-2 border-green-200 rounded-lg hover:shadow-lg transition-shadow">
            <div className="text-2xl mb-2">🤝</div>
            <h4 className="font-bold text-gray-800 mb-2">Distribuidores</h4>
            <ul className="text-sm text-gray-600 space-y-1">
              <li>• Casas de electricidad</li>
              <li>• Distribuidores de paneles solares</li>
              <li>• Ferreterías industriales</li>
              <li>• Instaladores certificados</li>
            </ul>
          </div>

          {/* Ventas Directas */}
          <div className="p-4 border-2 border-blue-200 rounded-lg hover:shadow-lg transition-shadow">
            <div className="text-2xl mb-2">👔</div>
            <h4 className="font-bold text-gray-800 mb-2">B2B Directo</h4>
            <ul className="text-sm text-gray-600 space-y-1">
              <li>• Empresas de energías renovables</li>
              <li>• Licitaciones gubernamentales</li>
              <li>• Proyectos de construcción</li>
              <li>• Estudios de arquitectura</li>
            </ul>
          </div>
        </div>
      </div>

      {/* Pricing */}
      <div className="card bg-gradient-to-br from-green-50 to-emerald-50">
        <h3 className="text-xl font-bold text-gray-800 mb-4 flex items-center">
          <DollarSign className="w-6 h-6 mr-2 text-green-600" />
          Estrategia de Precios
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-white p-6 rounded-xl shadow-md border-2 border-gray-200">
            <div className="text-center mb-4">
              <h4 className="text-lg font-bold text-gray-800">BÁSICO</h4>
              <p className="text-sm text-gray-500">Sistema 3kW</p>
            </div>
            <div className="text-center mb-4">
              <p className="text-4xl font-bold text-green-600">$4,500</p>
              <p className="text-xs text-gray-500">USD</p>
            </div>
            <ul className="text-sm text-gray-600 space-y-2">
              <li className="flex items-center">
                <span className="text-green-500 mr-2">✓</span>
                Paneles solares 2kW
              </li>
              <li className="flex items-center">
                <span className="text-green-500 mr-2">✓</span>
                Turbina eólica 1kW
              </li>
              <li className="flex items-center">
                <span className="text-green-500 mr-2">✓</span>
                Batería 5kWh
              </li>
              <li className="flex items-center">
                <span className="text-green-500 mr-2">✓</span>
                Inversor inteligente
              </li>
              <li className="flex items-center">
                <span className="text-green-500 mr-2">✓</span>
                Dashboard web
              </li>
            </ul>
          </div>

          <div className="bg-gradient-to-br from-blue-500 to-purple-600 p-6 rounded-xl shadow-lg text-white transform scale-105">
            <div className="text-center mb-4">
              <div className="inline-block bg-yellow-400 text-blue-900 px-3 py-1 rounded-full text-xs font-bold mb-2">
                MÁS VENDIDO
              </div>
              <h4 className="text-lg font-bold">PROFESIONAL</h4>
              <p className="text-sm text-blue-100">Sistema 6kW</p>
            </div>
            <div className="text-center mb-4">
              <p className="text-4xl font-bold">$8,900</p>
              <p className="text-xs text-blue-200">USD</p>
            </div>
            <ul className="text-sm space-y-2">
              <li className="flex items-center">
                <span className="text-yellow-300 mr-2">✓</span>
                Paneles solares 4kW
              </li>
              <li className="flex items-center">
                <span className="text-yellow-300 mr-2">✓</span>
                Turbina eólica 2kW
              </li>
              <li className="flex items-center">
                <span className="text-yellow-300 mr-2">✓</span>
                Batería 10kWh
              </li>
              <li className="flex items-center">
                <span className="text-yellow-300 mr-2">✓</span>
                Inversor inteligente Pro
              </li>
              <li className="flex items-center">
                <span className="text-yellow-300 mr-2">✓</span>
                IA Predictiva avanzada
              </li>
            </ul>
          </div>

          <div className="bg-white p-6 rounded-xl shadow-md border-2 border-gray-200">
            <div className="text-center mb-4">
              <h4 className="text-lg font-bold text-gray-800">INDUSTRIAL</h4>
              <p className="text-sm text-gray-500">Sistema 10kW+</p>
            </div>
            <div className="text-center mb-4">
              <p className="text-4xl font-bold text-purple-600">$15,000</p>
              <p className="text-xs text-gray-500">USD+</p>
            </div>
            <ul className="text-sm text-gray-600 space-y-2">
              <li className="flex items-center">
                <span className="text-green-500 mr-2">✓</span>
                Paneles solares 6-8kW
              </li>
              <li className="flex items-center">
                <span className="text-green-500 mr-2">✓</span>
                Turbinas eólicas 4kW
              </li>
              <li className="flex items-center">
                <span className="text-green-500 mr-2">✓</span>
                Batería 20kWh+
              </li>
              <li className="flex items-center">
                <span className="text-green-500 mr-2">✓</span>
                Inversores redundantes
              </li>
              <li className="flex items-center">
                <span className="text-green-500 mr-2">✓</span>
                Soporte 24/7
              </li>
            </ul>
          </div>
        </div>
      </div>

      {/* ROI y Beneficios */}
      <div className="card">
        <h3 className="text-xl font-bold text-gray-800 mb-4 flex items-center">
          <TrendingUp className="w-6 h-6 mr-2 text-orange-600" />
          Retorno de Inversión (ROI)
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <h4 className="font-bold text-gray-800 mb-3">💰 Análisis Económico</h4>
            <div className="space-y-3 text-sm">
              <div className="flex justify-between p-3 bg-green-50 rounded-lg">
                <span className="text-gray-700">Ahorro mensual promedio:</span>
                <span className="font-bold text-green-600">$150-300 USD</span>
              </div>
              <div className="flex justify-between p-3 bg-blue-50 rounded-lg">
                <span className="text-gray-700">Recuperación inversión:</span>
                <span className="font-bold text-blue-600">3-5 años</span>
              </div>
              <div className="flex justify-between p-3 bg-purple-50 rounded-lg">
                <span className="text-gray-700">Vida útil sistema:</span>
                <span className="font-bold text-purple-600">20-25 años</span>
              </div>
              <div className="flex justify-between p-3 bg-orange-50 rounded-lg">
                <span className="text-gray-700">ROI total:</span>
                <span className="font-bold text-orange-600">400-600%</span>
              </div>
            </div>
          </div>
          <div>
            <h4 className="font-bold text-gray-800 mb-3">🌱 Beneficios Adicionales</h4>
            <ul className="space-y-2 text-sm text-gray-700">
              <li className="flex items-start p-2 bg-green-50 rounded">
                <span className="text-green-600 mr-2">✓</span>
                <span><strong>Independencia energética:</strong> No más cortes de luz</span>
              </li>
              <li className="flex items-start p-2 bg-blue-50 rounded">
                <span className="text-blue-600 mr-2">✓</span>
                <span><strong>Revalorización propiedad:</strong> +15-20% valor inmueble</span>
              </li>
              <li className="flex items-start p-2 bg-purple-50 rounded">
                <span className="text-purple-600 mr-2">✓</span>
                <span><strong>Impacto ambiental:</strong> -3 toneladas CO₂/año</span>
              </li>
              <li className="flex items-start p-2 bg-yellow-50 rounded">
                <span className="text-yellow-600 mr-2">✓</span>
                <span><strong>Incentivos fiscales:</strong> Deducciones impositivas disponibles</span>
              </li>
            </ul>
          </div>
        </div>
      </div>

      {/* Call to Action */}
      <div className="card bg-gradient-to-br from-orange-500 to-red-600 text-white">
        <div className="text-center">
          <h3 className="text-2xl font-bold mb-4">¿Listo para Vender?</h3>
          <p className="text-orange-100 mb-6">
            Contacto comercial y canales de distribución
          </p>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="bg-white bg-opacity-20 p-4 rounded-lg">
              <p className="font-bold mb-2">📧 Email</p>
              <p className="text-sm">ventas@inversorinteligente.com</p>
            </div>
            <div className="bg-white bg-opacity-20 p-4 rounded-lg">
              <p className="font-bold mb-2">📱 WhatsApp</p>
              <p className="text-sm">+54 9 11 1234-5678</p>
            </div>
            <div className="bg-white bg-opacity-20 p-4 rounded-lg">
              <p className="font-bold mb-2">🌐 Web</p>
              <p className="text-sm">www.inversorinteligente.com</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default MarketingInfo;
