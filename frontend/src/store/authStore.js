import { create } from 'zustand';
import api from '../services/api';

export const useAuthStore = create((set) => ({
  user: null,
  isAuthenticated: !!localStorage.getItem('access_token'),
  loading: false,
  error: null,

  login: async (email, password) => {
    set({ loading: true, error: null });
    try {
      const res = await api.post('/auth/login/', { email, password });
      const { user, tokens } = res.data;

      localStorage.setItem('access_token', tokens.access);
      localStorage.setItem('refresh_token', tokens.refresh);

      set({ user, isAuthenticated: true, loading: false });
      return true;
    } catch (err) {
      set({ error: err.error?.message || 'Login failed', loading: false });
      return false;
    }
  },

  signup: async (username, email, password, confirmPassword) => {
    set({ loading: true, error: null });
    try {
      const res = await api.post('/auth/signup/', {
        username,
        email,
        password,
        password_confirm: confirmPassword
      });
      const { user, tokens } = res.data;

      localStorage.setItem('access_token', tokens.access);
      localStorage.setItem('refresh_token', tokens.refresh);

      set({ user, isAuthenticated: true, loading: false });
      return true;
    } catch (err) {
      set({ error: err.error?.message || 'Signup failed', loading: false });
      return false;
    }
  },

  logout: async () => {
    const refresh = localStorage.getItem('refresh_token');
    try {
      await api.post('/auth/logout/', { refresh });
    } catch (e) {
      // ignore
    } finally {
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      set({ user: null, isAuthenticated: false });
    }
  },

  fetchUserProfile: async () => {
    try {
      const res = await api.get('/users/profile/');
      set({ user: res.data });
    } catch (err) {
      // token probably invalid
    }
  }
}));
