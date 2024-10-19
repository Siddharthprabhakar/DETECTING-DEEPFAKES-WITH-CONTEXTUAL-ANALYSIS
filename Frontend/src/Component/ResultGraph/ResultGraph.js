import React from 'react';
import { Bar } from 'react-chartjs-2';
import { Chart, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend } from 'chart.js';

// Register required components for the chart
Chart.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

function ResultGraph({ confidence, result }) {
  const data = {
    labels: ['Confidence'], // You can add more labels for additional data points
    datasets: [
      {
        label: result === 'FAKE' ? 'Fake' : 'Real',
        data: [confidence], // Confidence score as data
        backgroundColor: result === 'FAKE' ? 'rgba(255, 99, 132, 0.2)' : 'rgba(75, 192, 192, 0.2)',
        borderColor: result === 'FAKE' ? 'rgba(255, 99, 132, 1)' : 'rgba(75, 192, 192, 1)',
        borderWidth: 1,
      },
    ],
  };

  const options = {
    scales: {
      y: {
        beginAtZero: true,
        max: 100, // Since confidence is a percentage
      },
    },
    plugins: {
      legend: {
        display: true,
        position: 'top',
      },
      title: {
        display: true,
        text: 'Detection Confidence',
      },
    },
  };

  return <Bar data={data} options={options} />;
}

export default ResultGraph;
