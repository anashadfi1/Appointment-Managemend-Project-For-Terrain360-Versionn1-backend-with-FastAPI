'use client';

import { useAuth } from '@/context/AuthContext';
import { Button } from '@/components/ui/button';
import { Avatar, AvatarFallback } from '@/components/ui/avatar';
import { LogOut, Calendar, RefreshCw } from 'lucide-react';

interface UserHeaderProps {
  onRefresh?: () => void;
}

export default function UserHeader({ onRefresh }: UserHeaderProps) {
  const { user, logout } = useAuth();

  if (!user) return null;

  const getInitials = (username: string) => {
    return username.substring(0, 2).toUpperCase();
  };

  return (
    <div className="bg-white border-b shadow-sm">
      <div className="px-6 py-4 flex justify-between items-center">
        <div className="flex items-center space-x-4">
          <div className="flex items-center space-x-2 text-blue-600">
            <Calendar className="h-6 w-6" />
            <h1 className="text-xl font-bold">Terrain360</h1>
          </div>
          <div className="h-6 w-px bg-gray-300"></div>
          <div className="flex items-center space-x-3">
            <Avatar className="h-8 w-8">
              <AvatarFallback className="bg-blue-600 text-white text-sm">
                {getInitials(user.username)}
              </AvatarFallback>
            </Avatar>
            <div className="flex flex-col">
              <p className="text-sm font-medium text-gray-900">{user.username}</p>
              <p className="text-xs text-gray-500">{user.email}</p>
            </div>
          </div>
        </div>
        
        <div className="flex items-center space-x-2">
          {onRefresh && (
            <Button 
              variant="outline" 
              size="sm"
              onClick={onRefresh}
              className="flex items-center space-x-2"
            >
              <RefreshCw className="h-4 w-4" />
              <span>Actualiser</span>
            </Button>
          )}
          <Button 
            variant="outline" 
            size="sm"
            onClick={logout}
            className="flex items-center space-x-2 hover:bg-red-50 hover:text-red-700 hover:border-red-200 transition-colors"
          >
            <LogOut className="h-4 w-4" />
            <span>Déconnexion</span>
          </Button>
        </div>
      </div>
    </div>
  );
}