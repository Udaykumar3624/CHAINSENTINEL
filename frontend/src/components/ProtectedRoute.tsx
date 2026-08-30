import React from 'react';
import { Navigate, useLocation, Outlet } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { ShieldAlert, Loader2 } from 'lucide-react';

interface ProtectedRouteProps {
  children?: React.ReactNode;
}

export const ProtectedRoute: React.FC<ProtectedRouteProps> = ({ children }) => {
  const { isAuthenticated, isLoading } = useAuth();
  const location = useLocation();

  if (isLoading) {
    return (
      <div className="min-h-screen bg-slate-950 flex flex-col items-center justify-center space-y-4 font-mono text-xs text-slate-300">
        <div className="p-4 rounded-full bg-slate-900 border border-slate-800 shadow-xl">
          <Loader2 className="w-8 h-8 text-cyan-400 animate-spin" />
        </div>
        <div className="text-center space-y-1">
          <p className="font-bold tracking-wider uppercase text-slate-200">CHAIN SENTINEL SYSTEM</p>
          <p className="text-slate-500">Authenticating Investigator Session...</p>
        </div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  return children ? <>{children}</> : <Outlet />;
};
