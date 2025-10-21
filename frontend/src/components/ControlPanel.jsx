import React, { useState } from 'react';
import { 
  Power, 
  Settings, 
  Cpu, 
  AlertTriangle,
  CheckCircle2 
} from 'lucide-react';
import { setManualControl, setAutoMode } from '../api/api';

const ControlPanel = ({ autoMode, onAutoModeChange }) => {
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');

  const handleAutoModeToggle = async () => {
    setLoading(true);
    try {
      const result = await setAutoMode(!autoMode);
      setMessage(result.message);
      onAutoModeChange(!autoMode);
      setTimeout(() => setMessage(''), 3000);
    } catch (error) {
      setMessage('Error al cambiar modo: ' + error.message);
    } finally {
      setLoading(false);
    }
  };

  const handleSourceControl = async (source, action) => {
    setLoading(true);
    try {
      const result = await setManualControl(source, action);
      setMessage(result.message);
      setTimeout(() => setMessage(''), 3000);
    } catch (error) {
      setMessage('Error: ' + error.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card">
      <h3 className="card-title flex items-center">
        <Settings className="w-5 h-5 mr-2" />
        Panel de Control
      </h3>

      {/* Modo Automático */}
      <div className="mb-6 p-4 bg-gradient-to-r from-blue-50 to-indigo-50 rounded-lg border border-blue-200">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <Cpu className={`w-6 h-6 ${autoMode ? 'text-green-600' : 'text-gray-400'}`} />
            <div>
              <h4 className="font-semibold text-gray-900">Modo Automático IA</h4>
              <p className="text-sm text-gray-600">
                {autoMode 
                  ? 'La IA está controlando las fuentes de energía'
                  : 'Control manual activo'}
              </p>
            </div>
          </div>
          <button
            onClick={handleAutoModeToggle}
            disabled={loading}
            className={`switch ${autoMode ? 'enabled' : 'disabled'}`}
          >
            <span className="switch-toggle" />
          </button>
        </div>
      </div>

      {/* Control Manual */}
      {!autoMode && (
        <div className="space-y-4">
          <div className="flex items-center space-x-2 mb-3">
            <AlertTriangle className="w-5 h-5 text-yellow-600" />
            <p className="text-sm text-yellow-700 font-medium">
              Control manual activo - Las decisiones automáticas están deshabilitadas
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {/* Solar */}
            <div className="p-4 border border-gray-200 rounded-lg hover:border-blue-400 transition-colors">
              <div className="flex items-center justify-between mb-3">
                <span className="font-medium text-gray-900">☀️ Solar</span>
                <span className="badge badge-info">Renovable</span>
              </div>
              <div className="flex space-x-2">
                <button
                  onClick={() => handleSourceControl('solar', 'enable')}
                  disabled={loading}
                  className="btn btn-success flex-1 text-sm"
                >
                  <Power className="w-4 h-4 mr-1" />
                  Activar
                </button>
                <button
                  onClick={() => handleSourceControl('solar', 'disable')}
                  disabled={loading}
                  className="btn btn-secondary flex-1 text-sm"
                >
                  Desactivar
                </button>
              </div>
            </div>

            {/* Eólica */}
            <div className="p-4 border border-gray-200 rounded-lg hover:border-blue-400 transition-colors">
              <div className="flex items-center justify-between mb-3">
                <span className="font-medium text-gray-900">🌬️ Eólica</span>
                <span className="badge badge-info">Renovable</span>
              </div>
              <div className="flex space-x-2">
                <button
                  onClick={() => handleSourceControl('wind', 'enable')}
                  disabled={loading}
                  className="btn btn-success flex-1 text-sm"
                >
                  <Power className="w-4 h-4 mr-1" />
                  Activar
                </button>
                <button
                  onClick={() => handleSourceControl('wind', 'disable')}
                  disabled={loading}
                  className="btn btn-secondary flex-1 text-sm"
                >
                  Desactivar
                </button>
              </div>
            </div>

            {/* Batería */}
            <div className="p-4 border border-gray-200 rounded-lg hover:border-blue-400 transition-colors">
              <div className="flex items-center justify-between mb-3">
                <span className="font-medium text-gray-900">🔋 Batería</span>
                <span className="badge badge-success">Almacenamiento</span>
              </div>
              <div className="flex space-x-2">
                <button
                  onClick={() => handleSourceControl('battery', 'enable')}
                  disabled={loading}
                  className="btn btn-success flex-1 text-sm"
                >
                  <Power className="w-4 h-4 mr-1" />
                  Activar
                </button>
                <button
                  onClick={() => handleSourceControl('battery', 'disable')}
                  disabled={loading}
                  className="btn btn-secondary flex-1 text-sm"
                >
                  Desactivar
                </button>
              </div>
            </div>

            {/* Red */}
            <div className="p-4 border border-gray-200 rounded-lg hover:border-blue-400 transition-colors">
              <div className="flex items-center justify-between mb-3">
                <span className="font-medium text-gray-900">⚡ Red Eléctrica</span>
                <span className="badge badge-warning">Externa</span>
              </div>
              <div className="flex space-x-2">
                <button
                  onClick={() => handleSourceControl('grid', 'enable')}
                  disabled={loading}
                  className="btn btn-success flex-1 text-sm"
                >
                  <Power className="w-4 h-4 mr-1" />
                  Conectar
                </button>
                <button
                  onClick={() => handleSourceControl('grid', 'disable')}
                  disabled={loading}
                  className="btn btn-secondary flex-1 text-sm"
                >
                  Desconectar
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Mensaje de estado */}
      {message && (
        <div className="mt-4 p-3 bg-blue-50 border border-blue-200 rounded-lg">
          <div className="flex items-center">
            <CheckCircle2 className="w-5 h-5 text-blue-600 mr-2" />
            <p className="text-sm text-blue-800">{message}</p>
          </div>
        </div>
      )}
    </div>
  );
};

export default ControlPanel;
