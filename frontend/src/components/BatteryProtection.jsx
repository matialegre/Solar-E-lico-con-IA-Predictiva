import React from 'react';
import { Battery, Shield, AlertTriangle, CheckCircle, Zap, Sun, Wind, Power } from 'lucide-react';

const BatteryProtection = ({ energyData }) => {
  if (!energyData) {
    return (
      <div className="card animate-pulse">
        <div className="h-48 bg-gray-200 rounded"></div>
      </div>
    );
  }

  const {
    battery_soc_percent = 50,
    battery_power_w = 0,
    solar_power_w = 0,
    wind_power_w = 0,
    load_power_w = 0,
    total_generation_w = 0
  } = energyData;

  // Zona óptima de batería: 25-80%
  const isOptimalZone = battery_soc_percent >= 25 && battery_soc_percent <= 80;
  const isLowBattery = battery_soc_percent < 25;
  const isHighBattery = battery_soc_percent > 80;

  // Estados de relés (simulado - en producción vendría del ESP32)
  const solarConnected = solar_power_w > 10;
  const windConnected = wind_power_w > 10;
  const batteryCharging = battery_power_w > 0;
  const batteryDischarging = battery_power_w < 0;

  // Prioridad de fuentes (lo ideal: Solar/Eólica → Batería solo si es necesario)
  const directPowerFromRenewables = total_generation_w;
  const powerFromBattery = batteryDischarging ? Math.abs(battery_power_w) : 0;
  const renewablesCoverage = load_power_w > 0 ? ((directPowerFromRenewables / load_power_w) * 100) : 0;

  return (
    <div className="space-y-6">
      {/* Estado de Batería - Visual Grande */}
      <div className={`rounded-2xl shadow-xl p-6 ${
        isOptimalZone 
          ? 'bg-gradient-to-br from-green-500 to-emerald-600' 
          : isLowBattery
            ? 'bg-gradient-to-br from-yellow-500 to-orange-600'
            : 'bg-gradient-to-br from-blue-500 to-indigo-600'
      } text-white`}>
        <div className="flex items-center justify-between mb-6">
          <div>
            <h2 className="text-3xl font-bold mb-2 flex items-center">
              <Battery className="w-8 h-8 mr-3" />
              Protección de Batería
            </h2>
            <p className="text-sm opacity-90">
              {isOptimalZone && '✅ Zona óptima (25-80%) - Máxima vida útil'}
              {isLowBattery && '⚠️ Batería baja - Cargando prioritariamente'}
              {isHighBattery && '🔋 Batería cargada - Usando renovables directamente'}
            </p>
          </div>
          <Shield className="w-16 h-16 opacity-50" />
        </div>

        {/* Barra de batería visual */}
        <div className="bg-white bg-opacity-20 rounded-lg p-4 mb-4">
          <div className="flex justify-between items-center mb-2">
            <span className="text-sm font-medium">Nivel de Carga</span>
            <span className="text-2xl font-black">{battery_soc_percent.toFixed(1)}%</span>
          </div>
          
          {/* Barra de progreso con zonas */}
          <div className="relative h-8 bg-white bg-opacity-30 rounded-full overflow-hidden">
            {/* Zona peligrosa (0-25%) */}
            <div className="absolute left-0 h-full bg-red-500 bg-opacity-30" style={{ width: '25%' }}></div>
            {/* Zona óptima (25-80%) */}
            <div className="absolute left-1/4 h-full bg-green-500 bg-opacity-30" style={{ width: '55%' }}></div>
            {/* Zona alta (80-100%) */}
            <div className="absolute right-0 h-full bg-blue-500 bg-opacity-30" style={{ width: '20%' }}></div>
            
            {/* Nivel actual */}
            <div 
              className="absolute left-0 h-full bg-white transition-all duration-500 flex items-center justify-end pr-2"
              style={{ width: `${battery_soc_percent}%` }}
            >
              {battery_soc_percent > 10 && (
                <Battery className="w-5 h-5 text-gray-900" />
              )}
            </div>
          </div>
          
          {/* Marcadores de zona */}
          <div className="flex justify-between text-xs mt-1 opacity-75">
            <span>0%</span>
            <span className="text-yellow-200">25%</span>
            <span>50%</span>
            <span className="text-blue-200">80%</span>
            <span>100%</span>
          </div>
        </div>

        {/* Estado actual de batería */}
        <div className="grid grid-cols-3 gap-3">
          <div className="bg-white bg-opacity-20 rounded-lg p-3 text-center">
            <p className="text-xs opacity-75 mb-1">Estado</p>
            <p className="text-sm font-bold">
              {batteryCharging && '🔋 Cargando'}
              {batteryDischarging && '⚡ Descargando'}
              {!batteryCharging && !batteryDischarging && '⏸️ En reposo'}
            </p>
          </div>
          <div className="bg-white bg-opacity-20 rounded-lg p-3 text-center">
            <p className="text-xs opacity-75 mb-1">Potencia</p>
            <p className="text-sm font-bold">{Math.abs(battery_power_w).toFixed(0)} W</p>
          </div>
          <div className="bg-white bg-opacity-20 rounded-lg p-3 text-center">
            <p className="text-xs opacity-75 mb-1">Prioridad</p>
            <p className="text-sm font-bold">
              {renewablesCoverage >= 90 ? '🌱 Renovables' : '🔋 Batería'}
            </p>
          </div>
        </div>
      </div>

      {/* Estrategia de Uso de Energía */}
      <div className="bg-white rounded-xl shadow-lg p-6">
        <h3 className="text-xl font-bold text-gray-900 mb-4 flex items-center">
          <Zap className="w-6 h-6 mr-2 text-yellow-600" />
          Estrategia de Uso de Energía
        </h3>
        
        <div className="space-y-4">
          {/* Prioridad 1: Solar/Eólica Directo */}
          <div className={`p-4 rounded-lg border-2 ${
            renewablesCoverage >= 90 
              ? 'bg-green-50 border-green-500' 
              : 'bg-gray-50 border-gray-300'
          }`}>
            <div className="flex items-center justify-between mb-2">
              <div className="flex items-center">
                <div className={`w-8 h-8 rounded-full flex items-center justify-center mr-3 ${
                  renewablesCoverage >= 90 ? 'bg-green-500' : 'bg-gray-400'
                }`}>
                  <span className="text-white font-bold">1</span>
                </div>
                <div>
                  <p className="font-bold text-gray-900">Uso Directo de Renovables</p>
                  <p className="text-xs text-gray-600">Solar + Eólica → Casa (SIN usar batería)</p>
                </div>
              </div>
              {renewablesCoverage >= 90 && <CheckCircle className="w-6 h-6 text-green-600" />}
            </div>
            <div className="ml-11">
              <div className="flex justify-between text-sm mb-1">
                <span className="text-gray-600">Cobertura renovables:</span>
                <span className="font-bold text-green-600">{renewablesCoverage.toFixed(0)}%</span>
              </div>
              <div className="h-2 bg-gray-200 rounded-full overflow-hidden">
                <div 
                  className="h-full bg-green-500 transition-all duration-500"
                  style={{ width: `${Math.min(renewablesCoverage, 100)}%` }}
                ></div>
              </div>
            </div>
          </div>

          {/* Prioridad 2: Excedente a Batería (si está entre 25-80%) */}
          <div className={`p-4 rounded-lg border-2 ${
            batteryCharging && isOptimalZone
              ? 'bg-blue-50 border-blue-500' 
              : 'bg-gray-50 border-gray-300'
          }`}>
            <div className="flex items-center justify-between mb-2">
              <div className="flex items-center">
                <div className={`w-8 h-8 rounded-full flex items-center justify-center mr-3 ${
                  batteryCharging && isOptimalZone ? 'bg-blue-500' : 'bg-gray-400'
                }`}>
                  <span className="text-white font-bold">2</span>
                </div>
                <div>
                  <p className="font-bold text-gray-900">Cargar Batería (Zona Óptima)</p>
                  <p className="text-xs text-gray-600">Excedente → Batería (solo si está 25-80%)</p>
                </div>
              </div>
              {batteryCharging && isOptimalZone && <CheckCircle className="w-6 h-6 text-blue-600" />}
            </div>
            {batteryCharging && (
              <div className="ml-11">
                <p className="text-sm text-gray-700">
                  ⚡ Cargando con {battery_power_w.toFixed(0)}W de excedente
                </p>
              </div>
            )}
          </div>

          {/* Prioridad 3: Batería como Respaldo (solo si falta energía) */}
          <div className={`p-4 rounded-lg border-2 ${
            batteryDischarging
              ? 'bg-orange-50 border-orange-500' 
              : 'bg-gray-50 border-gray-300'
          }`}>
            <div className="flex items-center justify-between mb-2">
              <div className="flex items-center">
                <div className={`w-8 h-8 rounded-full flex items-center justify-center mr-3 ${
                  batteryDischarging ? 'bg-orange-500' : 'bg-gray-400'
                }`}>
                  <span className="text-white font-bold">3</span>
                </div>
                <div>
                  <p className="font-bold text-gray-900">Batería como Respaldo</p>
                  <p className="text-xs text-gray-600">Solo cuando renovables no alcanzan</p>
                </div>
              </div>
              {batteryDischarging && <AlertTriangle className="w-6 h-6 text-orange-600" />}
            </div>
            {batteryDischarging && (
              <div className="ml-11">
                <p className="text-sm text-gray-700">
                  ⚠️ Suministrando {Math.abs(battery_power_w).toFixed(0)}W desde batería
                </p>
                <p className="text-xs text-orange-600 mt-1">
                  Reduciendo vida útil - Considerar aumentar generación renovable
                </p>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Estado de Relés y Conexiones */}
      <div className="bg-gradient-to-br from-gray-50 to-blue-50 rounded-xl shadow-lg p-6 border-2 border-gray-300">
        <h3 className="text-xl font-bold text-gray-900 mb-4 flex items-center">
          <Power className="w-6 h-6 mr-2 text-indigo-600" />
          Estado de Relés y Fuentes
        </h3>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {/* Relé Solar */}
          <div className={`p-4 rounded-lg border-2 ${
            solarConnected 
              ? 'bg-yellow-50 border-yellow-500' 
              : 'bg-gray-100 border-gray-400'
          }`}>
            <div className="flex items-center justify-between mb-3">
              <Sun className={`w-8 h-8 ${solarConnected ? 'text-yellow-600' : 'text-gray-400'}`} />
              <div className={`px-3 py-1 rounded-full text-xs font-bold ${
                solarConnected 
                  ? 'bg-green-500 text-white' 
                  : 'bg-gray-400 text-white'
              }`}>
                {solarConnected ? 'CONECTADO' : 'DESCONECTADO'}
              </div>
            </div>
            <p className="font-bold text-gray-900 mb-1">Energía Solar</p>
            <p className="text-2xl font-black text-yellow-600">{solar_power_w.toFixed(0)} W</p>
            <p className="text-xs text-gray-600 mt-2">
              Relé GPIO16: {solarConnected ? 'CERRADO ✅' : 'ABIERTO ⭕'}
            </p>
          </div>

          {/* Relé Eólica */}
          <div className={`p-4 rounded-lg border-2 ${
            windConnected 
              ? 'bg-blue-50 border-blue-500' 
              : 'bg-gray-100 border-gray-400'
          }`}>
            <div className="flex items-center justify-between mb-3">
              <Wind className={`w-8 h-8 ${windConnected ? 'text-blue-600' : 'text-gray-400'}`} />
              <div className={`px-3 py-1 rounded-full text-xs font-bold ${
                windConnected 
                  ? 'bg-green-500 text-white' 
                  : 'bg-gray-400 text-white'
              }`}>
                {windConnected ? 'CONECTADO' : 'DESCONECTADO'}
              </div>
            </div>
            <p className="font-bold text-gray-900 mb-1">Energía Eólica</p>
            <p className="text-2xl font-black text-blue-600">{wind_power_w.toFixed(0)} W</p>
            <p className="text-xs text-gray-600 mt-2">
              Relé GPIO17: {windConnected ? 'CERRADO ✅' : 'ABIERTO ⭕'}
            </p>
          </div>

          {/* Estado Batería */}
          <div className={`p-4 rounded-lg border-2 ${
            batteryCharging || batteryDischarging
              ? 'bg-green-50 border-green-500' 
              : 'bg-gray-100 border-gray-400'
          }`}>
            <div className="flex items-center justify-between mb-3">
              <Battery className={`w-8 h-8 ${
                batteryCharging || batteryDischarging ? 'text-green-600' : 'text-gray-400'
              }`} />
              <div className={`px-3 py-1 rounded-full text-xs font-bold ${
                batteryCharging 
                  ? 'bg-blue-500 text-white'
                  : batteryDischarging
                    ? 'bg-orange-500 text-white'
                    : 'bg-gray-400 text-white'
              }`}>
                {batteryCharging && 'CARGANDO'}
                {batteryDischarging && 'DESCARGANDO'}
                {!batteryCharging && !batteryDischarging && 'EN REPOSO'}
              </div>
            </div>
            <p className="font-bold text-gray-900 mb-1">Batería</p>
            <p className="text-2xl font-black text-green-600">{battery_soc_percent.toFixed(1)}%</p>
            <p className="text-xs text-gray-600 mt-2">
              {Math.abs(battery_power_w).toFixed(0)} W {batteryCharging ? '⬆️' : batteryDischarging ? '⬇️' : '⏸️'}
            </p>
          </div>
        </div>
      </div>

      {/* Beneficios de la Estrategia */}
      <div className="bg-gradient-to-br from-purple-50 to-pink-50 rounded-xl shadow-lg p-6 border-l-4 border-purple-500">
        <h3 className="text-xl font-bold text-purple-900 mb-4">
          💎 Beneficios de la Protección de Batería
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <h4 className="font-bold text-gray-800 mb-2">🔋 Mayor Vida Útil</h4>
            <ul className="space-y-1 text-sm text-gray-700">
              <li>✅ Mantener entre 25-80% = 5000+ ciclos</li>
              <li>✅ Evitar descargas profundas (daño permanente)</li>
              <li>✅ Evitar sobrecarga constante</li>
              <li>✅ Menos estrés = más años de servicio</li>
            </ul>
          </div>
          <div>
            <h4 className="font-bold text-gray-800 mb-2">💰 Ahorro Económico</h4>
            <ul className="space-y-1 text-sm text-gray-700">
              <li>✅ Batería dura 10-15 años vs 5-7 años</li>
              <li>✅ Ahorro: ~$200,000 en reemplazo</li>
              <li>✅ Uso directo renovables = máxima eficiencia</li>
              <li>✅ ROI más rápido del sistema</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};

export default BatteryProtection;
