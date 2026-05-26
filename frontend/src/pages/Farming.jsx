import React, { useState, useEffect } from 'react';
import { Shovel, Sparkles, Wind, Droplets, Thermometer, AlertCircle } from 'lucide-react';
import api from '../services/api';
import DashboardLayout from '../layouts/DashboardLayout';

export const Farming = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadFarmingData = async () => {
      try {
        const res = await api.get('/farming/');
        setData(res.data);
      } catch (err) {
        console.error('Failed to load farming metadata', err);
      } finally {
        setLoading(false);
      }
    };
    loadFarmingData();
  }, []);

  if (loading) {
    return (
      <DashboardLayout>
        <div className="flex flex-col items-center justify-center min-h-[60vh] gap-4">
          <div className="w-10 h-10 border-4 border-slate-200 border-t-brand-500 rounded-full animate-spin"></div>
          <span className="text-sm font-medium text-slate-400">Loading Soil & Agricultural Data...</span>
        </div>
      </DashboardLayout>
    );
  }

  return (
    <DashboardLayout>
      <div className="space-y-8">
        {/* Header */}
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-200/50 dark:border-slate-800/50 pb-6">
          <div>
            <span className="text-xs font-semibold text-brand-500 uppercase tracking-widest">Agricultural Systems</span>
            <h1 className="text-3xl font-display font-bold text-slate-900 dark:text-white mt-1">Farming Weather Portal</h1>
          </div>
          <span className="text-xs text-slate-400">Calculated for New Delhi Coordinates • Updated hourly</span>
        </div>

        {/* Soil properties grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="premium-card">
            <h3 className="text-xs font-semibold uppercase text-slate-400 tracking-wider mb-4 flex items-center gap-1.5">
              <Thermometer className="h-4 w-4" /> Soil Temperature
            </h3>
            <div className="flex items-baseline gap-1 mb-2">
              <span className="text-4xl font-display font-bold text-slate-900 dark:text-white">
                {data?.soil?.temperature || 24.2}
              </span>
              <span className="text-sm text-slate-400">°C</span>
            </div>
            <span className="text-xs text-slate-400 font-medium">Recorded at 10cm depth</span>
          </div>

          <div className="premium-card">
            <h3 className="text-xs font-semibold uppercase text-slate-400 tracking-wider mb-4 flex items-center gap-1.5">
              <Droplets className="h-4 w-4" /> Soil Moisture
            </h3>
            <div className="flex items-baseline gap-1 mb-2">
              <span className="text-4xl font-display font-bold text-brand-500">
                {data?.soil?.moisture_percentage || 58}%
              </span>
              <span className="text-xs font-semibold uppercase px-2 py-0.5 rounded bg-brand-500/10 text-brand-500 dark:text-brand-400 ml-2">
                Optimal
              </span>
            </div>
            <span className="text-xs text-slate-400 font-medium">{data?.soil?.status}</span>
          </div>

          <div className="premium-card">
            <h3 className="text-xs font-semibold uppercase text-slate-400 tracking-wider mb-4 flex items-center gap-1.5">
              <Wind className="h-4 w-4" /> Evapotranspiration
            </h3>
            <div className="flex items-baseline gap-1 mb-2">
              <span className="text-4xl font-display font-bold text-slate-900 dark:text-white">
                {data?.evapotranspiration_rate || '3.2'}
              </span>
              <span className="text-sm text-slate-400">mm/day</span>
            </div>
            <span className="text-xs text-slate-400 font-medium">Daily water evaporation rate</span>
          </div>
        </div>

        {/* Advisory and Spray Condition Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
          {/* Crop Advisories: 7 cols */}
          <div className="lg:col-span-7 bg-white dark:bg-slate-900 border border-slate-200/50 dark:border-slate-800/80 rounded-2xl p-6 shadow-premium">
            <h3 className="font-display font-semibold text-slate-900 dark:text-white mb-6 flex items-center gap-2">
              <Shovel className="h-5 w-5 text-brand-500" />
              <span>Crop Advisory Reports</span>
            </h3>
            <div className="space-y-6">
              {data?.crop_advisories?.map((item) => (
                <div key={item.crop} className="border-b border-slate-100 dark:border-slate-800 pb-4 last:border-0 last:pb-0">
                  <div className="flex justify-between items-baseline mb-2">
                    <span className="text-sm font-semibold text-slate-900 dark:text-white">{item.crop}</span>
                    <span className="text-xs text-slate-400 font-medium">{item.stage}</span>
                  </div>
                  <p className="text-xs text-slate-500 dark:text-slate-400 leading-relaxed">{item.advisory}</p>
                </div>
              ))}
            </div>
          </div>

          {/* Spraying conditions: 5 cols */}
          <div className="lg:col-span-5 bg-white dark:bg-slate-900 border border-slate-200/50 dark:border-slate-800/80 rounded-2xl p-6 shadow-premium">
            <h3 className="font-display font-semibold text-slate-900 dark:text-white mb-4 flex items-center gap-2">
              <Wind className="h-5 w-5 text-brand-500" />
              <span>Spraying Conditions</span>
            </h3>
            <div className="p-4 rounded-xl bg-emerald-500/10 border border-emerald-500/20 text-emerald-600 dark:text-emerald-400 mb-4 flex gap-3">
              <AlertCircle className="h-5 w-5 flex-shrink-0" />
              <div>
                <span className="block text-xs font-bold uppercase tracking-wider mb-1">Status: {data?.spraying_conditions?.status}</span>
                <p className="text-xs">{data?.spraying_conditions?.reason}</p>
              </div>
            </div>
            <p className="text-xs text-slate-400 leading-relaxed">
              Ideal wind speeds for spraying are between 3-10 km/h. High winds cause drift risk, while absolute calm indicates thermal inversion trapping chemicals.
            </p>
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
};
export default Farming;
