import { useState, useRef } from 'react';
import { uploadCSV } from '../services/api';

function FileUpload({ onUploadSuccess }) {
    const [dragOver, setDragOver] = useState(false);
    const [uploading, setUploading] = useState(false);
    const [error, setError] = useState('');
    const fileInputRef = useRef(null);

    const handleFile = async (file) => {
        if (!file) return;

        if (!file.name.endsWith('.csv')) {
            setError('Please upload a CSV file');
            return;
        }

        setError('');
        setUploading(true);

        try {
            const result = await uploadCSV(file);
            onUploadSuccess(result);
        } catch (err) {
            setError(err.response?.data?.error || 'Upload failed. Please try again.');
        } finally {
            setUploading(false);
        }
    };

    const handleDrop = (e) => {
        e.preventDefault();
        setDragOver(false);
        const file = e.dataTransfer.files[0];
        handleFile(file);
    };

    const handleDragOver = (e) => {
        e.preventDefault();
        setDragOver(true);
    };

    const handleDragLeave = () => {
        setDragOver(false);
    };

    const handleClick = () => {
        fileInputRef.current?.click();
    };

    const handleInputChange = (e) => {
        const file = e.target.files[0];
        handleFile(file);
    };

    return (
        <div className="card">
            <div className="card-header">
                <h2 className="card-title">📤 Upload CSV File</h2>
            </div>

            <div
                className={`upload-zone ${dragOver ? 'dragover' : ''}`}
                onDrop={handleDrop}
                onDragOver={handleDragOver}
                onDragLeave={handleDragLeave}
                onClick={handleClick}
            >
                <input
                    ref={fileInputRef}
                    type="file"
                    accept=".csv"
                    onChange={handleInputChange}
                    style={{ display: 'none' }}
                />

                {uploading ? (
                    <div className="loading">
                        <div className="spinner"></div>
                        <p>Processing file...</p>
                    </div>
                ) : (
                    <>
                        <div className="upload-icon">📁</div>
                        <p className="upload-text">
                            <strong>Click to upload</strong> or drag and drop
                        </p>
                        <p className="upload-hint">CSV files only (max 10MB)</p>
                    </>
                )}
            </div>

            {error && (
                <p className="error-message" style={{ marginTop: 'var(--space-md)' }}>
                    {error}
                </p>
            )}

            <div style={{ marginTop: 'var(--space-lg)', padding: 'var(--space-md)', background: 'var(--bg-tertiary)', borderRadius: 'var(--radius-md)' }}>
                <p style={{ fontSize: '0.875rem', color: 'var(--text-secondary)', marginBottom: 'var(--space-sm)' }}>
                    <strong>Expected CSV Format:</strong>
                </p>
                <code style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                    Equipment Name, Type, Flowrate, Pressure, Temperature
                </code>
            </div>
        </div>
    );
}

export default FileUpload;
