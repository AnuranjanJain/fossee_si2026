function DataTable({ equipment }) {
    if (!equipment || equipment.length === 0) {
        return (
            <div className="card">
                <div className="card-header">
                    <h2 className="card-title">📊 Equipment Data</h2>
                </div>
                <div className="empty-state">
                    <div className="empty-icon">📋</div>
                    <p>No data available. Upload a CSV file to get started.</p>
                </div>
            </div>
        );
    }

    const getTypeBadgeClass = (type) => {
        const typeMap = {
            'Pump': 'pump',
            'Compressor': 'compressor',
            'Valve': 'valve',
            'HeatExchanger': 'heatexchanger',
            'Heat Exchanger': 'heatexchanger',
            'Reactor': 'reactor',
            'Condenser': 'condenser',
        };
        return typeMap[type] || '';
    };

    return (
        <div className="card">
            <div className="card-header">
                <h2 className="card-title">📊 Equipment Data</h2>
                <span className="text-muted" style={{ fontSize: '0.875rem' }}>
                    {equipment.length} records
                </span>
            </div>

            <div className="table-container">
                <table className="data-table">
                    <thead>
                        <tr>
                            <th>Equipment Name</th>
                            <th>Type</th>
                            <th>Flowrate</th>
                            <th>Pressure</th>
                            <th>Temperature</th>
                        </tr>
                    </thead>
                    <tbody>
                        {equipment.map((item, index) => (
                            <tr key={item.id || index}>
                                <td style={{ fontWeight: 500 }}>{item.name}</td>
                                <td>
                                    <span className={`type-badge ${getTypeBadgeClass(item.equipment_type)}`}>
                                        {item.equipment_type}
                                    </span>
                                </td>
                                <td>{item.flowrate}</td>
                                <td>{item.pressure}</td>
                                <td>{item.temperature}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
}

export default DataTable;
