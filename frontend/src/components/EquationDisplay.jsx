/**
 * Componente para mostrar ecuaciones paso a paso
 */

import React from 'react';

export default function EquationDisplay({ calculos }) {
  if (!calculos) return null;

  return (
    <div className="space-y-3">
      {Object.entries(calculos).map(([key, paso]) => (
        <div key={key} className="p-4 bg-gray-900 rounded border-l-4 border-blue-500">
          <div className="flex items-start gap-3">
            <div className="bg-blue-500 text-white w-8 h-8 rounded-full flex items-center justify-center font-bold flex-shrink-0">
              {key.replace('paso', '')}
            </div>
            <div className="flex-1">
              <h4 className="font-bold mb-1">{paso.nombre}</h4>
              <div className="text-sm space-y-1">
                <p className="text-blue-400 font-mono">{paso.ecuacion}</p>
                <p className="text-gray-400 font-mono text-xs">{paso.valores}</p>
                <p className="text-green-400 font-bold">→ {paso.resultado}</p>
              </div>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}
