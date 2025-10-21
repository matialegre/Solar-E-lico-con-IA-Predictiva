"""
Estrategia Inteligente de Carga Basada en Pronóstico del Clima
Toma decisiones anticipadas según predicción meteorológica
"""
from typing import Dict, List
from datetime import datetime, timedelta

class SmartChargingStrategy:
    """
    Sistema inteligente que analiza el pronóstico del clima
    y toma decisiones de carga proactivas
    """
    
    def __init__(self):
        self.umbral_lluvia_mm = 5.0  # >5mm = día lluvioso
        self.umbral_nubosidad = 80  # >80% = muy nublado
        self.umbral_viento_bueno = 8.0  # >8 m/s = buen viento
        
    def analizar_pronostico(self, forecast_data: List[Dict]) -> Dict:
        """
        Analiza pronóstico y genera estrategia de carga
        
        Args:
            forecast_data: Lista de pronósticos por día
            
        Returns:
            Estrategia con decisiones y recomendaciones
        """
        
        if not forecast_data:
            return {
                'status': 'error',
                'mensaje': 'Sin datos de pronóstico'
            }
        
        # Analizar próximos días
        dias_sin_sol = []
        dias_con_viento = []
        oportunidades_carga = []
        alertas = []
        
        for idx, dia in enumerate(forecast_data[:4]):  # Próximos 4 días
            fecha = dia.get('date', f'Día {idx+1}')
            
            # Condiciones del día
            lluvia = dia.get('total_rain_mm', 0)
            nubosidad = dia.get('avg_clouds_percent', 0)
            viento_prom = dia.get('avg_wind_speed_ms', 0)
            viento_max = dia.get('max_wind_speed_ms', 0)
            
            # ¿Día sin sol?
            sin_sol = (lluvia > self.umbral_lluvia_mm or 
                      nubosidad > self.umbral_nubosidad)
            
            if sin_sol:
                dias_sin_sol.append({
                    'dia': idx + 1,
                    'fecha': fecha,
                    'razon': 'lluvia' if lluvia > self.umbral_lluvia_mm else 'nubosidad',
                    'lluvia_mm': lluvia,
                    'nubosidad': nubosidad
                })
            
            # ¿Buen viento?
            if viento_prom > self.umbral_viento_bueno or viento_max > 12:
                dias_con_viento.append({
                    'dia': idx + 1,
                    'fecha': fecha,
                    'viento_promedio': viento_prom,
                    'viento_maximo': viento_max
                })
        
        # ESTRATEGIA INTELIGENTE
        estrategia = self._generar_estrategia(
            dias_sin_sol, 
            dias_con_viento,
            forecast_data[0] if forecast_data else None  # Hoy
        )
        
        return {
            'status': 'success',
            'timestamp': datetime.now().isoformat(),
            'analisis': {
                'dias_sin_sol': len(dias_sin_sol),
                'dias_con_viento': len(dias_con_viento),
                'detalle_sin_sol': dias_sin_sol,
                'detalle_viento': dias_con_viento
            },
            'estrategia': estrategia,
            'urgencia': estrategia.get('nivel_urgencia', 'NORMAL')
        }
    
    def _generar_estrategia(
        self, 
        dias_sin_sol: List[Dict], 
        dias_con_viento: List[Dict],
        condiciones_hoy: Dict
    ) -> Dict:
        """Genera estrategia inteligente de carga"""
        
        decisiones = []
        recomendaciones = []
        nivel_urgencia = 'NORMAL'
        
        # CASO 1: Mañana sin sol + hoy hay viento
        if dias_sin_sol and dias_sin_sol[0]['dia'] <= 2:  # Mañana o pasado
            # Mañana será malo para solar
            proximo_malo = dias_sin_sol[0]
            
            # ¿Hoy hay viento?
            viento_hoy = condiciones_hoy.get('avg_wind_speed_ms', 0) if condiciones_hoy else 0
            
            if viento_hoy > self.umbral_viento_bueno:
                nivel_urgencia = 'ALTA'
                decisiones.append({
                    'accion': 'CARGAR_BATERIA_URGENTE',
                    'razon': f'Mañana {proximo_malo["razon"]} - Aprovechar viento de HOY',
                    'prioridad': 'CRÍTICA'
                })
                recomendaciones.append(
                    f"🚨 URGENTE: Mañana habrá {proximo_malo['razon']} "
                    f"({proximo_malo['lluvia_mm']:.1f}mm lluvia). "
                    f"¡Aprovecha el viento de HOY ({viento_hoy:.1f} m/s) para cargar batería al máximo!"
                )
            else:
                decisiones.append({
                    'accion': 'CONSERVAR_BATERIA',
                    'razon': f'Mañana sin sol y hoy sin viento - Reducir consumo',
                    'prioridad': 'ALTA'
                })
                recomendaciones.append(
                    f"⚠️ Mañana habrá poca generación solar. "
                    f"Reduce consumo HOY para llegar con batería cargada."
                )
        
        # CASO 2: Varios días sin sol seguidos
        if len(dias_sin_sol) >= 2:
            dias_malos = [d['dia'] for d in dias_sin_sol]
            nivel_urgencia = 'CRÍTICA'
            
            decisiones.append({
                'accion': 'PREPARAR_AUTONOMIA',
                'razon': f'{len(dias_sin_sol)} días con poca generación solar',
                'prioridad': 'CRÍTICA'
            })
            recomendaciones.append(
                f"🚨 CRÍTICO: {len(dias_sin_sol)} días con mal clima adelante (días {dias_malos}). "
                f"Carga batería al MÁXIMO y reduce consumo no esencial."
            )
            
            # ¿Hay viento en esos días?
            viento_alternativo = [d for d in dias_con_viento if d['dia'] in dias_malos]
            if viento_alternativo:
                recomendaciones.append(
                    f"💨 Buena noticia: Habrá viento en días {[d['dia'] for d in viento_alternativo]}. "
                    f"La turbina eólica será tu salvación."
                )
        
        # CASO 3: Hoy hay mucho viento nocturno
        if dias_con_viento and dias_con_viento[0]['dia'] == 1:
            viento_dia = dias_con_viento[0]
            if viento_dia['viento_maximo'] > 15:
                decisiones.append({
                    'accion': 'APROVECHAR_VIENTO_NOCTURNO',
                    'razon': f'Viento fuerte esperado ({viento_dia["viento_maximo"]:.1f} m/s)',
                    'prioridad': 'ALTA'
                })
                recomendaciones.append(
                    f"💨 HOY habrá viento fuerte (hasta {viento_dia['viento_maximo']:.1f} m/s). "
                    f"¡Perfecto para cargar con turbina durante la noche!"
                )
        
        # CASO 4: Buenos días solares adelante
        if not dias_sin_sol or (dias_sin_sol and dias_sin_sol[0]['dia'] > 2):
            decisiones.append({
                'accion': 'OPERACION_NORMAL',
                'razon': 'Buen clima próximos días',
                'prioridad': 'BAJA'
            })
            recomendaciones.append(
                "☀️ Buenos días solares adelante. Operación normal del sistema."
            )
        
        # CASO 5: Oportunidad de carga óptima
        if dias_con_viento and not dias_sin_sol:
            decisiones.append({
                'accion': 'OPTIMIZAR_CARGA',
                'razon': 'Condiciones ideales: sol + viento',
                'prioridad': 'MEDIA'
            })
            recomendaciones.append(
                "✅ Condiciones ideales: Buena generación solar Y eólica. "
                "Aprovecha para cargar batería al máximo."
            )
        
        # Calcular autonomía necesaria
        dias_autonomia_necesaria = len(dias_sin_sol)
        if dias_sin_sol:
            # Buscar si hay viento en días malos
            viento_en_dias_malos = sum(1 for d in dias_con_viento 
                                       if any(d['dia'] == ds['dia'] for ds in dias_sin_sol))
            # Si hay viento, no necesitas tanta autonomía
            dias_autonomia_necesaria = max(1, len(dias_sin_sol) - viento_en_dias_malos)
        
        return {
            'decisiones': decisiones,
            'recomendaciones': recomendaciones,
            'nivel_urgencia': nivel_urgencia,
            'autonomia_necesaria_dias': dias_autonomia_necesaria,
            'accion_inmediata': decisiones[0] if decisiones else None
        }
    
    def calcular_carga_objetivo(
        self, 
        bateria_actual_percent: float,
        dias_sin_sol: int,
        consumo_diario_kwh: float,
        capacidad_bateria_kwh: float
    ) -> Dict:
        """
        Calcula nivel de carga objetivo según pronóstico
        """
        
        # Carga mínima para días sin sol
        energia_necesaria_kwh = consumo_diario_kwh * dias_sin_sol
        
        # Considerar zona óptima de batería (no pasar de 80% idealmente)
        carga_objetivo_percent = min(
            80.0,  # Máximo recomendado
            (energia_necesaria_kwh / capacidad_bateria_kwh) * 100
        )
        
        # Si hay emergencia, permitir carga hasta 95%
        if dias_sin_sol >= 2:
            carga_objetivo_percent = min(95.0, carga_objetivo_percent)
        
        deficit_percent = max(0, carga_objetivo_percent - bateria_actual_percent)
        deficit_kwh = (deficit_percent / 100) * capacidad_bateria_kwh
        
        urgente = deficit_percent > 30
        
        return {
            'carga_actual_percent': bateria_actual_percent,
            'carga_objetivo_percent': round(carga_objetivo_percent, 1),
            'deficit_percent': round(deficit_percent, 1),
            'deficit_kwh': round(deficit_kwh, 2),
            'urgente': urgente,
            'mensaje': self._generar_mensaje_carga(
                bateria_actual_percent, 
                carga_objetivo_percent, 
                urgente
            )
        }
    
    def _generar_mensaje_carga(
        self, 
        actual: float, 
        objetivo: float, 
        urgente: bool
    ) -> str:
        """Genera mensaje para objetivo de carga"""
        
        if actual >= objetivo:
            return f"✅ Batería suficiente ({actual:.1f}% >= {objetivo:.1f}%)"
        elif urgente:
            return f"🚨 URGENTE: Cargar batería de {actual:.1f}% a {objetivo:.1f}%"
        else:
            return f"💡 Recomendado: Cargar batería hasta {objetivo:.1f}%"


# Instancia global
smart_strategy = SmartChargingStrategy()
