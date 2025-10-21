"""
Monitor de Eficiencia de Paneles Solares y Turbina Eólica
Compara generación real vs teórica para detectar problemas
"""
from typing import Dict, List, Optional
from datetime import datetime
import math

class EfficiencyMonitor:
    """
    Monitorea la eficiencia real de los componentes y detecta problemas
    """
    
    def __init__(self):
        # Eficiencias teóricas (condiciones ideales)
        self.eficiencia_solar_ideal = 0.18  # 18% para paneles policristalinos
        self.eficiencia_turbina_ideal = 0.45  # 45% (Betz limit: 59.3%, real: 40-50%)
        
        # Umbrales de alerta
        self.umbral_critico = 0.60  # <60% eficiencia = CRÍTICO
        self.umbral_advertencia = 0.75  # <75% eficiencia = ADVERTENCIA
        
        # Historial para detección de degradación
        self.historial_eficiencia_solar = []
        self.historial_eficiencia_eolica = []
    
    def calcular_eficiencia_solar(
        self,
        irradiancia_w_m2: float,
        area_paneles_m2: float,
        potencia_generada_w: float,
        temperatura_ambiente_c: float = 25.0
    ) -> Dict:
        """
        Calcula eficiencia real de paneles solares
        
        Args:
            irradiancia_w_m2: Irradiancia solar medida (W/m²) - del sensor LDR
            area_paneles_m2: Área total de paneles en m²
            potencia_generada_w: Potencia real generada (W) - del sensor de corriente
            temperatura_ambiente_c: Temperatura ambiente
        
        Returns:
            Dict con eficiencia y diagnóstico
        """
        
        # Potencia solar disponible
        potencia_disponible_w = irradiancia_w_m2 * area_paneles_m2
        
        if potencia_disponible_w < 10:
            return {
                'status': 'no_solar',
                'mensaje': 'Muy poca luz solar para medir',
                'eficiencia_percent': 0,
                'potencia_teorica_w': 0,
                'potencia_real_w': potencia_generada_w,
                'perdida_w': 0
            }
        
        # Potencia teórica (con eficiencia ideal y factor de temperatura)
        # Los paneles pierden ~0.5% por cada °C sobre 25°C
        factor_temperatura = 1 - (0.005 * (temperatura_ambiente_c - 25))
        factor_temperatura = max(0.7, min(1.0, factor_temperatura))  # Entre 70% y 100%
        
        potencia_teorica_w = potencia_disponible_w * self.eficiencia_solar_ideal * factor_temperatura
        
        # Eficiencia real
        if potencia_teorica_w > 0:
            eficiencia_real = potencia_generada_w / potencia_teorica_w
        else:
            eficiencia_real = 0
        
        eficiencia_percent = eficiencia_real * 100
        perdida_w = potencia_teorica_w - potencia_generada_w
        
        # Diagnóstico
        if eficiencia_real < self.umbral_critico:
            nivel = 'CRÍTICO'
            diagnostico = self._diagnosticar_problema_solar(eficiencia_real)
            alerta = True
        elif eficiencia_real < self.umbral_advertencia:
            nivel = 'ADVERTENCIA'
            diagnostico = 'Eficiencia reducida - Revisar paneles'
            alerta = True
        else:
            nivel = 'NORMAL'
            diagnostico = 'Paneles operando correctamente'
            alerta = False
        
        # Guardar en historial
        self.historial_eficiencia_solar.append({
            'timestamp': datetime.now().isoformat(),
            'eficiencia': eficiencia_real
        })
        
        # Mantener solo últimos 100 registros
        if len(self.historial_eficiencia_solar) > 100:
            self.historial_eficiencia_solar.pop(0)
        
        return {
            'status': 'success',
            'componente': 'Paneles Solares',
            'eficiencia_percent': round(eficiencia_percent, 1),
            'eficiencia_decimal': round(eficiencia_real, 3),
            'nivel': nivel,
            'alerta': alerta,
            'diagnostico': diagnostico,
            'mediciones': {
                'irradiancia_w_m2': round(irradiancia_w_m2, 1),
                'area_m2': area_paneles_m2,
                'potencia_disponible_w': round(potencia_disponible_w, 1),
                'potencia_teorica_w': round(potencia_teorica_w, 1),
                'potencia_real_w': round(potencia_generada_w, 1),
                'perdida_w': round(perdida_w, 1),
                'temperatura_c': temperatura_ambiente_c,
                'factor_temperatura': round(factor_temperatura, 3)
            },
            'recomendaciones': self._generar_recomendaciones_solar(eficiencia_real, temperatura_ambiente_c)
        }
    
    def calcular_eficiencia_eolica(
        self,
        velocidad_viento_ms: float,
        potencia_generada_w: float,
        potencia_nominal_turbina_w: float,
        area_barrido_m2: Optional[float] = None,
        densidad_aire: float = 1.225  # kg/m³ a nivel del mar, 15°C
    ) -> Dict:
        """
        Calcula eficiencia real de turbina eólica
        
        Args:
            velocidad_viento_ms: Velocidad del viento (m/s)
            potencia_generada_w: Potencia real generada (W)
            potencia_nominal_turbina_w: Potencia nominal de la turbina
            area_barrido_m2: Área de barrido de las palas (opcional)
            densidad_aire: Densidad del aire
        
        Returns:
            Dict con eficiencia y diagnóstico
        """
        
        if velocidad_viento_ms < 2.5:
            return {
                'status': 'viento_bajo',
                'mensaje': 'Viento insuficiente para medición (< 2.5 m/s)',
                'eficiencia_percent': 0,
                'potencia_teorica_w': 0,
                'potencia_real_w': potencia_generada_w,
                'perdida_w': 0
            }
        
        # Si no se proporciona área, estimarla desde potencia nominal
        if area_barrido_m2 is None:
            # Estimación: P = 0.5 * densidad * área * v³ * eficiencia
            # Para v=12 m/s (velocidad nominal típica) y eficiencia 0.4
            area_barrido_m2 = potencia_nominal_turbina_w / (0.5 * densidad_aire * (12**3) * 0.4)
        
        # Potencia disponible en el viento (fórmula de Betz)
        potencia_viento_w = 0.5 * densidad_aire * area_barrido_m2 * (velocidad_viento_ms ** 3)
        
        # Potencia teórica máxima (límite de Betz: 59.3%, en práctica 40-50%)
        potencia_teorica_w = potencia_viento_w * self.eficiencia_turbina_ideal
        
        # Limitar por potencia nominal de la turbina
        potencia_teorica_w = min(potencia_teorica_w, potencia_nominal_turbina_w)
        
        # Eficiencia real
        if potencia_teorica_w > 0:
            eficiencia_real = potencia_generada_w / potencia_teorica_w
        else:
            eficiencia_real = 0
        
        eficiencia_percent = eficiencia_real * 100
        perdida_w = potencia_teorica_w - potencia_generada_w
        
        # Diagnóstico
        if eficiencia_real < self.umbral_critico:
            nivel = 'CRÍTICO'
            diagnostico = self._diagnosticar_problema_eolico(eficiencia_real, velocidad_viento_ms)
            alerta = True
        elif eficiencia_real < self.umbral_advertencia:
            nivel = 'ADVERTENCIA'
            diagnostico = 'Eficiencia reducida - Revisar turbina'
            alerta = True
        else:
            nivel = 'NORMAL'
            diagnostico = 'Turbina operando correctamente'
            alerta = False
        
        # Guardar en historial
        self.historial_eficiencia_eolica.append({
            'timestamp': datetime.now().isoformat(),
            'eficiencia': eficiencia_real
        })
        
        if len(self.historial_eficiencia_eolica) > 100:
            self.historial_eficiencia_eolica.pop(0)
        
        return {
            'status': 'success',
            'componente': 'Turbina Eólica',
            'eficiencia_percent': round(eficiencia_percent, 1),
            'eficiencia_decimal': round(eficiencia_real, 3),
            'nivel': nivel,
            'alerta': alerta,
            'diagnostico': diagnostico,
            'mediciones': {
                'velocidad_viento_ms': round(velocidad_viento_ms, 2),
                'area_barrido_m2': round(area_barrido_m2, 2),
                'potencia_viento_w': round(potencia_viento_w, 1),
                'potencia_teorica_w': round(potencia_teorica_w, 1),
                'potencia_real_w': round(potencia_generada_w, 1),
                'perdida_w': round(perdida_w, 1),
                'potencia_nominal_w': potencia_nominal_turbina_w
            },
            'recomendaciones': self._generar_recomendaciones_eolica(eficiencia_real, velocidad_viento_ms)
        }
    
    def _diagnosticar_problema_solar(self, eficiencia: float) -> str:
        """Diagnostica problemas en paneles solares"""
        if eficiencia < 0.40:
            return '🚨 CRÍTICO: Paneles sucios, sombreados o dañados. ¡Revisar urgente!'
        elif eficiencia < 0.50:
            return '⚠️ Paneles muy sucios o con sombra parcial. Limpiar pronto.'
        elif eficiencia < 0.60:
            return '⚠️ Paneles necesitan limpieza o hay sombra.'
        else:
            return '💡 Eficiencia reducida - Revisar orientación o limpieza.'
    
    def _diagnosticar_problema_eolico(self, eficiencia: float, viento: float) -> str:
        """Diagnostica problemas en turbina eólica"""
        if eficiencia < 0.40:
            return '🚨 CRÍTICO: Turbina con problemas mecánicos o palas dañadas. ¡Revisar!'
        elif eficiencia < 0.50:
            return '⚠️ Posible fricción en rodamientos o palas sucias/dañadas.'
        elif eficiencia < 0.60:
            return '⚠️ Turbina necesita mantenimiento. Revisar palas y rodamientos.'
        else:
            return '💡 Eficiencia reducida - Verificar alineación y lubricación.'
    
    def _generar_recomendaciones_solar(self, eficiencia: float, temperatura: float) -> List[str]:
        """Genera recomendaciones para paneles solares"""
        recomendaciones = []
        
        if eficiencia < 0.60:
            recomendaciones.append('🧹 Limpiar paneles con agua y paño suave')
            recomendaciones.append('🌳 Verificar que no haya sombras de árboles o edificios')
            recomendaciones.append('🔍 Inspeccionar visualmente en busca de daños')
        elif eficiencia < 0.75:
            recomendaciones.append('💧 Programar limpieza de paneles')
            recomendaciones.append('📐 Verificar ángulo de inclinación óptimo')
        
        if temperatura > 40:
            recomendaciones.append('🌡️ Alta temperatura reduce eficiencia (~0.5% por °C)')
            recomendaciones.append('💨 Considerar mejor ventilación de paneles')
        
        if eficiencia > 0.85:
            recomendaciones.append('✅ Paneles en excelente estado')
            recomendaciones.append('📅 Mantener limpieza regular (cada 3-6 meses)')
        
        return recomendaciones
    
    def _generar_recomendaciones_eolica(self, eficiencia: float, viento: float) -> List[str]:
        """Genera recomendaciones para turbina eólica"""
        recomendaciones = []
        
        if eficiencia < 0.60:
            recomendaciones.append('🔧 Revisar rodamientos y lubricar si es necesario')
            recomendaciones.append('🌀 Inspeccionar palas en busca de daños o suciedad')
            recomendaciones.append('⚙️ Verificar alineación del rotor')
            recomendaciones.append('🔩 Apretar todos los tornillos y conexiones')
        elif eficiencia < 0.75:
            recomendaciones.append('🛠️ Programar mantenimiento preventivo')
            recomendaciones.append('🧼 Limpiar palas si están sucias')
        
        if viento > 15:
            recomendaciones.append('💨 Viento fuerte - Verificar sistema de frenado')
            recomendaciones.append('🛡️ Confirmar que protección anti-embalamiento funciona')
        
        if eficiencia > 0.85:
            recomendaciones.append('✅ Turbina en excelente estado')
            recomendaciones.append('📅 Continuar con mantenimiento regular')
        
        return recomendaciones
    
    def analizar_tendencia(self, componente: str = 'solar') -> Dict:
        """Analiza tendencia de eficiencia en el tiempo"""
        historial = self.historial_eficiencia_solar if componente == 'solar' else self.historial_eficiencia_eolica
        
        if len(historial) < 5:
            return {
                'status': 'insuficiente',
                'mensaje': 'Datos insuficientes para análisis de tendencia'
            }
        
        # Calcular promedio de últimos 10 vs primeros 10
        ultimos = [h['eficiencia'] for h in historial[-10:]]
        primeros = [h['eficiencia'] for h in historial[:10]]
        
        promedio_actual = sum(ultimos) / len(ultimos)
        promedio_inicial = sum(primeros) / len(primeros)
        
        cambio = ((promedio_actual - promedio_inicial) / promedio_inicial) * 100
        
        if cambio < -10:
            tendencia = 'DEGRADACIÓN'
            mensaje = f'Eficiencia cayó {abs(cambio):.1f}% - Requiere mantenimiento'
        elif cambio < -5:
            tendencia = 'DISMINUCIÓN'
            mensaje = f'Eficiencia bajó {abs(cambio):.1f}% - Monitorear'
        elif cambio > 5:
            tendencia = 'MEJORA'
            mensaje = f'Eficiencia mejoró {cambio:.1f}% - Excelente'
        else:
            tendencia = 'ESTABLE'
            mensaje = 'Eficiencia estable en el tiempo'
        
        return {
            'status': 'success',
            'tendencia': tendencia,
            'cambio_percent': round(cambio, 1),
            'eficiencia_actual': round(promedio_actual * 100, 1),
            'eficiencia_inicial': round(promedio_inicial * 100, 1),
            'mensaje': mensaje,
            'registros_analizados': len(historial)
        }


# Instancia global
efficiency_monitor = EfficiencyMonitor()
