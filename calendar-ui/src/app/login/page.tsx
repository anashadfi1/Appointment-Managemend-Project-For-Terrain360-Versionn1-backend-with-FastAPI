'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/context/AuthContext';
import Image from 'next/image';
import { Eye, EyeOff, Loader2 } from 'lucide-react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { Alert, AlertDescription } from "@/components/ui/alert";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://127.0.0.1:8000';
const LOGIN_ENDPOINT = process.env.NEXT_PUBLIC_API_LOGIN_ENDPOINT || '/api/agents/login';
const APP_NAME = process.env.NEXT_PUBLIC_APP_NAME || 'Terrain360';

export default function LoginPage() {
  const router = useRouter();
  const { user, login, isLoading: authLoading } = useAuth();
  const [showPassword, setShowPassword] = useState(false);
  const [formData, setFormData] = useState({
    username: '',
    password: ''
  });
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  // Redirect if already logged in
  useEffect(() => {
    console.log('LoginPage: user state changed:', user);
    if (user && !authLoading) {
      console.log('User is logged in, redirecting to calendar');
      router.push('/calendrier');
    }
  }, [user, authLoading, router]);

  const togglePasswordVisibility = () => {
    setShowPassword(!showPassword);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    console.log('Login form submitted');
    setIsLoading(true);
    setError('');

    try {
      const formBody = new URLSearchParams({
        username: formData.username.trim(),
        password: formData.password
      });

      const url = `${API_BASE_URL}${LOGIN_ENDPOINT}`;
      console.log('Making login request to:', url);

      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: formBody,
        mode: 'cors',
      });

      console.log('Login response status:', response.status);

      if (response.ok) {
        const data = await response.json();
        console.log('Login successful, received data:', data);
        
        // Use the auth context login method
        login(data.access_token, {
          username: data.username,
          email: data.email
        });
        
        console.log('AuthContext login called, should redirect soon...');
      } else {
        const errorData = await response.json().catch(() => ({ 
          detail: 'Erreur de connexion au serveur' 
        }));
        console.error('Login failed:', errorData);
        setError(errorData.detail || 'Identifiants incorrects');
      }
    } catch (error) {
      console.error('Login error:', error);
      setError('Impossible de se connecter au serveur. Vérifiez votre connexion internet.');
    } finally {
      setIsLoading(false);
    }
  };

  // Show loading while checking auth state
  if (authLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 via-white to-cyan-50">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto"></div>
          <p className="mt-4 text-muted-foreground">Vérification de l'authentification...</p>
        </div>
      </div>
    );
  }

  // Don't render login form if user is already logged in
  if (user) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 via-white to-cyan-50">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto"></div>
          <p className="mt-4 text-muted-foreground">Redirection en cours...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 via-white to-cyan-50">
      <Card className="w-full max-w-md mx-4 shadow-xl border-0">
        <CardHeader className="space-y-4 items-center text-center pb-6">
          <div className="w-24 h-24 relative mb-2">
            <Image
              src="/logo.png"
              alt={`${APP_NAME} Logo`}
              fill
              className="object-contain drop-shadow-sm"
              priority
            />
          </div>
          <div>
            <CardTitle className="text-2xl font-bold text-foreground">
              Bienvenue sur {APP_NAME}
            </CardTitle>
            <CardDescription className="text-muted-foreground mt-2">
              Connectez-vous pour accéder à votre calendrier
            </CardDescription>
          </div>
        </CardHeader>
        
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-5">
            {error && (
              <Alert variant="destructive" className="animate-in slide-in-from-top-1">
                <AlertDescription className="font-medium">
                  {error}
                </AlertDescription>
              </Alert>
            )}
            
            <div className="space-y-2">
              <Label htmlFor="username" className="text-foreground font-medium">
                Nom d'utilisateur
              </Label>
              <Input
                id="username"
                type="text"
                placeholder="Votre nom d'utilisateur"
                value={formData.username}
                onChange={(e) => setFormData({ ...formData, username: e.target.value })}
                required
                className="h-11 text-foreground placeholder:text-muted-foreground"
                disabled={isLoading}
              />
            </div>
            
            <div className="space-y-2">
              <Label htmlFor="password" className="text-foreground font-medium">
                Mot de passe
              </Label>
              <div className="relative">
                <Input
                  id="password"
                  type={showPassword ? "text" : "password"}
                  placeholder="Votre mot de passe"
                  value={formData.password}
                  onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                  required
                  className="h-11 pr-11 text-foreground placeholder:text-muted-foreground"
                  disabled={isLoading}
                />
                <button
                  type="button"
                  onClick={togglePasswordVisibility}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground transition-colors"
                  disabled={isLoading}
                >
                  {showPassword ? (
                    <EyeOff className="h-5 w-5" />
                  ) : (
                    <Eye className="h-5 w-5" />
                  )}
                </button>
              </div>
            </div>

            <Button 
              type="submit" 
              className="w-full h-11 bg-primary hover:bg-primary/90 text-primary-foreground font-medium"
              disabled={isLoading}
            >
              {isLoading ? (
                <>
                  <Loader2 className="h-4 w-4 animate-spin mr-2" />
                  Connexion en cours...
                </>
              ) : (
                "Se connecter"
              )}
            </Button>
          </form>
        </CardContent>
      </Card>
    </div>
  );
}