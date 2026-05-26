import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Sun, Moon, CloudSun, User, Bell } from 'lucide-react';
import { useTheme } from '../../context/ThemeContext';
import { useAuthStore } from '../../store/authStore';

export const Navbar = () => {
  const { theme, toggleTheme } = useTheme();
  const { isAuthenticated, logout } = useAuthStore();
  const location = useLocation();

  const isLinkActive = (path) => location.pathname === path;

  return (
    <header className="sticky top-0 z-40 w-full border-b border-slate-200/80 bg-white/80 backdrop-blur-md dark:border-slate-800/80 dark:bg-slate-950/80 transition-colors duration-300">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="flex h-16 items-center justify-between">
          <div className="flex items-center gap-8">
            <Link to="/" className="flex items-center gap-2 text-slate-900 dark:text-white font-display font-semibold text-lg tracking-tight">
              <CloudSun className="h-6 w-6 text-brand-500" />
              <span>AETHER</span>
            </Link>

            <nav className="hidden md:flex items-center gap-6">
              {[
                { label: 'Dashboard', path: '/dashboard' },
                { label: 'Radar Map', path: '/radar' },
                { label: 'AQI & Health', path: '/health' },
                { label: 'Agricultural', path: '/farming' },
                { label: 'Forecasts', path: '/forecast' },
              ].map((item) => (
                <Link
                  key={item.path}
                  to={item.path}
                  className={`text-sm font-medium transition-colors ${
                    isLinkActive(item.path)
                      ? 'text-brand-500 dark:text-brand-400'
                      : 'text-slate-500 hover:text-slate-900 dark:text-slate-400 dark:hover:text-slate-100'
                  }`}
                >
                  {item.label}
                </Link>
              ))}
            </nav>
          </div>

          <div className="flex items-center gap-4">
            <button
              onClick={toggleTheme}
              className="rounded-lg p-2 text-slate-500 hover:bg-slate-100 dark:text-slate-400 dark:hover:bg-slate-900 transition-colors"
              aria-label="Toggle theme"
            >
              {theme === 'dark' ? <Sun className="h-5 w-5" /> : <Moon className="h-5 w-5" />}
            </button>

            <button className="relative rounded-lg p-2 text-slate-500 hover:bg-slate-100 dark:text-slate-400 dark:hover:bg-slate-900 transition-colors">
              <Bell className="h-5 w-5" />
              <span className="absolute top-1.5 right-1.5 h-2 w-2 rounded-full bg-accent-rose"></span>
            </button>

            <div className="h-6 w-px bg-slate-200 dark:bg-slate-800"></div>

            {isAuthenticated ? (
              <div className="flex items-center gap-4">
                <Link
                  to="/profile"
                  className="flex items-center gap-2 text-sm font-medium text-slate-700 hover:text-slate-900 dark:text-slate-300 dark:hover:text-white"
                >
                  <User className="h-4 w-4" />
                  <span className="hidden sm:inline">Profile</span>
                </Link>
                <button
                  onClick={logout}
                  className="text-xs font-semibold text-slate-500 hover:text-slate-950 dark:hover:text-white transition-colors"
                >
                  Logout
                </button>
              </div>
            ) : (
              <div className="flex items-center gap-3">
                <Link
                  to="/login"
                  className="text-sm font-medium text-slate-600 hover:text-slate-900 dark:text-slate-400 dark:hover:text-white transition-colors"
                >
                  Sign In
                </Link>
                <Link
                  to="/signup"
                  className="px-4 py-2 bg-slate-900 hover:bg-slate-800 dark:bg-white dark:hover:bg-slate-100 text-white dark:text-slate-950 text-xs font-semibold rounded-lg transition-all"
                >
                  Get Started
                </Link>
              </div>
            )}
          </div>
        </div>
      </div>
    </header>
  );
};
export default Navbar;
