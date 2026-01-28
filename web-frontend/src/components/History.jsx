import { useState, useEffect } from 'react';
import { getHistory, downloadPDF } from '../services/api';

function History({ onSelectSession, activeSessionId }) {
    const [history, setHistory] = useState([]);
    const [loading, setLoading] = useState(true);
    const [downloading, setDownloading] = useState(null);

    useEffect(() => {
        loadHistory();
    }, []);

    const loadHistory = async () => {
        try {
            const data = await getHistory();
            setHistory(data);
        } catch (err) {
            console.error('Failed to load history:', err);
        } finally {
            setLoading(false);
        }
    };

    const handleDownloadPDF = async (e, sessionId) => {
        e.stopPropagation();
        setDownloading(sessionId);
        try {
            await downloadPDF(sessionId);
        } catch (err) {
            console.error('Failed to download PDF:', err);
        } finally {
            setDownloading(null);
        }
    };

    const formatDate = (dateString) => {
        const date = new Date(dateString);
        return date.toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit',
        });
    };

    if (loading) {
        return (
            <div className="card">
                <div className="card-header">
                    <h2 className="card-title">📜 Upload History</h2>
                </div>
                <div className="loading">
                    <div className="spinner"></div>
                    <p>Loading history...</p>
                </div>
            </div>
        );
    }

    return (
        <div className="card">
            <div className="card-header">
                <h2 className="card-title">📜 Upload History</h2>
                <span className="text-muted" style={{ fontSize: '0.875rem' }}>
                    Last 5 uploads
                </span>
            </div>

            {history.length === 0 ? (
                <div className="empty-state">
                    <div className="empty-icon">📁</div>
                    <p>No upload history yet.</p>
                </div>
            ) : (
                <div className="history-list">
                    {history.map((session) => (
                        <div
                            key={session.id}
                            className={`history-item ${activeSessionId === session.id ? 'active' : ''}`}
                            onClick={() => onSelectSession(session.id)}
                        >
                            <div className="history-info">
                                <span className="history-filename">📄 {session.filename}</span>
                                <div className="history-meta">
                                    <span>{formatDate(session.uploaded_at)}</span>
                                    <span>•</span>
                                    <span>{session.equipment_count} records</span>
                                </div>
                            </div>
                            <div className="history-actions">
                                <button
                                    className="btn btn-secondary"
                                    onClick={(e) => handleDownloadPDF(e, session.id)}
                                    disabled={downloading === session.id}
                                    style={{ padding: 'var(--space-xs) var(--space-sm)', fontSize: '0.75rem' }}
                                >
                                    {downloading === session.id ? '⏳' : '📥'} PDF
                                </button>
                            </div>
                        </div>
                    ))}
                </div>
            )}

            <div style={{ marginTop: 'var(--space-lg)', textAlign: 'center' }}>
                <button className="btn btn-secondary" onClick={loadHistory}>
                    🔄 Refresh History
                </button>
            </div>
        </div>
    );
}

export default History;
