import React, { useState, useEffect } from 'react';
import { Play, Pause, RotateCcw, CloudLightning, ShieldAlert, Layers } from 'lucide-react';
import api from '../services/api';
import DashboardLayout from '../layouts/DashboardLayout';

export const Radar = () => {
  const [frames, setFrames] = useState([]);
  const [currentFrameIdx, setCurrentFrameIdx] = useState(0);
  const [isPlaying, setIsPlaying] = useState(false);
  const [loading, setLoading] = useState(true);
  const [layer, setLayer] = useState('precipitation');

  useEffect(() => {
    const fetchRadar = async () => {
      try {
        const res = await api.get(`/radar/frames/?layer=${layer}`);
        setFrames(res.data || []);
      } catch (err) {
        console.error('Failed to load radar timeline', err);
      } finally {
        setLoading(false);
      }
    };
    fetchRadar();
  }, [layer]);

  useEffect(() => {
    let interval = null;
    if (isPlaying && frames.length > 0) {
      interval = setInterval(() => {
        setCurrentFrameIdx((prev) => (prev + 1) % frames.length);
      }, 1000);
    }
    return () => clearInterval(interval);
  }, [isPlaying, frames]);

  if (loading) {
    return (
      <DashboardLayout>
        <div className="flex flex-col items-center justify-center min-h-[60vh] gap-4">
          <div className="w-10 h-10 border-4 border-slate-200 border-t-brand-500 rounded-full animate-spin"></div>
          <span className="text-sm font-medium text-slate-400">Loading Weather Radar Layers...</span>
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
            <span className="text-xs font-semibold text-brand-500 uppercase tracking-widest">Active Radar Timeline</span>
            <h1 className="text-3xl font-display font-bold text-slate-900 dark:text-white mt-1">High-Definition Radar Map</h1>
          </div>
          <div className="flex gap-2">
            <button
              onClick={() => setLayer('precipitation')}
              className={`px-4 py-2 rounded-xl text-xs font-semibold transition-all ${
                layer === 'precipitation'
                  ? 'bg-slate-900 text-white dark:bg-white dark:text-slate-950'
                  : 'bg-slate-100 text-slate-600 dark:bg-slate-900 dark:text-slate-400 hover:opacity-90'
              }`}
            >
              Precipitation
            </button>
            <button
              onClick={() => setLayer('clouds')}
              className={`px-4 py-2 rounded-xl text-xs font-semibold transition-all ${
                layer === 'clouds'
                  ? 'bg-slate-900 text-white dark:bg-white dark:text-slate-950'
                  : 'bg-slate-100 text-slate-600 dark:bg-slate-900 dark:text-slate-400 hover:opacity-90'
              }`}
            >
              Cloud Cover
            </button>
          </div>
        </div>

        {/* Asymmetrical layout: Map on left, stats/controls on right */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
          {/* Radar Viewer: 8 cols */}
          <div className="lg:col-span-8 bg-white dark:bg-slate-900 border border-slate-200/50 dark:border-slate-800/80 rounded-2xl p-4 shadow-premium space-y-4">
            <div className="relative aspect-video w-full rounded-xl overflow-hidden bg-slate-950 flex items-center justify-center border border-slate-200/50 dark:border-slate-800/80">
              {/* Simulated radar visualization mapping lines */}
              <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,rgba(59,130,246,0.1)_0%,transparent_70%)]"></div>
              
              {/* Map coordinate simulation */}
              <div className="absolute inset-0 flex items-center justify-center opacity-30 select-none">
                <div className="h-[90%] w-[90%] border border-dashed border-slate-700 rounded-full"></div>
                <div className="absolute h-[60%] w-[60%] border border-dashed border-slate-700 rounded-full"></div>
                <div className="absolute h-[30%] w-[30%] border border-dashed border-slate-700 rounded-full"></div>
              </div>

              {/* Rain/precip storm mock overlays */}
              <div className="absolute top-[20%] left-[30%] h-32 w-48 rounded-full bg-emerald-500/20 blur-xl animate-pulse"></div>
              <div className="absolute top-[25%] left-[35%] h-24 w-32 rounded-full bg-brand-500/20 blur-xl"></div>
              <div className="absolute top-[28%] left-[38%] h-12 w-16 rounded-full bg-accent-rose/30 blur-md"></div>

              {/* Dynamic Sweep Line representing real sweep sweeps */}
              <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 h-full w-[2px] bg-brand-500/40 origin-center rotate-45 animate-[spin_6s_linear_infinite]"></div>

              {/* Frame HUD metadata */}
              <div className="absolute bottom-4 left-4 p-3 bg-slate-900/90 text-white border border-slate-800 rounded-lg backdrop-blur-md">
                <span className="block text-[10px] text-slate-400 font-bold uppercase tracking-wider">Timestamp</span>
                <span className="text-xs font-semibold">{frames[currentFrameIdx]?.timestamp ? new Date(frames[currentFrameIdx].timestamp).toLocaleString() : 'N/A'}</span>
              </div>
            </div>

            {/* Timeline playback controls */}
            <div className="flex items-center gap-4 bg-slate-50 dark:bg-slate-950 p-4 rounded-xl">
              <button
                onClick={() => setIsPlaying(!isPlaying)}
                className="p-2.5 bg-slate-900 text-white dark:bg-white dark:text-slate-950 rounded-lg hover:opacity-90"
              >
                {isPlaying ? <Pause className="h-4 w-4" /> : <Play className="h-4 w-4" />}
              </button>
              <button
                onClick={() => setCurrentFrameIdx(0)}
                className="p-2.5 bg-slate-100 hover:bg-slate-200 dark:bg-slate-900 text-slate-600 dark:text-slate-400 rounded-lg"
              >
                <RotateCcw className="h-4 w-4" />
              </button>

              <div className="flex-1 flex gap-1">
                {frames.map((frame, idx) => (
                  <button
                    key={idx}
                    onClick={() => {
                      setIsPlaying(false);
                      setCurrentFrameIdx(idx);
                    }}
                    className={`h-2 flex-1 rounded transition-colors ${
                      idx === currentFrameIdx
                        ? 'bg-brand-500'
                        : 'bg-slate-200 dark:bg-slate-800 hover:bg-slate-300 dark:hover:bg-slate-700'
                    }`}
                    title={frame.description}
                  ></button>
                ))}
              </div>
            </div>
          </div>

          {/* Info Sidepanel: 4 cols */}
          <div className="lg:col-span-4 bg-white dark:bg-slate-900 border border-slate-200/50 dark:border-slate-800/80 rounded-2xl p-6 shadow-premium space-y-6">
            <h3 className="font-display font-semibold text-slate-900 dark:text-white mb-4 flex items-center gap-2">
              <Layers className="h-5 w-5 text-brand-500" />
              <span>Map Layer Info</span>
            </h3>

            <div className="space-y-4">
              <div className="p-3 bg-slate-50 dark:bg-slate-950 rounded-xl">
                <span className="block text-xs font-semibold">Precipitation Reflection</span>
                <p className="text-xs text-slate-400 mt-1">Shows active rainfall, snow, or thunderstorm locations. The color spectrum ranges from emerald (light rain) to rose (heavy hail).</p>
              </div>
              <div className="p-3 bg-slate-50 dark:bg-slate-950 rounded-xl">
                <span className="block text-xs font-semibold">Update Frequency</span>
                <p className="text-xs text-slate-400 mt-1">Radar metrics are parsed from local meteorological Doppler radar stations and update at 10-minute intervals.</p>
              </div>
            </div>

            <div className="p-4 rounded-xl bg-accent-amber/10 border border-accent-amber/20 text-accent-amber flex gap-3 text-xs leading-relaxed">
              <CloudLightning className="h-5 w-5 flex-shrink-0" />
              <div>
                <span className="font-bold block uppercase tracking-wider mb-1">Doppler Alert</span>
                <span>Localized cells indicate thunderstorm development 45km northwest of current station coordinates.</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
};
export default Radar;
