import React, { useState } from 'react';
import { Code, Cpu, Database, Zap, Wifi, Brain, CheckCircle, ExternalLink } from 'lucide-react';

const ProjectInfo = () => {
  const [activeTab, setActiveTab] = useState('frontend');

  const techStack = {
    frontend: [
      { name: 'React 18', desc: 'Framework principal', icon: '⚛️' },
      { name: 'Axios', desc: 'Cliente HTTP', icon: '🌐' },
      { name: 'Lucide React', desc: 'Iconos', icon: '🎨' },
      { name: 'TailwindCSS', desc: 'Estilos', icon: '💅' },
      { name: 'React Router', desc: 'Navegación', icon: '🧭' }
    ],
    backend: [
      { name: 'FastAPI', desc: 'Framework REST API', icon: '⚡' },
      { name: 'Python 3.12', desc: 'Lenguaje backend', icon: '🐍' },
      { name: 'SQLAlchemy', desc: 'ORM Base de datos', icon: '🗄️' },
      { name: 'scikit-learn', desc: 'Machine Learning', icon: '🧠' },
      { name: 'Uvicorn', desc: 'Servidor ASGI', icon: '🚀' },
      { name: 'Pydantic', desc: 'Validación de datos', icon: '✅' }
    ],
    firmware: [
      { name: 'ESP32', desc: 'Microcontrolador WiFi', icon: '📡' },
      { name: 'Arduino IDE', desc: 'Desarrollo firmware', icon: '⚙️' },
      { name: 'ESPAsyncWebServer', desc: 'Servidor web local', icon: '🌐' },
      { name: 'ArduinoJson', desc: 'Parseo JSON', icon: '📄' },
      { name: 'AsyncTCP', desc: 'Conexiones asíncronas', icon: '🔗' }
    ],
    ml: [
      { name: 'Random Forest', desc: 'Modelo de predicción', icon: '🌲' },
      { name: 'NASA POWER API', desc: 'Datos climáticos históricos', icon: '🛰️' },
      { name: 'scikit-learn', desc: 'Librería ML', icon: '🧠' },
      { name: 'NumPy', desc: 'Cálculos numéricos', icon: '🔢' },
      { name: 'Pandas', desc: 'Procesamiento de datos', icon: '🐼' }
    ]
  };

  const features = [
    { name: 'Panel ESP32 en tiempo real', desc: 'Monitoreo de dispositivos conectados', status: '✅' },
    { name: 'Wizard de configuración', desc: '4 pasos para setup inicial', status: '✅' },
    { name: 'Modelo ML con scikit-learn', desc: 'Random Forest para predicciones', status: '✅' },
    { name: 'NASA POWER Integration', desc: 'Datos climáticos reales (5 años)', status: '✅' },
    { name: 'Web local ESP32', desc: 'Dashboard en el router local', status: '✅' },
    { name: 'Recomendaciones inteligentes', desc: 'Basadas en ubicación y clima', status: '✅' },
    { name: 'Mapa interactivo', desc: 'Selección de ubicación con lat/long', status: '✅' },
    { name: 'Configuración persistente', desc: 'Guardado en backend + localStorage', status: '✅' },
    { name: 'API REST completa', desc: 'Endpoints para todas las funciones', status: '✅' },
    { name: 'Fallback automático', desc: 'Si ML falla, usa cálculos tradicionales', status: '✅' }
  ];

  const architecture = [
    { layer: 'Frontend', tech: 'React (Puerto 11113)', color: 'from-blue-500 to-blue-600' },
    { layer: 'Backend', tech: 'FastAPI (Puerto 11112)', color: 'from-green-500 to-green-600' },
    { layer: 'ML Engine', tech: 'scikit-learn Random Forest', color: 'from-purple-500 to-purple-600' },
    { layer: 'Data Source', tech: 'NASA POWER API', color: 'from-orange-500 to-orange-600' },
    { layer: 'IoT Device', tech: 'ESP32 (Web local puerto 80)', color: 'from-red-500 to-red-600' }
  ];

  return (
    <div className="card">
      <div className="mb-6">
        <h2 className="text-3xl font-bold text-gray-800 mb-2 flex items-center">
          <Code className="w-8 h-8 mr-3 text-indigo-600" />
          Información del Proyecto
        </h2>
        <p className="text-gray-600">
          Sistema completo de gestión inteligente de energía con ML
        </p>
      </div>

      {/* Arquitectura */}
      <div className="mb-8">
        <h3 className="text-xl font-bold text-gray-800 mb-4 flex items-center">
          <Database className="w-5 h-5 mr-2" />
          Arquitectura del Sistema
        </h3>
        <div className="space-y-2">
          {architecture.map((item, idx) => (
            <div 
              key={idx}
              className={`p-4 rounded-lg bg-gradient-to-r ${item.color} text-white shadow-md`}
            >
              <div className="flex justify-between items-center">
                <span className="font-bold">{item.layer}</span>
                <span className="text-sm opacity-90">{item.tech}</span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Tech Stack Tabs */}
      <div className="mb-8">
        <h3 className="text-xl font-bold text-gray-800 mb-4 flex items-center">
          <Cpu className="w-5 h-5 mr-2" />
          Stack Tecnológico
        </h3>
        
        <div className="flex gap-2 mb-4 flex-wrap">
          {Object.keys(techStack).map((tab) => (
            <button
              key={tab}
              onClick={() => setActiveTab(tab)}
              className={`px-4 py-2 rounded-lg font-semibold transition ${
                activeTab === tab
                  ? 'bg-indigo-600 text-white'
                  : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
              }`}
            >
              {tab.charAt(0).toUpperCase() + tab.slice(1)}
            </button>
          ))}
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {techStack[activeTab].map((tech, idx) => (
            <div key={idx} className="p-4 bg-gray-50 rounded-lg border border-gray-200">
              <div className="flex items-center mb-2">
                <span className="text-2xl mr-3">{tech.icon}</span>
                <h4 className="font-bold text-gray-800">{tech.name}</h4>
              </div>
              <p className="text-sm text-gray-600">{tech.desc}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Features */}
      <div className="mb-8">
        <h3 className="text-xl font-bold text-gray-800 mb-4 flex items-center">
          <Zap className="w-5 h-5 mr-2" />
          Características Implementadas
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          {features.map((feature, idx) => (
            <div key={idx} className="flex items-start p-3 bg-green-50 rounded-lg border border-green-200">
              <CheckCircle className="w-5 h-5 text-green-600 mr-3 flex-shrink-0 mt-0.5" />
              <div>
                <h4 className="font-semibold text-gray-800">{feature.name}</h4>
                <p className="text-sm text-gray-600">{feature.desc}</p>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Especificaciones */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="p-4 bg-gradient-to-br from-blue-50 to-indigo-50 rounded-lg">
          <h4 className="font-bold text-gray-800 mb-2 flex items-center">
            <Brain className="w-5 h-5 mr-2 text-blue-600" />
            Machine Learning
          </h4>
          <ul className="text-sm space-y-1 text-gray-700">
            <li>• Random Forest (50 árboles)</li>
            <li>• 1000 datos de entrenamiento</li>
            <li>• Predicción solar y eólica</li>
            <li>• Fallback automático</li>
          </ul>
        </div>

        <div className="p-4 bg-gradient-to-br from-green-50 to-emerald-50 rounded-lg">
          <h4 className="font-bold text-gray-800 mb-2 flex items-center">
            <Wifi className="w-5 h-5 mr-2 text-green-600" />
            Conectividad
          </h4>
          <ul className="text-sm space-y-1 text-gray-700">
            <li>• API REST (FastAPI)</li>
            <li>• WebSocket (deshabilitado)</li>
            <li>• HTTP ESP32 → Servidor</li>
            <li>• Web local ESP32 (puerto 80)</li>
          </ul>
        </div>

        <div className="p-4 bg-gradient-to-br from-purple-50 to-pink-50 rounded-lg">
          <h4 className="font-bold text-gray-800 mb-2 flex items-center">
            <Database className="w-5 h-5 mr-2 text-purple-600" />
            Datos
          </h4>
          <ul className="text-sm space-y-1 text-gray-700">
            <li>• NASA POWER API</li>
            <li>• 5 años histórico</li>
            <li>• Promedios estacionales</li>
            <li>• Configuración persistente</li>
          </ul>
        </div>
      </div>

      {/* Enlaces */}
      <div className="mt-6 p-4 bg-gray-50 rounded-lg">
        <h4 className="font-bold text-gray-800 mb-3">📚 Recursos</h4>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
          <a href="http://190.211.201.217:11112/docs" target="_blank" rel="noopener noreferrer" 
             className="flex items-center text-sm text-indigo-600 hover:text-indigo-800">
            <ExternalLink className="w-4 h-4 mr-2" />
            API Documentation (FastAPI Docs)
          </a>
          <a href="https://power.larc.nasa.gov/" target="_blank" rel="noopener noreferrer"
             className="flex items-center text-sm text-indigo-600 hover:text-indigo-800">
            <ExternalLink className="w-4 h-4 mr-2" />
            NASA POWER API
          </a>
        </div>
      </div>

      {/* Footer */}
      <div className="mt-6 pt-4 border-t border-gray-200 text-center text-sm text-gray-600">
        <p>🚀 Sistema desarrollado con tecnologías modernas y ML real</p>
        <p className="mt-1">© 2025 - Inversor Híbrido Inteligente</p>
      </div>
    </div>
  );
};

export default ProjectInfo;
