import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  }
});

// Request Interceptor: Attach JWT token if present
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response Interceptor: Handle token refresh or auth expiration
api.interceptors.response.use(
  (response) => response.data,
  async (error) => {
    const originalRequest = error.config;
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      const refreshToken = localStorage.getItem('refresh_token');

      if (refreshToken) {
        try {
          const res = await axios.post(`${api.defaults.baseURL}/auth/token/refresh/`, {
            refresh: refreshToken
          });
          const newAccess = res.data?.data?.access || res.data?.access;
          if (newAccess) {
            localStorage.setItem('access_token', newAccess);
            originalRequest.headers.Authorization = `Bearer ${newAccess}`;
            return axios(originalRequest);
          }
        } catch (refreshError) {
          // Clear and force logout if refresh token expires
          localStorage.removeItem('access_token');
          localStorage.removeItem('refresh_token');
          window.location.href = '/login';
        }
      }
    }
    return Promise.reject(error.response?.data || error.message);
  }
);

export default api;
