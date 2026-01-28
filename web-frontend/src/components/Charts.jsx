import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    BarElement,
    ArcElement,
    Title,
    Tooltip,
    Legend,
} from 'chart.js';
import { Bar, Pie } from 'react-chartjs-2';

// Register Chart.js components
ChartJS.register(
    CategoryScale,
    LinearScale,
    BarElement,
    ArcElement,
    Title,
    Tooltip,
    Legend
);

function Charts({ equipment, summary }) {
    if (!equipment || equipment.length === 0) {
        return (
            <div className="card">
                <div className="card-header">
                    <h2 className="card-title">📊 Charts</h2>
                </div>
                <div className="empty-state">
                    <div className="empty-icon">📈</div>
                    <p>No data available for visualization.</p>
                </div>
            </div>
        );
    }

    // Bar chart data - Flowrate by Equipment
    const barData = {
        labels: equipment.slice(0, 15).map(eq => eq.name),
        datasets: [
            {
                label: 'Flowrate',
                data: equipment.slice(0, 15).map(eq => eq.flowrate),
                backgroundColor: 'rgba(59, 130, 246, 0.7)',
                borderColor: 'rgba(59, 130, 246, 1)',
                borderWidth: 1,
                borderRadius: 4,
            },
            {
                label: 'Pressure',
                data: equipment.slice(0, 15).map(eq => eq.pressure),
                backgroundColor: 'rgba(139, 92, 246, 0.7)',
                borderColor: 'rgba(139, 92, 246, 1)',
                borderWidth: 1,
                borderRadius: 4,
            },
        ],
    };

    const barOptions = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                position: 'top',
                labels: {
                    color: '#94a3b8',
                    font: { family: 'Inter' },
                },
            },
        },
        scales: {
            x: {
                ticks: {
                    color: '#64748b',
                    maxRotation: 45,
                    minRotation: 45,
                    font: { size: 10 },
                },
                grid: { color: 'rgba(148, 163, 184, 0.1)' },
            },
            y: {
                ticks: { color: '#64748b' },
                grid: { color: 'rgba(148, 163, 184, 0.1)' },
            },
        },
    };

    // Pie chart data - Type Distribution
    const typeColors = {
        'Pump': 'rgba(59, 130, 246, 0.8)',
        'Compressor': 'rgba(139, 92, 246, 0.8)',
        'Valve': 'rgba(16, 185, 129, 0.8)',
        'HeatExchanger': 'rgba(245, 158, 11, 0.8)',
        'Heat Exchanger': 'rgba(245, 158, 11, 0.8)',
        'Reactor': 'rgba(244, 63, 94, 0.8)',
        'Condenser': 'rgba(6, 182, 212, 0.8)',
    };

    const typeDistribution = summary?.type_distribution || {};
    const pieData = {
        labels: Object.keys(typeDistribution),
        datasets: [
            {
                data: Object.values(typeDistribution),
                backgroundColor: Object.keys(typeDistribution).map(
                    type => typeColors[type] || 'rgba(148, 163, 184, 0.8)'
                ),
                borderWidth: 0,
            },
        ],
    };

    const pieOptions = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                position: 'right',
                labels: {
                    color: '#94a3b8',
                    font: { family: 'Inter' },
                    padding: 15,
                },
            },
        },
    };

    return (
        <div className="charts-grid">
            <div className="chart-card">
                <h3 className="chart-title">📊 Flowrate & Pressure by Equipment</h3>
                <div className="chart-container">
                    <Bar data={barData} options={barOptions} />
                </div>
            </div>

            <div className="chart-card">
                <h3 className="chart-title">🥧 Equipment Type Distribution</h3>
                <div className="chart-container">
                    <Pie data={pieData} options={pieOptions} />
                </div>
            </div>
        </div>
    );
}

export default Charts;
