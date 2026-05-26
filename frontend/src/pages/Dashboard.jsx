import React, { useState, useEffect } from 'react';
import { useLocation, Link } from 'react-router-dom';
import { Wind, Droplets, Thermometer, Sun, CloudRain, ShieldAlert, Sparkles, MapPin, Eye, Compass, ArrowRight } from 'lucide-react';
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';
import api from '../services/api';
import DashboardLayout from '../layouts/DashboardLayout';

export const Dashboard = () => {
  const routerLocation = useLocation();
  const searchParams = new URLSearchParams(routerLocation.search);
  const cityQuery = searchParams.get('city') || 'New Delhi';

  const [loading, setLoading] = useState(true);
  const [weatherData, setWeatherData] = useState(null);
  const [airQuality, setAirQuality] = useState(null);
  const [recommendations, setRecommendations] = useState([]);
  const [savedCities, setSavedCities] = useState([]);
  const [newCity, setNewCity] = useState('');

  // Forecast charts dummy data (represents temperature fluctuation over 24h)
  const chartData = [
    { time: '06:00', temp: 24 },
    { time: '09:00', temp: 28 },
    { time: '12:00', temp: 32 },
    { time: '15:00', temp: 35 },
    { time: '18:00', temp: 31 },
    { time: '21:00', temp: 27 },
    { time: '00:00', temp: 25 },
  ];

  useEffect(() => {
    const loadDashboardData = async () => {
      setLoading(true);
      try {
        // Fetch current weather via API
        const weatherRes = await api.get(`/weather/hyperlocal/?city=${cityQuery}`);
        setWeatherData(weatherRes.data.weather);
        setAirQuality(weatherRes.data.air_quality);

        // Fetch recommendations
        const recsRes = await api.get('/recommendations/');
        setRecommendations(recsRes.data.activities || []);

        // Load saved locations mock list
        setSavedCities(['London', 'Mumbai', 'Tokyo']);
      } catch (err) {
        console.error('Failed to load telemetry', err);
      } finally {
        setLoading(false);
      }
    };

    loadDashboardData();
  }, [cityQuery]);

  const handleSaveCity = () => {
    if (newCity && !savedCities.includes(newCity)) {
      setSavedCities([...savedCities, newCity]);
      setNewCity('');
    }
  };

  if (loading) {
    return (
      <DashboardLayout>
        <div className="flex flex-col items-center justify-center min-h-[60vh] gap-4">
          <div className="w-10 h-10 border-4 border-slate-200 border-t-brand-500 rounded-full animate-spin"></div>
          <span className="text-sm font-medium text-slate-400">Loading Meteorological Data...</span>
        </div>
      </DashboardLayout>
    );
  }

  return (
    <DashboardLayout>
      <div className="space-y-8">
        {/* Dynamic Alert Banner */}
        <div className="p-4 rounded-xl bg-accent-amber/10 border border-accent-amber/20 text-accent-amber flex items-center justify-between gap-4">
          <div className="flex items-center gap-2">
            <ShieldAlert className="h-5 w-5 flex-shrink-0" />
            <span className="text-xs font-semibold uppercase tracking-wider">Alert</span>
            <span className="text-xs font-medium">Elevated UV Index expected between 11:00 and 14:00. Protective layers recommended.</span>
          </div>
          <button className="text-xs font-bold underline hover:text-amber-600">Dismiss</button>
        </div>

        {/* Main Grid: Asymmetrical Layout */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
          {/* Main Weather Telemetry: 8 cols */}
          <div className="lg:col-span-8 space-y-8">
            <div className="bg-white dark:bg-slate-900 border border-slate-200/50 dark:border-slate-800/80 rounded-2xl p-8 relative overflow-hidden shadow-premium">
              {/* Card Background Blur Accent */}
              <div className="absolute top-0 right-0 h-48 w-48 bg-brand-500/5 rounded-full blur-[80px]"></div>

              {/* Location metadata */}
              <div className="flex items-center justify-between mb-8">
                <div className="flex items-center gap-2">
                  <MapPin className="h-4 w-4 text-brand-500" />
                  <h1 className="text-2xl font-display font-bold text-slate-900 dark:text-white">
                    {weatherData?.location_name || cityQuery}
                  </h1>
                </div>
                <span className="text-xs text-slate-400 font-semibold uppercase tracking-wider">Live Telemetry</span>
              </div>

              {/* Primary Weather Values */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-8 items-end">
                <div className="space-y-4">
                  <div className="flex items-baseline gap-2">
                    <span className="text-7xl font-display font-bold tracking-tighter text-slate-900 dark:text-white">
                      {weatherData?.temperature || 32.5}
                    </span>
                    <span className="text-2xl text-slate-400">°C</span>
                  </div>
                  <div>
                    <span className="text-base font-semibold text-slate-800 dark:text-slate-200">
                      {weatherData?.weather_main || 'Scattered Clouds'}
                    </span>
                    <p className="text-xs text-slate-400 mt-1 capitalize">
                      Feels like {weatherData?.feels_like || 35}°C • {weatherData?.weather_description || 'scattered clouds'}
                    </p>
                  </div>
                </div>

                {/* Micro-telemetry columns */}
                <div className="grid grid-cols-2 gap-4">
                  <div className="p-3 bg-slate-50 dark:bg-slate-950 rounded-xl flex items-center gap-3">
                    <Wind className="h-5 w-5 text-brand-500" />
                    <div>
                      <span className="block text-[10px] text-slate-400 uppercase font-bold">Wind</span>
                      <span className="text-sm font-semibold">{weatherData?.wind_speed || 3.5} m/s</span>
                    </div>
                  </div>
                  <div className="p-3 bg-slate-50 dark:bg-slate-950 rounded-xl flex items-center gap-3">
                    <Droplets className="h-5 w-5 text-brand-500" />
                    <div>
                      <span className="block text-[10px] text-slate-400 uppercase font-bold">Humidity</span>
                      <span className="text-sm font-semibold">{weatherData?.humidity || 65}%</span>
                    </div>
                  </div>
                  <div className="p-3 bg-slate-50 dark:bg-slate-950 rounded-xl flex items-center gap-3">
                    <Thermometer className="h-5 w-5 text-brand-500" />
                    <div>
                      <span className="block text-[10px] text-slate-400 uppercase font-bold">UV Index</span>
                      <span className="text-sm font-semibold">{weatherData?.uv_index || 8.5}</span>
                    </div>
                  </div>
                  <div className="p-3 bg-slate-50 dark:bg-slate-950 rounded-xl flex items-center gap-3">
                    <Eye className="h-5 w-5 text-brand-500" />
                    <div>
                      <span className="block text-[10px] text-slate-400 uppercase font-bold">Visibility</span>
                      <span className="text-sm font-semibold">{(weatherData?.visibility || 10000) / 1000} km</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* Visual Temperature Trend Curve */}
            <div className="bg-white dark:bg-slate-900 border border-slate-200/50 dark:border-slate-800/80 rounded-2xl p-6 shadow-premium">
              <h3 className="font-display font-semibold text-slate-900 dark:text-white mb-6">24-Hour Temperature Curve</h3>
              <div className="h-[200px] w-full">
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={chartData}>
                    <XAxis dataKey="time" stroke="#64748b" fontSize={11} tickLine={false} axisLine={false} />
                    <YAxis stroke="#64748b" fontSize={11} tickLine={false} axisLine={false} domain={['auto', 'auto']} />
                    <Tooltip contentStyle={{ background: '#0f172a', border: 'none', borderRadius: '8px', color: '#fff', fontSize: '12px' }} />
                    <Line type="monotone" dataKey="temp" stroke="#3b82f6" strokeWidth={2.5} dot={{ fill: '#3b82f6', r: 4 }} activeDot={{ r: 6 }} />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            </div>
          </div>

          {/* Location sidebar & Quick Controls: 4 cols */}
          <div className="lg:col-span-4 space-y-8">
            {/* Air Quality (AQI) Metric panel */}
            <div className="bg-white dark:bg-slate-900 border border-slate-200/50 dark:border-slate-800/80 rounded-2xl p-6 shadow-premium flex flex-col justify-between">
              <div>
                <h3 className="font-display font-semibold text-slate-900 dark:text-white mb-4">Air Quality Index</h3>
                <div className="flex items-center gap-4">
                  <div className="relative flex items-center justify-center">
                    {/* Circle display representing AQI state */}
                    <div className="h-16 w-16 rounded-full border-4 border-emerald-500/20 border-t-emerald-500 flex items-center justify-center font-display font-bold text-lg text-emerald-500">
                      {airQuality?.pm2_5 || 35}
                    </div>
                  </div>
                  <div>
                    <span className="text-sm font-semibold text-slate-800 dark:text-slate-200">
                      {airQuality?.aqi_label || 'Moderate'}
                    </span>
                    <p className="text-xs text-slate-400 mt-1">PM2.5 concentration is within safe metrics for healthy adults.</p>
                  </div>
                </div>
              </div>
            </div>

            {/* Saved Locations List */}
            <div className="bg-white dark:bg-slate-900 border border-slate-200/50 dark:border-slate-800/80 rounded-2xl p-6 shadow-premium">
              <h3 className="font-display font-semibold text-slate-900 dark:text-white mb-4">Saved Locations</h3>
              <div className="space-y-3 mb-4">
                {savedCities.map((city) => (
                  <div key={city} className="flex items-center justify-between p-3 bg-slate-50 dark:bg-slate-950 rounded-xl hover:bg-slate-100 dark:hover:bg-slate-900 transition-colors">
                    <span className="text-sm font-medium">{city}</span>
                    <button
                      onClick={() => window.location.search = `?city=${city}`}
                      className="text-xs font-semibold text-brand-500 hover:text-brand-400 flex items-center gap-1"
                    >
                      <span>View</span>
                      <ArrowRight className="h-3 w-3" />
                    </button>
                  </div>
                ))}
              </div>
              <div className="flex gap-2">
                <input
                  type="text"
                  placeholder="Add location..."
                  value={newCity}
                  onChange={(e) => setNewCity(e.target.value)}
                  className="flex-1 px-3 py-2 bg-slate-100/50 dark:bg-slate-950 border border-slate-200/60 dark:border-slate-800 rounded-lg text-xs focus:outline-none focus:border-brand-500"
                />
                <button
                  onClick={handleSaveCity}
                  className="px-4 py-2 bg-slate-900 dark:bg-white text-white dark:text-slate-900 rounded-lg text-xs font-semibold hover:opacity-90"
                >
                  Save
                </button>
              </div>
            </div>

            {/* AI Assistant Quick Access */}
            <div className="bg-white dark:bg-slate-900 border border-slate-200/50 dark:border-slate-800/80 rounded-2xl p-6 shadow-premium">
              <div className="flex items-center gap-2 mb-3">
                <Sparkles className="h-5 w-5 text-brand-500" />
                <h3 className="font-display font-semibold text-slate-900 dark:text-white">Aether AI Insights</h3>
              </div>
              <p className="text-xs text-slate-400 mb-4 leading-relaxed">
                Need weather advice for traveling, wedding planning, or harvesting crops? Ask our neural assistant.
              </p>
              <Link
                to="/assistant"
                className="w-full py-2.5 bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700/80 rounded-xl text-xs font-semibold flex items-center justify-center gap-2 text-slate-700 dark:text-slate-200 transition-colors"
              >
                <span>Launch Assistant</span>
                <ArrowRight className="h-3.5 w-3.5" />
              </Link>
            </div>
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
};
export default Dashboard;
