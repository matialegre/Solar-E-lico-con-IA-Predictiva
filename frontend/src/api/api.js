import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://190.211.201.217:11112';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// ===== ENERGÍA =====

export const getCurrentEnergy = async () => {
  const response = await api.get('/api/energy/current');
  return response.data;
};

export const getEnergyHistory = async (hours = 24) => {
  const response = await api.get(`/api/energy/history?hours=${hours}`);
  return response.data;
};

export const recordEnergyData = async (data) => {
  const response = await api.post('/api/energy/record', data);
  return response.data;
};

// ===== CLIMA =====

export const getCurrentWeather = async () => {
  const response = await api.get('/api/weather/current');
  return response.data;
};

export const getWeatherForecast = async (hours = 24) => {
  const response = await api.get(`/api/weather/forecast?hours=${hours}`);
  return response.data;
};

// ===== PREDICCIONES =====

export const getPredictions24h = async () => {
  const response = await axios.get(`${API_BASE_URL}/api/predictions/24h`);
  return response.data;
};

export const getForecast5Days = async () => {
  const response = await axios.get(`${API_BASE_URL}/api/weather/forecast`);
  return response.data;
};

export const getAutonomy = async () => {
  const response = await api.get('/api/predictions/autonomy');
  return response.data;
};

// ===== CONTROL =====

export const setManualControl = async (source, action, value = null) => {
  const response = await api.post('/api/control/manual', {
    source,
    action,
    value,
  });
  return response.data;
};

export const setAutoMode = async (enabled) => {
  const response = await api.post('/api/control/auto', {
    enabled,
  });
  return response.data;
};

export const getAIDecision = async () => {
  const response = await api.get('/api/control/decision');
  return response.data;
};

// ===== ALERTAS =====

export const getCurrentAlerts = async () => {
  const response = await api.get('/api/alerts/current');
  return response.data;
};

export const getAlertsHistory = async () => {
  const response = await api.get('/api/alerts/history');
  return response.data;
};

// ===== DASHBOARD =====

export const getDashboardData = async () => {
  const response = await api.get('/api/dashboard');
  return response.data;
};

// ===== SISTEMA =====

export const getSystemStatus = async () => {
  const response = await api.get('/api/system/status');
  return response.data;
};

// ===== WEBSOCKET =====

export const createWebSocket = (onMessage, onError) => {
  const wsUrl = API_BASE_URL.replace('http', 'ws') + '/api/ws';
  const ws = new WebSocket(wsUrl);

  ws.onopen = () => {
    console.log('✅ WebSocket conectado');
  };

  ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    onMessage(data);
  };

  ws.onerror = (error) => {
    console.error('❌ WebSocket error:', error);
    if (onError) onError(error);
  };

  ws.onclose = () => {
    console.log('🔌 WebSocket desconectado');
  };

  return ws;
};

export default api;
