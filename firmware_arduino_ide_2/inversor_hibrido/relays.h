/**
 * @file relays.h
 * @brief Control de relés y resistencia de frenado
 * 
 * Hardware:
 * - 4 relés modulares (30A, 250VAC)
 * - Resistencia frenado 10Ω 2000W
 */

#ifndef RELAYS_H
#define RELAYS_H

#include <Arduino.h>
#include "config.h"

// ===== ESTADO DE RELÉS =====
struct RelayState {
  bool solar_conectado;
  bool eolica_conectada;
  bool red_conectada;
  bool carga_conectada;
  bool freno_activo;
  
  unsigned long ultima_actualizacion;
};

RelayState relay_state;

// ===== INICIALIZACIÓN =====
void initRelays() {
  // Configurar pines como OUTPUT
  pinMode(PIN_RELE_SOLAR, OUTPUT);
  pinMode(PIN_RELE_EOLICA, OUTPUT);
  pinMode(PIN_RELE_RED, OUTPUT);
  pinMode(PIN_RELE_CARGA, OUTPUT);
  pinMode(PIN_RELE_FRENO, OUTPUT);
  
  // Estado inicial: TODO APAGADO (seguro)
  digitalWrite(PIN_RELE_SOLAR, LOW);
  digitalWrite(PIN_RELE_EOLICA, LOW);
  digitalWrite(PIN_RELE_RED, LOW);
  digitalWrite(PIN_RELE_CARGA, LOW);
  digitalWrite(PIN_RELE_FRENO, LOW);
  
  // Inicializar estado
  relay_state.solar_conectado = false;
  relay_state.eolica_conectada = false;
  relay_state.red_conectada = false;
  relay_state.carga_conectada = false;
  relay_state.freno_activo = false;
  relay_state.ultima_actualizacion = millis();
  
  Serial.println("✅ Relés inicializados (todos APAGADOS)");
}

// ===== CONTROL INDIVIDUAL =====
void setRelaySolar(bool estado) {
  digitalWrite(PIN_RELE_SOLAR, estado ? HIGH : LOW);
  relay_state.solar_conectado = estado;
  relay_state.ultima_actualizacion = millis();
  
  #ifdef DEBUG_RELAYS
  Serial.printf("⚡ Relé Solar: %s\n", estado ? "CONECTADO" : "DESCONECTADO");
  #endif
}

void setRelayEolica(bool estado) {
  // SEGURIDAD: Si freno está activo, NO conectar eólica
  if (relay_state.freno_activo && estado) {
    Serial.println("🚨 ERROR: No se puede conectar eólica con freno activo");
    return;
  }
  
  digitalWrite(PIN_RELE_EOLICA, estado ? HIGH : LOW);
  relay_state.eolica_conectada = estado;
  relay_state.ultima_actualizacion = millis();
  
  #ifdef DEBUG_RELAYS
  Serial.printf("⚡ Relé Eólica: %s\n", estado ? "CONECTADO" : "DESCONECTADO");
  #endif
}

void setRelayRed(bool estado) {
  digitalWrite(PIN_RELE_RED, estado ? HIGH : LOW);
  relay_state.red_conectada = estado;
  relay_state.ultima_actualizacion = millis();
  
  #ifdef DEBUG_RELAYS
  Serial.printf("⚡ Relé Red: %s\n", estado ? "CONECTADO" : "DESCONECTADO");
  #endif
}

void setRelayCarga(bool estado) {
  digitalWrite(PIN_RELE_CARGA, estado ? HIGH : LOW);
  relay_state.carga_conectada = estado;
  relay_state.ultima_actualizacion = millis();
  
  #ifdef DEBUG_RELAYS
  Serial.printf("⚡ Relé Carga: %s\n", estado ? "CONECTADO" : "DESCONECTADO");
  #endif
}

void setRelayFreno(bool estado) {
  // SEGURIDAD: Si freno se activa, desconectar eólica primero
  if (estado && relay_state.eolica_conectada) {
    Serial.println("🚨 Desconectando eólica antes de activar freno");
    setRelayEolica(false);
    delay(100);  // Esperar desconexión
  }
  
  digitalWrite(PIN_RELE_FRENO, estado ? HIGH : LOW);
  relay_state.freno_activo = estado;
  relay_state.ultima_actualizacion = millis();
  
  #ifdef DEBUG_RELAYS
  Serial.printf("🔥 Freno: %s\n", estado ? "ACTIVO" : "INACTIVO");
  #endif
}

// ===== APAGAR TODO (EMERGENCIA) =====
void apagarTodo() {
  Serial.println("🚨 EMERGENCIA: Apagando todos los relés");
  
  setRelaySolar(false);
  setRelayEolica(false);
  setRelayRed(false);
  setRelayCarga(false);
  setRelayFreno(false);
  
  Serial.println("✅ Todos los relés apagados");
}

// ===== ESTRATEGIA AUTOMÁTICA =====
void aplicarEstrategia(float soc, float potencia_solar, float potencia_eolica, float consumo) {
  // Esta función implementa la lógica inteligente del dashboard
  
  float generacion_total = potencia_solar + potencia_eolica;
  float balance = generacion_total - consumo;
  
  #ifdef DEBUG_RELAYS
  Serial.println("\n🤖 ESTRATEGIA AUTOMÁTICA:");
  Serial.printf("   SOC: %.1f%% | Gen: %.0fW | Cons: %.0fW | Balance: %.0fW\n", 
                soc, generacion_total, consumo, balance);
  #endif
  
  // REGLA 1: Uso directo de renovables (prioridad)
  if (generacion_total >= consumo) {
    // Hay suficiente generación
    setRelaySolar(potencia_solar > 50);  // Conectar si genera >50W
    setRelayEolica(potencia_eolica > 50);
    setRelayCarga(true);
    
    // ¿Sobra energía? Cargar batería si está en zona óptima
    if (balance > 100 && soc >= SOC_MIN_DESCARGA && soc < SOC_MAX_CARGA) {
      #ifdef DEBUG_RELAYS
      Serial.println("   💡 Excedente → Cargando batería");
      #endif
    } else if (soc >= SOC_MAX_CARGA) {
      #ifdef DEBUG_RELAYS
      Serial.println("   🔋 Batería llena (>80%) - No cargar más");
      #endif
    }
  }
  // REGLA 2: Generación insuficiente - Usar batería
  else if (soc > SOC_MIN_DESCARGA) {
    setRelaySolar(potencia_solar > 50);
    setRelayEolica(potencia_eolica > 50);
    setRelayCarga(true);
    
    #ifdef DEBUG_RELAYS
    Serial.printf("   🔋 Déficit: %.0fW - Usando batería (SOC: %.1f%%)\n", 
                  -balance, soc);
    #endif
  }
  // REGLA 3: Batería baja - Usar red backup
  else if (soc <= SOC_MIN_DESCARGA) {
    setRelayRed(true);
    setRelayCarga(true);
    
    #ifdef DEBUG_RELAYS
    Serial.println("   ⚠️ Batería baja (<25%) - Activando red backup");
    #endif
  }
  // REGLA 4: Crítico - Alertar
  else if (soc <= SOC_CRITICO) {
    Serial.println("🚨 CRÍTICO: Batería <10% - Reducir consumo");
  }
  
  #ifdef DEBUG_RELAYS
  Serial.printf("   Estado: Solar:%d Eólica:%d Red:%d Carga:%d\n",
                relay_state.solar_conectado,
                relay_state.eolica_conectada,
                relay_state.red_conectada,
                relay_state.carga_conectada);
  #endif
}

// ===== EJECUTAR COMANDO DEL SERVIDOR =====
bool ejecutarComandoRele(String comando, String parametro) {
  if (comando == "solar") {
    setRelaySolar(parametro == "on" || parametro == "1");
    return true;
  }
  else if (comando == "eolica") {
    setRelayEolica(parametro == "on" || parametro == "1");
    return true;
  }
  else if (comando == "red") {
    setRelayRed(parametro == "on" || parametro == "1");
    return true;
  }
  else if (comando == "carga") {
    setRelayCarga(parametro == "on" || parametro == "1");
    return true;
  }
  else if (comando == "freno") {
    setRelayFreno(parametro == "on" || parametro == "1");
    return true;
  }
  else if (comando == "apagar_todo") {
    apagarTodo();
    return true;
  }
  
  return false;
}

#endif // RELAYS_H
