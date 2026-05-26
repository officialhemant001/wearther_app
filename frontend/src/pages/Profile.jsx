import React, { useState, useEffect } from 'react';
import { User, ShieldCheck, Mail, Phone, Laptop, Trash2, ShieldAlert } from 'lucide-react';
import api from '../services/api';
import DashboardLayout from '../layouts/DashboardLayout';

export const Profile = () => {
  const [profile, setProfile] = useState(null);
  const [devices, setDevices] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadProfileData = async () => {
      try {
        const profileRes = await api.get('/users/profile/');
        setProfile(profileRes.data || {});

        const devicesRes = await api.get('/users/devices/');
        setDevices(devicesRes.data || []);
      } catch (err) {
        console.error('Failed to load profile details', err);
      } finally {
        setLoading(false);
      }
    };
    loadProfileData();
  }, []);

  const handleRevokeDevice = async (id) => {
    try {
      await api.delete(`/users/devices/${id}/`);
      setDevices(devices.filter((device) => device.id !== id));
    } catch (err) {
      console.error('Failed to revoke device session', err);
    }
  };

  if (loading) {
    return (
      <DashboardLayout>
        <div className="flex flex-col items-center justify-center min-h-[60vh] gap-4">
          <div className="w-10 h-10 border-4 border-slate-200 border-t-brand-500 rounded-full animate-spin"></div>
          <span className="text-sm font-medium text-slate-400">Loading User Profile...</span>
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
            <span className="text-xs font-semibold text-brand-500 uppercase tracking-widest">Account Manager</span>
            <h1 className="text-3xl font-display font-bold text-slate-900 dark:text-white mt-1">User Profile</h1>
          </div>
        </div>

        {/* Asymmetrical layout: Profile details on left, device list on right */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
          
          {/* Profile details: 7 cols */}
          <div className="lg:col-span-7 bg-white dark:bg-slate-900 border border-slate-200/50 dark:border-slate-800/80 rounded-2xl p-6 shadow-premium space-y-6">
            <h3 className="font-display font-semibold text-slate-900 dark:text-white flex items-center gap-2 pb-3 border-b border-slate-100 dark:border-slate-800">
              <User className="h-5 w-5 text-brand-500" />
              <span>Personal Details</span>
            </h3>

            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Username</span>
                <span className="text-sm font-medium">{profile?.username}</span>
              </div>
              
              <div className="flex items-center justify-between">
                <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Email Address</span>
                <span className="text-sm font-medium flex items-center gap-1.5">
                  <Mail className="h-4 w-4 text-slate-400" />
                  <span>{profile?.email}</span>
                  {profile?.is_email_verified && <ShieldCheck className="h-4 w-4 text-emerald-500" />}
                </span>
              </div>

              <div className="flex items-center justify-between">
                <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Phone Number</span>
                <span className="text-sm font-medium flex items-center gap-1.5">
                  <Phone className="h-4 w-4 text-slate-400" />
                  <span>{profile?.phone_number || 'Not Linked'}</span>
                </span>
              </div>

              <div className="flex items-center justify-between">
                <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Billing Tier</span>
                <span className={`text-xs font-bold px-2.5 py-1 rounded-full uppercase tracking-wider ${
                  profile?.profile?.is_premium ? 'bg-amber-500/10 text-amber-500 border border-amber-500/20' : 'bg-slate-100 text-slate-500 dark:bg-slate-800'
                }`}>
                  {profile?.profile?.is_premium ? 'Premium' : 'Free Member'}
                </span>
              </div>
            </div>
          </div>

          {/* Session Device Manager: 5 cols */}
          <div className="lg:col-span-5 bg-white dark:bg-slate-900 border border-slate-200/50 dark:border-slate-800/80 rounded-2xl p-6 shadow-premium space-y-6">
            <h3 className="font-display font-semibold text-slate-900 dark:text-white flex items-center gap-2 pb-3 border-b border-slate-100 dark:border-slate-800">
              <Laptop className="h-5 w-5 text-brand-500" />
              <span>Active Devices</span>
            </h3>

            <div className="space-y-4">
              {devices.length === 0 ? (
                <div className="text-center py-6 text-xs text-slate-400">No active login sessions.</div>
              ) : (
                devices.map((device) => (
                  <div key={device.id} className="flex justify-between items-center p-3 bg-slate-50 dark:bg-slate-950 rounded-xl">
                    <div className="space-y-1">
                      <span className="text-xs font-bold block">{device.device_name}</span>
                      <span className="text-[10px] text-slate-400 block">{device.ip_address} • Active now</span>
                    </div>
                    <button
                      onClick={() => handleRevokeDevice(device.id)}
                      className="p-2 text-slate-400 hover:text-accent-rose hover:bg-accent-rose/10 rounded-lg transition-colors"
                      title="Revoke session"
                    >
                      <Trash2 className="h-4 w-4" />
                    </button>
                  </div>
                ))
              )}
            </div>

            <div className="p-4 rounded-xl bg-slate-50 dark:bg-slate-950 border border-slate-100 dark:border-slate-900 text-xs flex gap-3 text-slate-400">
              <ShieldAlert className="h-5 w-5 text-brand-500 flex-shrink-0" />
              <p className="leading-relaxed">
                Revoking a device will blacklist its session and immediately force a signout on that terminal.
              </p>
            </div>
          </div>

        </div>
      </div>
    </DashboardLayout>
  );
};
export default Profile;
