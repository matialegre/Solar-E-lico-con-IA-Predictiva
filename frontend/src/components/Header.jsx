import React from 'react';
import { Zap, Activity, Wifi, WifiOff } from 'lucide-react';

const Header = ({ systemStatus, connected }) => {
  return (
    <header className="bg-white shadow-md">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo y Título */}
          <div className="flex items-center space-x-3">
            <Zap className="w-8 h-8 text-blue-600" />
            <div>
              <h1 className="text-2xl font-bold text-gray-900">
                Sistema Híbrido Inteligente
              </h1>
              <p className="text-sm text-gray-600">
                Solar + Eólico con IA Predictiva
              </p>
            </div>
          </div>

          {/* Estado del Sistema */}
          <div className="flex items-center space-x-6">
            {/* Estado de conexión */}
            <div className="flex items-center space-x-2">
              {connected ? (
                <>
                  <Wifi className="w-5 h-5 text-green-600" />
                  <span className="text-sm font-medium text-green-600">
                    Conectado
                  </span>
                </>
              ) : (
                <>
                  <WifiOff className="w-5 h-5 text-red-600" />
                  <span className="text-sm font-medium text-red-600">
                    Desconectado
                  </span>
                </>
              )}
            </div>

            {/* Estado general */}
            {systemStatus && (
              <div className="flex items-center space-x-2">
                <div className="relative">
                  <Activity className="w-5 h-5 text-blue-600" />
                  {systemStatus.status === 'online' && (
                    <span className="absolute -top-1 -right-1 w-2 h-2 bg-green-500 rounded-full animate-pulse"></span>
                  )}
                </div>
                <div className="text-left">
                  <p className="text-xs text-gray-500">Estado</p>
                  <p className="text-sm font-medium text-gray-900 capitalize">
                    {systemStatus.status}
                  </p>
                </div>
              </div>
            )}

            {/* Modo de simulación */}
            {systemStatus?.simulation_mode && (
              <div className="badge badge-warning">
                🔬 Modo Simulación
              </div>
            )}

            {/* Versión */}
            <div className="text-xs text-gray-500">
              v{systemStatus?.version || '1.0.0'}
            </div>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
