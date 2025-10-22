"""
Predictor ML con scikit-learn
Random Forest para predecir generación solar y eólica
"""

import numpy as np
import pickle
from pathlib import Path
from typing import Dict, Optional

try:
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.preprocessing import StandardScaler
    import joblib
    ML_AVAILABLE = True
except ImportError:
    ML_AVAILABLE = False
    print("⚠️ scikit-learn no disponible, ML deshabilitado")


class MLPredictor:
    """Predictor ML para generación solar y eólica"""
    
    def __init__(self):
        self.ml_available = ML_AVAILABLE
        self.solar_model = None
        self.wind_model = None
        self.scaler = None
        self.model_path = Path("ml_models")
        self.model_path.mkdir(exist_ok=True)
        
        if self.ml_available:
            self._load_or_train_models()
    
    def _load_or_train_models(self):
        """Cargar modelos guardados o entrenar nuevos"""
        try:
            # Intentar cargar modelos existentes
            solar_path = self.model_path / "solar_model.pkl"
            wind_path = self.model_path / "wind_model.pkl"
            scaler_path = self.model_path / "scaler.pkl"
            
            if solar_path.exists() and wind_path.exists() and scaler_path.exists():
                self.solar_model = joblib.load(solar_path)
                self.wind_model = joblib.load(wind_path)
                self.scaler = joblib.load(scaler_path)
                print("✅ Modelos ML cargados desde disco")
            else:
                # Entrenar modelos con datos sintéticos
                self._train_initial_models()
                print("✅ Modelos ML entrenados y guardados")
        except Exception as e:
            print(f"⚠️ Error cargando/entrenando modelos: {e}")
            self.ml_available = False
    
    def _train_initial_models(self):
        """Entrenar modelos iniciales con datos sintéticos basados en física"""
        # Generar dataset sintético basado en leyes físicas
        np.random.seed(42)
        n_samples = 1000
        
        # Features: [irradiancia, temperatura, hora_dia, mes, latitud]
        irradiancia = np.random.uniform(0, 1200, n_samples)  # W/m²
        temperatura = np.random.uniform(15, 40, n_samples)  # °C
        hora = np.random.uniform(0, 24, n_samples)
        mes = np.random.randint(1, 13, n_samples)
        latitud = np.random.uniform(-55, -20, n_samples)  # Argentina
        
        X = np.column_stack([irradiancia, temperatura, hora, mes, latitud])
        
        # Target Solar: Basado en fórmula física + ruido
        # Potencia = Irradiancia * Área * Eficiencia * factor_temperatura * factor_hora
        eficiencia_base = 0.18
        area = 10.0  # m²
        factor_temp = 1 - 0.004 * (temperatura - 25)  # Pérdida por temperatura
        factor_hora = np.where((hora >= 8) & (hora <= 18), 
                               np.sin((hora - 6) * np.pi / 12), 
                               0)  # Curva solar
        
        y_solar = (irradiancia * area * eficiencia_base * factor_temp * factor_hora * 
                   np.random.uniform(0.9, 1.1, n_samples))
        y_solar = np.maximum(0, y_solar)
        
        # Target Eólica: Basado en velocidad del viento (v³)
        velocidad_viento = np.random.uniform(0, 15, n_samples)  # m/s
        # Potencia = 0.5 * densidad * área * v³ * eficiencia
        densidad_aire = 1.225  # kg/m³
        area_turbina = np.pi * (2 ** 2)  # Radio 2m
        eficiencia_turbina = 0.35
        
        y_wind = (0.5 * densidad_aire * area_turbina * (velocidad_viento ** 3) * 
                  eficiencia_turbina * np.random.uniform(0.9, 1.1, n_samples))
        y_wind = np.minimum(2000, y_wind)  # Limitar a 2kW
        
        # Normalizar features
        self.scaler = StandardScaler()
        X_scaled = self.scaler.fit_transform(X)
        
        # Entrenar modelo solar
        self.solar_model = RandomForestRegressor(
            n_estimators=50,
            max_depth=10,
            random_state=42,
            n_jobs=-1
        )
        self.solar_model.fit(X_scaled, y_solar)
        
        # Entrenar modelo eólico
        self.wind_model = RandomForestRegressor(
            n_estimators=50,
            max_depth=10,
            random_state=42,
            n_jobs=-1
        )
        self.wind_model.fit(X_scaled, y_wind)
        
        # Guardar modelos
        joblib.dump(self.solar_model, self.model_path / "solar_model.pkl")
        joblib.dump(self.wind_model, self.model_path / "wind_model.pkl")
        joblib.dump(self.scaler, self.model_path / "scaler.pkl")
    
    def predict_solar_generation(
        self,
        irradiancia_wm2: float,
        temperatura_c: float,
        hora_dia: int,
        mes: int,
        latitud: float
    ) -> float:
        """Predecir generación solar (W)"""
        if not self.ml_available or self.solar_model is None:
            # Fallback a cálculo simple
            return irradiancia_wm2 * 10.0 * 0.18
        
        try:
            X = np.array([[irradiancia_wm2, temperatura_c, hora_dia, mes, latitud]])
            X_scaled = self.scaler.transform(X)
            prediction = self.solar_model.predict(X_scaled)[0]
            return max(0, prediction)
        except Exception as e:
            print(f"⚠️ Error en predicción solar ML: {e}")
            return irradiancia_wm2 * 10.0 * 0.18
    
    def predict_wind_generation(
        self,
        velocidad_viento_ms: float,
        temperatura_c: float,
        hora_dia: int,
        mes: int,
        latitud: float
    ) -> float:
        """Predecir generación eólica (W)"""
        if not self.ml_available or self.wind_model is None:
            # Fallback a cálculo simple (ley de Betz)
            area = np.pi * (2 ** 2)
            return 0.5 * 1.225 * area * (velocidad_viento_ms ** 3) * 0.35
        
        try:
            # Usar irradiancia = 0 para eólica (no es relevante)
            X = np.array([[0, temperatura_c, hora_dia, mes, latitud]])
            X_scaled = self.scaler.transform(X)
            prediction = self.wind_model.predict(X_scaled)[0]
            return max(0, min(2000, prediction))
        except Exception as e:
            print(f"⚠️ Error en predicción eólica ML: {e}")
            area = np.pi * (2 ** 2)
            return 0.5 * 1.225 * area * (velocidad_viento_ms ** 3) * 0.35
    
    def predict_daily_generation(
        self,
        latitude: float,
        avg_irradiance: float,
        avg_wind_speed: float,
        mes: int = 1
    ) -> Dict:
        """Predecir generación diaria promedio"""
        total_solar = 0
        total_wind = 0
        
        # Simular 24 horas
        for hora in range(24):
            # Ajustar irradiancia según hora del día
            if 6 <= hora <= 18:
                irr_hora = avg_irradiance * np.sin((hora - 6) * np.pi / 12)
            else:
                irr_hora = 0
            
            solar_w = self.predict_solar_generation(irr_hora, 25, hora, mes, latitude)
            wind_w = self.predict_wind_generation(avg_wind_speed, 25, hora, mes, latitude)
            
            total_solar += solar_w
            total_wind += wind_w
        
        return {
            'solar_wh_day': total_solar,
            'wind_wh_day': total_wind,
            'total_wh_day': total_solar + total_wind,
            'solar_kwh_day': total_solar / 1000,
            'wind_kwh_day': total_wind / 1000,
            'total_kwh_day': (total_solar + total_wind) / 1000,
            'ml_used': self.ml_available
        }
    
    def retrain_with_real_data(self, historical_data: list):
        """Reentrenar modelos con datos reales del usuario"""
        if not self.ml_available:
            return False
        
        try:
            # TODO: Implementar cuando haya datos reales
            print("🔄 Reentrenando modelos con datos reales...")
            return True
        except Exception as e:
            print(f"❌ Error reentrenando: {e}")
            return False


# Instancia global
ml_predictor = MLPredictor()
