import { Appointment } from '../types/appointment';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL;
const APPOINTMENTS_ENDPOINT = process.env.NEXT_PUBLIC_API_APPOINTMENTS_ENDPOINT || '/api/appointments';

export const fetchUserAppointments = async (token: string): Promise<Appointment[]> => {
  try {
    const url = `${API_BASE_URL}${APPOINTMENTS_ENDPOINT}`;
    
    const response = await fetch(url, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      if (response.status === 401) {
        // Token expired or invalid
        localStorage.removeItem('access_token');
        localStorage.removeItem('user_data');
        window.location.href = '/login';
        throw new Error('Session expirée');
      }
      throw new Error(`Erreur HTTP ${response.status}: Impossible de charger les rendez-vous`);
    }

    return await response.json();
  } catch (error) {
    console.error('Erreur lors du chargement des rendez-vous:', error);
    throw error;
  }
};

export const deleteAppointment = async (token: string, appointmentId: number): Promise<void> => {
  try {
    const url = `${API_BASE_URL}${APPOINTMENTS_ENDPOINT}/${appointmentId}`;
    
    const response = await fetch(url, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      if (response.status === 401) {
        localStorage.removeItem('access_token');
        localStorage.removeItem('user_data');
        window.location.href = '/login';
        throw new Error('Session expirée');
      }
      throw new Error(`Impossible de supprimer le rendez-vous: ${response.status}`);
    }
  } catch (error) {
    console.error('Erreur lors de la suppression:', error);
    throw error;
  }
};

export const updateAppointmentStatus = async (
  token: string, 
  appointmentId: number, 
  status: string
): Promise<void> => {
  try {
    const url = `${API_BASE_URL}${APPOINTMENTS_ENDPOINT}/${appointmentId}`;
    
    const response = await fetch(url, {
      method: 'PATCH',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ status }),
    });

    if (!response.ok) {
      if (response.status === 401) {
        localStorage.removeItem('access_token');
        localStorage.removeItem('user_data');
        window.location.href = '/login';
        throw new Error('Session expirée');
      }
      throw new Error(`Impossible de mettre à jour le rendez-vous: ${response.status}`);
    }
  } catch (error) {
    console.error('Erreur lors de la mise à jour:', error);
    throw error;
  }
};