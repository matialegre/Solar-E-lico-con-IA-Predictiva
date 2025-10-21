/**
 * Componente de mapa interactivo con Leaflet
 * Permite seleccionar ubicación arrastrando marcador
 */

import React, { useEffect, useRef } from 'react';

export default function MapSelector({ initialLat, initialLon, onChange }) {
  const mapRef = useRef(null);
  const mapInstanceRef = useRef(null);
  const markerRef = useRef(null);

  useEffect(() => {
    // Cargar Leaflet dinámicamente
    if (!window.L) {
      const link = document.createElement('link');
      link.rel = 'stylesheet';
      link.href = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.css';
      document.head.appendChild(link);

      const script = document.createElement('script');
      script.src = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.js';
      script.onload = initMap;
      document.body.appendChild(script);
    } else {
      initMap();
    }

    return () => {
      if (mapInstanceRef.current) {
        mapInstanceRef.current.remove();
      }
    };
  }, []);

  useEffect(() => {
    if (mapInstanceRef.current && markerRef.current) {
      const newLatLng = window.L.latLng(initialLat, initialLon);
      markerRef.current.setLatLng(newLatLng);
      mapInstanceRef.current.setView(newLatLng, mapInstanceRef.current.getZoom());
    }
  }, [initialLat, initialLon]);

  const initMap = () => {
    if (!mapRef.current || mapInstanceRef.current) return;

    const L = window.L;

    // Crear mapa
    const map = L.map(mapRef.current).setView([initialLat, initialLon], 10);

    // Agregar capa de OpenStreetMap
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '© OpenStreetMap contributors',
      maxZoom: 18,
    }).addTo(map);

    // Crear marcador arrastrable
    const marker = L.marker([initialLat, initialLon], {
      draggable: true,
      icon: L.icon({
        iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png',
        shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-shadow.png',
        iconSize: [25, 41],
        iconAnchor: [12, 41],
        popupAnchor: [1, -34],
        shadowSize: [41, 41]
      })
    }).addTo(map);

    marker.bindPopup('Arrastra el marcador para cambiar la ubicación').openPopup();

    // Event listener para arrastre
    marker.on('dragend', function(e) {
      const position = e.target.getLatLng();
      onChange(position.lat, position.lng);
      marker.setPopupContent(`📍 ${position.lat.toFixed(4)}, ${position.lng.toFixed(4)}`).openPopup();
    });

    // Event listener para click en el mapa
    map.on('click', function(e) {
      marker.setLatLng(e.latlng);
      onChange(e.latlng.lat, e.latlng.lng);
      marker.setPopupContent(`📍 ${e.latlng.lat.toFixed(4)}, ${e.latlng.lng.toFixed(4)}`).openPopup();
    });

    mapInstanceRef.current = map;
    markerRef.current = marker;
  };

  return (
    <div className="relative">
      <div
        ref={mapRef}
        className="w-full h-96 rounded-lg overflow-hidden border border-gray-700"
        style={{ zIndex: 1 }}
      />
      <div className="mt-2 text-xs text-gray-500">
        💡 Click en el mapa o arrastra el marcador para seleccionar ubicación
      </div>
    </div>
  );
}
