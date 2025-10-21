"""
Servicio de dimensionamiento de sistemas solares y eólicos

Implementa:
1. Cálculos de dimensionamiento solar (similar a pvlib)
2. Fórmulas de Betz para eólico
3. Dimensionamiento de baterías
4. Análisis de viabilidad

Muestra ecuaciones y pasos de cálculo
"""

import math
from typing import Dict, Tuple, List
from dataclasses import dataclass


@dataclass
class ComponenteSolar:
    """Componente solar disponible"""
    nombre: str
    potencia_w: int
    area_m2: float
    eficiencia: float
    precio_usd: float
    fabricante: str


@dataclass
class ComponenteEolico:
    """Componente eólico disponible"""
    nombre: str
    potencia_w: int
    diametro_m: float
    velocidad_arranque_ms: float
    velocidad_nominal_ms: float
    precio_usd: float
    fabricante: str


class DimensionamientoService:
    """
    Servicio de dimensionamiento de sistemas renovables
    """
    
    # Constantes
    HORAS_SOL_PICO_STANDAR = 4.0  # HSP estándar
    EFICIENCIA_SISTEMA_SOLAR = 0.85  # Pérdidas cables, inversor, etc
    PROFUNDIDAD_DESCARGA_BATERIA = 0.80  # DoD 80%
    DENSIDAD_AIRE = 1.225  # kg/m³ al nivel del mar
    LIMITE_BETZ = 0.593  # 59.3% eficiencia máxima teórica
    EFICIENCIA_TURBINA_REAL = 0.35  # 35% eficiencia real típica
    
    # Base de datos de componentes (simplificada)
    PANELES_DISPONIBLES = [
        ComponenteSolar("Panel 300W Monocristalino", 300, 1.65, 0.18, 150, "Generic"),
        ComponenteSolar("Panel 400W Monocristalino", 400, 2.0, 0.20, 200, "Generic"),
        ComponenteSolar("Panel 500W Bifacial", 500, 2.3, 0.22, 280, "Generic"),
    ]
    
    TURBINAS_DISPONIBLES = [
        ComponenteEolico("Turbina 400W", 400, 1.2, 2.5, 12.0, 350, "Generic"),
        ComponenteEolico("Turbina 1000W", 1000, 1.8, 3.0, 12.0, 650, "Generic"),
        ComponenteEolico("Turbina 2000W", 2000, 2.5, 3.5, 12.0, 1200, "Generic"),
        ComponenteEolico("Turbina 5000W", 5000, 4.0, 4.0, 13.0, 2800, "Generic"),
    ]
    
    def calcular_hsp_real(
        self,
        irradiancia_promedio_kwh_m2_dia: float
    ) -> float:
        """
        Calcular Horas Sol Pico reales
        
        ECUACIÓN:
        HSP = Irradiancia_diaria (kWh/m²/día)
        
        Args:
            irradiancia_promedio_kwh_m2_dia: Irradiancia promedio diaria
        
        Returns:
            HSP (horas)
        """
        return irradiancia_promedio_kwh_m2_dia
    
    def dimensionar_solar_opcion1(
        self,
        consumo_diario_kwh: float,
        irradiancia_kwh_m2_dia: float,
        dias_autonomia: int = 2
    ) -> Dict:
        """
        OPCIÓN 1: Tengo X consumo, ¿qué sistema necesito?
        
        ECUACIONES:
        
        1) Energía solar necesaria por día:
           E_solar = Consumo_diario / % cobertura_solar
        
        2) Potencia pico necesaria:
           P_pico = E_solar / (HSP * Eficiencia_sistema)
        
        3) Número de paneles:
           N_paneles = P_pico / Potencia_panel
        
        4) Área total:
           Área = N_paneles * Área_panel
        
        Args:
            consumo_diario_kwh: Consumo diario (kWh/día)
            irradiancia_kwh_m2_dia: Irradiancia solar (kWh/m²/día)
            dias_autonomia: Días de autonomía batería
        
        Returns:
            Dict con dimensionamiento y ecuaciones
        """
        hsp = self.calcular_hsp_real(irradiancia_kwh_m2_dia)
        
        # Asumimos 60% cobertura solar, 40% eólica
        energia_solar_necesaria = consumo_diario_kwh * 0.60
        
        # Potencia pico necesaria
        potencia_pico_w = (energia_solar_necesaria * 1000) / (hsp * self.EFICIENCIA_SISTEMA_SOLAR)
        
        # Elegir panel óptimo
        panel_elegido = self.PANELES_DISPONIBLES[1]  # 400W por defecto
        
        # Número de paneles
        num_paneles = math.ceil(potencia_pico_w / panel_elegido.potencia_w)
        
        # Ajustar potencia total real
        potencia_total_w = num_paneles * panel_elegido.potencia_w
        
        # Área total
        area_total_m2 = num_paneles * panel_elegido.area_m2
        
        # Generación diaria estimada
        generacion_diaria_kwh = (potencia_total_w / 1000) * hsp * self.EFICIENCIA_SISTEMA_SOLAR
        
        # Costo
        costo_total_usd = num_paneles * panel_elegido.precio_usd
        
        return {
            "sistema": "solar",
            "tipo": "opcion1_desde_consumo",
            "entrada": {
                "consumo_diario_kwh": consumo_diario_kwh,
                "irradiancia_kwh_m2_dia": irradiancia_kwh_m2_dia,
                "dias_autonomia": dias_autonomia
            },
            "calculos": {
                "paso1": {
                    "nombre": "Horas Sol Pico (HSP)",
                    "ecuacion": "HSP = Irradiancia_diaria",
                    "valores": f"HSP = {irradiancia_kwh_m2_dia}",
                    "resultado": f"{hsp:.2f} horas"
                },
                "paso2": {
                    "nombre": "Energía solar necesaria",
                    "ecuacion": "E_solar = Consumo_diario × 60%",
                    "valores": f"E_solar = {consumo_diario_kwh} × 0.60",
                    "resultado": f"{energia_solar_necesaria:.2f} kWh/día"
                },
                "paso3": {
                    "nombre": "Potencia pico necesaria",
                    "ecuacion": "P_pico = E_solar / (HSP × η_sistema)",
                    "valores": f"P_pico = {energia_solar_necesaria * 1000:.0f} / ({hsp:.2f} × {self.EFICIENCIA_SISTEMA_SOLAR})",
                    "resultado": f"{potencia_pico_w:.0f} W"
                },
                "paso4": {
                    "nombre": "Número de paneles",
                    "ecuacion": "N = ceil(P_pico / P_panel)",
                    "valores": f"N = ceil({potencia_pico_w:.0f} / {panel_elegido.potencia_w})",
                    "resultado": f"{num_paneles} paneles"
                }
            },
            "resultado": {
                "paneles": {
                    "modelo": panel_elegido.nombre,
                    "cantidad": num_paneles,
                    "potencia_unitaria_w": panel_elegido.potencia_w,
                    "potencia_total_w": potencia_total_w,
                    "area_total_m2": area_total_m2,
                    "eficiencia": panel_elegido.eficiencia
                },
                "generacion": {
                    "diaria_kwh": generacion_diaria_kwh,
                    "mensual_kwh": generacion_diaria_kwh * 30,
                    "anual_kwh": generacion_diaria_kwh * 365
                },
                "cobertura": {
                    "porcentaje": (generacion_diaria_kwh / consumo_diario_kwh) * 100,
                    "excedente_kwh": generacion_diaria_kwh - energia_solar_necesaria
                },
                "costo": {
                    "paneles_usd": costo_total_usd,
                    "estructura_usd": costo_total_usd * 0.15,
                    "inversor_usd": potencia_total_w * 0.3,
                    "instalacion_usd": costo_total_usd * 0.20,
                    "total_estimado_usd": costo_total_usd * 1.65
                }
            }
        }
    
    def dimensionar_eolico_opcion1(
        self,
        consumo_diario_kwh: float,
        velocidad_viento_promedio_ms: float
    ) -> Dict:
        """
        Dimensionamiento eólico desde consumo
        
        ECUACIONES:
        
        1) Potencia del viento disponible:
           P_viento = 0.5 × ρ × A × v³
           donde:
           - ρ = densidad aire (1.225 kg/m³)
           - A = área barrido (π × r²)
           - v = velocidad viento (m/s)
        
        2) Potencia aprovechable (Límite de Betz):
           P_max_teorica = P_viento × 0.593
        
        3) Potencia real (eficiencia turbina):
           P_real = P_viento × η_turbina (≈35%)
        
        4) Energía diaria:
           E_diaria = P_real × 24h
        
        Args:
            consumo_diario_kwh: Consumo diario
            velocidad_viento_promedio_ms: Velocidad promedio viento
        
        Returns:
            Dict con dimensionamiento y ecuaciones
        """
        # Asumimos 40% cobertura eólica
        energia_eolica_necesaria = consumo_diario_kwh * 0.40
        
        # Energía necesaria en Wh
        energia_necesaria_wh = energia_eolica_necesaria * 1000
        
        # Potencia promedio necesaria
        potencia_promedio_w = energia_necesaria_wh / 24
        
        # Elegir turbina
        turbina_elegida = None
        for turbina in sorted(self.TURBINAS_DISPONIBLES, key=lambda x: x.potencia_w):
            # Calcular potencia real a velocidad promedio
            area_barrido = math.pi * (turbina.diametro_m / 2) ** 2
            potencia_viento = 0.5 * self.DENSIDAD_AIRE * area_barrido * (velocidad_viento_promedio_ms ** 3)
            potencia_real = potencia_viento * self.EFICIENCIA_TURBINA_REAL
            
            if potencia_real >= potencia_promedio_w:
                turbina_elegida = turbina
                break
        
        if turbina_elegida is None:
            turbina_elegida = self.TURBINAS_DISPONIBLES[-1]  # La más grande
        
        # Calcular con turbina elegida
        area_barrido = math.pi * (turbina_elegida.diametro_m / 2) ** 2
        potencia_viento_disponible = 0.5 * self.DENSIDAD_AIRE * area_barrido * (velocidad_viento_promedio_ms ** 3)
        potencia_max_teorica = potencia_viento_disponible * self.LIMITE_BETZ
        potencia_real = potencia_viento_disponible * self.EFICIENCIA_TURBINA_REAL
        
        # Generación diaria
        generacion_diaria_kwh = (potencia_real * 24) / 1000
        
        # Número de turbinas necesarias
        num_turbinas = math.ceil(energia_eolica_necesaria / generacion_diaria_kwh)
        
        # Ajustar generación total
        generacion_total_kwh = generacion_diaria_kwh * num_turbinas
        
        return {
            "sistema": "eolico",
            "tipo": "opcion1_desde_consumo",
            "entrada": {
                "consumo_diario_kwh": consumo_diario_kwh,
                "velocidad_viento_ms": velocidad_viento_promedio_ms
            },
            "calculos": {
                "paso1": {
                    "nombre": "Área de barrido",
                    "ecuacion": "A = π × r²",
                    "valores": f"A = π × ({turbina_elegida.diametro_m}/2)²",
                    "resultado": f"{area_barrido:.2f} m²"
                },
                "paso2": {
                    "nombre": "Potencia del viento",
                    "ecuacion": "P_viento = 0.5 × ρ × A × v³",
                    "valores": f"P = 0.5 × {self.DENSIDAD_AIRE} × {area_barrido:.2f} × {velocidad_viento_promedio_ms}³",
                    "resultado": f"{potencia_viento_disponible:.0f} W"
                },
                "paso3": {
                    "nombre": "Límite de Betz (máximo teórico)",
                    "ecuacion": "P_max = P_viento × 59.3%",
                    "valores": f"P_max = {potencia_viento_disponible:.0f} × 0.593",
                    "resultado": f"{potencia_max_teorica:.0f} W"
                },
                "paso4": {
                    "nombre": "Potencia real aprovechable",
                    "ecuacion": "P_real = P_viento × η_turbina",
                    "valores": f"P_real = {potencia_viento_disponible:.0f} × {self.EFICIENCIA_TURBINA_REAL}",
                    "resultado": f"{potencia_real:.0f} W"
                },
                "paso5": {
                    "nombre": "Generación diaria",
                    "ecuacion": "E_diaria = P_real × 24h",
                    "valores": f"E = {potencia_real:.0f} × 24",
                    "resultado": f"{generacion_diaria_kwh:.2f} kWh/día"
                }
            },
            "resultado": {
                "turbinas": {
                    "modelo": turbina_elegida.nombre,
                    "cantidad": num_turbinas,
                    "potencia_unitaria_w": turbina_elegida.potencia_w,
                    "diametro_m": turbina_elegida.diametro_m,
                    "velocidad_arranque_ms": turbina_elegida.velocidad_arranque_ms
                },
                "generacion": {
                    "diaria_kwh": generacion_total_kwh,
                    "mensual_kwh": generacion_total_kwh * 30,
                    "anual_kwh": generacion_total_kwh * 365
                },
                "cobertura": {
                    "porcentaje": (generacion_total_kwh / consumo_diario_kwh) * 100,
                    "excedente_kwh": generacion_total_kwh - energia_eolica_necesaria
                },
                "costo": {
                    "turbinas_usd": num_turbinas * turbina_elegida.precio_usd,
                    "torre_usd": num_turbinas * 400,
                    "controlador_usd": num_turbinas * 200,
                    "instalacion_usd": num_turbinas * turbina_elegida.precio_usd * 0.25,
                    "total_estimado_usd": num_turbinas * turbina_elegida.precio_usd * 1.60
                }
            }
        }
    
    def dimensionar_bateria(
        self,
        consumo_diario_kwh: float,
        dias_autonomia: int = 2,
        voltaje_sistema: int = 48
    ) -> Dict:
        """
        Dimensionamiento de batería
        
        ECUACIONES:
        
        1) Capacidad necesaria:
           C_bat = (Consumo_diario × Días_autonomía) / DoD
        
        2) Capacidad en Ah:
           C_Ah = (C_bat × 1000) / V_sistema
        
        3) Número de baterías en serie:
           N_serie = V_sistema / V_bateria
        
        4) Número de baterías en paralelo:
           N_paralelo = C_Ah_necesaria / C_Ah_bateria
        
        Args:
            consumo_diario_kwh: Consumo diario
            dias_autonomia: Días de autonomía
            voltaje_sistema: Voltaje del sistema (12, 24, 48V)
        
        Returns:
            Dict con dimensionamiento batería
        """
        # Capacidad en kWh
        capacidad_kwh = (consumo_diario_kwh * dias_autonomia) / self.PROFUNDIDAD_DESCARGA_BATERIA
        
        # Capacidad en Ah
        capacidad_ah = (capacidad_kwh * 1000) / voltaje_sistema
        
        # Batería típica: 12V 200Ah
        voltaje_bateria = 12
        capacidad_bateria_ah = 200
        
        # Baterías en serie para voltaje
        num_serie = voltaje_sistema // voltaje_bateria
        
        # Baterías en paralelo para capacidad
        num_paralelo = math.ceil(capacidad_ah / capacidad_bateria_ah)
        
        # Total baterías
        total_baterias = num_serie * num_paralelo
        
        # Capacidad real
        capacidad_real_kwh = (num_paralelo * capacidad_bateria_ah * voltaje_sistema) / 1000
        
        return {
            "sistema": "bateria",
            "entrada": {
                "consumo_diario_kwh": consumo_diario_kwh,
                "dias_autonomia": dias_autonomia,
                "voltaje_sistema": voltaje_sistema
            },
            "calculos": {
                "paso1": {
                    "nombre": "Capacidad necesaria",
                    "ecuacion": "C = (Consumo × Días) / DoD",
                    "valores": f"C = ({consumo_diario_kwh} × {dias_autonomia}) / {self.PROFUNDIDAD_DESCARGA_BATERIA}",
                    "resultado": f"{capacidad_kwh:.2f} kWh"
                },
                "paso2": {
                    "nombre": "Capacidad en Ah",
                    "ecuacion": "C_Ah = (C_kWh × 1000) / V_sistema",
                    "valores": f"C_Ah = ({capacidad_kwh:.2f} × 1000) / {voltaje_sistema}",
                    "resultado": f"{capacidad_ah:.0f} Ah"
                },
                "paso3": {
                    "nombre": "Configuración serie/paralelo",
                    "ecuacion": "Serie = V_sistema / V_bat, Paralelo = C_Ah / C_bat",
                    "valores": f"Serie = {voltaje_sistema} / {voltaje_bateria}, Paralelo = {capacidad_ah:.0f} / {capacidad_bateria_ah}",
                    "resultado": f"{num_serie}S × {num_paralelo}P"
                }
            },
            "resultado": {
                "baterias": {
                    "tipo": "LiFePO4 (recomendado)",
                    "voltaje_unitario": voltaje_bateria,
                    "capacidad_unitaria_ah": capacidad_bateria_ah,
                    "configuracion_serie": num_serie,
                    "configuracion_paralelo": num_paralelo,
                    "total_baterias": total_baterias,
                    "capacidad_total_kwh": capacidad_real_kwh,
                    "voltaje_total": voltaje_sistema
                },
                "autonomia": {
                    "dias": dias_autonomia,
                    "profundidad_descarga": self.PROFUNDIDAD_DESCARGA_BATERIA * 100
                },
                "costo": {
                    "baterias_usd": total_baterias * 450,  # $450/batería LiFePO4
                    "bms_usd": 300,
                    "cables_usd": 150,
                    "total_estimado_usd": total_baterias * 450 + 450
                }
            }
        }


# Singleton instance
dimensionamiento_service = DimensionamientoService()
