import React, { useState, useEffect } from 'react';
import { MapPin, Navigation, Search, CheckCircle } from 'lucide-react';

const MapaUbicacion = ({ onLocationSelect, initialLat = -38.7183, initialLon = -62.2663 }) => {
  const [coords, setCoords] = useState({ lat: initialLat, lon: initialLon });
  const [ciudad, setCiudad] = useState('');
  const [buscando, setBuscando] = useState(false);

  const handleMapClick = (e) => {
    const lat = parseFloat(e.target.dataset.lat);
    const lon = parseFloat(e.target.dataset.lon);
    
    if (!isNaN(lat) && !isNaN(lon)) {
      setCoords({ lat, lon });
      if (onLocationSelect) {
        onLocationSelect(lat, lon);
      }
    }
  };

  const buscarCiudad = async () => {
    if (!ciudad) return;
    
    setBuscando(true);
    try {
      // Usar API de geocoding de OpenStreetMap (gratis)
      const response = await fetch(
        `https://nominatim.openstreetmap.org/search?q=${encodeURIComponent(ciudad)}&format=json&limit=1`
      );
      const data = await response.json();
      
      if (data && data.length > 0) {
        const lat = parseFloat(data[0].lat);
        const lon = parseFloat(data[0].lon);
        setCoords({ lat, lon });
        if (onLocationSelect) {
          onLocationSelect(lat, lon);
        }
      }
    } catch (error) {
      console.error('Error buscando ciudad:', error);
    }
    setBuscando(false);
  };

  const obtenerUbicacionActual = () => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          const lat = position.coords.latitude;
          const lon = position.coords.longitude;
          setCoords({ lat, lon });
          if (onLocationSelect) {
            onLocationSelect(lat, lon);
          }
        },
        (error) => {
          console.error('Error obteniendo ubicación:', error);
          alert('No se pudo obtener tu ubicación. Usa el mapa o busca tu ciudad.');
        }
      );
    }
  };

  return (
    <div className="space-y-4">
      {/* Búsqueda de ciudad */}
      <div className="flex gap-2">
        <div className="flex-1 relative">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
          <input
            type="text"
            value={ciudad}
            onChange={(e) => setCiudad(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && buscarCiudad()}
            placeholder="Buscar ciudad (ej: Bahía Blanca, Argentina)"
            className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
        </div>
        <button
          onClick={buscarCiudad}
          disabled={buscando || !ciudad}
          className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed"
        >
          {buscando ? 'Buscando...' : 'Buscar'}
        </button>
        <button
          onClick={obtenerUbicacionActual}
          className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 flex items-center gap-2"
          title="Usar mi ubicación actual"
        >
          <Navigation className="w-5 h-5" />
          Mi Ubicación
        </button>
      </div>

      {/* Mapa interactivo con Leaflet o iframe de OpenStreetMap */}
      <div className="border-2 border-gray-300 rounded-lg overflow-hidden bg-gray-100">
        <iframe
          width="100%"
          height="400"
          frameBorder="0"
          scrolling="no"
          marginHeight="0"
          marginWidth="0"
          src={`https://www.openstreetmap.org/export/embed.html?bbox=${coords.lon-0.5},${coords.lat-0.5},${coords.lon+0.5},${coords.lat+0.5}&layer=mapnik&marker=${coords.lat},${coords.lon}`}
          style={{ border: 0 }}
        ></iframe>
      </div>

      {/* Coordenadas seleccionadas */}
      <div className="bg-green-50 border-2 border-green-300 rounded-lg p-4">
        <div className="flex items-center mb-2">
          <CheckCircle className="w-5 h-5 text-green-600 mr-2" />
          <h4 className="font-bold text-green-900">Ubicación Seleccionada:</h4>
        </div>
        <div className="grid grid-cols-2 gap-4 text-sm">
          <div>
            <span className="text-gray-600">Latitud:</span>
            <p className="font-mono font-bold text-gray-900">{coords.lat.toFixed(4)}</p>
          </div>
          <div>
            <span className="text-gray-600">Longitud:</span>
            <p className="font-mono font-bold text-gray-900">{coords.lon.toFixed(4)}</p>
          </div>
        </div>
      </div>

      {/* Instrucciones */}
      <div className="bg-blue-50 border-l-4 border-blue-500 rounded-lg p-4">
        <p className="text-sm text-blue-900">
          <strong>💡 Cómo usar:</strong>
        </p>
        <ul className="text-sm text-blue-800 mt-2 ml-4 space-y-1">
          <li>• <strong>Buscar:</strong> Ingresa tu ciudad arriba y presiona "Buscar"</li>
          <li>• <strong>GPS:</strong> Click en "Mi Ubicación" para usar tu ubicación actual</li>
          <li>• <strong>Mapa:</strong> Click en el marcador rojo para ajustar la posición</li>
        </ul>
      </div>
    </div>
  );
};

export default MapaUbicacion;
