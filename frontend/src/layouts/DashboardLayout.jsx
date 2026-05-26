import React from 'react';
import Navbar from '../components/layout/Navbar';

export const DashboardLayout = ({ children }) => {
  return (
    <div className="min-h-screen bg-slate-50 dark:bg-slate-950 text-slate-900 dark:text-slate-100 flex flex-col transition-colors duration-300">
      <Navbar />
      <main className="flex-1 w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {children}
      </main>
      <footer className="border-t border-slate-200/50 dark:border-slate-800/50 py-6 text-center text-xs text-slate-400 dark:text-slate-600 transition-colors">
        © 2026 Aether Weather Platform. All rights reserved.
      </footer>
    </div>
  );
};
export default DashboardLayout;
