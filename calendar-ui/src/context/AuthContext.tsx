'use client';

import { createContext, useContext, useEffect, useState, ReactNode } from 'react';
import { useRouter } from 'next/navigation';

interface User {
  username: string;
  email: string;
}

interface AuthContextType {
  user: User | null;
  token: string | null;
  login: (token: string, userData: User) => void;
  logout: () => void;
  isLoading: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    // Check for existing authentication on mount
    const savedToken = localStorage.getItem('access_token');
    const savedUser = localStorage.getItem('user_data');

    if (savedToken && savedUser) {
      try {
        const userData = JSON.parse(savedUser);
        setToken(savedToken);
        setUser(userData);
        console.log('User loaded from localStorage:', userData);
      } catch (error) {
        console.error('Invalid user data in localStorage:', error);
        // Clear invalid data
        localStorage.removeItem('access_token');
        localStorage.removeItem('user_data');
      }
    }
    setIsLoading(false);
  }, []);

  const login = (newToken: string, userData: User) => {
    console.log('AuthContext login called with:', { token: newToken, user: userData });
    localStorage.setItem('access_token', newToken);
    localStorage.setItem('user_data', JSON.stringify(userData));
    setToken(newToken);
    setUser(userData);
    
    // Force navigation to calendar
    setTimeout(() => {
      router.push('/calendrier');
    }, 100);
  };

  const logout = () => {
    console.log('Logging out user');
    localStorage.removeItem('access_token');
    localStorage.removeItem('user_data');
    setToken(null);
    setUser(null);
    router.push('/login');
  };

  return (
    <AuthContext.Provider value={{ user, token, login, logout, isLoading }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}