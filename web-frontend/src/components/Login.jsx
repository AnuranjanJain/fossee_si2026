import { useState } from 'react';
import { login, register } from '../services/api';

function Login({ onLogin }) {
    const [isSignUp, setIsSignUp] = useState(false);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState('');

    // Login form state
    const [loginData, setLoginData] = useState({ username: '', password: '' });

    // Signup form state
    const [signupData, setSignupData] = useState({
        username: '',
        email: '',
        password: '',
        confirmPassword: ''
    });

    const handleLogin = async (e) => {
        e.preventDefault();
        setIsLoading(true);
        setError('');

        try {
            const data = await login(loginData.username, loginData.password);
            localStorage.setItem('authToken', data.token);
            onLogin(data.user);
        } catch (err) {
            setError(err.response?.data?.error || 'Login failed. Please try again.');
        } finally {
            setIsLoading(false);
        }
    };

    const handleSignup = async (e) => {
        e.preventDefault();
        setIsLoading(true);
        setError('');

        if (signupData.password !== signupData.confirmPassword) {
            setError('Passwords do not match');
            setIsLoading(false);
            return;
        }

        try {
            const data = await register(
                signupData.username,
                signupData.email,
                signupData.password,
                signupData.confirmPassword
            );
            localStorage.setItem('authToken', data.token);
            onLogin(data.user);
        } catch (err) {
            const errors = err.response?.data;
            if (errors) {
                const firstError = Object.values(errors)[0];
                setError(Array.isArray(firstError) ? firstError[0] : firstError);
            } else {
                setError('Registration failed. Please try again.');
            }
        } finally {
            setIsLoading(false);
        }
    };

    const toggleMode = () => {
        setIsSignUp(!isSignUp);
        setError('');
    };

    return (
        <div className="login-container">
            <div className={`auth-slider ${isSignUp ? 'signup-mode' : ''}`}>
                {/* Login Panel */}
                <div className="auth-panel login-panel">
                    <div className="login-card">
                        <div className="login-header">
                            <div className="logo-icon">🧪</div>
                            <h1 className="login-title">Chemical Equipment Visualizer</h1>
                            <p className="login-subtitle">Sign in to access your dashboard</p>
                        </div>

                        <form className="login-form" onSubmit={handleLogin}>
                            {error && !isSignUp && <div className="error-message">{error}</div>}

                            <div className="form-group">
                                <label htmlFor="login-username">Username</label>
                                <input
                                    type="text"
                                    id="login-username"
                                    value={loginData.username}
                                    onChange={(e) => setLoginData({ ...loginData, username: e.target.value })}
                                    placeholder="Enter username"
                                    required
                                />
                            </div>

                            <div className="form-group">
                                <label htmlFor="login-password">Password</label>
                                <input
                                    type="password"
                                    id="login-password"
                                    value={loginData.password}
                                    onChange={(e) => setLoginData({ ...loginData, password: e.target.value })}
                                    placeholder="Enter password"
                                    required
                                />
                            </div>

                            <button type="submit" className="btn btn-primary btn-full" disabled={isLoading}>
                                {isLoading ? 'Signing In...' : 'Sign In'}
                            </button>
                        </form>

                        <p className="auth-switch">
                            Don't have an account?
                            <button type="button" className="link-btn" onClick={toggleMode}>
                                Sign Up
                            </button>
                        </p>

                        <p className="demo-credentials">Demo credentials: admin / admin123</p>
                    </div>
                </div>

                {/* Signup Panel */}
                <div className="auth-panel signup-panel">
                    <div className="login-card">
                        <div className="login-header">
                            <div className="logo-icon">🧪</div>
                            <h1 className="login-title">Create Account</h1>
                            <p className="login-subtitle">Join us to analyze your equipment data</p>
                        </div>

                        <form className="login-form" onSubmit={handleSignup}>
                            {error && isSignUp && <div className="error-message">{error}</div>}

                            <div className="form-group">
                                <label htmlFor="signup-username">Username</label>
                                <input
                                    type="text"
                                    id="signup-username"
                                    value={signupData.username}
                                    onChange={(e) => setSignupData({ ...signupData, username: e.target.value })}
                                    placeholder="Choose a username"
                                    required
                                    minLength={3}
                                />
                            </div>

                            <div className="form-group">
                                <label htmlFor="signup-email">Email</label>
                                <input
                                    type="email"
                                    id="signup-email"
                                    value={signupData.email}
                                    onChange={(e) => setSignupData({ ...signupData, email: e.target.value })}
                                    placeholder="Enter your email"
                                    required
                                />
                            </div>

                            <div className="form-group">
                                <label htmlFor="signup-password">Password</label>
                                <input
                                    type="password"
                                    id="signup-password"
                                    value={signupData.password}
                                    onChange={(e) => setSignupData({ ...signupData, password: e.target.value })}
                                    placeholder="Create a password"
                                    required
                                    minLength={6}
                                />
                            </div>

                            <div className="form-group">
                                <label htmlFor="signup-confirm">Confirm Password</label>
                                <input
                                    type="password"
                                    id="signup-confirm"
                                    value={signupData.confirmPassword}
                                    onChange={(e) => setSignupData({ ...signupData, confirmPassword: e.target.value })}
                                    placeholder="Confirm your password"
                                    required
                                />
                            </div>

                            <button type="submit" className="btn btn-primary btn-full" disabled={isLoading}>
                                {isLoading ? 'Creating Account...' : 'Sign Up'}
                            </button>
                        </form>

                        <p className="auth-switch">
                            Already have an account?
                            <button type="button" className="link-btn" onClick={toggleMode}>
                                Sign In
                            </button>
                        </p>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default Login;
