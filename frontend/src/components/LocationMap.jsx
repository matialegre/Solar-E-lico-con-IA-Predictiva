import React from 'react';
import { MapPin } from 'lucide-react';

const LocationMap = ({ latitude, longitude, location }) => {
  // Mapa de Google Maps con vista satelital y zoom cercano
  const zoom = 18; // Zoom muy cercano para ver los paneles
  const mapUrl = `https://maps.google.com/maps?q=${latitude},${longitude}&t=k&z=${zoom}&ie=UTF8&iwloc=&output=embed`;
  
  return (
    <div className="card bg-gradient-to-br from-green-50 to-blue-50">
      <h3 className="card-title flex items-center mb-4">
        <MapPin className="w-6 h-6 mr-2 text-green-600" />
        <span className="text-lg font-bold">Ubicación del Sistema</span>
      </h3>

      {/* Mapa satelital con zoom cercano */}
      <div className="mb-4 rounded-xl overflow-hidden border-4 border-green-500 shadow-2xl relative">
        <div className="absolute top-4 left-4 z-10 bg-green-600 text-white px-3 py-1 rounded-full text-xs font-bold">
          🛰️ Vista Satelital
        </div>
        <iframe
          width="100%"
          height="400"
          frameBorder="0"
          scrolling="no"
          marginHeight="0"
          marginWidth="0"
          src={mapUrl}
          title="Mapa de ubicación satelital"
          className="hover:shadow-2xl transition-shadow"
        />
      </div>

      {/* Información de coordenadas */}
      <div className="grid grid-cols-2 gap-4">
        <div className="p-4 bg-gradient-to-br from-blue-500 to-blue-600 rounded-xl shadow-md">
          <p className="text-xs text-blue-100 mb-1 font-medium">LATITUD</p>
          <p className="text-xl font-bold text-white">{latitude}°</p>
          <p className="text-xs text-blue-200 mt-1">Sur</p>
        </div>
        <div className="p-4 bg-gradient-to-br from-green-500 to-green-600 rounded-xl shadow-md">
          <p className="text-xs text-green-100 mb-1 font-medium">LONGITUD</p>
          <p className="text-xl font-bold text-white">{longitude}°</p>
          <p className="text-xs text-green-200 mt-1">Oeste</p>
        </div>
      </div>

      {location && (
        <div className="mt-4 p-4 bg-white rounded-xl shadow-md border-l-4 border-green-500">
          <p className="text-sm font-semibold text-gray-800 flex items-center">
            <MapPin className="w-4 h-4 mr-2 text-green-600" />
            {location}
          </p>
        </div>
      )}

      {/* Link a Google Maps */}
      <div className="mt-4">
        <a
          href={`https://www.google.com/maps?q=${latitude},${longitude}&z=15`}
          target="_blank"
          rel="noopener noreferrer"
          className="inline-flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors shadow-md hover:shadow-lg font-medium text-sm"
        >
          <MapPin className="w-4 h-4 mr-2" />
          Ver en Google Maps
          <span className="ml-2">→</span>
        </a>
      </div>
    </div>
  );
};

export default LocationMap;
