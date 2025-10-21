import React from 'react';
import { Cpu, Zap, Battery, Wind, Sun, Wifi, Activity, Code } from 'lucide-react';

const HardwareInfo = () => {
  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="card bg-gradient-to-br from-indigo-600 to-purple-700 text-white">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-3xl font-bold flex items-center mb-2">
              <Cpu className="w-8 h-8 mr-3" />
              Hardware & Electrónica
            </h2>
            <p className="text-indigo-100">
              Especificaciones técnicas completas del sistema ESP32
            </p>
          </div>
          <Activity className="w-20 h-20 opacity-20" />
        </div>
      </div>

      {/* Diagrama de Sistema */}
      <div className="card">
        <h3 className="text-xl font-bold text-gray-800 mb-4">🔌 Arquitectura del Sistema</h3>
        <div className="bg-gray-50 p-6 rounded-lg border-2 border-gray-200">
          <pre className="text-xs font-mono overflow-x-auto">
{`
┌─────────────────────────────────────────────────────────────────────┐
│                         SISTEMA INVERSOR HÍBRIDO                    │
└─────────────────────────────────────────────────────────────────────┘

    ┌──────────────┐         ┌──────────────┐         ┌──────────────┐
    │  PANELES     │         │  TURBINA     │         │   RED 220V   │
    │  SOLARES     │         │  EÓLICA      │────┐    │   BACKUP     │
    │  (3kW)       │         │  (2kW)       │    │    │              │
    └──────┬───────┘         └──────┬───────┘    │    └──────┬───────┘
           │                        │            │           │
           │                        │    ┌───────▼────────┐  │
           │                        │    │  RESISTENCIA   │  │
           │                        │    │  FRENADO 10Ω   │  │
           │                        │    │  (2kW)         │  │
           │                        │    └────────────────┘  │
           │                        │    Protección embalamiento
           └────────────────┬───────┴────────────────────────┘
                            │
                     ┌──────▼────────┐
                     │   BATERÍA     │
                     │   LiFePO4     │
                     │   48V 200Ah   │
                     │   (10kWh)     │
                     └──────┬────────┘
                            │
           ┌────────────────┼────────────────┐
           │                │                │
    ┌──────▼──────┐  ┌──────▼──────┐  ┌──────▼──────┐
    │  INVERSOR   │  │   ESP32     │  │   SHUNT     │
    │  48V→220V   │  │  CONTROL    │  │  CORRIENTE  │
    │  5000W      │  │  + WiFi     │  │  ±100A      │
    └──────┬──────┘  └──────┬──────┘  └─────────────┘
           │                │
           │         ┌──────▼──────────────────────────┐
           │         │  SENSORES:                      │
           │         │  • Voltaje baterías (3x)        │
           │         │  • Corriente solar              │
           │         │  • Corriente eólica             │
           │         │  • Corriente consumo            │
           │         │  • Temperatura paneles          │
           │         │  • Velocidad viento             │
           │         │  • Radiación solar (LDR)        │
           │         └─────────────────────────────────┘
           │
    ┌──────▼──────────────────┐
    │    CARGAS 220V AC       │
    │  • Iluminación          │
    │  • Electrodomésticos    │
    │  • Equipos              │
    └─────────────────────────┘
`}
          </pre>
        </div>
      </div>

      {/* Componentes Principales */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* ESP32 */}
        <div className="card bg-gradient-to-br from-blue-50 to-indigo-50">
          <h4 className="font-bold text-gray-800 mb-4 flex items-center">
            <Cpu className="w-5 h-5 mr-2 text-blue-600" />
            Microcontrolador ESP32
          </h4>
          <div className="space-y-3 text-sm">
            <div className="flex justify-between p-2 bg-white rounded">
              <span className="text-gray-600">Modelo:</span>
              <span className="font-bold">ESP32-WROOM-32</span>
            </div>
            <div className="flex justify-between p-2 bg-white rounded">
              <span className="text-gray-600">CPU:</span>
              <span className="font-bold">Dual Core 240MHz</span>
            </div>
            <div className="flex justify-between p-2 bg-white rounded">
              <span className="text-gray-600">RAM:</span>
              <span className="font-bold">520 KB SRAM</span>
            </div>
            <div className="flex justify-between p-2 bg-white rounded">
              <span className="text-gray-600">Flash:</span>
              <span className="font-bold">4 MB</span>
            </div>
            <div className="flex justify-between p-2 bg-white rounded">
              <span className="text-gray-600">WiFi:</span>
              <span className="font-bold">802.11 b/g/n</span>
            </div>
            <div className="flex justify-between p-2 bg-white rounded">
              <span className="text-gray-600">ADC:</span>
              <span className="font-bold">12-bit, 18 canales</span>
            </div>
            <div className="flex justify-between p-2 bg-white rounded">
              <span className="text-gray-600">GPIO:</span>
              <span className="font-bold">34 pines programables</span>
            </div>
          </div>
        </div>

        {/* Sensores */}
        <div className="card bg-gradient-to-br from-green-50 to-emerald-50">
          <h4 className="font-bold text-gray-800 mb-4 flex items-center">
            <Activity className="w-5 h-5 mr-2 text-green-600" />
            Sensores y Medición
          </h4>
          <div className="space-y-2 text-sm">
            <div className="p-3 bg-white rounded">
              <div className="flex items-center mb-1">
                <Battery className="w-4 h-4 mr-2 text-blue-600" />
                <span className="font-bold">Voltaje Baterías</span>
              </div>
              <p className="text-xs text-gray-600">3x Divisor resistivo 100kΩ/10kΩ (0-60V)</p>
            </div>
            <div className="p-3 bg-white rounded">
              <div className="flex items-center mb-1">
                <Zap className="w-4 h-4 mr-2 text-yellow-600" />
                <span className="font-bold">Corriente</span>
              </div>
              <p className="text-xs text-gray-600">ACS712-30A + Shunt 100A/75mV</p>
            </div>
            <div className="p-3 bg-white rounded">
              <div className="flex items-center mb-1">
                <Sun className="w-4 h-4 mr-2 text-orange-600" />
                <span className="font-bold">Radiación Solar</span>
              </div>
              <p className="text-xs text-gray-600">Fotoresistencia LDR GL5528</p>
            </div>
            <div className="p-3 bg-white rounded">
              <div className="flex items-center mb-1">
                <Wind className="w-4 h-4 mr-2 text-blue-600" />
                <span className="font-bold">Velocidad Viento</span>
              </div>
              <p className="text-xs text-gray-600">Anemómetro digital (pulsos/seg)</p>
            </div>
            <div className="p-3 bg-white rounded">
              <div className="flex items-center mb-1">
                <Activity className="w-4 h-4 mr-2 text-red-600" />
                <span className="font-bold">Temperatura</span>
              </div>
              <p className="text-xs text-gray-600">DS18B20 (rango: -55°C a +125°C)</p>
            </div>
          </div>
        </div>
      </div>

      {/* Lista de Materiales (BOM) */}
      <div className="card">
        <h3 className="text-xl font-bold text-gray-800 mb-4">📋 Lista de Materiales (BOM)</h3>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead className="bg-gray-100">
              <tr>
                <th className="p-3 text-left font-bold">Componente</th>
                <th className="p-3 text-left font-bold">Especificación</th>
                <th className="p-3 text-left font-bold">Cant.</th>
                <th className="p-3 text-left font-bold">Precio Unit.</th>
                <th className="p-3 text-left font-bold">Total</th>
              </tr>
            </thead>
            <tbody className="divide-y">
              <tr className="hover:bg-gray-50">
                <td className="p-3">ESP32-WROOM-32</td>
                <td className="p-3">DevKit v1, 38 pines</td>
                <td className="p-3">1</td>
                <td className="p-3">$8</td>
                <td className="p-3 font-bold">$8</td>
              </tr>
              <tr className="hover:bg-gray-50">
                <td className="p-3">Sensor corriente ACS712</td>
                <td className="p-3">±30A, salida analógica</td>
                <td className="p-3">3</td>
                <td className="p-3">$3</td>
                <td className="p-3 font-bold">$9</td>
              </tr>
              <tr className="hover:bg-gray-50">
                <td className="p-3">Shunt de corriente</td>
                <td className="p-3">100A 75mV</td>
                <td className="p-3">1</td>
                <td className="p-3">$12</td>
                <td className="p-3 font-bold">$12</td>
              </tr>
              <tr className="hover:bg-gray-50">
                <td className="p-3">Sensor temperatura DS18B20</td>
                <td className="p-3">Digital 1-Wire</td>
                <td className="p-3">2</td>
                <td className="p-3">$4</td>
                <td className="p-3 font-bold">$8</td>
              </tr>
              <tr className="hover:bg-gray-50">
                <td className="p-3">Módulo relé</td>
                <td className="p-3">4 canales, 30A, 250VAC</td>
                <td className="p-3">1</td>
                <td className="p-3">$15</td>
                <td className="p-3 font-bold">$15</td>
              </tr>
              <tr className="hover:bg-gray-50">
                <td className="p-3">LDR GL5528</td>
                <td className="p-3">Fotoresistencia</td>
                <td className="p-3">1</td>
                <td className="p-3">$1</td>
                <td className="p-3 font-bold">$1</td>
              </tr>
              <tr className="hover:bg-gray-50">
                <td className="p-3">Resistencias</td>
                <td className="p-3">100kΩ, 10kΩ (1% precisión)</td>
                <td className="p-3">10</td>
                <td className="p-3">$0.50</td>
                <td className="p-3 font-bold">$5</td>
              </tr>
              <tr className="hover:bg-gray-50">
                <td className="p-3">Fuente 5V</td>
                <td className="p-3">2A, aislada</td>
                <td className="p-3">1</td>
                <td className="p-3">$8</td>
                <td className="p-3 font-bold">$8</td>
              </tr>
              <tr className="hover:bg-gray-50">
                <td className="p-3">PCB personalizado</td>
                <td className="p-3">2 capas, 100x150mm</td>
                <td className="p-3">1</td>
                <td className="p-3">$25</td>
                <td className="p-3 font-bold">$25</td>
              </tr>
              <tr className="hover:bg-gray-50">
                <td className="p-3">Caja IP65</td>
                <td className="p-3">Plástico ABS, 200x150x75mm</td>
                <td className="p-3">1</td>
                <td className="p-3">$18</td>
                <td className="p-3 font-bold">$18</td>
              </tr>
              <tr className="bg-green-100">
                <td colSpan="4" className="p-3 text-right font-bold">TOTAL ELECTRÓNICA:</td>
                <td className="p-3 font-bold text-green-600 text-lg">$109</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      {/* Firmware */}
      <div className="card bg-gradient-to-br from-purple-50 to-pink-50">
        <h3 className="text-xl font-bold text-gray-800 mb-4 flex items-center">
          <Code className="w-6 h-6 mr-2 text-purple-600" />
          Firmware ESP32
        </h3>
        <div className="space-y-4">
          <div className="bg-white p-4 rounded-lg">
            <h4 className="font-bold text-gray-800 mb-2">📁 Estructura del Proyecto</h4>
            <pre className="text-xs font-mono bg-gray-50 p-3 rounded overflow-x-auto">
{`firmware/
├── src/
│   └── main.cpp              (550 líneas)
├── include/
│   └── config.h              (85 líneas)
├── platformio.ini            (Configuración PlatformIO)
└── README.md`}
            </pre>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="bg-white p-4 rounded-lg">
              <h4 className="font-bold text-gray-800 mb-3">⚙️ Tareas FreeRTOS</h4>
              <ul className="space-y-2 text-sm">
                <li className="flex items-start">
                  <span className="text-purple-600 mr-2">•</span>
                  <span><strong>Task 1:</strong> Lectura de sensores (100ms)</span>
                </li>
                <li className="flex items-start">
                  <span className="text-purple-600 mr-2">•</span>
                  <span><strong>Task 2:</strong> Control de relés (50ms)</span>
                </li>
                <li className="flex items-start">
                  <span className="text-purple-600 mr-2">•</span>
                  <span><strong>Task 3:</strong> Comunicación WiFi (1s)</span>
                </li>
              </ul>
            </div>

            <div className="bg-white p-4 rounded-lg">
              <h4 className="font-bold text-gray-800 mb-3">📡 Comunicación</h4>
              <ul className="space-y-2 text-sm">
                <li className="flex items-start">
                  <span className="text-blue-600 mr-2">•</span>
                  <span><strong>Protocolo:</strong> HTTP REST + JSON</span>
                </li>
                <li className="flex items-start">
                  <span className="text-blue-600 mr-2">•</span>
                  <span><strong>Endpoint:</strong> POST /api/energy/record</span>
                </li>
                <li className="flex items-start">
                  <span className="text-blue-600 mr-2">•</span>
                  <span><strong>Frecuencia:</strong> Cada 10 segundos</span>
                </li>
              </ul>
            </div>
          </div>

          <div className="bg-white p-4 rounded-lg">
            <h4 className="font-bold text-gray-800 mb-3">🔧 Compilación y Carga</h4>
            <div className="space-y-2 text-sm">
              <div className="bg-gray-50 p-3 rounded">
                <p className="font-mono text-xs mb-2">$ cd firmware</p>
                <p className="font-mono text-xs mb-2">$ pio run</p>
                <p className="font-mono text-xs">$ pio run --target upload</p>
              </div>
              <p className="text-xs text-gray-600 mt-2">
                <strong>Nota:</strong> Requiere PlatformIO instalado. Compatible con VS Code.
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Diagrama de Conexiones */}
      <div className="card bg-gradient-to-br from-yellow-50 to-orange-50">
        <h3 className="text-xl font-bold text-gray-800 mb-4">🔌 Diagrama de Pines ESP32</h3>
        <div className="overflow-x-auto">
          <table className="w-full text-xs">
            <thead className="bg-orange-100">
              <tr>
                <th className="p-2 text-left">GPIO</th>
                <th className="p-2 text-left">Función</th>
                <th className="p-2 text-left">Conexión</th>
                <th className="p-2 text-left">Tipo</th>
              </tr>
            </thead>
            <tbody className="divide-y bg-white">
              <tr><td className="p-2 font-mono">GPIO34</td><td className="p-2">ADC1_CH6</td><td className="p-2">Voltaje Batería 1</td><td className="p-2"><span className="bg-blue-100 px-2 py-1 rounded text-xs">Analog In</span></td></tr>
              <tr><td className="p-2 font-mono">GPIO35</td><td className="p-2">ADC1_CH7</td><td className="p-2">Voltaje Batería 2</td><td className="p-2"><span className="bg-blue-100 px-2 py-1 rounded text-xs">Analog In</span></td></tr>
              <tr><td className="p-2 font-mono">GPIO32</td><td className="p-2">ADC1_CH4</td><td className="p-2">Voltaje Batería 3</td><td className="p-2"><span className="bg-blue-100 px-2 py-1 rounded text-xs">Analog In</span></td></tr>
              <tr><td className="p-2 font-mono">GPIO33</td><td className="p-2">ADC1_CH5</td><td className="p-2">Corriente Solar</td><td className="p-2"><span className="bg-blue-100 px-2 py-1 rounded text-xs">Analog In</span></td></tr>
              <tr><td className="p-2 font-mono">GPIO36</td><td className="p-2">ADC1_CH0</td><td className="p-2">Corriente Eólica</td><td className="p-2"><span className="bg-blue-100 px-2 py-1 rounded text-xs">Analog In</span></td></tr>
              <tr><td className="p-2 font-mono">GPIO39</td><td className="p-2">ADC1_CH3</td><td className="p-2">Corriente Consumo</td><td className="p-2"><span className="bg-blue-100 px-2 py-1 rounded text-xs">Analog In</span></td></tr>
              <tr><td className="p-2 font-mono">GPIO25</td><td className="p-2">ADC2_CH8</td><td className="p-2">LDR (radiación solar)</td><td className="p-2"><span className="bg-blue-100 px-2 py-1 rounded text-xs">Analog In</span></td></tr>
              <tr><td className="p-2 font-mono">GPIO4</td><td className="p-2">GPIO</td><td className="p-2">DS18B20 (temperatura)</td><td className="p-2"><span className="bg-green-100 px-2 py-1 rounded text-xs">1-Wire</span></td></tr>
              <tr><td className="p-2 font-mono">GPIO16</td><td className="p-2">GPIO</td><td className="p-2">Relé 1 (Solar ON/OFF)</td><td className="p-2"><span className="bg-red-100 px-2 py-1 rounded text-xs">Digital Out</span></td></tr>
              <tr><td className="p-2 font-mono">GPIO17</td><td className="p-2">GPIO</td><td className="p-2">Relé 2 (Eólica ON/OFF)</td><td className="p-2"><span className="bg-red-100 px-2 py-1 rounded text-xs">Digital Out</span></td></tr>
              <tr><td className="p-2 font-mono">GPIO18</td><td className="p-2">GPIO</td><td className="p-2">Relé 3 (Red ON/OFF)</td><td className="p-2"><span className="bg-red-100 px-2 py-1 rounded text-xs">Digital Out</span></td></tr>
              <tr><td className="p-2 font-mono">GPIO19</td><td className="p-2">GPIO</td><td className="p-2">Relé 4 (Carga ON/OFF)</td><td className="p-2"><span className="bg-red-100 px-2 py-1 rounded text-xs">Digital Out</span></td></tr>
              <tr><td className="p-2 font-mono">GPIO21</td><td className="p-2">I2C_SDA</td><td className="p-2">Display OLED (opcional)</td><td className="p-2"><span className="bg-purple-100 px-2 py-1 rounded text-xs">I2C</span></td></tr>
              <tr><td className="p-2 font-mono">GPIO22</td><td className="p-2">I2C_SCL</td><td className="p-2">Display OLED (opcional)</td><td className="p-2"><span className="bg-purple-100 px-2 py-1 rounded text-xs">I2C</span></td></tr>
            </tbody>
          </table>
        </div>
      </div>

      {/* Consideraciones de Seguridad */}
      <div className="card bg-gradient-to-br from-red-50 to-orange-50 border-l-4 border-red-500">
        <h3 className="text-xl font-bold text-gray-800 mb-4">⚠️ Consideraciones de Seguridad</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
          <div>
            <h4 className="font-bold text-red-800 mb-2">⚡ Protección Eléctrica</h4>
            <ul className="space-y-1 text-gray-700">
              <li>• Fusibles en todas las líneas de potencia</li>
              <li>• Aislamiento galvánico (optoacopladores)</li>
              <li>• Varistores para sobretensiones</li>
              <li>• Puesta a tierra obligatoria</li>
            </ul>
          </div>
          <div>
            <h4 className="font-bold text-red-800 mb-2">🌡️ Protección Térmica</h4>
            <ul className="space-y-1 text-gray-700">
              <li>• Apagado automático {'>'}60°C</li>
              <li>• Ventilación forzada en gabinete</li>
              <li>• Sensores de temperatura redundantes</li>
              <li>• Disipadores en componentes de potencia</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};

export default HardwareInfo;
