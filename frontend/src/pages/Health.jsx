import React, { useState, useEffect } from 'react';
import { ShieldCheck, HeartPulse, Sparkles, Wind, Sun, AlertTriangle } from 'lucide-react';
import api from '../services/api';
import DashboardLayout from '../layouts/DashboardLayout';

export const Health = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadHealthData = async () => {
      try {
        const res = await api.get('/health/');
        setData(res.data);
      } catch (err) {
        console.error('Failed to load health metrics', err);
      } finally {
        setLoading(false);
      }
    };
    loadHealthData();
  }, []);

  if (loading) {
    return (
      <DashboardLayout>
        <div className="flex flex-col items-center justify-center min-h-[60vh] gap-4">
          <div className="w-10 h-10 border-4 border-slate-200 border-t-brand-500 rounded-full animate-spin"></div>
          <span className="text-sm font-medium text-slate-400">Loading Wellness Indices...</span>
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
            <span className="text-xs font-semibold text-brand-500 uppercase tracking-widest">Wellness Indicators</span>
            <h1 className="text-3xl font-display font-bold text-slate-900 dark:text-white mt-1">Health & Air Quality</h1>
          </div>
          <span className="text-xs text-slate-400">Station ID: AQ-DEL98 • Updated 10m ago</span>
        </div>

        {/* Top Info Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {/* AQI Panel */}
          <div className="premium-card relative overflow-hidden">
            <div className="absolute top-0 right-0 h-32 w-32 bg-emerald-500/5 rounded-full blur-3xl"></div>
            <h3 className="text-xs font-semibold uppercase text-slate-400 tracking-wider mb-4">Air Quality Index</h3>
            <div className="flex items-baseline gap-2 mb-3">
              <span className="text-5xl font-display font-bold text-emerald-500">{data?.aqi || 85}</span>
              <span className="text-sm font-medium text-emerald-600 dark:text-emerald-400">{data?.aqi_status || 'Moderate'}</span>
            </div>
            <p className="text-xs text-slate-400 leading-relaxed">
              Air quality is acceptable; however, for some pollutants there may be a moderate health concern for a very small number of people.
            </p>
          </div>

          {/* UV Panel */}
          <div className="premium-card relative overflow-hidden">
            <div className="absolute top-0 right-0 h-32 w-32 bg-accent-amber/5 rounded-full blur-3xl"></div>
            <h3 className="text-xs font-semibold uppercase text-slate-400 tracking-wider mb-4">UV Radiation</h3>
            <div className="flex items-baseline gap-2 mb-3">
              <span className="text-5xl font-display font-bold text-accent-amber">{data?.uv_index || 6.2}</span>
              <span className="text-sm font-medium text-amber-600 dark:text-amber-400">{data?.uv_status || 'High'}</span>
            </div>
            <p className="text-xs text-slate-400 leading-relaxed">
              Protection is essential. Reduce time in the sun between 10 AM and 4 PM. Wear a hat, sunglasses, and SPF 30+ protection.
            </p>
          </div>

          {/* Pollen Panel */}
          <div className="premium-card relative overflow-hidden">
            <h3 className="text-xs font-semibold uppercase text-slate-400 tracking-wider mb-4">Pollen Count</h3>
            <div className="space-y-3">
              {[
                { label: 'Tree Pollen', value: data?.pollen?.tree || 'Moderate', color: 'text-amber-500' },
                { label: 'Grass Pollen', value: data?.pollen?.grass || 'Low', color: 'text-emerald-500' },
                { label: 'Ragweed Pollen', value: data?.pollen?.ragweed || 'Low', color: 'text-emerald-500' },
              ].map((pollen) => (
                <div key={pollen.label} className="flex justify-between items-center text-xs">
                  <span className="font-medium text-slate-500 dark:text-slate-400">{pollen.label}</span>
                  <span className={`font-semibold ${pollen.color}`}>{pollen.value}</span>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Asymmetrical Risks and Suggestions Layout */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
          {/* Wellness Risks: 7 cols */}
          <div className="lg:col-span-7 bg-white dark:bg-slate-900 border border-slate-200/50 dark:border-slate-800/80 rounded-2xl p-6 shadow-premium">
            <h3 className="font-display font-semibold text-slate-900 dark:text-white mb-6 flex items-center gap-2">
              <HeartPulse className="h-5 w-5 text-brand-500" />
              <span>Sensitivity Advisory</span>
            </h3>
            <div className="space-y-6">
              {[
                { condition: 'Asthma Severity', description: data?.wellness_risks?.asthma || 'Moderate risk due to particulate matter', status: 'Moderate' },
                { condition: 'Rheumatoid Joint Pain', description: data?.wellness_risks?.joint_pain || 'Low risk (warm and dry)', status: 'Low' },
                { condition: 'Migraine Trigger Rate', description: data?.wellness_risks?.migraine || 'Low risk', status: 'Low' },
              ].map((risk) => (
                <div key={risk.condition} className="border-b border-slate-100 dark:border-slate-800 pb-4 last:border-0 last:pb-0">
                  <div className="flex justify-between items-center mb-1">
                    <span className="text-sm font-semibold text-slate-800 dark:text-slate-200">{risk.condition}</span>
                    <span className={`text-[10px] uppercase font-bold tracking-wider px-2 py-0.5 rounded ${
                      risk.status === 'Low' ? 'bg-emerald-500/10 text-emerald-500' : 'bg-amber-500/10 text-amber-500'
                    }`}>{risk.status}</span>
                  </div>
                  <p className="text-xs text-slate-400 leading-relaxed">{risk.description}</p>
                </div>
              ))}
            </div>
          </div>

          {/* Actionable Guidelines: 5 cols */}
          <div className="lg:col-span-5 bg-white dark:bg-slate-900 border border-slate-200/50 dark:border-slate-800/80 rounded-2xl p-6 shadow-premium">
            <h3 className="font-display font-semibold text-slate-900 dark:text-white mb-6 flex items-center gap-2">
              <Sparkles className="h-5 w-5 text-brand-500" />
              <span>Recommendations</span>
            </h3>
            <ul className="space-y-4">
              {(data?.recommendations && data.recommendations.length > 0) ? data.recommendations.map((rec, idx) => (
                <li key={idx} className="flex gap-3 text-xs leading-relaxed text-slate-500 dark:text-slate-400">
                  <div className="h-5 w-5 rounded-full bg-brand-500/10 text-brand-500 flex items-center justify-center flex-shrink-0 font-bold text-[10px]">
                    {idx + 1}
                  </div>
                  <span>{rec}</span>
                </li>
              )) : (
                ['Stay hydrated and avoid direct sun during peak hours.', 'Wear sunscreen with SPF 30+ when going outdoors.', 'Use an N95 mask in areas with AQI above 150.'].map((rec, idx) => (
                  <li key={idx} className="flex gap-3 text-xs leading-relaxed text-slate-500 dark:text-slate-400">
                    <div className="h-5 w-5 rounded-full bg-brand-500/10 text-brand-500 flex items-center justify-center flex-shrink-0 font-bold text-[10px]">
                      {idx + 1}
                    </div>
                    <span>{rec}</span>
                  </li>
                ))
              )}
            </ul>
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
};
export default Health;
