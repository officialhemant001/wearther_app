import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { ArrowRight, Wind, Droplets, Thermometer, CloudRain, Shield, Sparkles, Compass } from 'lucide-react';
import { motion } from 'framer-motion';

export const Landing = () => {
  const [searchQuery, setSearchQuery] = useState('');

  return (
    <div className="min-h-screen bg-slate-50 dark:bg-slate-950 text-slate-900 dark:text-slate-100 transition-colors duration-300 overflow-x-hidden">
      {/* Dynamic Sub-header Banner */}
      <div className="bg-slate-900 text-white dark:bg-slate-900/40 text-center py-2.5 px-4 text-xs font-medium tracking-wide flex items-center justify-center gap-2 border-b border-slate-800">
        <span className="inline-flex items-center gap-1 rounded bg-brand-500/20 px-1.5 py-0.5 text-[10px] font-semibold text-brand-400 uppercase">New</span>
        <span>Aether AI 1.2 is now active for hyperlocal forecasts</span>
        <ArrowRight className="h-3.5 w-3.5" />
      </div>

      {/* Hero Section */}
      <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-20 pb-16 md:pt-32 md:pb-24">
        {/* Asymmetrical decorative background element */}
        <div className="absolute top-1/4 left-1/2 -z-10 h-[400px] w-[600px] -translate-x-1/2 -translate-y-1/2 rounded-full bg-brand-500/5 blur-[120px] dark:bg-brand-500/10"></div>

        <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 lg:gap-8 items-center">
          <div className="lg:col-span-7 flex flex-col items-start text-left">
            <motion.div
              initial={{ opacity: 0, y: 15 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6 }}
              className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full border border-slate-200 dark:border-slate-800 bg-white/50 dark:bg-slate-900/50 backdrop-blur-sm text-xs font-semibold text-slate-600 dark:text-slate-300 mb-6"
            >
              <Sparkles className="h-3.5 w-3.5 text-brand-500" />
              <span>Next Generation Weather Intelligence</span>
            </motion.div>

            <motion.h1
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.7, delay: 0.1 }}
              className="text-4xl sm:text-5xl md:text-6xl font-display font-bold text-slate-900 dark:text-white leading-[1.05] tracking-tight mb-6"
            >
              Weather, <br />
              <span className="text-brand-500">beautifully resolved</span>.
            </motion.h1>

            <motion.p
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.7, delay: 0.2 }}
              className="text-base sm:text-lg text-slate-500 dark:text-slate-400 max-w-xl mb-8 leading-relaxed"
            >
              A professional meteorological platform delivering hyperlocal precision, customized alert rule evaluation, real-time radar mapping, and AI-powered agricultural insight.
            </motion.p>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.7, delay: 0.3 }}
              className="w-full max-w-md flex flex-col sm:flex-row gap-3 mb-4"
            >
              <div className="relative flex-1">
                <input
                  type="text"
                  placeholder="Enter location (e.g. London, Paris...)"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="w-full px-4 py-3 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl focus:outline-none focus:border-brand-500 focus:ring-2 focus:ring-brand-500/10 transition-all text-sm text-slate-800 dark:text-white shadow-premium"
                />
              </div>
              <Link
                to={`/dashboard?city=${encodeURIComponent(searchQuery || 'New Delhi')}`}
                className="px-6 py-3 bg-slate-900 hover:bg-slate-800 dark:bg-white dark:hover:bg-slate-100 text-white dark:text-slate-900 font-semibold text-sm rounded-xl transition-all shadow-lg flex items-center justify-center gap-2 whitespace-nowrap"
              >
                <span>Check Weather</span>
                <ArrowRight className="h-4 w-4" />
              </Link>
            </motion.div>
            <span className="text-xs text-slate-400 dark:text-slate-500">No login required for general queries.</span>
          </div>

          {/* Right Live Weather Widget Mockup (Asymmetrical Balance) */}
          <div className="lg:col-span-5 relative">
            <motion.div
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.8, delay: 0.2 }}
              className="premium-card relative bg-white/70 dark:bg-slate-900/60 backdrop-blur-xl border border-slate-200/50 dark:border-slate-800/80 shadow-premium"
            >
              {/* Widget Header */}
              <div className="flex items-center justify-between border-b border-slate-100 dark:border-slate-800 pb-4 mb-6">
                <div>
                  <h3 className="font-display font-semibold text-slate-900 dark:text-white">New Delhi</h3>
                  <span className="text-xs text-slate-400">Live Telemetry • 2 mins ago</span>
                </div>
                <span className="px-2.5 py-1 rounded-full bg-emerald-500/10 text-emerald-500 dark:text-emerald-400 text-xs font-medium">Optimal AQI</span>
              </div>

              {/* Main Temp Row */}
              <div className="flex items-baseline gap-2 mb-6">
                <span className="text-5xl sm:text-6xl font-display font-bold tracking-tighter text-slate-900 dark:text-white">32.5°</span>
                <span className="text-lg text-slate-400 dark:text-slate-500">C</span>
                <span className="ml-auto text-sm font-medium text-slate-600 dark:text-slate-300">Scattered Clouds</span>
              </div>

              {/* Grid of Micro-telemetry */}
              <div className="grid grid-cols-3 gap-4 border-t border-slate-100 dark:border-slate-800 pt-6">
                <div className="flex flex-col">
                  <span className="text-xs text-slate-400 mb-1 flex items-center gap-1"><Wind className="h-3.5 w-3.5" /> Wind</span>
                  <span className="text-sm font-semibold">3.5 m/s</span>
                </div>
                <div className="flex flex-col">
                  <span className="text-xs text-slate-400 mb-1 flex items-center gap-1"><Droplets className="h-3.5 w-3.5" /> Humidity</span>
                  <span className="text-sm font-semibold">65%</span>
                </div>
                <div className="flex flex-col">
                  <span className="text-xs text-slate-400 mb-1 flex items-center gap-1"><Thermometer className="h-3.5 w-3.5" /> UV Index</span>
                  <span className="text-sm font-semibold">8.5 High</span>
                </div>
              </div>
            </motion.div>
          </div>
        </div>
      </div>

      {/* Feature Section with Clean Spacing & High Spacing Balance */}
      <div className="py-24 border-t border-slate-200/50 dark:border-slate-800/50 bg-slate-100/30 dark:bg-slate-950/20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center max-w-3xl mx-auto mb-20">
            <h2 className="text-3xl font-display font-bold tracking-tight text-slate-900 dark:text-white mb-4">Precision-engineered features for absolute reliability.</h2>
            <p className="text-slate-500 dark:text-slate-400 text-sm sm:text-base leading-relaxed">
              Every detail is calibrated to load in milliseconds, deliver readable visual indicators, and offer high-end agricultural analytics.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="premium-card flex flex-col items-start">
              <div className="p-3 bg-brand-500/10 text-brand-500 rounded-xl mb-6">
                <Compass className="h-6 w-6" />
              </div>
              <h3 className="font-display font-semibold text-slate-900 dark:text-white text-lg mb-2">Hyperlocal Precision</h3>
              <p className="text-slate-500 dark:text-slate-400 text-sm leading-relaxed">
                Utilizes high-resolution sensor nodes and direct satellite feeds to compute local conditions within a 500-meter radius.
              </p>
            </div>

            <div className="premium-card flex flex-col items-start">
              <div className="p-3 bg-accent-indigo/10 text-accent-indigo rounded-xl mb-6">
                <Sparkles className="h-6 w-6" />
              </div>
              <h3 className="font-display font-semibold text-slate-900 dark:text-white text-lg mb-2">Aether AI Insights</h3>
              <p className="text-slate-500 dark:text-slate-400 text-sm leading-relaxed">
                A custom generative AI model that parses meteorological patterns and converts raw indices into activity and safety guidelines.
              </p>
            </div>

            <div className="premium-card flex flex-col items-start">
              <div className="p-3 bg-accent-emerald/10 text-accent-emerald rounded-xl mb-6">
                <Shield className="h-6 w-6" />
              </div>
              <h3 className="font-display font-semibold text-slate-900 dark:text-white text-lg mb-2">Smart Alert Rules</h3>
              <p className="text-slate-500 dark:text-slate-400 text-sm leading-relaxed">
                Configure your own trigger conditions (e.g. if temperature is above 35°C or rain chance is below 10%) to receive instant updates.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
export default Landing;
