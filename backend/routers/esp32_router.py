"""
Router para gestión de dispositivos ESP32
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import json

router = APIRouter(prefix="/api/esp32", tags=["ESP32"])

# Base de datos en memoria (temporal - reemplazar con PostgreSQL)
dispositivos_db = {}
heartbeat_db = {}


class ESP32Register(BaseModel):
    """Modelo para registro de ESP32"""
    device_id: str
    ip_local: str
    mac_address: str
    firmware_version: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class ESP32Heartbeat(BaseModel):
    """Modelo para heartbeat"""
    device_id: str
    uptime: int
    free_heap: int
    rssi: int


class ESP32Config(BaseModel):
    """Modelo para configuración"""
    latitude: float
    longitude: float
    battery_capacity_wh: Optional[float] = 5000.0
    solar_area_m2: Optional[float] = 16.0
    wind_power_w: Optional[float] = 2000.0
    proteccion_activa: Optional[bool] = True
    aprendizaje_activo: Optional[bool] = False


@router.post("/register")
async def register_device(device: ESP32Register):
    """
    Registrar un nuevo dispositivo ESP32
    
    El ESP32 llama a este endpoint al iniciar
    """
    device_id = device.device_id
    
    # Guardar información del dispositivo
    dispositivos_db[device_id] = {
        "device_id": device_id,
        "ip_local": device.ip_local,
        "mac_address": device.mac_address,
        "firmware_version": device.firmware_version,
        "latitude": device.latitude or -38.7183,
        "longitude": device.longitude or -62.2663,
        "registered_at": datetime.now().isoformat(),
        "last_seen": datetime.now().isoformat(),
        "status": "online"
    }
    
    print(f"✅ Dispositivo registrado: {device_id} ({device.ip_local})")
    
    return {
        "status": "registered",
        "device_id": device_id,
        "message": "Dispositivo registrado correctamente",
        "timestamp": datetime.now().isoformat()
    }


@router.post("/heartbeat")
async def receive_heartbeat(heartbeat: ESP32Heartbeat):
    """
    Recibir heartbeat del ESP32
    
    Mantiene el estado online/offline actualizado
    """
    device_id = heartbeat.device_id
    
    # Actualizar heartbeat
    heartbeat_db[device_id] = {
        "device_id": device_id,
        "uptime": heartbeat.uptime,
        "free_heap": heartbeat.free_heap,
        "rssi": heartbeat.rssi,
        "timestamp": datetime.now().isoformat()
    }
    
    # Actualizar last_seen en dispositivo
    if device_id in dispositivos_db:
        dispositivos_db[device_id]["last_seen"] = datetime.now().isoformat()
        dispositivos_db[device_id]["status"] = "online"
    else:
        # Si no existe, registrarlo automáticamente
        dispositivos_db[device_id] = {
            "device_id": device_id,
            "last_seen": datetime.now().isoformat(),
            "status": "online",
            "registered_at": datetime.now().isoformat()
        }
    
    return {
        "status": "ok",
        "timestamp": datetime.now().isoformat()
    }


@router.get("/devices")
async def list_devices():
    """
    Listar todos los dispositivos registrados
    
    Usado por el frontend para mostrar dispositivos conectados
    Lee del DEVICES_STORE unificado (main.py)
    """
    # Importar el store global desde main.py
    from main import DEVICES_STORE, load_store_from_disk
    
    # Cargar desde disco por si es un proceso nuevo
    load_store_from_disk()
    
    print(f"🔵 [ROUTER /devices] Dispositivos en DEVICES_STORE: {len(DEVICES_STORE)}")
    if DEVICES_STORE:
        print(f"🔵 [ROUTER /devices] Device IDs: {list(DEVICES_STORE.keys())}")
    
    devices = []
    now = datetime.now()
    online_count = 0
    
    for device_id, info in DEVICES_STORE.items():
        last_seen = datetime.fromisoformat(info['last_seen'])
        seconds_ago = (now - last_seen).total_seconds()
        is_online = seconds_ago < 10  # Online si se vio en últimos 10 segundos
        
        if is_online:
            online_count += 1
        
        # Construir objeto de dispositivo con todos los datos
        telemetry_data = info.get('telemetry', {})
        relays_data = info.get('relays', {})
        raw_adc_data = info.get('raw_adc', {})
        
        # Debug: imprimir raw_adc para verificar
        if raw_adc_data:
            print(f"📊 [ROUTER] raw_adc para {device_id}:", raw_adc_data)
        
        device_data = {
            'device_id': device_id,
            'status': 'online' if is_online else 'offline',
            'last_seen': info['last_seen'],
            'registered_at': info.get('registered_at', info['last_seen']),
            'contador': info.get('contador', 0),  # ← CONTADOR PARA DEBUG
            'heartbeat': info.get('heartbeat', {}),
            'relays': relays_data,      # ← Nivel superior, no dentro de telemetry
            'raw_adc': raw_adc_data,    # ← Nivel superior, no dentro de telemetry
            'telemetry': {
                'battery_voltage': telemetry_data.get('battery_voltage', 0),
                'battery_soc': telemetry_data.get('battery_soc', 0),
                'solar_power': telemetry_data.get('solar_power', 0),
                'wind_power': telemetry_data.get('wind_power', 0),
                'load_power': telemetry_data.get('load_power', 0),
                'temperature': telemetry_data.get('temperature', 0),
                'v_bat_v': telemetry_data.get('v_bat_v', 0),
                'v_wind_v_dc': telemetry_data.get('v_wind_v_dc', 0),
                'v_solar_v': telemetry_data.get('v_solar_v', 0),
                'v_load_v': telemetry_data.get('v_load_v', 0),
                'rpm': telemetry_data.get('rpm', 0),
                'frequency_hz': telemetry_data.get('frequency_hz', 0),
                'turbine_rpm': telemetry_data.get('turbine_rpm', 0.0)
            }
        }
        
        devices.append(device_data)
    
    return {
        "devices": devices,
        "total": len(devices),
        "online": online_count,
        "offline": len(devices) - online_count
    }


@router.get("/devices/{device_id}")
async def get_device(device_id: str):
    """
    Obtener información de un dispositivo específico
    """
    if device_id not in dispositivos_db:
        raise HTTPException(status_code=404, detail="Dispositivo no encontrado")
    
    device = dispositivos_db[device_id].copy()
    
    # Agregar heartbeat
    if device_id in heartbeat_db:
        device["heartbeat"] = heartbeat_db[device_id]
    
    return device


@router.get("/config/{device_id}")
async def get_config(device_id: str):
    """
    Obtener configuración del dispositivo
    
    El ESP32 llama a este endpoint para obtener su configuración
    """
    if device_id not in dispositivos_db:
        raise HTTPException(status_code=404, detail="Dispositivo no encontrado")
    
    device = dispositivos_db[device_id]
    
    return {
        "device_id": device_id,
        "latitude": device.get("latitude", -38.7183),
        "longitude": device.get("longitude", -62.2663),
        "battery_capacity_wh": device.get("battery_capacity_wh", 5000.0),
        "solar_area_m2": device.get("solar_area_m2", 16.0),
        "wind_power_w": device.get("wind_power_w", 2000.0),
        "proteccion_activa": device.get("proteccion_activa", True),
        "aprendizaje_activo": device.get("aprendizaje_activo", False)
    }


@router.post("/config/{device_id}")
async def update_config(device_id: str, config: ESP32Config):
    """
    Actualizar configuración del dispositivo
    
    Llamado desde el frontend cuando se configura la ubicación
    """
    if device_id not in dispositivos_db:
        raise HTTPException(status_code=404, detail="Dispositivo no encontrado")
    
    # Actualizar configuración
    dispositivos_db[device_id].update({
        "latitude": config.latitude,
        "longitude": config.longitude,
        "battery_capacity_wh": config.battery_capacity_wh,
        "solar_area_m2": config.solar_area_m2,
        "wind_power_w": config.wind_power_w,
        "proteccion_activa": config.proteccion_activa,
        "aprendizaje_activo": config.aprendizaje_activo,
        "configured_at": datetime.now().isoformat()
    })
    
    print(f"✅ Configuración actualizada: {device_id} → Lat: {config.latitude}, Lon: {config.longitude}")
    
    return {
        "status": "updated",
        "device_id": device_id,
        "config": config.dict(),
        "timestamp": datetime.now().isoformat()
    }


@router.delete("/devices/{device_id}")
async def delete_device(device_id: str):
    """
    Eliminar un dispositivo
    """
    if device_id not in dispositivos_db:
        raise HTTPException(status_code=404, detail="Dispositivo no encontrado")
    
    del dispositivos_db[device_id]
    
    if device_id in heartbeat_db:
        del heartbeat_db[device_id]
    
    return {
        "status": "deleted",
        "device_id": device_id,
        "timestamp": datetime.now().isoformat()
    }
