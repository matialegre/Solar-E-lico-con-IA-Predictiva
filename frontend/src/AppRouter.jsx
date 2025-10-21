/**
 * Router principal de la aplicación
 */

import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import { Home, Activity, Settings, Calculator } from 'lucide-react';
import App from './App';
import DispositivosPage from './pages/DispositivosPage';
import ConfigurarPage from './pages/ConfigurarPage';
import DimensionamientoPage from './pages/DimensionamientoPage';
import DashboardTabs from './pages/DashboardTabs';

export default function AppRouter() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-900">
        {/* Navigation */}
        <nav className="bg-gray-800 border-b border-gray-700 sticky top-0 z-50">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex items-center justify-between h-16">
              <div className="flex items-center gap-8">
                <Link to="/" className="text-white font-bold text-xl">
                  🔋 Sistema Inversor
                </Link>
                <div className="flex gap-4">
                  <Link
                    to="/"
                    className="text-gray-300 hover:text-white px-3 py-2 rounded-md text-sm font-medium flex items-center gap-2"
                  >
                    <Home className="w-4 h-4" />
                    Dashboard
                  </Link>
                  <Link
                    to="/dispositivos"
                    className="text-gray-300 hover:text-white px-3 py-2 rounded-md text-sm font-medium flex items-center gap-2"
                  >
                    <Activity className="w-4 h-4" />
                    Dispositivos
                  </Link>
                  <Link
                    to="/dimensionamiento"
                    className="text-gray-300 hover:text-white px-3 py-2 rounded-md text-sm font-medium flex items-center gap-2"
                  >
                    <Calculator className="w-4 h-4" />
                    Dimensionamiento
                  </Link>
                </div>
              </div>
            </div>
          </div>
        </nav>

        {/* Routes */}
        <Routes>
          <Route path="/" element={<App />} />
          <Route path="/dispositivos" element={<DispositivosPage />} />
          <Route path="/configurar/:deviceId" element={<ConfigurarPage />} />
          <Route path="/dimensionamiento" element={<DimensionamientoPage />} />
        </Routes>
      </div>
    </Router>
  );
}
