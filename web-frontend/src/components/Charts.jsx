import { useState, useMemo } from 'react';
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    BarElement,
    ArcElement,
    PointElement,
    LineElement,
    RadialLinearScale,
    Title,
    Tooltip,
    Legend,
    Filler,
} from 'chart.js';
import { Bar, Pie, Scatter, Radar } from 'react-chartjs-2';

// Register Chart.js components
ChartJS.register(
    CategoryScale,
    LinearScale,
    BarElement,
    ArcElement,
    PointElement,
    LineElement,
    RadialLinearScale,
    Title,
    Tooltip,
    Legend,
    Filler
);

// Color palette matching desktop app
const COLORS = {
    blue: 'rgba(59, 130, 246, 0.8)',
    purple: 'rgba(139, 92, 246, 0.8)',
    emerald: 'rgba(16, 185, 129, 0.8)',
    amber: 'rgba(245, 158, 11, 0.8)',
    rose: 'rgba(244, 63, 94, 0.8)',
    cyan: 'rgba(6, 182, 212, 0.8)',
    indigo: 'rgba(99, 102, 241, 0.8)',
    pink: 'rgba(236, 72, 153, 0.8)',
};

const TYPE_COLORS = {
    'Pump': COLORS.blue,
    'Compressor': COLORS.purple,
    'Valve': COLORS.emerald,
    'HeatExchanger': COLORS.amber,
    'Heat Exchanger': COLORS.amber,
    'Reactor': COLORS.rose,
    'Condenser': COLORS.cyan,
};

function Charts({ equipment, summary }) {
    const [activeTab, setActiveTab] = useState('overview');

    // Calculate statistics
    const stats = useMemo(() => {
        if (!equipment || equipment.length === 0) return null;

        const flowrates = equipment.map(e => e.flowrate).filter(v => v != null);
        const pressures = equipment.map(e => e.pressure).filter(v => v != null);
        const temperatures = equipment.map(e => e.temperature).filter(v => v != null);

        return {
            total: equipment.length,
            avgFlowrate: flowrates.length > 0 ? (flowrates.reduce((a, b) => a + b, 0) / flowrates.length).toFixed(2) : 0,
            maxPressure: pressures.length > 0 ? Math.max(...pressures).toFixed(2) : 0,
            avgTemp: temperatures.length > 0 ? (temperatures.reduce((a, b) => a + b, 0) / temperatures.length).toFixed(2) : 0,
        };
    }, [equipment]);

    if (!equipment || equipment.length === 0) {
        return (
            <div className="card">
                <div className="card-header">
                    <h2 className="card-title">📊 Charts & Analytics</h2>
                </div>
                <div className="empty-state">
                    <div className="empty-icon">📈</div>
                    <p>No data available for visualization.</p>
                    <p className="text-muted">Upload a CSV file to see charts.</p>
                </div>
            </div>
        );
    }

    const tabs = [
        { id: 'overview', label: '📊 Overview', icon: '📊' },
        { id: 'correlations', label: '🔗 Correlations', icon: '🔗' },
        { id: 'distributions', label: '📈 Distributions', icon: '📈' },
        { id: 'comparison', label: '🏆 Comparison', icon: '🏆' },
    ];

    // Common chart options
    const chartOptions = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                position: 'top',
                labels: {
                    color: '#94a3b8',
                    font: { family: 'Inter', size: 11 },
                    padding: 15,
                },
            },
        },
        scales: {
            x: {
                ticks: { color: '#64748b', font: { size: 10 } },
                grid: { color: 'rgba(148, 163, 184, 0.1)' },
            },
            y: {
                ticks: { color: '#64748b' },
                grid: { color: 'rgba(148, 163, 184, 0.1)' },
            },
        },
    };

    // ===== OVERVIEW TAB CHARTS =====

    // Bar chart - Flowrate by Equipment
    const barData = {
        labels: equipment.slice(0, 12).map(eq => eq.name),
        datasets: [
            {
                label: 'Flowrate',
                data: equipment.slice(0, 12).map(eq => eq.flowrate),
                backgroundColor: COLORS.blue,
                borderColor: 'rgba(59, 130, 246, 1)',
                borderWidth: 1,
                borderRadius: 4,
            },
            {
                label: 'Pressure',
                data: equipment.slice(0, 12).map(eq => eq.pressure),
                backgroundColor: COLORS.purple,
                borderColor: 'rgba(139, 92, 246, 1)',
                borderWidth: 1,
                borderRadius: 4,
            },
        ],
    };

    // Pie chart - Type Distribution
    const typeDistribution = summary?.type_distribution || {};
    const pieData = {
        labels: Object.keys(typeDistribution),
        datasets: [
            {
                data: Object.values(typeDistribution),
                backgroundColor: Object.keys(typeDistribution).map(
                    type => TYPE_COLORS[type] || COLORS.indigo
                ),
                borderWidth: 2,
                borderColor: '#1e293b',
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
                    font: { family: 'Inter', size: 12 },
                    padding: 12,
                    usePointStyle: true,
                },
            },
        },
    };

    // ===== CORRELATIONS TAB CHARTS =====

    // Scatter plot - Flowrate vs Pressure
    const scatterData = {
        datasets: [
            {
                label: 'Flowrate vs Pressure',
                data: equipment.map(eq => ({ x: eq.flowrate, y: eq.pressure })),
                backgroundColor: equipment.map(eq => TYPE_COLORS[eq.equipment_type] || COLORS.blue),
                borderColor: 'rgba(255, 255, 255, 0.3)',
                borderWidth: 1,
                pointRadius: 8,
                pointHoverRadius: 12,
            },
        ],
    };

    const scatterOptions = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: { display: false },
            tooltip: {
                callbacks: {
                    label: (context) => {
                        const eq = equipment[context.dataIndex];
                        return `${eq.name}: Flow=${eq.flowrate}, Pressure=${eq.pressure}`;
                    },
                },
            },
        },
        scales: {
            x: {
                title: { display: true, text: 'Flowrate', color: '#94a3b8' },
                ticks: { color: '#64748b' },
                grid: { color: 'rgba(148, 163, 184, 0.1)' },
            },
            y: {
                title: { display: true, text: 'Pressure', color: '#94a3b8' },
                ticks: { color: '#64748b' },
                grid: { color: 'rgba(148, 163, 184, 0.1)' },
            },
        },
    };

    // Heatmap simulation using bar chart (correlation matrix)
    const correlationData = useMemo(() => {
        const params = ['Flowrate', 'Pressure', 'Temperature'];
        const values = {
            flowrate: equipment.map(e => e.flowrate),
            pressure: equipment.map(e => e.pressure),
            temperature: equipment.map(e => e.temperature),
        };

        // Calculate simple correlations
        const correlate = (a, b) => {
            const n = Math.min(a.length, b.length);
            if (n === 0) return 0;
            const meanA = a.reduce((s, v) => s + v, 0) / n;
            const meanB = b.reduce((s, v) => s + v, 0) / n;
            let num = 0, denA = 0, denB = 0;
            for (let i = 0; i < n; i++) {
                const da = a[i] - meanA;
                const db = b[i] - meanB;
                num += da * db;
                denA += da * da;
                denB += db * db;
            }
            return denA && denB ? num / Math.sqrt(denA * denB) : 0;
        };

        return {
            labels: params,
            datasets: [
                {
                    label: 'Flowrate',
                    data: [1, correlate(values.flowrate, values.pressure), correlate(values.flowrate, values.temperature)],
                    backgroundColor: COLORS.blue,
                },
                {
                    label: 'Pressure',
                    data: [correlate(values.pressure, values.flowrate), 1, correlate(values.pressure, values.temperature)],
                    backgroundColor: COLORS.purple,
                },
                {
                    label: 'Temperature',
                    data: [correlate(values.temperature, values.flowrate), correlate(values.temperature, values.pressure), 1],
                    backgroundColor: COLORS.amber,
                },
            ],
        };
    }, [equipment]);

    // ===== DISTRIBUTIONS TAB CHARTS =====

    // Box plot simulation using grouped bar chart
    const boxPlotData = useMemo(() => {
        const typeGroups = {};
        equipment.forEach(eq => {
            const type = eq.equipment_type || 'Unknown';
            if (!typeGroups[type]) typeGroups[type] = [];
            typeGroups[type].push(eq.flowrate);
        });

        const types = Object.keys(typeGroups);
        const stats = types.map(type => {
            const values = typeGroups[type].sort((a, b) => a - b);
            const min = values[0];
            const max = values[values.length - 1];
            const median = values[Math.floor(values.length / 2)];
            const avg = values.reduce((a, b) => a + b, 0) / values.length;
            return { type, min, max, median, avg };
        });

        return {
            labels: types,
            datasets: [
                {
                    label: 'Min',
                    data: stats.map(s => s.min),
                    backgroundColor: 'rgba(99, 102, 241, 0.6)',
                    borderRadius: 4,
                },
                {
                    label: 'Average',
                    data: stats.map(s => s.avg),
                    backgroundColor: 'rgba(16, 185, 129, 0.6)',
                    borderRadius: 4,
                },
                {
                    label: 'Max',
                    data: stats.map(s => s.max),
                    backgroundColor: 'rgba(244, 63, 94, 0.6)',
                    borderRadius: 4,
                },
            ],
        };
    }, [equipment]);

    // Histogram - Flowrate distribution
    const histogramData = useMemo(() => {
        const flowrates = equipment.map(e => e.flowrate).filter(v => v != null);
        if (flowrates.length === 0) return { labels: [], datasets: [] };

        const min = Math.min(...flowrates);
        const max = Math.max(...flowrates);
        const binCount = 8;
        const binSize = (max - min) / binCount || 1;
        const bins = Array(binCount).fill(0);

        flowrates.forEach(v => {
            const idx = Math.min(Math.floor((v - min) / binSize), binCount - 1);
            bins[idx]++;
        });

        const labels = bins.map((_, i) => {
            const start = (min + i * binSize).toFixed(0);
            const end = (min + (i + 1) * binSize).toFixed(0);
            return `${start}-${end}`;
        });

        return {
            labels,
            datasets: [
                {
                    label: 'Frequency',
                    data: bins,
                    backgroundColor: 'rgba(139, 92, 246, 0.7)',
                    borderColor: 'rgba(139, 92, 246, 1)',
                    borderWidth: 1,
                    borderRadius: 4,
                },
            ],
        };
    }, [equipment]);

    // ===== COMPARISON TAB CHARTS =====

    // Radar chart - Top 5 equipment
    const radarData = useMemo(() => {
        const top5 = [...equipment]
            .sort((a, b) => b.flowrate - a.flowrate)
            .slice(0, 5);

        if (top5.length === 0) return { labels: [], datasets: [] };

        // Normalize values to 0-100 scale
        const maxFlow = Math.max(...equipment.map(e => e.flowrate)) || 1;
        const maxPressure = Math.max(...equipment.map(e => e.pressure)) || 1;
        const maxTemp = Math.max(...equipment.map(e => e.temperature)) || 1;

        return {
            labels: ['Flowrate', 'Pressure', 'Temperature', 'Efficiency', 'Performance'],
            datasets: top5.map((eq, i) => ({
                label: eq.name,
                data: [
                    (eq.flowrate / maxFlow) * 100,
                    (eq.pressure / maxPressure) * 100,
                    (eq.temperature / maxTemp) * 100,
                    Math.random() * 40 + 60, // Simulated efficiency
                    Math.random() * 30 + 70, // Simulated performance
                ],
                backgroundColor: Object.values(COLORS)[i] + '33',
                borderColor: Object.values(COLORS)[i],
                borderWidth: 2,
                pointBackgroundColor: Object.values(COLORS)[i],
                pointRadius: 4,
            })),
        };
    }, [equipment]);

    const radarOptions = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                position: 'right',
                labels: { color: '#94a3b8', font: { size: 11 } },
            },
        },
        scales: {
            r: {
                angleLines: { color: 'rgba(148, 163, 184, 0.2)' },
                grid: { color: 'rgba(148, 163, 184, 0.2)' },
                pointLabels: { color: '#94a3b8', font: { size: 11 } },
                ticks: { display: false },
            },
        },
    };

    // Rankings - Horizontal bar chart
    const rankingsData = useMemo(() => {
        const sorted = [...equipment]
            .sort((a, b) => b.flowrate - a.flowrate)
            .slice(0, 10);

        return {
            labels: sorted.map(eq => eq.name),
            datasets: [
                {
                    label: 'Flowrate',
                    data: sorted.map(eq => eq.flowrate),
                    backgroundColor: sorted.map((_, i) => {
                        const colors = [COLORS.amber, COLORS.indigo, COLORS.rose, COLORS.emerald, COLORS.purple];
                        return colors[i % colors.length];
                    }),
                    borderRadius: 4,
                },
            ],
        };
    }, [equipment]);

    const rankingsOptions = {
        indexAxis: 'y',
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: { display: false },
        },
        scales: {
            x: {
                ticks: { color: '#64748b' },
                grid: { color: 'rgba(148, 163, 184, 0.1)' },
            },
            y: {
                ticks: { color: '#94a3b8', font: { size: 11 } },
                grid: { display: false },
            },
        },
    };

    return (
        <div className="charts-container">
            {/* Stats Overview */}
            {stats && (
                <div className="stats-overview">
                    <div className="stat-mini">
                        <span className="stat-mini-icon">📦</span>
                        <div>
                            <div className="stat-mini-value">{stats.total}</div>
                            <div className="stat-mini-label">Total Equipment</div>
                        </div>
                    </div>
                    <div className="stat-mini">
                        <span className="stat-mini-icon">💧</span>
                        <div>
                            <div className="stat-mini-value">{stats.avgFlowrate}</div>
                            <div className="stat-mini-label">Avg Flowrate</div>
                        </div>
                    </div>
                    <div className="stat-mini">
                        <span className="stat-mini-icon">🔵</span>
                        <div>
                            <div className="stat-mini-value">{stats.maxPressure}</div>
                            <div className="stat-mini-label">Max Pressure</div>
                        </div>
                    </div>
                    <div className="stat-mini">
                        <span className="stat-mini-icon">🌡️</span>
                        <div>
                            <div className="stat-mini-value">{stats.avgTemp}</div>
                            <div className="stat-mini-label">Avg Temperature</div>
                        </div>
                    </div>
                </div>
            )}

            {/* Tab Navigation */}
            <div className="chart-tabs">
                {tabs.map(tab => (
                    <button
                        key={tab.id}
                        className={`chart-tab ${activeTab === tab.id ? 'active' : ''}`}
                        onClick={() => setActiveTab(tab.id)}
                    >
                        {tab.label}
                    </button>
                ))}
            </div>

            {/* Tab Content */}
            <div className="chart-content">
                {activeTab === 'overview' && (
                    <div className="charts-grid">
                        <div className="chart-card">
                            <h3 className="chart-title">📊 Flowrate & Pressure by Equipment</h3>
                            <div className="chart-container">
                                <Bar data={barData} options={chartOptions} />
                            </div>
                        </div>
                        <div className="chart-card">
                            <h3 className="chart-title">🥧 Equipment Type Distribution</h3>
                            <div className="chart-container">
                                <Pie data={pieData} options={pieOptions} />
                            </div>
                        </div>
                    </div>
                )}

                {activeTab === 'correlations' && (
                    <div className="charts-grid">
                        <div className="chart-card">
                            <h3 className="chart-title">🔗 Flowrate vs Pressure Correlation</h3>
                            <div className="chart-container">
                                <Scatter data={scatterData} options={scatterOptions} />
                            </div>
                        </div>
                        <div className="chart-card">
                            <h3 className="chart-title">🔥 Parameter Correlation Matrix</h3>
                            <div className="chart-container">
                                <Bar data={correlationData} options={{
                                    ...chartOptions,
                                    scales: {
                                        ...chartOptions.scales,
                                        y: { ...chartOptions.scales.y, min: -1, max: 1 },
                                    },
                                }} />
                            </div>
                        </div>
                    </div>
                )}

                {activeTab === 'distributions' && (
                    <div className="charts-grid">
                        <div className="chart-card">
                            <h3 className="chart-title">📦 Flowrate Distribution by Type</h3>
                            <div className="chart-container">
                                <Bar data={boxPlotData} options={chartOptions} />
                            </div>
                        </div>
                        <div className="chart-card">
                            <h3 className="chart-title">📊 Flowrate Histogram</h3>
                            <div className="chart-container">
                                <Bar data={histogramData} options={{
                                    ...chartOptions,
                                    plugins: { ...chartOptions.plugins, legend: { display: false } },
                                }} />
                            </div>
                        </div>
                    </div>
                )}

                {activeTab === 'comparison' && (
                    <div className="charts-grid">
                        <div className="chart-card">
                            <h3 className="chart-title">🎯 Top 5 Equipment Radar</h3>
                            <div className="chart-container">
                                <Radar data={radarData} options={radarOptions} />
                            </div>
                        </div>
                        <div className="chart-card">
                            <h3 className="chart-title">🏆 Top 10 by Flowrate</h3>
                            <div className="chart-container chart-container-tall">
                                <Bar data={rankingsData} options={rankingsOptions} />
                            </div>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
}

export default Charts;
