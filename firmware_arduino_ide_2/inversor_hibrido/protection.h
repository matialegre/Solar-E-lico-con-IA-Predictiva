/**
 * @file protection.h
 * @brief Protección contra embalamiento de turbina eólica
 * 
 * Detecta condiciones peligrosas:
 * - Velocidad viento >25 m/s
 * - Voltaje turbina >65V
 * - RPM >500
 * 
 * Acción: Desconectar turbina + Activar resistencia frenado
 */

#ifndef PROTECTION_H
#define PROTECTION_H

#include <Arduino.h>
#include "config.h"
#include "relays.h"
#include "sensors.h"

// ===== ESTADO DE PROTECCIÓN =====
struct ProtectionState {
  bool embalamiento_detectado;
  bool freno_activado;
  unsigned long tiempo_deteccion;
  unsigned long tiempo_activacion_freno;
  
  // Causas
  bool viento_excesivo;
  bool voltaje_excesivo;
  bool rpm_excesivo;
  
  // Historial
  int contador_activaciones;
};

ProtectionState protection_state;

// ===== INICIALIZACIÓN =====
void initProtection() {
  protection_state.embalamiento_detectado = false;
  protection_state.freno_activado = false;
  protection_state.tiempo_deteccion = 0;
  protection_state.tiempo_activacion_freno = 0;
  protection_state.viento_excesivo = false;
  protection_state.voltaje_excesivo = false;
  protection_state.rpm_excesivo = false;
  protection_state.contador_activaciones = 0;
  
  Serial.println("✅ Sistema de protección inicializado");
}

// ===== CALCULAR RPM =====
float calcularRPM(float velocidad_viento_ms) {
  // Estimación RPM basada en velocidad del viento
  // TSR (Tip Speed Ratio) típico de turbina pequeña: ~6
  // RPM = (Velocidad viento * TSR * 60) / (2 * PI * radio)
  
  float tsr = 6.0;
  float radio = VIENTO_RADIO_M * 10;  // Radio en metros (asumiendo 1m)
  
  if (radio < 0.1) radio = 1.0;  // Evitar división por 0
  
  float rpm = (velocidad_viento_ms * tsr * 60.0) / (2.0 * PI * radio);
  
  return rpm;
}

// ===== VERIFICAR EMBALAMIENTO =====
bool verificarEmbalamiento() {
  float velocidad_viento = sensores.velocidad_viento;
  float voltaje = sensores.voltaje_promedio;
  float rpm = calcularRPM(velocidad_viento);
  
  bool peligro = false;
  
  // Verificar viento excesivo
  if (velocidad_viento > MAX_VIENTO_MS) {
    protection_state.viento_excesivo = true;
    peligro = true;
    
    #ifdef DEBUG_PROTECTION
    Serial.printf("🚨 VIENTO EXCESIVO: %.1f m/s (máx: %.1f)\n", 
                  velocidad_viento, MAX_VIENTO_MS);
    #endif
  } else {
    protection_state.viento_excesivo = false;
  }
  
  // Verificar voltaje excesivo
  if (voltaje > MAX_VOLTAJE_V) {
    protection_state.voltaje_excesivo = true;
    peligro = true;
    
    #ifdef DEBUG_PROTECTION
    Serial.printf("🚨 VOLTAJE EXCESIVO: %.1fV (máx: %.1f)\n", 
                  voltaje, MAX_VOLTAJE_V);
    #endif
  } else {
    protection_state.voltaje_excesivo = false;
  }
  
  // Verificar RPM excesivo
  if (rpm > MAX_RPM) {
    protection_state.rpm_excesivo = true;
    peligro = true;
    
    #ifdef DEBUG_PROTECTION
    Serial.printf("🚨 RPM EXCESIVO: %.0f RPM (máx: %d)\n", 
                  rpm, MAX_RPM);
    #endif
  } else {
    protection_state.rpm_excesivo = false;
  }
  
  return peligro;
}

// ===== ACTIVAR PROTECCIÓN =====
void activarProteccion() {
  if (!protection_state.embalamiento_detectado) {
    protection_state.embalamiento_detectado = true;
    protection_state.tiempo_deteccion = millis();
    
    Serial.println("\n╔════════════════════════════════════════╗");
    Serial.println("║   🚨 EMBALAMIENTO DETECTADO 🚨        ║");
    Serial.println("╚════════════════════════════════════════╝");
    
    if (protection_state.viento_excesivo) {
      Serial.println("   • Viento excesivo");
    }
    if (protection_state.voltaje_excesivo) {
      Serial.println("   • Voltaje excesivo");
    }
    if (protection_state.rpm_excesivo) {
      Serial.println("   • RPM excesivo");
    }
    
    Serial.println("\n🔧 ACCIONES:");
  }
  
  // Paso 1: Desconectar turbina inmediatamente
  if (relay_state.eolica_conectada) {
    Serial.println("   1. Desconectando turbina eólica...");
    setRelayEolica(false);
  }
  
  // Paso 2: Esperar FRENO_ACTIVACION_DELAY antes de activar freno
  unsigned long tiempo_desde_deteccion = millis() - protection_state.tiempo_deteccion;
  
  if (tiempo_desde_deteccion >= FRENO_ACTIVACION_DELAY && !protection_state.freno_activado) {
    Serial.println("   2. Activando resistencia de frenado...");
    setRelayFreno(true);
    protection_state.freno_activado = true;
    protection_state.tiempo_activacion_freno = millis();
    protection_state.contador_activaciones++;
    
    // Calcular potencia disipada
    float potencia_freno = (sensores.voltaje_promedio * sensores.voltaje_promedio) / RESISTENCIA_FRENADO_OHM;
    
    Serial.println("\n📊 FRENADO ACTIVO:");
    Serial.printf("   Voltaje: %.1fV\n", sensores.voltaje_promedio);
    Serial.printf("   Resistencia: %.1fΩ\n", RESISTENCIA_FRENADO_OHM);
    Serial.printf("   Potencia disipada: %.0fW\n", potencia_freno);
    Serial.printf("   Máx permitido: %.0fW\n", RESISTENCIA_MAX_W);
    
    if (potencia_freno > RESISTENCIA_MAX_W) {
      Serial.println("   ⚠️ ADVERTENCIA: Potencia sobre límite resistencia");
    }
  }
}

// ===== DESACTIVAR PROTECCIÓN =====
void desactivarProteccion() {
  if (protection_state.embalamiento_detectado) {
    Serial.println("\n✅ Condiciones normales restauradas");
    Serial.println("   Desactivando freno...");
    
    setRelayFreno(false);
    
    protection_state.embalamiento_detectado = false;
    protection_state.freno_activado = false;
    protection_state.viento_excesivo = false;
    protection_state.voltaje_excesivo = false;
    protection_state.rpm_excesivo = false;
    
    Serial.println("✅ Sistema listo para operación normal");
  }
}

// ===== MONITOREO CONTINUO =====
void monitorearProteccion() {
  static unsigned long lastCheck = 0;
  
  // Verificar cada 500ms
  if (millis() - lastCheck < 500) return;
  lastCheck = millis();
  
  if (verificarEmbalamiento()) {
    activarProteccion();
  } else {
    // Si no hay peligro y el freno está activo, desactivar
    if (protection_state.freno_activado) {
      // Esperar al menos 10 segundos con freno activo antes de desactivar
      if (millis() - protection_state.tiempo_activacion_freno > 10000) {
        desactivarProteccion();
      }
    } else if (protection_state.embalamiento_detectado) {
      desactivarProteccion();
    }
  }
}

// ===== OBTENER ESTADO =====
String getProtectionStatus() {
  if (protection_state.embalamiento_detectado) {
    return "EMBALAMIENTO";
  } else {
    return "NORMAL";
  }
}

#endif // PROTECTION_H
