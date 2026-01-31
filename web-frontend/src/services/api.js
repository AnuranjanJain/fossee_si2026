import axios from 'axios';

// Use relative path for same-domain deployment, or environment variable for separate deployment
const API_BASE_URL = import.meta.env.VITE_API_URL || '/api';

// Create axios instance
const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Add auth token to requests
api.interceptors.request.use((config) => {
    const token = localStorage.getItem('authToken');
    if (token) {
        config.headers.Authorization = `Token ${token}`;
    }
    return config;
});

// Handle auth errors
api.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response?.status === 401) {
            localStorage.removeItem('authToken');
            window.location.reload();
        }
        return Promise.reject(error);
    }
);

// Auth API
export const login = async (username, password) => {
    const response = await api.post('/auth/login/', { username, password });
    return response.data;
};

export const logout = async () => {
    await api.post('/auth/logout/');
    localStorage.removeItem('authToken');
};

// Data API
export const uploadCSV = async (file) => {
    const formData = new FormData();
    formData.append('file', file);

    const response = await api.post('/upload/', formData, {
        headers: {
            'Content-Type': 'multipart/form-data',
        },
    });
    return response.data;
};

export const getEquipment = async (sessionId = null) => {
    const params = sessionId ? { session_id: sessionId } : {};
    const response = await api.get('/equipment/', { params });
    return response.data;
};

export const getSummary = async (sessionId = null) => {
    const params = sessionId ? { session_id: sessionId } : {};
    const response = await api.get('/summary/', { params });
    return response.data;
};

export const getHistory = async () => {
    const response = await api.get('/history/');
    return response.data;
};

export const downloadPDF = async (sessionId = null) => {
    const params = sessionId ? { session_id: sessionId } : {};
    const response = await api.get('/report/pdf/', {
        params,
        responseType: 'blob',
    });

    // Create download link
    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', `equipment_report_${sessionId || 'latest'}.pdf`);
    document.body.appendChild(link);
    link.click();
    link.remove();
    window.URL.revokeObjectURL(url);
};

export default api;
