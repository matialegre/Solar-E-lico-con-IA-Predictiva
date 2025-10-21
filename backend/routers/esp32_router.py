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
    
    return {
        "status": "ok",
        "timestamp": datetime.now().isoformat()
    }


@router.get("/devices")
async def list_devices():
    """
    Listar todos los dispositivos registrados
    
    Usado por el frontend para mostrar dispositivos conectados
    """
    # Marcar como offline los que no han enviado heartbeat en >60 seg
    now = datetime.now()
    for device_id, device in dispositivos_db.items():
        last_seen = datetime.fromisoformat(device["last_seen"])
        diff = (now - last_seen).total_seconds()
        
        if diff > 60:
            device["status"] = "offline"
        
        # Agregar info de heartbeat si existe
        if device_id in heartbeat_db:
            device["heartbeat"] = heartbeat_db[device_id]
    
    return {
        "devices": list(dispositivos_db.values()),
        "total": len(dispositivos_db),
        "online": sum(1 for d in dispositivos_db.values() if d["status"] == "online"),
        "offline": sum(1 for d in dispositivos_db.values() if d["status"] == "offline")
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
