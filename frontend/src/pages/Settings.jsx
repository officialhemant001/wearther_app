import React, { useState, useEffect } from 'react';
import { Settings as SettingsIcon, Bell, Shield, Sliders, Moon, Sun, Monitor, HelpCircle } from 'lucide-react';
import { useTheme } from '../context/ThemeContext';
import api from '../services/api';
import DashboardLayout from '../layouts/DashboardLayout';

export const Settings = () => {
  const { theme, toggleTheme } = useTheme();
  
  const [tempUnit, setTempUnit] = useState('celsius');
  const [notifications, setNotifications] = useState({
    push: true,
    email: true,
    sms: false,
    aqiAlerts: true,
  });
  const [saving, setSaving] = useState(false);
  const [savedMessage, setSavedMessage] = useState('');

  useEffect(() => {
    const fetchSettings = async () => {
      try {
        const res = await api.get('/users/settings/');
        if (res.data) {
          setTempUnit(res.data.temperature_unit || 'celsius');
          setNotifications({
            push: res.data.push_notifications ?? true,
            email: res.data.email_notifications ?? true,
            sms: res.data.sms_notifications ?? false,
            aqiAlerts: res.data.aqi_alerts_enabled ?? true,
          });
        }
      } catch (err) {
        console.error('Failed to load user preferences', err);
      }
    };
    fetchSettings();
  }, []);

  const handleSave = async () => {
    setSaving(true);
    setSavedMessage('');
    try {
      await api.put('/users/settings/', {
        temperature_unit: tempUnit,
        push_notifications: notifications.push,
        email_notifications: notifications.email,
        sms_notifications: notifications.sms,
        aqi_alerts_enabled: notifications.aqiAlerts,
      });
      setSavedMessage('Settings updated successfully.');
    } catch (err) {
      console.error('Failed to save settings', err);
      setSavedMessage('Failed to update settings.');
    } finally {
      setSaving(false);
    }
  };

  return (
    <DashboardLayout>
      <div className="space-y-8">
        {/* Header */}
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-200/50 dark:border-slate-800/50 pb-6">
          <div>
            <span className="text-xs font-semibold text-brand-500 uppercase tracking-widest">Preferences</span>
            <h1 className="text-3xl font-display font-bold text-slate-900 dark:text-white mt-1">Platform Settings</h1>
          </div>
        </div>

        {/* Setting grids */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
          {/* Main settings panel: 8 cols */}
          <div className="lg:col-span-8 bg-white dark:bg-slate-900 border border-slate-200/50 dark:border-slate-800/80 rounded-2xl p-6 shadow-premium space-y-8">
            
            {savedMessage && (
              <div className="p-4 rounded-xl bg-brand-500/10 border border-brand-500/20 text-brand-500 text-xs font-semibold">
                {savedMessage}
              </div>
            )}

            {/* Display & theme */}
            <div className="space-y-4">
              <h3 className="text-sm font-semibold uppercase text-slate-400 tracking-wider flex items-center gap-1.5 pb-2 border-b border-slate-100 dark:border-slate-800">
                <Sliders className="h-4 w-4" /> Preferences
              </h3>
              
              <div className="flex flex-col sm:flex-row justify-between sm:items-center gap-4">
                <div>
                  <span className="text-sm font-semibold text-slate-900 dark:text-white">Temperature Unit</span>
                  <p className="text-xs text-slate-400 mt-0.5">Toggle default unit for weather parameters throughout the application.</p>
                </div>
                <div className="flex gap-2">
                  {['celsius', 'fahrenheit'].map((unit) => (
                    <button
                      key={unit}
                      onClick={() => setTempUnit(unit)}
                      className={`px-4 py-2 rounded-xl text-xs font-semibold capitalize transition-all ${
                        tempUnit === unit
                          ? 'bg-slate-900 text-white dark:bg-white dark:text-slate-950'
                          : 'bg-slate-100 text-slate-600 dark:bg-slate-800 dark:text-slate-400 hover:opacity-90'
                      }`}
                    >
                      {unit}
                    </button>
                  ))}
                </div>
              </div>

              <div className="flex justify-between items-center pt-4">
                <div>
                  <span className="text-sm font-semibold text-slate-900 dark:text-white">Interface Theme</span>
                  <p className="text-xs text-slate-400 mt-0.5">Switch active theme between light and dark palettes.</p>
                </div>
                <button
                  onClick={toggleTheme}
                  className="px-4 py-2 bg-slate-100 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-xs font-semibold rounded-xl flex items-center gap-2 hover:bg-slate-200 transition-colors"
                >
                  {theme === 'dark' ? <Sun className="h-4 w-4 text-accent-amber" /> : <Moon className="h-4 w-4 text-brand-500" />}
                  <span>{theme === 'dark' ? 'Light Mode' : 'Dark Mode'}</span>
                </button>
              </div>
            </div>

            {/* Notification triggers */}
            <div className="space-y-4">
              <h3 className="text-sm font-semibold uppercase text-slate-400 tracking-wider flex items-center gap-1.5 pb-2 border-b border-slate-100 dark:border-slate-800">
                <Bell className="h-4 w-4" /> Notification Preferences
              </h3>

              {[
                { key: 'push', label: 'Push Notifications', desc: 'Receive instant notifications regarding emergency weather alerts on this browser session.' },
                { key: 'email', label: 'Email Advisories', desc: 'Receive weekly agricultural analysis digests and severe warning alerts in your inbox.' },
                { key: 'aqiAlerts', label: 'AQI Warning Alerts', desc: 'Trigger warnings if PM2.5 or PM10 counts exceed safe limits.' },
              ].map((item) => (
                <div key={item.key} className="flex items-start justify-between gap-4 py-2">
                  <div className="max-w-xl">
                    <span className="text-sm font-semibold text-slate-900 dark:text-white">{item.label}</span>
                    <p className="text-xs text-slate-400 mt-0.5">{item.desc}</p>
                  </div>
                  <button
                    onClick={() => setNotifications({ ...notifications, [item.key]: !notifications[item.key] })}
                    className={`relative inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 focus:outline-none ${
                      notifications[item.key] ? 'bg-brand-500' : 'bg-slate-200 dark:bg-slate-800'
                    }`}
                  >
                    <span className={`pointer-events-none inline-block h-5 w-5 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out ${
                      notifications[item.key] ? 'translate-x-5' : 'translate-x-0'
                    }`}></span>
                  </button>
                </div>
              ))}
            </div>

            <div className="pt-4 border-t border-slate-100 dark:border-slate-800 flex justify-end">
              <button
                onClick={handleSave}
                disabled={saving}
                className="premium-btn-primary disabled:opacity-50"
              >
                {saving ? 'Saving...' : 'Save Settings'}
              </button>
            </div>

          </div>

          {/* Settings Sidepanel: 4 cols */}
          <div className="lg:col-span-4 bg-white dark:bg-slate-900 border border-slate-200/50 dark:border-slate-800/80 rounded-2xl p-6 shadow-premium space-y-6">
            <h3 className="font-display font-semibold text-slate-900 dark:text-white mb-4 flex items-center gap-2">
              <Shield className="h-5 w-5 text-brand-500" />
              <span>Premium Tier benefits</span>
            </h3>
            
            <p className="text-xs text-slate-400 leading-relaxed">
              Unlock historical weather reports, advanced agricultural advisories for multiple crop categories, unlimited custom warning rules, and hourly AI dialog replies.
            </p>

            <button
              onClick={() => alert('Premium billing triggers. Stripe configurations require active secure payment tokens.')}
              className="w-full py-2.5 bg-slate-900 text-white dark:bg-white dark:text-slate-950 font-semibold rounded-xl text-xs hover:opacity-90 transition-all flex items-center justify-center gap-2"
            >
              <span>Manage Premium Subscription</span>
            </button>
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
};
export default Settings;
