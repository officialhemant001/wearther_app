import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { useAuthStore } from './store/authStore';
import Landing from './pages/Landing';
import Login from './pages/Login';
import Signup from './pages/Signup';
import Dashboard from './pages/Dashboard';
import Forecast from './pages/Forecast';
import Health from './pages/Health';
import Farming from './pages/Farming';
import Radar from './pages/Radar';
import Settings from './pages/Settings';
import Profile from './pages/Profile';
import Assistant from './pages/Assistant';

const ProtectedRoute = ({ children }) => {
  const isAuthenticated = useAuthStore((state) => state.isAuthenticated);
  return isAuthenticated ? children : <Navigate to="/login" replace />;
};

export const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Landing />} />
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
        
        {/* Core feature dashboards */}
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/forecast" element={<Forecast />} />
        <Route path="/health" element={<Health />} />
        <Route path="/farming" element={<Farming />} />
        <Route path="/radar" element={<Radar />} />
        
        {/* Protected customer panel routes */}
        <Route
          path="/settings"
          element={
            <ProtectedRoute>
              <Settings />
            </ProtectedRoute>
          }
        />
        <Route
          path="/profile"
          element={
            <ProtectedRoute>
              <Profile />
            </ProtectedRoute>
          }
        />
        <Route
          path="/assistant"
          element={
            <ProtectedRoute>
              <Assistant />
            </ProtectedRoute>
          }
        />
        
        {/* Catch all fallback */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Router>
  );
};
export default App;
