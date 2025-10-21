import React from 'react';
import { 
  AlertTriangle, 
  AlertCircle, 
  Info, 
  CheckCircle2,
  X 
} from 'lucide-react';

const AlertItem = ({ alert }) => {
  const severityConfig = {
    critical: {
      icon: AlertTriangle,
      bgColor: 'bg-red-50',
      borderColor: 'border-red-300',
      textColor: 'text-red-800',
      iconColor: 'text-red-600',
    },
    warning: {
      icon: AlertCircle,
      bgColor: 'bg-yellow-50',
      borderColor: 'border-yellow-300',
      textColor: 'text-yellow-800',
      iconColor: 'text-yellow-600',
    },
    info: {
      icon: Info,
      bgColor: 'bg-blue-50',
      borderColor: 'border-blue-300',
      textColor: 'text-blue-800',
      iconColor: 'text-blue-600',
    },
  };

  const config = severityConfig[alert.severity] || severityConfig.info;
  const Icon = config.icon;

  return (
    <div className={`p-4 rounded-lg border ${config.bgColor} ${config.borderColor}`}>
      <div className="flex items-start">
        <Icon className={`w-5 h-5 ${config.iconColor} mt-0.5 mr-3 flex-shrink-0`} />
        <div className="flex-1">
          <div className="flex items-start justify-between">
            <div>
              <h4 className={`font-semibold ${config.textColor}`}>
                {alert.type.replace(/_/g, ' ').toUpperCase()}
              </h4>
              <p className={`text-sm ${config.textColor} mt-1`}>
                {alert.message}
              </p>
              {alert.action && (
                <p className={`text-xs ${config.textColor} mt-2 font-medium`}>
                  💡 {alert.action}
                </p>
              )}
            </div>
            <button className="text-gray-400 hover:text-gray-600">
              <X className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

const AlertsPanel = ({ alerts }) => {
  if (!alerts || alerts.length === 0) {
    return (
      <div className="card">
        <h3 className="card-title">Alertas del Sistema</h3>
        <div className="flex items-center justify-center py-8">
          <div className="text-center">
            <CheckCircle2 className="w-12 h-12 text-green-500 mx-auto mb-3" />
            <p className="text-gray-600 font-medium">
              No hay alertas activas
            </p>
            <p className="text-sm text-gray-500 mt-1">
              El sistema está funcionando correctamente
            </p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="card">
      <h3 className="card-title flex items-center justify-between">
        <span>Alertas del Sistema</span>
        <span className="badge badge-danger">{alerts.length}</span>
      </h3>
      <div className="space-y-3">
        {alerts.map((alert, index) => (
          <AlertItem key={index} alert={alert} />
        ))}
      </div>
    </div>
  );
};

export default AlertsPanel;
