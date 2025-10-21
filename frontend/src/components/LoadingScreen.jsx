import React, { useEffect, useState } from 'react';
import { Zap, Sun, Wind, Battery, Activity } from 'lucide-react';

const LoadingScreen = () => {
  const [progress, setProgress] = useState(0);
  const [loadingText, setLoadingText] = useState('Iniciando sistema...');

  useEffect(() => {
    const messages = [
      'Conectando con sensores...',
      'Cargando datos meteorológicos...',
      'Inicializando sistema...',
      'Listo'
    ];

    let currentMessage = 0;
    const messageInterval = setInterval(() => {
      if (currentMessage < messages.length) {
        setLoadingText(messages[currentMessage]);
        currentMessage++;
      }
    }, 200);

    const progressInterval = setInterval(() => {
      setProgress(prev => {
        if (prev >= 100) {
          clearInterval(progressInterval);
          return 100;
        }
        return prev + 10;
      });
    }, 50);

    return () => {
      clearInterval(messageInterval);
      clearInterval(progressInterval);
    };
  }, []);

  return (
    <div className="fixed inset-0 bg-gradient-to-br from-gray-900 via-blue-900 to-purple-900 flex items-center justify-center z-50">
      {/* Fondo animado */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute top-20 left-20 w-96 h-96 bg-blue-500 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-pulse"></div>
        <div className="absolute bottom-20 right-20 w-96 h-96 bg-purple-500 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-pulse" style={{ animationDelay: '1s' }}></div>
        <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-green-500 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-pulse" style={{ animationDelay: '2s' }}></div>
      </div>

      {/* Contenido */}
      <div className="relative z-10 text-center px-8">
        {/* Logo/Icono principal */}
        <div className="mb-8 relative">
          <div className="inline-block relative">
            {/* Círculo exterior rotando */}
            <div className="absolute inset-0 animate-spin" style={{ animationDuration: '3s' }}>
              <Sun className="w-32 h-32 text-yellow-400 opacity-30" />
            </div>
            
            
            {/* Icono central pulsante */}
            <div className="relative animate-pulse">
              <Zap className="w-32 h-32 text-green-400 drop-shadow-2xl" />
            </div>
          </div>
        </div>

        {/* Título */}
        <h1 className="text-5xl font-bold text-white mb-4 tracking-wider">
          SISTEMA HÍBRIDO INTELIGENTE
        </h1>
        <p className="text-xl text-blue-300 mb-12 font-light">
          Solar + Eólico con IA Predictiva
        </p>

        {/* Indicadores de estado */}
        <div className="flex justify-center gap-6 mb-8">
          <div className="flex flex-col items-center">
            <Sun className="w-10 h-10 text-yellow-400 mb-2 animate-pulse" />
            <span className="text-sm text-gray-300 font-medium">Solar</span>
          </div>
          <div className="flex flex-col items-center">
            <Wind className="w-10 h-10 text-blue-400 mb-2 animate-pulse" style={{ animationDelay: '0.2s' }} />
            <span className="text-sm text-gray-300 font-medium">Eólica</span>
          </div>
          <div className="flex flex-col items-center">
            <Battery className="w-10 h-10 text-green-400 mb-2 animate-pulse" style={{ animationDelay: '0.4s' }} />
            <span className="text-sm text-gray-300 font-medium">Batería</span>
          </div>
          <div className="flex flex-col items-center">
            <Activity className="w-10 h-10 text-purple-400 mb-2 animate-pulse" style={{ animationDelay: '0.6s' }} />
            <span className="text-sm text-gray-300 font-medium">IA</span>
          </div>
        </div>

        {/* Barra de progreso */}
        <div className="w-96 max-w-full mx-auto mb-6">
          <div className="bg-gray-800 rounded-full h-3 overflow-hidden shadow-inner">
            <div 
              className="bg-gradient-to-r from-green-400 via-blue-400 to-purple-500 h-full transition-all duration-300 ease-out rounded-full relative overflow-hidden"
              style={{ width: `${progress}%` }}
            >
              {/* Efecto de brillo */}
              <div className="absolute inset-0 bg-white opacity-30 animate-pulse"></div>
            </div>
          </div>
          <div className="mt-3 text-sm text-gray-400 flex justify-between">
            <span>{loadingText}</span>
            <span className="font-mono text-blue-400">{progress}%</span>
          </div>
        </div>

        {/* Versión */}
        <p className="text-xs text-gray-500 mt-8">
          v1.0.0 | Bahía Blanca, Argentina
        </p>
      </div>
    </div>
  );
};

export default LoadingScreen;
