import { useState, useEffect } from 'react';
import { useAuth } from '@/context/AuthContext';
import { Appointment } from '../types/appointment';
import { fetchUserAppointments } from '../utils/apiUtils';

export const useAppointments = () => {
  const [appointments, setAppointments] = useState<Appointment[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const { token, user, logout } = useAuth();

  useEffect(() => {
    const loadAppointments = async () => {
      if (!token || !user) {
        logout();
        return;
      }

      try {
        setLoading(true);
        setError(null);
        
        const userAppointments = await fetchUserAppointments(token);
        
        // Filter appointments to only show the current user's appointments
        const filteredAppointments = userAppointments.filter(
          appointment => appointment.agent.username === user.username
        );
        
        setAppointments(filteredAppointments);
        console.log(`Chargé ${filteredAppointments.length} rendez-vous pour ${user.username}`);
      } catch (err) {
        console.error('Erreur lors du chargement des rendez-vous:', err);
        
        if (err instanceof Error) {
          if (err.message.includes('Session expirée') || err.message.includes('401')) {
            logout();
            return;
          }
          setError(err.message);
        } else {
          setError('Erreur lors du chargement des rendez-vous');
        }
      } finally {
        setLoading(false);
      }
    };

    loadAppointments();
  }, [token, user, logout]);

  const refreshAppointments = async () => {
    if (!token || !user) {
      logout();
      return;
    }

    try {
      setError(null);
      const userAppointments = await fetchUserAppointments(token);
      const filteredAppointments = userAppointments.filter(
        appointment => appointment.agent.username === user.username
      );
      setAppointments(filteredAppointments);
      console.log('Rendez-vous actualisés avec succès');
    } catch (err) {
      console.error('Erreur lors de l\'actualisation:', err);
      if (err instanceof Error && (err.message.includes('Session expirée') || err.message.includes('401'))) {
        logout();
      }
    }
  };

  return {
    appointments,
    loading,
    error,
    refreshAppointments
  };
};