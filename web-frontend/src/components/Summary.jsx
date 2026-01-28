function Summary({ summary }) {
    if (!summary) {
        return null;
    }

    const stats = [
        { label: 'Total Equipment', value: summary.total_count, icon: '📦' },
        { label: 'Avg Flowrate', value: summary.avg_flowrate?.toFixed(2), icon: '💧' },
        { label: 'Avg Pressure', value: summary.avg_pressure?.toFixed(2), icon: '🔵' },
        { label: 'Avg Temperature', value: summary.avg_temperature?.toFixed(2), icon: '🌡️' },
        { label: 'Min Flowrate', value: summary.min_flowrate?.toFixed(2), icon: '⬇️' },
        { label: 'Max Flowrate', value: summary.max_flowrate?.toFixed(2), icon: '⬆️' },
    ];

    return (
        <div className="card mb-xl">
            <div className="card-header">
                <h2 className="card-title">📈 Summary Statistics</h2>
                {summary.filename && (
                    <span className="text-muted" style={{ fontSize: '0.875rem' }}>
                        {summary.filename}
                    </span>
                )}
            </div>

            <div className="stats-grid">
                {stats.map((stat, index) => (
                    <div key={index} className="stat-card">
                        <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--space-sm)', marginBottom: 'var(--space-xs)' }}>
                            <span>{stat.icon}</span>
                            <span className="stat-label">{stat.label}</span>
                        </div>
                        <div className="stat-value">{stat.value || '—'}</div>
                    </div>
                ))}
            </div>

            {summary.type_distribution && Object.keys(summary.type_distribution).length > 0 && (
                <div style={{ marginTop: 'var(--space-lg)' }}>
                    <h3 style={{ fontSize: '0.875rem', color: 'var(--text-secondary)', marginBottom: 'var(--space-md)' }}>
                        Equipment Type Distribution
                    </h3>
                    <div style={{ display: 'flex', flexWrap: 'wrap', gap: 'var(--space-sm)' }}>
                        {Object.entries(summary.type_distribution).map(([type, count]) => (
                            <div
                                key={type}
                                style={{
                                    padding: 'var(--space-sm) var(--space-md)',
                                    background: 'var(--bg-tertiary)',
                                    borderRadius: 'var(--radius-md)',
                                    fontSize: '0.875rem',
                                }}
                            >
                                <span style={{ color: 'var(--text-primary)', fontWeight: 500 }}>{type}</span>
                                <span style={{ color: 'var(--text-muted)', marginLeft: 'var(--space-sm)' }}>×{count}</span>
                            </div>
                        ))}
                    </div>
                </div>
            )}
        </div>
    );
}

export default Summary;
