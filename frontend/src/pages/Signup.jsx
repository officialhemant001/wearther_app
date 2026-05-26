import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { CloudSun, ArrowRight, User, Mail, Lock } from 'lucide-react';
import { useAuthStore } from '../store/authStore';

export const Signup = () => {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [loadingLocal, setLoadingLocal] = useState(false);
  const [errorLocal, setErrorLocal] = useState('');

  const navigate = useNavigate();
  const signup = useAuthStore(state => state.signup);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (password !== confirmPassword) {
      setErrorLocal('Passwords do not match.');
      return;
    }

    setLoadingLocal(true);
    setErrorLocal('');

    const success = await signup(username, email, password, confirmPassword);
    setLoadingLocal(false);

    if (success) {
      navigate('/dashboard');
    } else {
      setErrorLocal('Registration failed. Please choose another email or username.');
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 dark:bg-slate-950 flex flex-col justify-center py-12 sm:px-6 lg:px-8 transition-colors duration-300">
      <div className="sm:mx-auto sm:w-full sm:max-w-md flex flex-col items-center">
        <Link to="/" className="flex items-center gap-2 font-display font-semibold text-xl tracking-tight text-slate-900 dark:text-white mb-6">
          <CloudSun className="h-8 w-8 text-brand-500" />
          <span>AETHER</span>
        </Link>
        <h2 className="text-2xl font-display font-bold text-slate-900 dark:text-white tracking-tight text-center">
          Create your account
        </h2>
        <p className="mt-2 text-sm text-slate-400">
          Or{' '}
          <Link to="/login" className="font-medium text-brand-500 hover:text-brand-400 transition-colors">
            sign in to existing account
          </Link>
        </p>
      </div>

      <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
        <div className="bg-white dark:bg-slate-900 border border-slate-200/60 dark:border-slate-800/80 py-8 px-4 shadow-premium rounded-2xl sm:px-10">
          {errorLocal && (
            <div className="mb-6 p-4 rounded-xl bg-accent-rose/10 border border-accent-rose/20 text-accent-rose text-xs font-semibold">
              {errorLocal}
            </div>
          )}

          <form className="space-y-5" onSubmit={handleSubmit}>
            <div>
              <label htmlFor="username" className="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">
                Username
              </label>
              <div className="relative">
                <span className="absolute inset-y-0 left-0 pl-3.5 flex items-center text-slate-400">
                  <User className="h-4 w-4" />
                </span>
                <input
                  id="username"
                  type="text"
                  required
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  placeholder="username"
                  className="premium-input pl-10"
                />
              </div>
            </div>

            <div>
              <label htmlFor="email" className="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">
                Email Address
              </label>
              <div className="relative">
                <span className="absolute inset-y-0 left-0 pl-3.5 flex items-center text-slate-400">
                  <Mail className="h-4 w-4" />
                </span>
                <input
                  id="email"
                  type="email"
                  required
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="name@example.com"
                  className="premium-input pl-10"
                />
              </div>
            </div>

            <div>
              <label htmlFor="password" className="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">
                Password
              </label>
              <div className="relative">
                <span className="absolute inset-y-0 left-0 pl-3.5 flex items-center text-slate-400">
                  <Lock className="h-4 w-4" />
                </span>
                <input
                  id="password"
                  type="password"
                  required
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="••••••••"
                  className="premium-input pl-10"
                />
              </div>
            </div>

            <div>
              <label htmlFor="confirmPassword" className="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">
                Confirm Password
              </label>
              <div className="relative">
                <span className="absolute inset-y-0 left-0 pl-3.5 flex items-center text-slate-400">
                  <Lock className="h-4 w-4" />
                </span>
                <input
                  id="confirmPassword"
                  type="password"
                  required
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                  placeholder="••••••••"
                  className="premium-input pl-10"
                />
              </div>
            </div>

            <button
              type="submit"
              disabled={loadingLocal}
              className="premium-btn-primary w-full disabled:opacity-50"
            >
              <span>{loadingLocal ? 'Creating Account...' : 'Create Account'}</span>
              <ArrowRight className="h-4 w-4" />
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};
export default Signup;
