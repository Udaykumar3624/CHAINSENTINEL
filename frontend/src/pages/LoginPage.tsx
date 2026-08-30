import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { ShieldAlert, Lock, User, Key, ArrowRight, Loader2, AlertTriangle, ArrowLeft } from 'lucide-react';

export const LoginPage: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { login, isAuthenticated } = useAuth();

  const [username, setUsername] = useState<string>('');
  const [password, setPassword] = useState<string>('');
  const [isSubmitting, setIsSubmitting] = useState<boolean>(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  // If redirecting from a protected route, use that; otherwise default to /dashboard
  const from = (location.state as any)?.from?.pathname;
  const targetDestination = from && from !== '/' && from !== '/login' ? from : '/dashboard';

  // Safely redirect ONLY after authentication state confirms in an effect
  useEffect(() => {
    if (isAuthenticated) {
      navigate(targetDestination, { replace: true });
    }
  }, [isAuthenticated, navigate, targetDestination]);

  const handleSubmit = async (e?: React.FormEvent) => {
    if (e) {
      e.preventDefault();
      e.stopPropagation();
    }

    const trimmedUser = username.trim();
    if (!trimmedUser || !password) {
      setErrorMessage('Username/Email and Password are required.');
      return;
    }

    setIsSubmitting(true);
    setErrorMessage(null);

    try {
      await login(trimmedUser, password);
      navigate(targetDestination, { replace: true });
    } catch (err: any) {
      const detail = err.response?.data?.detail;
      if (typeof detail === 'string') {
        setErrorMessage(detail);
      } else if (err.code === 'ERR_NETWORK' || !err.response) {
        setErrorMessage('Unable to connect to ChainSentinel Backend. Please verify backend service at http://localhost:8000');
      } else {
        setErrorMessage('Invalid username/email or password.');
      }
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleInputKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    // Stop propagation for paste/copy/select-all keys so they never bubble to form submit
    if ((e.ctrlKey || e.metaKey) && ['v', 'c', 'a', 'x'].includes(e.key.toLowerCase())) {
      e.stopPropagation();
      return;
    }

    // Submit only on explicit Enter press
    if (e.key === 'Enter') {
      e.preventDefault();
      handleSubmit();
    }
  };

  const handleInputPaste = (e: React.ClipboardEvent<HTMLInputElement>) => {
    // Normal paste behavior without bubbling or triggering submission
    e.stopPropagation();
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col justify-between p-4 sm:p-6 font-sans antialiased relative overflow-hidden">
      {/* Background Subtle Grid Effect */}
      <div className="absolute inset-0 bg-[linear-gradient(to_right,#1e293b_1px,transparent_1px),linear-gradient(to_bottom,#1e293b_1px,transparent_1px)] bg-[size:4rem_4rem] [mask-image:radial-gradient(ellipse_60%_50%_at_50%_0%,#000_70%,transparent_100%)] opacity-20 pointer-events-none" />

      {/* Top Header Branding & Back Link */}
      <header className="flex items-center justify-between max-w-5xl mx-auto w-full z-10">
        <Link to="/" className="flex items-center space-x-3 group">
          <div className="p-2.5 bg-cyan-500/10 border border-cyan-500/30 rounded-xl shadow-lg shadow-cyan-950/40 group-hover:border-cyan-400 transition-colors">
            <ShieldAlert className="w-5 h-5 text-cyan-400" />
          </div>
          <div>
            <h1 className="font-mono text-sm font-bold tracking-wider text-slate-100 uppercase">
              CHAIN SENTINEL
            </h1>
            <p className="text-[10px] font-mono text-slate-400">Bitcoin AI Risk Analytics</p>
          </div>
        </Link>

        <div className="flex items-center space-x-3">
          <Link
            to="/"
            className="text-xs font-mono text-slate-400 hover:text-cyan-400 transition-colors flex items-center space-x-1"
          >
            <ArrowLeft className="w-3.5 h-3.5" />
            <span>Public Overview</span>
          </Link>
          <span className="text-[10px] font-mono px-2.5 py-1 bg-slate-900 border border-slate-800 text-cyan-400 rounded-full font-semibold">
            SIH26146
          </span>
        </div>
      </header>

      {/* Central Login Container */}
      <main className="max-w-md w-full mx-auto my-auto z-10 py-6">
        <div className="bg-slate-900/80 backdrop-blur-md p-8 rounded-2xl border border-slate-800 shadow-2xl shadow-slate-950 space-y-6">
          <div className="space-y-1.5 text-center">
            <div className="inline-flex items-center justify-center p-3 rounded-full bg-slate-950 border border-slate-800 text-cyan-400 mb-1">
              <Lock className="w-5 h-5" />
            </div>
            <h2 className="text-xl font-bold text-slate-100 tracking-tight font-mono uppercase">
              Investigator Login
            </h2>
            <p className="text-xs text-slate-400 font-mono">
              SIH26146 • Authorized Investigator Access
            </p>
          </div>

          {/* ERROR ALERT */}
          {errorMessage && (
            <div className="p-3.5 bg-rose-500/10 border border-rose-500/30 rounded-xl text-rose-400 text-xs font-mono flex items-start space-x-2.5">
              <AlertTriangle className="w-4 h-4 shrink-0 mt-0.5" />
              <span>{errorMessage}</span>
            </div>
          )}

          {/* LOGIN FORM */}
          <form
            onSubmit={(e) => {
              e.preventDefault();
              handleSubmit(e);
            }}
            noValidate
            className="space-y-4 font-mono text-xs"
          >
            <div className="space-y-1.5">
              <label className="text-slate-300 font-semibold block uppercase text-[11px]">
                Username or Email
              </label>
              <div className="relative">
                <User className="w-4 h-4 text-slate-500 absolute left-3 top-3 pointer-events-none" />
                <input
                  type="text"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  onKeyDown={handleInputKeyDown}
                  onPaste={handleInputPaste}
                  placeholder="Enter username or email"
                  required
                  autoComplete="username"
                  className="w-full pl-9 pr-4 py-2.5 bg-slate-950 border border-slate-800 rounded-xl text-slate-100 placeholder-slate-600 focus:outline-none focus:border-cyan-500/60 transition-colors"
                />
              </div>
            </div>

            <div className="space-y-1.5">
              <label className="text-slate-300 font-semibold block uppercase text-[11px]">
                Password
              </label>
              <div className="relative">
                <Key className="w-4 h-4 text-slate-500 absolute left-3 top-3 pointer-events-none" />
                <input
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  onKeyDown={handleInputKeyDown}
                  onPaste={handleInputPaste}
                  placeholder="Enter password"
                  required
                  autoComplete="current-password"
                  className="w-full pl-9 pr-4 py-2.5 bg-slate-950 border border-slate-800 rounded-xl text-slate-100 placeholder-slate-600 focus:outline-none focus:border-cyan-500/60 transition-colors"
                />
              </div>
            </div>

            <button
              type="submit"
              disabled={isSubmitting}
              className="w-full py-3 bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-bold rounded-xl flex items-center justify-center space-x-2 transition-all shadow-lg shadow-cyan-950/50 disabled:opacity-50 mt-2 cursor-pointer"
            >
              {isSubmitting ? (
                <>
                  <Loader2 className="w-4 h-4 animate-spin text-slate-950" />
                  <span>Authenticating...</span>
                </>
              ) : (
                <>
                  <span>Sign In</span>
                  <ArrowRight className="w-4 h-4" />
                </>
              )}
            </button>
          </form>
        </div>
      </main>

      {/* Footer */}
      <footer className="text-center font-mono text-[11px] text-slate-500 z-10 py-2">
        ChainSentinel SIH26146 • Authorized Triage Platform • Confidential & Read-Only
      </footer>
    </div>
  );
};
