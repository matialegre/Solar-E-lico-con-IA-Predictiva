"""
Servicio para gestión de cargas eléctricas
Diferencia entre cargas resistivas e inductivas
Calcula picos de arranque y factor de potencia
"""

from typing import List, Dict
from dataclasses import dataclass
from enum import Enum


class TipoCarga(str, Enum):
    """Tipo de carga eléctrica"""
    RESISTIVA = "resistiva"
    INDUCTIVA = "inductiva"
    CAPACITIVA = "capacitiva"


@dataclass
class Carga:
    """Modelo de carga eléctrica"""
    nombre: str
    potencia_nominal_w: float
    tipo: TipoCarga
    factor_potencia: float
    factor_arranque: float  # Multiplicador de pico
    duracion_pico_seg: float
    cantidad: int = 1
    
    @property
    def potencia_pico_w(self) -> float:
        """Potencia de pico durante arranque"""
        return self.potencia_nominal_w * self.factor_arranque
    
    @property
    def potencia_aparente_va(self) -> float:
        """Potencia aparente (VA)"""
        return self.potencia_nominal_w / self.factor_potencia


# Base de datos de cargas típicas
CARGAS_TIPICAS = {
    # RESISTIVAS (factor arranque ≈ 1.0)
    "luces_led": Carga("Luces LED", 100, TipoCarga.RESISTIVA, 1.0, 1.0, 0),
    "luces_incandescente": Carga("Luces Incandescentes", 100, TipoCarga.RESISTIVA, 1.0, 1.2, 0.1),
    "calefactor": Carga("Calefactor", 1500, TipoCarga.RESISTIVA, 1.0, 1.0, 0),
    "horno_electrico": Carga("Horno Eléctrico", 2000, TipoCarga.RESISTIVA, 1.0, 1.0, 0),
    "pava_electrica": Carga("Pava Eléctrica", 1500, TipoCarga.RESISTIVA, 1.0, 1.0, 0),
    "plancha": Carga("Plancha", 1200, TipoCarga.RESISTIVA, 1.0, 1.0, 0),
    "tv_led": Carga("TV LED", 150, TipoCarga.RESISTIVA, 0.95, 1.5, 0.5),
    "notebook": Carga("Notebook", 60, TipoCarga.CAPACITIVA, 0.90, 1.2, 0.1),
    "pc_escritorio": Carga("PC Escritorio", 300, TipoCarga.CAPACITIVA, 0.85, 1.8, 0.2),
    
    # INDUCTIVAS (factor arranque 3-7x)
    "heladera": Carga("Heladera", 400, TipoCarga.INDUCTIVA, 0.7, 4.0, 2.0),
    "freezer": Carga("Freezer", 300, TipoCarga.INDUCTIVA, 0.7, 4.0, 2.0),
    "lavarropas": Carga("Lavarropas", 500, TipoCarga.INDUCTIVA, 0.6, 5.0, 3.0),
    "secarropas": Carga("Secarropas", 2000, TipoCarga.INDUCTIVA, 0.65, 4.0, 2.0),
    "lavavajillas": Carga("Lavavajillas", 1500, TipoCarga.INDUCTIVA, 0.70, 3.5, 2.0),
    "aire_acondicionado_1500w": Carga("Aire Acondicionado 1500W", 1500, TipoCarga.INDUCTIVA, 0.85, 3.0, 2.0),
    "aire_acondicionado_2500w": Carga("Aire Acondicionado 2500W", 2500, TipoCarga.INDUCTIVA, 0.85, 3.5, 2.5),
    "bomba_agua": Carga("Bomba de Agua", 750, TipoCarga.INDUCTIVA, 0.75, 4.5, 2.0),
    "compresor": Carga("Compresor", 1500, TipoCarga.INDUCTIVA, 0.70, 5.0, 3.0),
    "taladro": Carga("Taladro", 600, TipoCarga.INDUCTIVA, 0.75, 3.0, 1.0),
    "amoladora": Carga("Amoladora", 800, TipoCarga.INDUCTIVA, 0.75, 3.5, 1.5),
    "soldadora": Carga("Soldadora", 3000, TipoCarga.INDUCTIVA, 0.60, 3.0, 1.0),
    "microondas": Carga("Microondas", 1000, TipoCarga.INDUCTIVA, 0.70, 2.0, 1.0),
}


class CargasService:
    """Servicio para gestión de cargas"""
    
    def __init__(self):
        self.cargas_disponibles = CARGAS_TIPICAS
    
    def calcular_sistema_cargas(self, cargas_seleccionadas: List[Dict]) -> Dict:
        """
        Calcular dimensionamiento considerando cargas reales
        
        Args:
            cargas_seleccionadas: Lista de cargas con formato:
                [{"tipo": "heladera", "cantidad": 1}, ...]
        
        Returns:
            Dict con análisis completo de cargas
        """
        cargas_activas = []
        
        # Procesar cargas seleccionadas
        for carga_sel in cargas_seleccionadas:
            tipo = carga_sel.get("tipo")
            cantidad = carga_sel.get("cantidad", 1)
            
            if tipo in self.cargas_disponibles:
                carga = self.cargas_disponibles[tipo]
                carga.cantidad = cantidad
                cargas_activas.append(carga)
        
        # Calcular consumos
        potencia_nominal_total = sum(c.potencia_nominal_w * c.cantidad for c in cargas_activas)
        potencia_pico_total = sum(c.potencia_pico_w * c.cantidad for c in cargas_activas)
        potencia_aparente_total = sum(c.potencia_aparente_va * c.cantidad for c in cargas_activas)
        
        # Separar por tipo
        resistivas = [c for c in cargas_activas if c.tipo == TipoCarga.RESISTIVA]
        inductivas = [c for c in cargas_activas if c.tipo == TipoCarga.INDUCTIVA]
        capacitivas = [c for c in cargas_activas if c.tipo == TipoCarga.CAPACITIVA]
        
        potencia_resistiva = sum(c.potencia_nominal_w * c.cantidad for c in resistivas)
        potencia_inductiva = sum(c.potencia_nominal_w * c.cantidad for c in inductivas)
        potencia_capacitiva = sum(c.potencia_nominal_w * c.cantidad for c in capacitivas)
        
        # Factor de potencia promedio ponderado
        if potencia_nominal_total > 0:
            fp_promedio = sum(
                c.potencia_nominal_w * c.cantidad * c.factor_potencia 
                for c in cargas_activas
            ) / potencia_nominal_total
        else:
            fp_promedio = 1.0
        
        # Dimensionamiento inversor
        # Regla: Inversor debe soportar el pico más alto
        inversor_minimo_w = potencia_pico_total * 1.2  # 20% margen seguridad
        inversor_recomendado_w = self._redondear_inversor(inversor_minimo_w)
        
        # Dimensionamiento conductores (por corriente RMS)
        corriente_nominal_a = potencia_aparente_total / 220  # Asumiendo 220V
        corriente_pico_a = (potencia_pico_total / 220) / fp_promedio
        
        # Sección cable recomendada (regla: 6A por mm²)
        seccion_cable_mm2 = max(1.5, corriente_pico_a / 6)
        seccion_cable_recomendada = self._redondear_seccion_cable(seccion_cable_mm2)
        
        # Protección térmica recomendada
        termomagnetica_a = corriente_nominal_a * 1.25  # 25% sobre nominal
        termomagnetica_recomendada = self._redondear_termomagnetica(termomagnetica_a)
        
        return {
            "resumen": {
                "potencia_nominal_total_w": potencia_nominal_total,
                "potencia_pico_total_w": potencia_pico_total,
                "potencia_aparente_total_va": potencia_aparente_total,
                "factor_potencia_promedio": fp_promedio,
                "consumo_diario_kwh": (potencia_nominal_total * 24) / 1000  # Asumiendo 24h
            },
            "distribucion": {
                "resistiva_w": potencia_resistiva,
                "resistiva_porcentaje": (potencia_resistiva / potencia_nominal_total * 100) if potencia_nominal_total > 0 else 0,
                "inductiva_w": potencia_inductiva,
                "inductiva_porcentaje": (potencia_inductiva / potencia_nominal_total * 100) if potencia_nominal_total > 0 else 0,
                "capacitiva_w": potencia_capacitiva,
                "capacitiva_porcentaje": (potencia_capacitiva / potencia_nominal_total * 100) if potencia_nominal_total > 0 else 0
            },
            "cargas_detalle": [
                {
                    "nombre": c.nombre,
                    "tipo": c.tipo.value,
                    "cantidad": c.cantidad,
                    "potencia_nominal_w": c.potencia_nominal_w * c.cantidad,
                    "potencia_pico_w": c.potencia_pico_w * c.cantidad,
                    "factor_potencia": c.factor_potencia,
                    "factor_arranque": c.factor_arranque,
                    "duracion_pico_seg": c.duracion_pico_seg
                }
                for c in cargas_activas
            ],
            "dimensionamiento": {
                "inversor_minimo_w": inversor_minimo_w,
                "inversor_recomendado_w": inversor_recomendado_w,
                "inversor_continuo_w": potencia_nominal_total * 1.3,
                "corriente_nominal_a": corriente_nominal_a,
                "corriente_pico_a": corriente_pico_a,
                "seccion_cable_mm2": seccion_cable_recomendada,
                "termomagnetica_a": termomagnetica_recomendada
            },
            "ecuaciones": {
                "potencia_aparente": {
                    "formula": "S (VA) = P (W) / FP",
                    "explicacion": "Potencia aparente considerando factor de potencia",
                    "ejemplo": f"S = {potencia_nominal_total:.0f} / {fp_promedio:.2f} = {potencia_aparente_total:.0f} VA"
                },
                "corriente_nominal": {
                    "formula": "I = S / V",
                    "explicacion": "Corriente en régimen normal",
                    "ejemplo": f"I = {potencia_aparente_total:.0f} / 220 = {corriente_nominal_a:.1f} A"
                },
                "corriente_pico": {
                    "formula": "I_pico = P_pico / (V × FP)",
                    "explicacion": "Corriente durante arranque de motores",
                    "ejemplo": f"I_pico = {potencia_pico_total:.0f} / (220 × {fp_promedio:.2f}) = {corriente_pico_a:.1f} A"
                },
                "inversor": {
                    "formula": "P_inv = P_pico × 1.2",
                    "explicacion": "Inversor debe soportar pico + 20% margen",
                    "ejemplo": f"P_inv = {potencia_pico_total:.0f} × 1.2 = {inversor_minimo_w:.0f} W"
                }
            },
            "advertencias": self._generar_advertencias(cargas_activas, inversor_recomendado_w, potencia_pico_total)
        }
    
    def _redondear_inversor(self, potencia_w: float) -> int:
        """Redondear a potencias comerciales de inversores"""
        potencias = [1000, 1500, 2000, 3000, 5000, 8000, 10000, 15000, 20000]
        for p in potencias:
            if p >= potencia_w:
                return p
        return int(potencia_w * 1.2)
    
    def _redondear_seccion_cable(self, seccion_mm2: float) -> float:
        """Redondear a secciones comerciales de cable"""
        secciones = [1.5, 2.5, 4, 6, 10, 16, 25, 35, 50]
        for s in secciones:
            if s >= seccion_mm2:
                return s
        return seccion_mm2
    
    def _redondear_termomagnetica(self, corriente_a: float) -> int:
        """Redondear a valores comerciales de termomagnéticas"""
        valores = [6, 10, 16, 20, 25, 32, 40, 50, 63, 80, 100]
        for v in valores:
            if v >= corriente_a:
                return v
        return int(corriente_a * 1.2)
    
    def _generar_advertencias(self, cargas: List[Carga], inversor_w: int, pico_w: float) -> List[str]:
        """Generar advertencias sobre el sistema"""
        advertencias = []
        
        # Verificar cargas inductivas grandes
        inductivas_grandes = [c for c in cargas if c.tipo == TipoCarga.INDUCTIVA and c.potencia_nominal_w > 1000]
        if inductivas_grandes:
            advertencias.append(
                f"⚠️ Cargas inductivas grandes detectadas: {', '.join(c.nombre for c in inductivas_grandes)}. "
                f"Considerar arranque secuencial para evitar picos simultáneos."
            )
        
        # Verificar si inversor está al límite
        if pico_w > inversor_w * 0.9:
            advertencias.append(
                f"⚠️ Inversor cerca del límite ({pico_w:.0f}W de {inversor_w}W). "
                f"Evitar arrancar todas las cargas simultáneamente."
            )
        
        # Verificar múltiples motores
        motores = [c for c in cargas if c.tipo == TipoCarga.INDUCTIVA]
        if len(motores) >= 3:
            advertencias.append(
                f"💡 Sistema con {len(motores)} cargas inductivas. "
                f"Recomendado: Arranque escalonado con 5-10 segundos entre cada carga."
            )
        
        return advertencias


# Singleton
cargas_service = CargasService()
