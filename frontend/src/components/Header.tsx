import React, { useEffect, useState } from 'react';
import { NavLink, Link, useNavigate } from 'react-router-dom';
import { Shield, Activity, Search, AlertTriangle, Briefcase, Info, Wifi, WifiOff, Database, LogOut } from 'lucide-react';
import { fetchBackendHealth, HealthResponse } from '../services/api';
import { useAuth } from '../context/AuthContext';

export const Header: React.FC = () => {
  const navigate = useNavigate();
  const { user, logout } = useAuth();
  const [health, setHealth] = useState<HealthResponse | null>(null);
  const [isOnline, setIsOnline] = useState<boolean>(false);

  const handleLogout = async () => {
    await logout();
    navigate('/login', { replace: true });
  };

  useEffect(() => {
    const checkHealth = async () => {
      try {
        const data = await fetchBackendHealth();
        setHealth(data);
        setIsOnline(true);
      } catch {
        setIsOnline(false);
      }
    };
    checkHealth();
    const interval = setInterval(checkHealth, 15000);
    return () => clearInterval(interval);
  }, []);

  const navItems = [
    { to: '/dashboard', label: 'Dashboard', icon: Activity },
    { to: '/analyze', label: 'Analyze', icon: Search },
    { to: '/investigate/demo', label: 'Investigation', icon: Shield },
    { to: '/alerts', label: 'Alerts', icon: AlertTriangle },
    { to: '/cases', label: 'Cases', icon: Briefcase },
    { to: '/dataset', label: 'Dataset', icon: Database },
    { to: '/explorer', label: 'Explorer', icon: Database },
    { to: '/judge-demo', label: 'Judge Demo', icon: Shield },
    { to: '/about', label: 'Methodology', icon: Info },
  ];

  return (
    <header className="sticky top-0 z-50 bg-[#0b1329]/90 backdrop-blur-md border-b border-slate-800">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo & Brand */}
          <Link to="/dashboard" className="flex items-center space-x-3 group">
            <div className="p-2 bg-cyan-500/10 border border-cyan-500/30 rounded-lg text-cyan-400 group-hover:border-cyan-400 transition-colors">
              <Shield className="w-6 h-6 animate-pulse" />
            </div>
            <div>
              <div className="flex items-center space-x-2">
                <span className="font-bold text-lg tracking-wider text-slate-100 uppercase font-mono">
                  Chain<span className="text-cyan-400">Sentinel</span>
                </span>
                <span className="px-2 py-0.5 text-[10px] font-mono tracking-wide uppercase bg-slate-800 border border-slate-700 text-cyan-400 rounded">
                  SIH26146
                </span>
              </div>
              <p className="text-[11px] text-slate-400 font-mono hidden sm:block">Bitcoin AI Risk Analytics</p>
            </div>
          </Link>

          {/* Navigation Links */}
          <nav className="hidden md:flex space-x-1">
            {navItems.map((item) => {
              const Icon = item.icon;
              return (
                <NavLink
                  key={item.to}
                  to={item.to}
                  className={({ isActive }) =>
                    `flex items-center space-x-1.5 px-3 py-2 rounded-md text-xs font-medium transition-colors ${
                      isActive
                        ? 'bg-cyan-500/10 text-cyan-400 border border-cyan-500/20'
                        : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/50'
                    }`
                  }
                >
                  <Icon className="w-4 h-4" />
                  <span>{item.label}</span>
                </NavLink>
              );
            })}
          </nav>

          {/* System Status & User Profile */}
          <div className="flex items-center space-x-3">
            <div className={`flex items-center space-x-1.5 px-2.5 py-1 rounded-full text-[11px] font-mono border ${
              isOnline
                ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30'
                : 'bg-red-500/10 text-red-400 border-red-500/30'
            }`}>
              {isOnline ? <Wifi className="w-3.5 h-3.5" /> : <WifiOff className="w-3.5 h-3.5" />}
              <span>{isOnline ? 'Online' : 'Offline'}</span>
            </div>

            {user && (
              <div className="flex items-center space-x-2 pl-2 border-l border-slate-800 font-mono text-xs">
                <div className="hidden lg:flex flex-col text-right">
                  <span className="font-bold text-slate-100 text-[11px] truncate max-w-[120px]">{user.full_name || 'Investigator'}</span>
                  <span className="text-[9px] text-cyan-400 uppercase tracking-wider">{user.role || 'LEAD_INVESTIGATOR'}</span>
                </div>

                <button
                  onClick={handleLogout}
                  title="Logout Investigator Session"
                  className="px-2.5 py-1.5 bg-slate-800 hover:bg-rose-500/20 text-slate-400 hover:text-rose-400 rounded-lg border border-slate-700 hover:border-rose-500/40 transition-colors flex items-center space-x-1.5 cursor-pointer"
                >
                  <LogOut className="w-3.5 h-3.5" />
                  <span className="text-[11px] font-medium">Logout</span>
                </button>
              </div>
            )}
          </div>
        </div>
      </div>
    </header>
  );
};
