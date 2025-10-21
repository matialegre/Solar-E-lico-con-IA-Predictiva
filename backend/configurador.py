"""
Configurador Interactivo del Sistema Híbrido
Permite al usuario configurar su sistema antes de iniciarlo
"""
import json
import requests
import sys
from typing import Dict, Optional
from datetime import datetime, timedelta

class SistemaConfigurador:
    def __init__(self):
        self.config_file = "configuracion_usuario.json"
        self.api_key = "9f500bee573bc32ca5bc872d42353626"  # OpenWeather API
        
    def inicio(self):
        """Pantalla de bienvenida"""
        print("=" * 70)
        print("  CONFIGURADOR DEL SISTEMA INVERSOR HÍBRIDO")
        print("=" * 70)
        print()
        print("Este asistente tiene 2 modos de configuración:")
        print()
        print("  1️⃣  Tengo consumo → Recomiéndame componentes")
        print("     (Te digo cuánto consumo, me dices qué necesito)")
        print()
        print("  2️⃣  Tengo componentes → Dime qué puedo alimentar")
        print("     (Te digo qué tengo, me dices qué potencia puedo usar)")
        print()
        
        while True:
            modo = input("Selecciona modo (1/2): ").strip()
            if modo in ['1', '2']:
                return modo
            print("❌ Selecciona 1 o 2")
        
    def obtener_ubicacion(self) -> Dict:
        """Obtener ubicación del usuario"""
        print("\n" + "="*70)
        print("  PASO 1: UBICACIÓN")
        print("="*70)
        print()
        print("Ingresa tu ubicación para calcular generación solar y eólica.")
        print()
        
        # Ciudad
        ciudad = input("Ciudad: ").strip()
        
        # Latitud
        while True:
            lat_str = input("Latitud (ej: -38.7183): ").strip()
            try:
                latitud = float(lat_str)
                if -90 <= latitud <= 90:
                    break
                print("❌ Latitud debe estar entre -90 y 90")
            except:
                print("❌ Ingresa un número válido")
        
        # Longitud
        while True:
            lon_str = input("Longitud (ej: -62.2663): ").strip()
            try:
                longitud = float(lon_str)
                if -180 <= longitud <= 180:
                    break
                print("❌ Longitud debe estar entre -180 y 180")
            except:
                print("❌ Ingresa un número válido")
        
        print()
        print(f"✅ Ubicación: {ciudad} ({latitud}, {longitud})")
        
        # Obtener datos climáticos históricos
        print()
        print("📡 Obteniendo datos climáticos de la zona...")
        clima_historico = self.obtener_clima_historico(latitud, longitud)
        
        return {
            "latitud": latitud,
            "longitud": longitud,
            "ciudad": ciudad,
            "zona_horaria": "America/Argentina/Buenos_Aires",  # Ajustar según país
            "clima_historico": clima_historico
        }
    
    def obtener_clima_historico(self, lat: float, lon: float) -> Dict:
        """Obtiene datos climáticos históricos de la zona"""
        try:
            # OpenWeather API - datos actuales y forecast
            url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={self.api_key}&units=metric"
            response = requests.get(url, timeout=5)
            data = response.json()
            
            # Obtener forecast para calcular promedios
            url_forecast = f"http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={self.api_key}&units=metric"
            response_forecast = requests.get(url_forecast, timeout=5)
            forecast = response_forecast.json()
            
            # Calcular promedios
            velocidades_viento = []
            for item in forecast.get('list', [])[:40]:  # 5 días
                velocidades_viento.append(item['wind']['speed'])
            
            viento_promedio = sum(velocidades_viento) / len(velocidades_viento) if velocidades_viento else 5.0
            viento_maximo = max(velocidades_viento) if velocidades_viento else 10.0
            
            print(f"   🌤️  Temperatura promedio: {data.get('main', {}).get('temp', 15)}°C")
            print(f"   💨 Viento promedio: {viento_promedio:.1f} m/s")
            print(f"   💨 Viento máximo: {viento_maximo:.1f} m/s")
            
            return {
                "temperatura_promedio_c": data.get('main', {}).get('temp', 15),
                "viento_promedio_ms": round(viento_promedio, 2),
                "viento_maximo_ms": round(viento_maximo, 2),
                "humedad_promedio": data.get('main', {}).get('humidity', 70),
                "ciudad_api": data.get('name', 'Desconocida')
            }
        except Exception as e:
            print(f"   ⚠️  No se pudieron obtener datos climáticos: {e}")
            print("   ℹ️  Usando valores estimados por defecto")
            return {
                "temperatura_promedio_c": 18,
                "viento_promedio_ms": 6.0,
                "viento_maximo_ms": 15.0,
                "humedad_promedio": 65,
                "ciudad_api": "N/A"
            }
    
    def obtener_consumo(self) -> Dict:
        """Obtener consumo del usuario"""
        print("\n" + "="*70)
        print("  PASO 2: CONSUMO DE TU CASA")
        print("="*70)
        print()
        print("¿Conoces tu consumo promedio?")
        print()
        print("Opciones:")
        print("  1. Tengo el consumo en kWh/día (de la factura de luz)")
        print("  2. Tengo el consumo en kWh/mes")
        print("  3. No lo sé, quiero estimarlo")
        print()
        
        opcion = input("Selecciona opción (1/2/3): ").strip()
        
        if opcion == "1":
            while True:
                try:
                    kwh_dia = float(input("Consumo diario (kWh/día): ").strip())
                    if kwh_dia > 0:
                        break
                    print("❌ Debe ser mayor a 0")
                except:
                    print("❌ Ingresa un número válido")
            
            promedio_watts = int((kwh_dia * 1000) / 24)
            
        elif opcion == "2":
            while True:
                try:
                    kwh_mes = float(input("Consumo mensual (kWh/mes): ").strip())
                    if kwh_mes > 0:
                        break
                    print("❌ Debe ser mayor a 0")
                except:
                    print("❌ Ingresa un número válido")
            
            kwh_dia = kwh_mes / 30
            promedio_watts = int((kwh_dia * 1000) / 24)
            
        else:  # Estimar
            kwh_dia, promedio_watts = self.estimar_consumo()
        
        print()
        print(f"✅ Consumo estimado:")
        print(f"   📊 {kwh_dia:.1f} kWh/día")
        print(f"   ⚡ {promedio_watts} W promedio")
        
        # Pico máximo
        print()
        pico_str = input("Pico máximo de consumo en Watts (ej: 2000, Enter para auto): ").strip()
        pico_maximo = int(pico_str) if pico_str else int(promedio_watts * 2.5)
        
        return {
            "promedio_diario_kwh": round(kwh_dia, 1),
            "promedio_watts": promedio_watts,
            "pico_maximo_watts": pico_maximo
        }
    
    def estimar_consumo(self) -> tuple:
        """Estimador de consumo basado en electrodomésticos"""
        print()
        print("Estimaremos tu consumo basándonos en tus electrodomésticos.")
        print()
        
        consumo_total_wh = 0
        
        # Heladera
        print("🔸 Heladera:")
        tiene = input("  ¿Tienes heladera? (s/n): ").strip().lower()
        if tiene == 's':
            consumo_total_wh += 150 * 24 * 0.5  # 150W, 24h, ciclo 50%
        
        # TV
        print("🔸 Televisión:")
        horas_tv = input("  ¿Cuántas horas al día usas TV? (0-24): ").strip()
        if horas_tv:
            consumo_total_wh += 80 * float(horas_tv)
        
        # Computadora
        print("🔸 Computadora:")
        horas_pc = input("  ¿Cuántas horas al día usas computadora? (0-24): ").strip()
        if horas_pc:
            consumo_total_wh += 150 * float(horas_pc)
        
        # Iluminación
        print("🔸 Iluminación:")
        lamparas = input("  ¿Cuántas lámparas LED tienes? (aprox): ").strip()
        if lamparas:
            consumo_total_wh += int(lamparas) * 10 * 5  # 10W por lámpara, 5h promedio
        
        # Microondas
        print("🔸 Microondas:")
        usa_micro = input("  ¿Usas microondas diariamente? (s/n): ").strip().lower()
        if usa_micro == 's':
            consumo_total_wh += 1000 * 0.25  # 15 minutos al día
        
        # Lavarropas
        print("🔸 Lavarropas:")
        lavados_semana = input("  ¿Cuántos lavados por semana? (0-7): ").strip()
        if lavados_semana:
            consumo_total_wh += (500 * float(lavados_semana)) / 7
        
        # Otros
        print("🔸 Otros electrodomésticos:")
        otros = input("  Consumo adicional estimado (Wh/día, Enter para 0): ").strip()
        if otros:
            consumo_total_wh += float(otros)
        
        kwh_dia = consumo_total_wh / 1000
        promedio_watts = int(consumo_total_wh / 24)
        
        return kwh_dia, promedio_watts
    
    def recomendar_sistema(self, ubicacion: Dict, consumo: Dict) -> Dict:
        """Recomienda componentes basándose en consumo y ubicación"""
        print("\n" + "="*70)
        print("  PASO 3: RECOMENDACIÓN DEL SISTEMA")
        print("="*70)
        print()
        print("📊 Analizando tus necesidades...")
        print()
        
        # Datos climáticos
        clima = ubicacion.get('clima_historico', {})
        viento_prom = clima.get('viento_promedio_ms', 6.0)
        latitud = abs(ubicacion.get('latitud', 38))
        
        # Consumo
        consumo_kwh_dia = consumo['promedio_diario_kwh']
        consumo_watts = consumo['promedio_watts']
        
        # Horas de sol promedio (estimado por latitud)
        horas_sol_pico = 4.5 + (30 - latitud) * 0.05  # Más sol cerca del ecuador
        horas_sol_pico = max(3.5, min(horas_sol_pico, 6.5))
        
        # PANELES SOLARES
        # Potencia necesaria considerando eficiencia y pérdidas
        potencia_solar_necesaria = (consumo_kwh_dia * 0.6) / horas_sol_pico * 1000  # 60% del consumo
        potencia_solar_necesaria *= 1.25  # Factor de pérdidas (sombra, temperatura, etc.)
        
        panel_tipo = 300  # Paneles de 300W
        cantidad_paneles = max(3, int(potencia_solar_necesaria / panel_tipo) + 1)
        potencia_solar_total = cantidad_paneles * panel_tipo
        
        # TURBINA EÓLICA
        # Capacidad factor típico: 25-30%
        if viento_prom >= 6.0:
            # Buenas condiciones eólicas
            potencia_eolica_nominal = (consumo_kwh_dia * 0.4) / 24 * 1000 / 0.3  # 40% del consumo
            if potencia_eolica_nominal < 800:
                turbina = {"cantidad": 1, "potencia_w": 1000, "recomendacion": "1x 1000W"}
            elif potencia_eolica_nominal < 2000:
                turbina = {"cantidad": 1, "potencia_w": 2000, "recomendacion": "1x 2000W"}
            else:
                turbina = {"cantidad": 2, "potencia_w": 2000, "recomendacion": "2x 2000W"}
        else:
            # Viento bajo, turbina más pequeña
            turbina = {"cantidad": 1, "potencia_w": 600, "recomendacion": "1x 600W (viento bajo)"}
        
        # BATERÍA
        # Autonomía deseada: 8-12 horas
        autonomia_horas = 10
        capacidad_bateria_kwh = (consumo_watts * autonomia_horas) / 1000
        capacidad_bateria_kwh *= 1.25  # No descargar completamente (zona óptima 25-80%)
        
        # Voltaje del sistema
        if consumo['pico_maximo_watts'] > 2000:
            voltaje_sistema = 48
            capacidad_ah = int((capacidad_bateria_kwh * 1000) / voltaje_sistema)
        else:
            voltaje_sistema = 24
            capacidad_ah = int((capacidad_bateria_kwh * 1000) / voltaje_sistema)
        
        # INVERSOR
        potencia_inversor = max(2000, int(consumo['pico_maximo_watts'] * 1.3))  # 30% margen
        
        # Mostrar recomendaciones
        print("✅ SISTEMA RECOMENDADO:")
        print()
        print(f"☀️  PANELES SOLARES:")
        print(f"   - Cantidad: {cantidad_paneles} paneles de {panel_tipo}W")
        print(f"   - Potencia total: {potencia_solar_total}W ({potencia_solar_total/1000:.1f} kW)")
        print(f"   - Generación estimada: {potencia_solar_total * horas_sol_pico / 1000:.1f} kWh/día")
        print()
        print(f"💨 TURBINA EÓLICA:")
        print(f"   - {turbina['recomendacion']}")
        print(f"   - Viento promedio en tu zona: {viento_prom:.1f} m/s")
        print(f"   - Generación estimada: {turbina['cantidad'] * turbina['potencia_w'] * 0.3 * 24 / 1000:.1f} kWh/día")
        print()
        print(f"🔋 BATERÍA:")
        print(f"   - Capacidad: {voltaje_sistema}V {capacidad_ah}Ah ({capacidad_bateria_kwh:.1f} kWh)")
        print(f"   - Autonomía: ~{autonomia_horas} horas")
        print(f"   - Tipo recomendado: LiFePO4")
        print()
        print(f"⚡ INVERSOR:")
        print(f"   - Potencia: {potencia_inversor}W continua")
        print(f"   - Pico: {potencia_inversor * 2}W")
        print()
        
        # GENERACIÓN TOTAL vs CONSUMO
        gen_solar = potencia_solar_total * horas_sol_pico / 1000
        gen_eolica = turbina['cantidad'] * turbina['potencia_w'] * 0.3 * 24 / 1000
        gen_total = gen_solar + gen_eolica
        cobertura = (gen_total / consumo_kwh_dia) * 100
        
        print(f"📊 BALANCE ENERGÉTICO:")
        print(f"   - Consumo diario: {consumo_kwh_dia:.1f} kWh")
        print(f"   - Generación estimada: {gen_total:.1f} kWh/día")
        print(f"   - Cobertura: {cobertura:.0f}%")
        print()
        
        if cobertura >= 90:
            print("   ✅ Sistema bien dimensionado para autonomía total")
        elif cobertura >= 70:
            print("   ⚠️  Sistema cubre la mayoría del consumo (necesitarás red backup)")
        else:
            print("   ❌ Sistema subdimensionado, considera agregar más capacidad")
        
        return {
            "paneles": {
                "cantidad": cantidad_paneles,
                "potencia_unitaria": panel_tipo,
                "potencia_total": potencia_solar_total,
                "generacion_dia_kwh": round(gen_solar, 1)
            },
            "turbina": {
                "cantidad": turbina['cantidad'],
                "potencia_unitaria": turbina['potencia_w'],
                "generacion_dia_kwh": round(gen_eolica, 1)
            },
            "bateria": {
                "voltaje": voltaje_sistema,
                "capacidad_ah": capacidad_ah,
                "capacidad_kwh": round(capacidad_bateria_kwh, 1),
                "autonomia_horas": autonomia_horas
            },
            "inversor": {
                "potencia_continua": potencia_inversor,
                "potencia_pico": potencia_inversor * 2
            },
            "cobertura_porcentaje": round(cobertura, 1),
            "generacion_total_dia_kwh": round(gen_total, 1)
        }
    
    def guardar_configuracion(self, ubicacion: Dict, consumo: Dict, sistema: Dict):
        """Guarda la configuración completa"""
        config = {
            "ubicacion": ubicacion,
            "consumo": consumo,
            "sistema_recomendado": sistema,
            "paneles_solares": {
                "cantidad": sistema['paneles']['cantidad'],
                "potencia_por_panel_w": sistema['paneles']['potencia_unitaria'],
                "potencia_total_w": sistema['paneles']['potencia_total'],
                "marca": "Canadian Solar",
                "modelo": "CS3W-300P",
                "tipo": "Policristalino"
            },
            "turbina_eolica": {
                "cantidad": sistema['turbina']['cantidad'],
                "potencia_nominal_w": sistema['turbina']['potencia_unitaria'],
                "marca": "Windmax",
                "tipo": "Eje horizontal, 3 palas",
                "velocidad_arranque_ms": 2.5,
                "velocidad_maxima_ms": 25.0
            },
            "bateria": {
                "tipo": "LiFePO4",
                "voltaje_nominal": sistema['bateria']['voltaje'],
                "capacidad_ah": sistema['bateria']['capacidad_ah'],
                "capacidad_kwh": sistema['bateria']['capacidad_kwh'],
                "soc_optimo_min": 25,
                "soc_optimo_max": 80
            },
            "inversor": {
                "potencia_continua_w": sistema['inversor']['potencia_continua'],
                "potencia_pico_w": sistema['inversor']['potencia_pico'],
                "tipo": "Onda pura"
            },
            "fecha_configuracion": datetime.now().isoformat()
        }
        
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        print()
        print(f"✅ Configuración guardada en: {self.config_file}")
    
    def obtener_componentes(self) -> Dict:
        """Obtener componentes que ya tiene el usuario"""
        print("\n" + "="*70)
        print("  PASO 2: ¿QUÉ COMPONENTES TIENES?")
        print("="*70)
        print()
        
        componentes = {}
        
        # PANELES SOLARES
        print("☀️  PANELES SOLARES:")
        tiene_paneles = input("  ¿Tienes paneles solares? (s/n): ").strip().lower()
        if tiene_paneles == 's':
            while True:
                try:
                    cantidad = int(input("  ¿Cuántos paneles?: ").strip())
                    potencia = int(input("  ¿Potencia de cada panel (W)? (ej: 300): ").strip())
                    if cantidad > 0 and potencia > 0:
                        break
                    print("  ❌ Valores deben ser mayores a 0")
                except:
                    print("  ❌ Ingresa números válidos")
            
            componentes['paneles'] = {
                'cantidad': cantidad,
                'potencia_w': potencia,
                'potencia_total_w': cantidad * potencia
            }
        else:
            componentes['paneles'] = None
        
        # TURBINA EÓLICA
        print("\n💨 TURBINA EÓLICA:")
        tiene_turbina = input("  ¿Tienes turbina eólica? (s/n): ").strip().lower()
        if tiene_turbina == 's':
            while True:
                try:
                    potencia = int(input("  ¿Potencia nominal (W)? (ej: 1000): ").strip())
                    if potencia > 0:
                        break
                    print("  ❌ Valor debe ser mayor a 0")
                except:
                    print("  ❌ Ingresa número válido")
            
            componentes['turbina'] = {
                'potencia_w': potencia
            }
        else:
            componentes['turbina'] = None
        
        # BATERÍA
        print("\n🔋 BATERÍA:")
        tiene_bateria = input("  ¿Tienes batería? (s/n): ").strip().lower()
        if tiene_bateria == 's':
            while True:
                try:
                    voltaje = int(input("  ¿Voltaje (V)? (ej: 12, 24, 48): ").strip())
                    ah = int(input("  ¿Capacidad (Ah)? (ej: 100): ").strip())
                    if voltaje > 0 and ah > 0:
                        break
                    print("  ❌ Valores deben ser mayores a 0")
                except:
                    print("  ❌ Ingresa números válidos")
            
            kwh = (voltaje * ah) / 1000
            componentes['bateria'] = {
                'voltaje': voltaje,
                'ah': ah,
                'kwh': round(kwh, 2)
            }
        else:
            componentes['bateria'] = None
        
        print()
        print("✅ Componentes registrados:")
        if componentes['paneles']:
            print(f"   ☀️  {componentes['paneles']['cantidad']}x {componentes['paneles']['potencia_w']}W = {componentes['paneles']['potencia_total_w']}W")
        if componentes['turbina']:
            print(f"   💨 Turbina {componentes['turbina']['potencia_w']}W")
        if componentes['bateria']:
            print(f"   🔋 Batería {componentes['bateria']['voltaje']}V {componentes['bateria']['ah']}Ah ({componentes['bateria']['kwh']} kWh)")
        
        return componentes
    
    def calcular_potencia_disponible(self, ubicacion: Dict, componentes: Dict) -> Dict:
        """Calcula qué potencia puede alimentar con los componentes que tiene"""
        print("\n" + "="*70)
        print("  PASO 3: CALCULANDO POTENCIA DISPONIBLE")
        print("="*70)
        print()
        print("📊 Analizando tu sistema...")
        print()
        
        # Datos climáticos
        clima = ubicacion.get('clima_historico', {})
        viento_prom = clima.get('viento_promedio_ms', 6.0)
        latitud = abs(ubicacion.get('latitud', 38))
        
        # Horas de sol promedio
        horas_sol_pico = 4.5 + (30 - latitud) * 0.05
        horas_sol_pico = max(3.5, min(horas_sol_pico, 6.5))
        
        # GENERACIÓN SOLAR
        gen_solar_dia_kwh = 0
        gen_solar_w_promedio = 0
        if componentes['paneles']:
            potencia_solar = componentes['paneles']['potencia_total_w']
            # Factor de rendimiento real: 80% (pérdidas por temperatura, polvo, etc.)
            gen_solar_dia_kwh = (potencia_solar * horas_sol_pico * 0.8) / 1000
            gen_solar_w_promedio = gen_solar_dia_kwh * 1000 / 24
        
        # GENERACIÓN EÓLICA
        gen_eolica_dia_kwh = 0
        gen_eolica_w_promedio = 0
        if componentes['turbina']:
            potencia_turbina = componentes['turbina']['potencia_w']
            # Factor de capacidad típico según viento
            if viento_prom >= 8:
                factor = 0.35  # Buen viento
            elif viento_prom >= 6:
                factor = 0.25  # Viento moderado
            else:
                factor = 0.15  # Viento bajo
            
            gen_eolica_dia_kwh = (potencia_turbina * 24 * factor) / 1000
            gen_eolica_w_promedio = gen_eolica_dia_kwh * 1000 / 24
        
        # GENERACIÓN TOTAL
        gen_total_dia_kwh = gen_solar_dia_kwh + gen_eolica_dia_kwh
        gen_total_w_promedio = gen_solar_w_promedio + gen_eolica_w_promedio
        
        # AUTONOMÍA DE BATERÍA
        autonomia_horas = 0
        if componentes['bateria']:
            # Usar solo 80% de capacidad (zona óptima 20-100%, usar 80%)
            capacidad_util = componentes['bateria']['kwh'] * 0.8
            if gen_total_w_promedio > 0:
                autonomia_horas = (capacidad_util * 1000) / gen_total_w_promedio
        
        # POTENCIA QUE PUEDE ALIMENTAR
        # Considerando que quiere usar renovables + batería sin descargarla completamente
        potencia_continua_recomendada = int(gen_total_w_promedio * 0.7)  # 70% para ser conservadores
        potencia_maxima_pico = int(gen_total_w_promedio * 1.5)  # Picos cortos
        
        # Mostrar resultados
        print("✅ ANÁLISIS DE TU SISTEMA:")
        print()
        print(f"📊 GENERACIÓN ESTIMADA:")
        if componentes['paneles']:
            print(f"   ☀️  Solar: {gen_solar_dia_kwh:.1f} kWh/día ({int(gen_solar_w_promedio)} W promedio)")
        if componentes['turbina']:
            print(f"   💨 Eólica: {gen_eolica_dia_kwh:.1f} kWh/día ({int(gen_eolica_w_promedio)} W promedio)")
        print(f"   ⚡ TOTAL: {gen_total_dia_kwh:.1f} kWh/día ({int(gen_total_w_promedio)} W promedio)")
        print()
        
        if componentes['bateria']:
            print(f"🔋 BATERÍA:")
            print(f"   • Capacidad: {componentes['bateria']['kwh']} kWh")
            print(f"   • Capacidad útil (80%): {componentes['bateria']['kwh'] * 0.8:.1f} kWh")
            print(f"   • Autonomía estimada: {autonomia_horas:.1f} horas")
            print()
        
        print(f"⚡ POTENCIA QUE PUEDES ALIMENTAR:")
        print(f"   • Continua (24h): {potencia_continua_recomendada} W")
        print(f"   • Picos cortos: {potencia_maxima_pico} W")
        print()
        
        print("📱 EJEMPLOS DE LO QUE PUEDES ALIMENTAR CON {0} W:".format(potencia_continua_recomendada))
        
        # Ejemplos prácticos
        if potencia_continua_recomendada >= 1500:
            print("   ✅ Casa completa pequeña (heladera + TV + PC + luces)")
        elif potencia_continua_recomendada >= 800:
            print("   ✅ Heladera + TV + iluminación LED + cargadores")
        elif potencia_continua_recomendada >= 400:
            print("   ✅ Heladera + iluminación LED + cargadores")
        elif potencia_continua_recomendada >= 200:
            print("   ✅ Iluminación LED + cargadores + laptop")
        else:
            print("   ⚠️  Solo iluminación básica y cargadores")
        
        print()
        
        # Advertencias
        if not componentes['bateria']:
            print("   ⚠️  SIN BATERÍA: Solo tendrás energía cuando haya sol/viento")
        
        if potencia_continua_recomendada < 500:
            print("   💡 Sistema pequeño - Considera agregar más paneles o turbina")
        
        return {
            'generacion_solar_dia_kwh': round(gen_solar_dia_kwh, 2),
            'generacion_eolica_dia_kwh': round(gen_eolica_dia_kwh, 2),
            'generacion_total_dia_kwh': round(gen_total_dia_kwh, 2),
            'potencia_promedio_w': int(gen_total_w_promedio),
            'potencia_continua_recomendada_w': potencia_continua_recomendada,
            'potencia_pico_max_w': potencia_maxima_pico,
            'autonomia_horas': round(autonomia_horas, 1) if componentes['bateria'] else 0
        }
    
    def ejecutar(self):
        """Ejecuta el configurador completo"""
        try:
            modo = self.inicio()
            
            # Paso 1: Ubicación (común para ambos modos)
            ubicacion = self.obtener_ubicacion()
            
            if modo == '1':
                # MODO 1: Tengo consumo, recomiéndame componentes
                consumo = self.obtener_consumo()
                sistema = self.recomendar_sistema(ubicacion, consumo)
                
                # Confirmar
                print()
                print("="*70)
                confirmar = input("¿Guardar esta configuración? (s/n): ").strip().lower()
                
                if confirmar == 's':
                    self.guardar_configuracion(ubicacion, consumo, sistema)
                    print()
                    print("="*70)
                    print("  ¡CONFIGURACIÓN COMPLETADA!")
                    print("="*70)
                    print()
                    print("Próximos pasos:")
                    print("  1. Revisa el archivo configuracion_usuario.json")
                    print("  2. Ejecuta INICIAR_TODO.bat")
                    print("  3. El sistema usará tu configuración personalizada")
                    print()
                    return 0
                else:
                    print()
                    print("Configuración cancelada.")
                    return 1
            
            else:  # modo == '2'
                # MODO 2: Tengo componentes, dime qué puedo alimentar
                componentes = self.obtener_componentes()
                capacidad = self.calcular_potencia_disponible(ubicacion, componentes)
                
                # Confirmar
                print()
                print("="*70)
                confirmar = input("¿Guardar esta configuración? (s/n): ").strip().lower()
                
                if confirmar == 's':
                    # Guardar en formato compatible
                    config = {
                        "ubicacion": ubicacion,
                        "modo": "componentes_existentes",
                        "componentes": componentes,
                        "capacidad_sistema": capacidad,
                        "paneles_solares": componentes['paneles'] if componentes['paneles'] else {"cantidad": 0, "potencia_w": 0},
                        "turbina_eolica": componentes['turbina'] if componentes['turbina'] else {"potencia_w": 0},
                        "bateria": componentes['bateria'] if componentes['bateria'] else {"voltaje": 0, "ah": 0, "kwh": 0},
                        "fecha_configuracion": datetime.now().isoformat()
                    }
                    
                    with open(self.config_file, 'w', encoding='utf-8') as f:
                        json.dump(config, f, indent=2, ensure_ascii=False)
                    
                    print()
                    print("="*70)
                    print("  ¡CONFIGURACIÓN COMPLETADA!")
                    print("="*70)
                    print()
                    print("Tu sistema puede alimentar:")
                    print(f"  ⚡ {capacidad['potencia_continua_recomendada_w']} W continuos")
                    print(f"  📊 {capacidad['generacion_total_dia_kwh']} kWh/día")
                    print()
                    print("Próximos pasos:")
                    print("  1. Revisa el archivo configuracion_usuario.json")
                    print("  2. Ejecuta INICIAR_TODO.bat")
                    print("  3. El dashboard mostrará tu capacidad real")
                    print()
                    return 0
                else:
                    print()
                    print("Configuración cancelada.")
                    return 1
                
        except KeyboardInterrupt:
            print("\n\n❌ Configuración cancelada por el usuario.")
            return 1
        except Exception as e:
            print(f"\n\n❌ Error: {e}")
            return 1


if __name__ == "__main__":
    configurador = SistemaConfigurador()
    sys.exit(configurador.ejecutar())
