import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
import joblib
from datetime import datetime, timedelta
from typing import List, Dict, Tuple
import os


class EnergyPredictor:
    """
    Modelo de IA para predicción de generación y consumo energético
    Usa Random Forest con datos meteorológicos e históricos
    """
    
    def __init__(self):
        self.solar_model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.wind_model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.consumption_model = RandomForestRegressor(n_estimators=50, random_state=42)
        
        self.scaler_solar = StandardScaler()
        self.scaler_wind = StandardScaler()
        self.scaler_consumption = StandardScaler()
        
        self.is_trained = False
        self.model_path = "models/"
        
        # Crear directorio de modelos
        os.makedirs(self.model_path, exist_ok=True)
        
        # Intentar cargar modelos existentes
        self._load_models()
    
    def _extract_time_features(self, timestamp: datetime) -> Dict[str, float]:
        """Extraer características temporales"""
        return {
            'hour': timestamp.hour,
            'day': timestamp.day,
            'month': timestamp.month,
            'day_of_week': timestamp.weekday(),
            'is_weekend': 1.0 if timestamp.weekday() >= 5 else 0.0,
            'hour_sin': np.sin(2 * np.pi * timestamp.hour / 24),
            'hour_cos': np.cos(2 * np.pi * timestamp.hour / 24),
            'month_sin': np.sin(2 * np.pi * timestamp.month / 12),
            'month_cos': np.cos(2 * np.pi * timestamp.month / 12),
        }
    
    def prepare_features_solar(self, 
                               timestamp: datetime,
                               temperature: float,
                               cloud_cover: float,
                               humidity: float,
                               solar_radiation: float = None) -> np.ndarray:
        """Preparar características para predicción solar"""
        
        time_features = self._extract_time_features(timestamp)
        
        # Estimar radiación solar si no está disponible
        if solar_radiation is None:
            # Modelo simplificado de radiación solar
            solar_radiation = self._estimate_solar_radiation(
                timestamp, cloud_cover, humidity
            )
        
        features = [
            time_features['hour'],
            time_features['day'],
            time_features['month'],
            time_features['hour_sin'],
            time_features['hour_cos'],
            time_features['month_sin'],
            time_features['month_cos'],
            temperature,
            cloud_cover / 100.0,
            humidity / 100.0,
            solar_radiation,
        ]
        
        return np.array(features).reshape(1, -1)
    
    def prepare_features_wind(self,
                              timestamp: datetime,
                              wind_speed: float,
                              wind_direction: float,
                              temperature: float,
                              pressure: float) -> np.ndarray:
        """Preparar características para predicción eólica"""
        
        time_features = self._extract_time_features(timestamp)
        
        features = [
            time_features['hour'],
            time_features['day'],
            time_features['month'],
            time_features['hour_sin'],
            time_features['hour_cos'],
            wind_speed,
            wind_direction,
            temperature,
            pressure,
        ]
        
        return np.array(features).reshape(1, -1)
    
    def prepare_features_consumption(self,
                                     timestamp: datetime,
                                     temperature: float,
                                     recent_consumption: float = 0) -> np.ndarray:
        """Preparar características para predicción de consumo"""
        
        time_features = self._extract_time_features(timestamp)
        
        features = [
            time_features['hour'],
            time_features['day_of_week'],
            time_features['is_weekend'],
            time_features['hour_sin'],
            time_features['hour_cos'],
            temperature,
            recent_consumption,
        ]
        
        return np.array(features).reshape(1, -1)
    
    def _estimate_solar_radiation(self, timestamp: datetime, 
                                   cloud_cover: float, humidity: float) -> float:
        """Estimar radiación solar basada en hora y nubosidad"""
        
        # Radiación solar máxima teórica al mediodía (W/m²)
        max_radiation = 1000.0
        
        # Factor de hora (máximo al mediodía)
        hour = timestamp.hour
        if hour < 6 or hour > 20:
            return 0.0
        
        # Curva sinusoidal para simular el día
        hour_factor = np.sin(np.pi * (hour - 6) / 14)
        
        # Factor de nubosidad (0-100% nubosidad reduce la radiación)
        cloud_factor = 1.0 - (cloud_cover / 100.0) * 0.75
        
        # Factor de humedad (alta humedad reduce ligeramente)
        humidity_factor = 1.0 - (humidity / 100.0) * 0.1
        
        radiation = max_radiation * hour_factor * cloud_factor * humidity_factor
        
        return max(0.0, radiation)
    
    def train_with_history(self, historical_data: pd.DataFrame):
        """Entrenar modelos con datos históricos"""
        
        if len(historical_data) < 100:
            print("⚠️ Datos insuficientes para entrenar (<100 registros)")
            # Crear modelo básico con datos sintéticos
            self._train_with_synthetic_data()
            return
        
        # Preparar datos para solar
        X_solar = []
        y_solar = []
        
        # Preparar datos para viento
        X_wind = []
        y_wind = []
        
        # Preparar datos para consumo
        X_consumption = []
        y_consumption = []
        
        for _, row in historical_data.iterrows():
            timestamp = row['timestamp']
            
            # Solar
            solar_features = self.prepare_features_solar(
                timestamp,
                row.get('temperature_c', 25),
                row.get('cloud_cover_percent', 0),
                row.get('humidity_percent', 50),
                row.get('solar_radiation_wm2', None)
            )
            X_solar.append(solar_features[0])
            y_solar.append(row['solar_power_w'])
            
            # Wind
            wind_features = self.prepare_features_wind(
                timestamp,
                row.get('wind_speed_ms', 0),
                row.get('wind_direction_deg', 0),
                row.get('temperature_c', 25),
                row.get('pressure_hpa', 1013)
            )
            X_wind.append(wind_features[0])
            y_wind.append(row['wind_power_w'])
            
            # Consumption
            consumption_features = self.prepare_features_consumption(
                timestamp,
                row.get('temperature_c', 25),
                row.get('load_power_w', 0)
            )
            X_consumption.append(consumption_features[0])
            y_consumption.append(row['load_power_w'])
        
        # Convertir a arrays
        X_solar = np.array(X_solar)
        y_solar = np.array(y_solar)
        X_wind = np.array(X_wind)
        y_wind = np.array(y_wind)
        X_consumption = np.array(X_consumption)
        y_consumption = np.array(y_consumption)
        
        # Normalizar y entrenar
        X_solar_scaled = self.scaler_solar.fit_transform(X_solar)
        self.solar_model.fit(X_solar_scaled, y_solar)
        
        X_wind_scaled = self.scaler_wind.fit_transform(X_wind)
        self.wind_model.fit(X_wind_scaled, y_wind)
        
        X_consumption_scaled = self.scaler_consumption.fit_transform(X_consumption)
        self.consumption_model.fit(X_consumption_scaled, y_consumption)
        
        self.is_trained = True
        self._save_models()
        
        print(f"✅ Modelos entrenados con {len(historical_data)} registros")
    
    def _train_with_synthetic_data(self):
        """Entrenar con datos sintéticos cuando no hay históricos suficientes"""
        
        print("🔧 Entrenando con datos sintéticos...")
        
        # Generar datos sintéticos para 30 días
        dates = pd.date_range(
            start=datetime.now() - timedelta(days=30),
            end=datetime.now(),
            freq='H'
        )
        
        synthetic_data = []
        for dt in dates:
            # Simular datos realistas
            hour = dt.hour
            
            # Solar: máximo al mediodía, cero de noche
            solar_base = max(0, 3000 * np.sin(np.pi * (hour - 6) / 14) if 6 <= hour <= 20 else 0)
            solar_power = solar_base + np.random.normal(0, 200)
            
            # Viento: más variable, picos en tarde/noche
            wind_power = 500 + 1000 * (1 + np.sin(2 * np.pi * hour / 24)) + np.random.normal(0, 300)
            
            # Consumo: picos en mañana y tarde
            if 7 <= hour <= 9 or 19 <= hour <= 23:
                load = 800 + np.random.normal(0, 100)
            else:
                load = 400 + np.random.normal(0, 50)
            
            synthetic_data.append({
                'timestamp': dt,
                'solar_power_w': max(0, solar_power),
                'wind_power_w': max(0, wind_power),
                'load_power_w': max(0, load),
                'temperature_c': 20 + 10 * np.sin(2 * np.pi * hour / 24),
                'cloud_cover_percent': np.random.uniform(0, 100),
                'humidity_percent': np.random.uniform(40, 80),
                'wind_speed_ms': np.random.uniform(0, 15),
                'wind_direction_deg': np.random.uniform(0, 360),
                'pressure_hpa': 1013 + np.random.uniform(-10, 10),
            })
        
        df = pd.DataFrame(synthetic_data)
        self.train_with_history(df)
    
    def predict_solar(self, timestamp: datetime, weather_data: Dict) -> float:
        """Predecir generación solar"""
        
        if not self.is_trained:
            self._train_with_synthetic_data()
        
        features = self.prepare_features_solar(
            timestamp,
            weather_data.get('temperature_c', 25),
            weather_data.get('cloud_cover_percent', 0),
            weather_data.get('humidity_percent', 50),
            weather_data.get('solar_radiation_wm2', None)
        )
        
        features_scaled = self.scaler_solar.transform(features)
        prediction = self.solar_model.predict(features_scaled)[0]
        
        return max(0.0, prediction)
    
    def predict_wind(self, timestamp: datetime, weather_data: Dict) -> float:
        """Predecir generación eólica"""
        
        if not self.is_trained:
            self._train_with_synthetic_data()
        
        features = self.prepare_features_wind(
            timestamp,
            weather_data.get('wind_speed_ms', 0),
            weather_data.get('wind_direction_deg', 0),
            weather_data.get('temperature_c', 25),
            weather_data.get('pressure_hpa', 1013)
        )
        
        features_scaled = self.scaler_wind.transform(features)
        prediction = self.wind_model.predict(features_scaled)[0]
        
        return max(0.0, prediction)
    
    def predict_consumption(self, timestamp: datetime, 
                           temperature: float, recent_consumption: float = 0) -> float:
        """Predecir consumo"""
        
        if not self.is_trained:
            self._train_with_synthetic_data()
        
        features = self.prepare_features_consumption(
            timestamp, temperature, recent_consumption
        )
        
        features_scaled = self.scaler_consumption.transform(features)
        prediction = self.consumption_model.predict(features_scaled)[0]
        
        return max(0.0, prediction)
    
    def predict_24h(self, weather_forecast: List[Dict], 
                    current_consumption: float = 0) -> List[Dict]:
        """Predecir 24 horas adelante"""
        
        predictions = []
        
        for i, weather in enumerate(weather_forecast):
            timestamp = weather['timestamp']
            
            solar_pred = self.predict_solar(timestamp, weather)
            wind_pred = self.predict_wind(timestamp, weather)
            consumption_pred = self.predict_consumption(
                timestamp, 
                weather.get('temperature_c', 25),
                current_consumption
            )
            
            predictions.append({
                'timestamp': timestamp,
                'predicted_solar_w': solar_pred,
                'predicted_wind_w': wind_pred,
                'predicted_consumption_w': consumption_pred,
            })
        
        return predictions
    
    def _save_models(self):
        """Guardar modelos entrenados"""
        joblib.dump(self.solar_model, f"{self.model_path}solar_model.pkl")
        joblib.dump(self.wind_model, f"{self.model_path}wind_model.pkl")
        joblib.dump(self.consumption_model, f"{self.model_path}consumption_model.pkl")
        joblib.dump(self.scaler_solar, f"{self.model_path}scaler_solar.pkl")
        joblib.dump(self.scaler_wind, f"{self.model_path}scaler_wind.pkl")
        joblib.dump(self.scaler_consumption, f"{self.model_path}scaler_consumption.pkl")
    
    def _load_models(self):
        """Cargar modelos guardados"""
        try:
            self.solar_model = joblib.load(f"{self.model_path}solar_model.pkl")
            self.wind_model = joblib.load(f"{self.model_path}wind_model.pkl")
            self.consumption_model = joblib.load(f"{self.model_path}consumption_model.pkl")
            self.scaler_solar = joblib.load(f"{self.model_path}scaler_solar.pkl")
            self.scaler_wind = joblib.load(f"{self.model_path}scaler_wind.pkl")
            self.scaler_consumption = joblib.load(f"{self.model_path}scaler_consumption.pkl")
            self.is_trained = True
            print("✅ Modelos cargados desde disco")
        except:
            print("ℹ️ No se encontraron modelos previos, se entrenarán con datos")


# Instancia global del predictor
energy_predictor = EnergyPredictor()
