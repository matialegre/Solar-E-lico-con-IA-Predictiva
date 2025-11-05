# 🤖 Anexo - Machine Learning Detallado

## 1. Preprocesamiento de Datos

### 1.1 Limpieza de Dataset

**Script Python**:
```python
import pandas as pd
import numpy as np
from datetime import datetime

# Cargar datos
df = pd.read_csv('telemetry_week.csv')

# Convertir timestamp
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Limpiar valores anómalos
df = df[(df['voltaje_bat'] > 10) & (df['voltaje_bat'] < 16)]
df = df[(df['rpm'] >= 0) & (df['rpm'] < 1000)]
df = df[(df['corriente_eolica'] >= 0) & (df['corriente_eolica'] < 30)]

# Rellenar valores faltantes
df['corriente_eolica'].fillna(method='ffill', inplace=True)
df['corriente_solar'].fillna(method='ffill', inplace=True)

# Eliminar duplicados
df.drop_duplicates(subset=['timestamp'], keep='first', inplace=True)

# Ordenar por timestamp
df.sort_values('timestamp', inplace=True)

# Guardar limpio
df.to_csv('dataset_clean.csv', index=False)
print(f'Dataset limpio: {len(df)} registros')
```

### 1.2 Feature Engineering

```python
# Crear features derivadas
df['potencia_eolica'] = df['voltaje_eolica'] * df['corriente_eolica']
df['potencia_solar'] = df['voltaje_solar'] * df['corriente_solar']
df['potencia_total'] = df['potencia_eolica'] + df['potencia_solar']

# Features temporales
df['hora'] = df['timestamp'].dt.hour
df['dia_semana'] = df['timestamp'].dt.dayofweek
df['mes'] = df['timestamp'].dt.month
df['es_fin_semana'] = df['dia_semana'].isin([5, 6]).astype(int)

# Features de ventana móvil (últimas 6 horas)
df['rpm_media_6h'] = df['rpm'].rolling(window=72, min_periods=1).mean()
df['potencia_eolica_max_6h'] = df['potencia_eolica'].rolling(window=72).max()

# Interacciones
df['viento_x_temperatura'] = df['wind_speed_api'] * df['temperatura_api']

# Normalizar
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
cols_normalizar = ['rpm', 'voltaje_bat', 'corriente_eolica', 'wind_speed_api']
df[cols_normalizar] = scaler.fit_transform(df[cols_normalizar])

df.to_csv('dataset_ml_ready.csv', index=False)
```

---

## 2. Modelo de Predicción de Generación Eólica

### 2.1 Preparación

```python
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score, mean_squared_error
import matplotlib.pyplot as plt

# Cargar dataset
df = pd.read_csv('dataset_ml_ready.csv')

# Features y label
features = ['wind_speed_api', 'wind_direction_api', 'temperatura_api', 
            'presion_api', 'hora', 'rpm_media_6h']
X = df[features]
y = df['potencia_eolica_real']

# Split train/test
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, shuffle=False  # shuffle=False para series temporales
)

print(f'Train: {len(X_train)} | Test: {len(X_test)}')
```

### 2.2 Entrenamiento

```python
# Modelo Random Forest
model = RandomForestRegressor(
    n_estimators=100,
    max_depth=15,
    min_samples_split=5,
    min_samples_leaf=2,
    random_state=42,
    n_jobs=-1
)

# Entrenar
model.fit(X_train, y_train)

# Predicciones
y_pred_train = model.predict(X_train)
y_pred_test = model.predict(X_test)

# Métricas
mae_train = mean_absolute_error(y_train, y_pred_train)
mae_test = mean_absolute_error(y_test, y_pred_test)
r2_train = r2_score(y_train, y_pred_train)
r2_test = r2_score(y_test, y_pred_test)
rmse_test = np.sqrt(mean_squared_error(y_test, y_pred_test))

print(f'Train MAE: {mae_train:.2f} W | R²: {r2_train:.3f}')
print(f'Test MAE: {mae_test:.2f} W | R²: {r2_test:.3f} | RMSE: {rmse_test:.2f} W')
```

**Resultado esperado**: MAE <20W, R² >0.75

### 2.3 Importancia de Features

```python
import pandas as pd

# Obtener importancia
importances = model.feature_importances_
feature_importance = pd.DataFrame({
    'feature': features,
    'importance': importances
}).sort_values('importance', ascending=False)

print(feature_importance)

# Visualizar
plt.figure(figsize=(10, 6))
plt.barh(feature_importance['feature'], feature_importance['importance'])
plt.xlabel('Importancia')
plt.title('Importancia de Features - Predicción Eólica')
plt.tight_layout()
plt.savefig('feature_importance.png')
```

### 2.4 Validación Cruzada Temporal

```python
from sklearn.model_selection import TimeSeriesSplit

tscv = TimeSeriesSplit(n_splits=5)
scores = []

for train_idx, test_idx in tscv.split(X):
    X_train_cv, X_test_cv = X.iloc[train_idx], X.iloc[test_idx]
    y_train_cv, y_test_cv = y.iloc[train_idx], y.iloc[test_idx]
    
    model.fit(X_train_cv, y_train_cv)
    y_pred_cv = model.predict(X_test_cv)
    
    mae_cv = mean_absolute_error(y_test_cv, y_pred_cv)
    scores.append(mae_cv)
    print(f'Fold MAE: {mae_cv:.2f} W')

print(f'\nMAE promedio: {np.mean(scores):.2f} ± {np.std(scores):.2f} W')
```

### 2.5 Guardar Modelo

```python
import joblib

# Guardar modelo y scaler
joblib.dump(model, 'modelo_prediccion_eolica.pkl')
joblib.dump(scaler, 'scaler.pkl')

# Cargar después
model_loaded = joblib.load('modelo_prediccion_eolica.pkl')
scaler_loaded = joblib.load('scaler.pkl')
```

---

## 3. Detección de Anomalías

### 3.1 Isolation Forest

```python
from sklearn.ensemble import IsolationForest

# Features para detección
X_anomaly = df[['voltaje_bat', 'corriente_eolica', 'rpm', 'temperatura']]

# Entrenar detector
detector = IsolationForest(
    contamination=0.05,  # 5% de datos son anomalías
    random_state=42
)
df['anomalia'] = detector.fit_predict(X_anomaly)

# Filtrar anomalías (-1 = anomalía, 1 = normal)
anomalias = df[df['anomalia'] == -1]
print(f'Anomalías detectadas: {len(anomalias)} ({len(anomalias)/len(df)*100:.1f}%)')

# Analizar causas
print('\nTop 10 anomalías:')
print(anomalias[['timestamp', 'voltaje_bat', 'rpm', 'temperatura']].head(10))

# Guardar para revisión
anomalias.to_csv('anomalias_detectadas.csv', index=False)
```

### 3.2 Visualización de Anomalías

```python
import matplotlib.pyplot as plt

fig, axes = plt.subplots(2, 2, figsize=(15, 10))

# Voltaje batería
axes[0, 0].scatter(df.index, df['voltaje_bat'], c=df['anomalia'], cmap='coolwarm', s=1)
axes[0, 0].set_title('Voltaje Batería')
axes[0, 0].set_ylabel('Voltaje (V)')

# RPM
axes[0, 1].scatter(df.index, df['rpm'], c=df['anomalia'], cmap='coolwarm', s=1)
axes[0, 1].set_title('RPM Turbina')
axes[0, 1].set_ylabel('RPM')

# Corriente eólica
axes[1, 0].scatter(df.index, df['corriente_eolica'], c=df['anomalia'], cmap='coolwarm', s=1)
axes[1, 0].set_title('Corriente Eólica')
axes[1, 0].set_ylabel('Corriente (A)')

# Temperatura
axes[1, 1].scatter(df.index, df['temperatura'], c=df['anomalia'], cmap='coolwarm', s=1)
axes[1, 1].set_title('Temperatura')
axes[1, 1].set_ylabel('Temperatura (°C)')

plt.tight_layout()
plt.savefig('anomalias_visualizacion.png')
```

---

## 4. Optimización de Estrategia de Carga

### 4.1 Reinforcement Learning (Q-Learning)

```python
import numpy as np

# Estados: (SOC, Generación, Consumo)
# SOC: 0=bajo(<30%), 1=medio(30-70%), 2=alto(>70%)
# Gen: 0=baja(<50W), 1=media(50-150W), 2=alta(>150W)
# Consumo: 0=bajo(<100W), 1=medio(100-200W), 2=alto(>200W)

# Acciones: 0=cargar_bateria, 1=alimentar_directo, 2=activar_dump

# Tabla Q
Q = np.zeros((3, 3, 3, 3))  # Estados × Acción

# Hiperparámetros
alpha = 0.1  # Tasa aprendizaje
gamma = 0.9  # Factor descuento
epsilon = 0.1  # Exploración

def get_state(soc, gen, consumo):
    """Discretizar estado continuo"""
    soc_state = 0 if soc < 30 else (1 if soc < 70 else 2)
    gen_state = 0 if gen < 50 else (1 if gen < 150 else 2)
    consumo_state = 0 if consumo < 100 else (1 if consumo < 200 else 2)
    return (soc_state, gen_state, consumo_state)

def choose_action(state, Q, epsilon):
    """Política epsilon-greedy"""
    if np.random.random() < epsilon:
        return np.random.randint(3)  # Exploración
    else:
        return np.argmax(Q[state])  # Explotación

def calculate_reward(soc, gen, consumo, action):
    """Función de recompensa"""
    reward = 0
    
    # Recompensas por SOC óptimo
    if 25 <= soc <= 80:
        reward += 2
    elif soc < 20:
        reward -= 5  # Penalizar descarga profunda
    elif soc > 90:
        reward -= 3  # Penalizar sobrecarga
    
    # Recompensas por uso eficiente
    if action == 1 and gen >= consumo:  # Alimentar directo
        reward += 3
    elif action == 0 and gen > consumo and soc < 80:  # Cargar batería
        reward += 1
    elif action == 2 and soc > 90:  # Dump load cuando batería llena
        reward += 1
    
    return reward

# Entrenamiento
episodes = 10000
for episode in range(episodes):
    # Simular estado inicial
    soc = np.random.uniform(20, 90)
    gen = np.random.uniform(0, 300)
    consumo = np.random.uniform(50, 250)
    
    state = get_state(soc, gen, consumo)
    action = choose_action(state, Q, epsilon)
    reward = calculate_reward(soc, gen, consumo, action)
    
    # Simular siguiente estado (simplificado)
    next_soc = soc + (gen - consumo) * 0.01
    next_state = get_state(next_soc, gen, consumo)
    
    # Actualizar Q
    Q[state][action] += alpha * (reward + gamma * np.max(Q[next_state]) - Q[state][action])

# Guardar política
np.save('politica_carga_ql.npy', Q)
print('Entrenamiento completado')
```

### 4.2 Uso de Política Entrenada

```python
# Cargar política
Q = np.load('politica_carga_ql.npy')

def decidir_accion(soc, gen, consumo):
    """Decidir acción óptima según política"""
    state = get_state(soc, gen, consumo)
    action = np.argmax(Q[state])
    
    acciones = ['Cargar batería', 'Alimentar directo', 'Activar dump load']
    return acciones[action]

# Ejemplo
soc_actual = 45  # %
gen_actual = 120  # W
consumo_actual = 80  # W

accion = decidir_accion(soc_actual, gen_actual, consumo_actual)
print(f'Acción recomendada: {accion}')
```

---

## 5. Predicción de Consumo

### 5.1 LSTM para Series Temporales

```python
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout

# Preparar secuencias
def create_sequences(data, seq_length=24):
    """Crear secuencias de 24 horas para predecir siguiente hora"""
    X, y = [], []
    for i in range(len(data) - seq_length):
        X.append(data[i:i+seq_length])
        y.append(data[i+seq_length])
    return np.array(X), np.array(y)

# Datos de consumo
consumo = df['potencia_consumo'].values
X, y = create_sequences(consumo, seq_length=24)

# Split
split = int(0.8 * len(X))
X_train, X_test = X[:split], X[split:]
y_train, y_test = y[:split], y[split:]

# Reshape para LSTM (samples, timesteps, features)
X_train = X_train.reshape((X_train.shape[0], X_train.shape[1], 1))
X_test = X_test.reshape((X_test.shape[0], X_test.shape[1], 1))

# Modelo LSTM
model = Sequential([
    LSTM(50, activation='relu', return_sequences=True, input_shape=(24, 1)),
    Dropout(0.2),
    LSTM(50, activation='relu'),
    Dropout(0.2),
    Dense(1)
])

model.compile(optimizer='adam', loss='mse', metrics=['mae'])

# Entrenar
history = model.fit(
    X_train, y_train,
    epochs=50,
    batch_size=32,
    validation_split=0.2,
    verbose=1
)

# Evaluar
loss, mae = model.evaluate(X_test, y_test)
print(f'Test MAE: {mae:.2f} W')

# Guardar
model.save('modelo_lstm_consumo.h5')
```

---

## 6. Dashboard de Análisis

### 6.1 Script de Visualización Completo

```python
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('dataset_ml_clean.csv')
df['timestamp'] = pd.to_datetime(df['timestamp'])

fig, axes = plt.subplots(3, 2, figsize=(16, 12))

# 1. Potencia eólica vs viento API
axes[0, 0].scatter(df['wind_speed_api'], df['potencia_eolica'], alpha=0.3)
axes[0, 0].set_xlabel('Velocidad Viento API (m/s)')
axes[0, 0].set_ylabel('Potencia Eólica (W)')
axes[0, 0].set_title('Potencia vs Viento')
axes[0, 0].grid(True)

# 2. RPM vs Potencia
axes[0, 1].scatter(df['rpm'], df['potencia_eolica'], alpha=0.3, c=df['wind_speed_api'], cmap='viridis')
axes[0, 1].set_xlabel('RPM')
axes[0, 1].set_ylabel('Potencia Eólica (W)')
axes[0, 1].set_title('RPM vs Potencia (color = viento)')
axes[0, 1].grid(True)

# 3. Serie temporal generación
axes[1, 0].plot(df['timestamp'], df['potencia_solar'], label='Solar', alpha=0.7)
axes[1, 0].plot(df['timestamp'], df['potencia_eolica'], label='Eólica', alpha=0.7)
axes[1, 0].set_xlabel('Tiempo')
axes[1, 0].set_ylabel('Potencia (W)')
axes[1, 0].set_title('Generación Temporal')
axes[1, 0].legend()
axes[1, 0].grid(True)

# 4. Distribución SOC batería
axes[1, 1].hist(df['soc_bateria'], bins=50, edgecolor='black')
axes[1, 1].axvline(25, color='r', linestyle='--', label='Límite bajo')
axes[1, 1].axvline(80, color='r', linestyle='--', label='Límite alto')
axes[1, 1].set_xlabel('SOC (%)')
axes[1, 1].set_ylabel('Frecuencia')
axes[1, 1].set_title('Distribución SOC Batería')
axes[1, 1].legend()

# 5. Heatmap hora vs día semana (potencia promedio)
pivot = df.pivot_table(values='potencia_total', index='hora', columns='dia_semana', aggfunc='mean')
sns.heatmap(pivot, ax=axes[2, 0], cmap='YlOrRd', annot=True, fmt='.0f')
axes[2, 0].set_title('Potencia Promedio (W) por Hora y Día')
axes[2, 0].set_xlabel('Día Semana (0=Lun)')
axes[2, 0].set_ylabel('Hora')

# 6. Eficiencia eólica
df['eficiencia_eolica'] = df['potencia_eolica'] / (df['potencia_teorica_viento'] + 1e-6)
axes[2, 1].scatter(df['wind_speed_api'], df['eficiencia_eolica'], alpha=0.3)
axes[2, 1].axhline(0.4, color='r', linestyle='--', label='Límite Betz (59.3%)')
axes[2, 1].set_xlabel('Velocidad Viento (m/s)')
axes[2, 1].set_ylabel('Eficiencia')
axes[2, 1].set_title('Eficiencia Eólica')
axes[2, 1].legend()
axes[2, 1].grid(True)

plt.tight_layout()
plt.savefig('dashboard_analisis.png', dpi=300)
plt.show()
```

---

**Complementa**: `PLAN_ELECTRONICA_POTENCIA_DETALLADO.md`
