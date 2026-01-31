import { useState, useEffect } from 'react';
import Login from './components/Login';
import FileUpload from './components/FileUpload';
import DataTable from './components/DataTable';
import Summary from './components/Summary';
import Charts from './components/Charts';
import History from './components/History';
import { getEquipment, getSummary, logout, downloadPDF } from './services/api';

function App() {
    const [user, setUser] = useState(null);
    const [activeTab, setActiveTab] = useState('upload');
    const [equipment, setEquipment] = useState([]);
    const [summary, setSummary] = useState(null);
    const [activeSessionId, setActiveSessionId] = useState(null);
    const [loading, setLoading] = useState(false);

    // Check for existing auth token on mount
    useEffect(() => {
        const token = localStorage.getItem('authToken');
        if (token) {
            // Assume logged in, will be redirected if token is invalid
            setUser({ username: 'User' });
            loadData();
        }
    }, []);

    const loadData = async (sessionId = null) => {
        setLoading(true);
        try {
            const [equipmentData, summaryData] = await Promise.all([
                getEquipment(sessionId),
                getSummary(sessionId),
            ]);
            setEquipment(equipmentData);
            setSummary(summaryData);
            if (sessionId) {
                setActiveSessionId(sessionId);
            }
        } catch (err) {
            console.error('Failed to load data:', err);
        } finally {
            setLoading(false);
        }
    };

    const handleLogin = (userData) => {
        setUser(userData);
        loadData();
    };

    const handleLogout = async () => {
        try {
            await logout();
        } catch (err) {
            console.error('Logout error:', err);
        }
        setUser(null);
        setEquipment([]);
        setSummary(null);
        localStorage.removeItem('authToken');
    };

    const handleUploadSuccess = (result) => {
        setSummary({
            ...result.summary,
            filename: result.session_id ? `Session ${result.session_id}` : 'Latest',
        });
        setActiveSessionId(result.session_id);
        loadData(result.session_id);
        setActiveTab('data');
    };

    const handleSelectSession = (sessionId) => {
        setActiveSessionId(sessionId);
        loadData(sessionId);
        setActiveTab('data');
    };

    const handleDownloadPDF = async () => {
        try {
            await downloadPDF(activeSessionId);
        } catch (err) {
            console.error('Failed to download PDF:', err);
        }
    };

    // Show login if not authenticated
    if (!user) {
        return <Login onLogin={handleLogin} />;
    }

    return (
        <div className="app">
            {/* Header */}
            <header className="header">
                <div className="header-content">
                    <div className="logo">
                        <div className="logo-icon">⚗️</div>
                        <span>Chemical Equipment Visualizer</span>
                    </div>

                    <nav className="nav-tabs">
                        <button
                            className={`nav-tab ${activeTab === 'upload' ? 'active' : ''}`}
                            onClick={() => setActiveTab('upload')}
                        >
                            📤 Upload
                        </button>
                        <button
                            className={`nav-tab ${activeTab === 'data' ? 'active' : ''}`}
                            onClick={() => setActiveTab('data')}
                        >
                            📊 Data
                        </button>
                        <button
                            className={`nav-tab ${activeTab === 'charts' ? 'active' : ''}`}
                            onClick={() => setActiveTab('charts')}
                        >
                            📈 Charts
                        </button>
                        <button
                            className={`nav-tab ${activeTab === 'history' ? 'active' : ''}`}
                            onClick={() => setActiveTab('history')}
                        >
                            📜 History
                        </button>
                    </nav>

                    <div className="user-info">
                        {summary && (
                            <button className="btn btn-success" onClick={handleDownloadPDF}>
                                📥 Download PDF
                            </button>
                        )}
                        <span className="user-name">👤 {user.username}</span>
                        <button className="btn btn-secondary" onClick={handleLogout}>
                            Logout
                        </button>
                    </div>
                </div>
            </header>

            {/* Main Content */}
            <main className="main-content">
                {loading ? (
                    <div className="loading">
                        <div className="spinner"></div>
                        <p>Loading data...</p>
                    </div>
                ) : (
                    <>
                        {activeTab === 'upload' && (
                            <div className="grid-2">
                                <FileUpload onUploadSuccess={handleUploadSuccess} />
                                <History
                                    onSelectSession={handleSelectSession}
                                    activeSessionId={activeSessionId}
                                />
                            </div>
                        )}

                        {activeTab === 'data' && (
                            <>
                                <Summary summary={summary} />
                                <DataTable equipment={equipment} />
                            </>
                        )}

                        {activeTab === 'charts' && (
                            <Charts equipment={equipment} summary={summary} />
                        )}

                        {activeTab === 'history' && (
                            <History
                                onSelectSession={handleSelectSession}
                                activeSessionId={activeSessionId}
                            />
                        )}
                    </>
                )}
            </main>
        </div>
    );
}

export default App;
