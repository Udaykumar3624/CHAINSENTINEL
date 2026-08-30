import React, { createContext, useContext, useState, useEffect } from 'react';
import { UserAuthResponse, loginUser, logoutUser, fetchCurrentUser } from '../services/api';

interface AuthContextType {
  user: UserAuthResponse | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (username: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
  refreshUser: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<UserAuthResponse | null>(() => {
    const savedUser = localStorage.getItem('chainsentinel_user');
    try {
      return savedUser ? JSON.parse(savedUser) : null;
    } catch {
      return null;
    }
  });

  const [token, setToken] = useState<string | null>(() => {
    return localStorage.getItem('chainsentinel_token');
  });

  const [isLoading, setIsLoading] = useState<boolean>(true);

  const refreshUser = async () => {
    const activeToken = localStorage.getItem('chainsentinel_token');
    if (!activeToken) {
      setUser(null);
      setToken(null);
      setIsLoading(false);
      return;
    }

    try {
      const userData = await fetchCurrentUser();
      setUser(userData);
      localStorage.setItem('chainsentinel_user', JSON.stringify(userData));
    } catch (err) {
      console.warn("Session restore failed, clearing token.", err);
      localStorage.removeItem('chainsentinel_token');
      localStorage.removeItem('chainsentinel_user');
      setUser(null);
      setToken(null);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    refreshUser();
  }, []);

  const login = async (username: string, password: string) => {
    setIsLoading(true);
    try {
      const res = await loginUser(username, password);
      setToken(res.access_token);
      setUser(res.user);
      localStorage.setItem('chainsentinel_token', res.access_token);
      localStorage.setItem('chainsentinel_user', JSON.stringify(res.user));
    } finally {
      setIsLoading(false);
    }
  };

  const logout = async () => {
    setIsLoading(true);
    try {
      await logoutUser();
    } finally {
      localStorage.removeItem('chainsentinel_token');
      localStorage.removeItem('chainsentinel_user');
      setToken(null);
      setUser(null);
      setIsLoading(false);
    }
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        token,
        isAuthenticated: !!user && !!token,
        isLoading,
        login,
        logout,
        refreshUser,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = (): AuthContextType => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
