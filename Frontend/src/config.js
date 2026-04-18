// API Configuration
export const API_BASE_URL = 'http://localhost:8000';

// API Endpoints
export const API_ENDPOINTS = {
    // User Authentication
    USER_SIGNUP: `${API_BASE_URL}/auth_user/signup`,
    USER_LOGIN: `${API_BASE_URL}/auth_user/login`,
    USER_ME: `${API_BASE_URL}/auth_user/me`,
    REQUEST_OTP: `${API_BASE_URL}/auth_user/request-otp`,
    VERIFY_OTP: `${API_BASE_URL}/auth_user/verify-otp`,

    // Admin Authentication
    ADMIN_SIGNUP: `${API_BASE_URL}/auth_admin/signup`,
    ADMIN_LOGIN: `${API_BASE_URL}/auth_admin/login`,

    // Other endpoints (for future use)
    SCORING: `${API_BASE_URL}/scoring`,
    SCORING_ME: `${API_BASE_URL}/scoring/me`,
    APPLICATIONS: `${API_BASE_URL}/applications`,
    APPLICATIONS_ME: `${API_BASE_URL}/applications/my-applications`,
    APPLICATIONS_APPLY: `${API_BASE_URL}/applications/apply`,
    ADMIN_APPLICATIONS: `${API_BASE_URL}/admin/applications`,
    ADMIN_DECISION: (appId) => `${API_BASE_URL}/admin/applications/${appId}/decision`,
    BANKS: `${API_BASE_URL}/aa/banks`,
    ADMIN: `${API_BASE_URL}/admin`,
    REPORTS_DOWNLOAD: (filename) => `${API_BASE_URL}/reports/download/${filename}`,
};

// Helper function for making authenticated API requests
export const apiRequest = async (url, options = {}) => {
    const token = localStorage.getItem('authToken');

    const headers = {
        'Content-Type': 'application/json',
        ...options.headers,
    };

    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }

    const response = await fetch(url, {
        ...options,
        headers,
    });

    // Handle 401 Unauthorized - token expired or invalid
    if (response.status === 401) {
        localStorage.removeItem('authToken');
        localStorage.removeItem('user');
        window.location.href = '/';
    }

    return response;
};
