import React from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
  Filler,
} from 'chart.js';
import { Line, Bar } from 'react-chartjs-2';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
  Filler
);

const EnergyCharts = ({ historyData, predictionData }) => {
  // Configuración de gráfico de histórico
  const historyChartData = {
    labels: historyData?.records?.map(r => {
      const date = new Date(r.timestamp);
      return date.toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit' });
    }) || [],
    datasets: [
      {
        label: 'Solar (W)',
        data: historyData?.records?.map(r => r.solar_power_w) || [],
        borderColor: 'rgb(234, 179, 8)',
        backgroundColor: 'rgba(234, 179, 8, 0.1)',
        fill: true,
        tension: 0.4,
      },
      {
        label: 'Eólica (W)',
        data: historyData?.records?.map(r => r.wind_power_w) || [],
        borderColor: 'rgb(59, 130, 246)',
        backgroundColor: 'rgba(59, 130, 246, 0.1)',
        fill: true,
        tension: 0.4,
      },
      {
        label: 'Consumo (W)',
        data: historyData?.records?.map(r => r.load_power_w) || [],
        borderColor: 'rgb(239, 68, 68)',
        backgroundColor: 'rgba(239, 68, 68, 0.1)',
        fill: true,
        tension: 0.4,
      },
    ],
  };

  const historyChartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: 'Histórico de Energía (24h)',
        font: {
          size: 16,
          weight: 'bold',
        },
      },
      tooltip: {
        mode: 'index',
        intersect: false,
      },
    },
    scales: {
      y: {
        beginAtZero: true,
        title: {
          display: true,
          text: 'Potencia (W)',
        },
      },
      x: {
        title: {
          display: true,
          text: 'Tiempo',
        },
      },
    },
    interaction: {
      mode: 'nearest',
      axis: 'x',
      intersect: false,
    },
  };

  // Configuración de gráfico de predicción
  const predictionChartData = {
    labels: predictionData?.predictions?.map(p => {
      const date = new Date(p.prediction_time);
      return date.toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit' });
    }) || [],
    datasets: [
      {
        label: 'Solar Prevista (W)',
        data: predictionData?.predictions?.map(p => p.predicted_solar_w) || [],
        backgroundColor: 'rgba(234, 179, 8, 0.7)',
      },
      {
        label: 'Eólica Prevista (W)',
        data: predictionData?.predictions?.map(p => p.predicted_wind_w) || [],
        backgroundColor: 'rgba(59, 130, 246, 0.7)',
      },
      {
        label: 'Consumo Previsto (W)',
        data: predictionData?.predictions?.map(p => p.predicted_consumption_w) || [],
        backgroundColor: 'rgba(239, 68, 68, 0.7)',
      },
    ],
  };

  const predictionChartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: 'Predicción de IA (24h)',
        font: {
          size: 16,
          weight: 'bold',
        },
      },
      tooltip: {
        mode: 'index',
        intersect: false,
      },
    },
    scales: {
      y: {
        beginAtZero: true,
        stacked: false,
        title: {
          display: true,
          text: 'Potencia (W)',
        },
      },
      x: {
        stacked: false,
        title: {
          display: true,
          text: 'Hora del día',
        },
      },
    },
  };

  // Gráfico de batería
  const batteryChartData = {
    labels: historyData?.records?.map(r => {
      const date = new Date(r.timestamp);
      return date.toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit' });
    }) || [],
    datasets: [
      {
        label: 'Estado de Carga (%)',
        data: historyData?.records?.map(r => r.battery_soc_percent) || [],
        borderColor: 'rgb(34, 197, 94)',
        backgroundColor: 'rgba(34, 197, 94, 0.2)',
        fill: true,
        tension: 0.4,
      },
    ],
  };

  const batteryChartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: false,
      },
      title: {
        display: true,
        text: 'Estado de Batería (SoC %)',
        font: {
          size: 16,
          weight: 'bold',
        },
      },
    },
    scales: {
      y: {
        min: 0,
        max: 100,
        title: {
          display: true,
          text: 'SoC (%)',
        },
      },
      x: {
        title: {
          display: true,
          text: 'Tiempo',
        },
      },
    },
  };

  return (
    <div className="space-y-6 bg-white bg-opacity-10 backdrop-blur-lg p-6 rounded-3xl shadow-2xl">
      <div className="card">
        <div className="h-80">
          <Line data={historyChartData} options={historyChartOptions} />
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="card">
          <div className="h-80">
            <Line data={batteryChartData} options={batteryChartOptions} />
          </div>
        </div>

        <div className="card">
          <div className="h-80">
            <Bar data={predictionChartData} options={predictionChartOptions} />
          </div>
        </div>
      </div>
    </div>
  );
};

export default EnergyCharts;
