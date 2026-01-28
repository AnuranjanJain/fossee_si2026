import { useState } from 'react';
import { login } from '../services/api';

function Login({ onLogin }) {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setLoading(true);

        try {
            const data = await login(username, password);
            localStorage.setItem('authToken', data.token);
            onLogin(data.user);
        } catch (err) {
            setError(err.response?.data?.error || 'Login failed. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="login-container">
            <div className="login-card">
                <div className="login-header">
                    <div className="logo-icon" style={{ margin: '0 auto var(--space-md)', width: '48px', height: '48px', fontSize: '1.5rem' }}>
                        ⚗️
                    </div>
                    <h1 className="login-title">Chemical Equipment Visualizer</h1>
                    <p className="login-subtitle">Sign in to access your dashboard</p>
                </div>

                <form className="login-form" onSubmit={handleSubmit}>
                    <div className="form-group">
                        <label className="form-label" htmlFor="username">Username</label>
                        <input
                            id="username"
                            type="text"
                            className="input"
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                            placeholder="Enter your username"
                            required
                        />
                    </div>

                    <div className="form-group">
                        <label className="form-label" htmlFor="password">Password</label>
                        <input
                            id="password"
                            type="password"
                            className="input"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            placeholder="Enter your password"
                            required
                        />
                    </div>

                    <button
                        type="submit"
                        className="btn btn-primary login-btn"
                        disabled={loading}
                    >
                        {loading ? 'Signing in...' : 'Sign In'}
                    </button>

                    {error && <p className="error-message">{error}</p>}
                </form>

                <p className="text-muted text-center" style={{ marginTop: 'var(--space-lg)', fontSize: '0.75rem' }}>
                    Demo credentials: admin / admin123
                </p>
            </div>
        </div>
    );
}

export default Login;
