import { format, parse, startOfWeek, getDay, addMonths, subMonths, addWeeks, subWeeks, addDays, subDays } from 'date-fns';
import { fr } from 'date-fns/locale';
import { View } from 'react-big-calendar';
import { Appointment } from '../types/appointment';

const locales = {
  'fr-FR': fr,
};

export const localizer = {
  format: (date: Date, formatStr: string) => format(date, formatStr, { locale: fr }),
  parse: (str: string, formatStr: string) => parse(str, formatStr, new Date()),
  startOfWeek: (date: Date) => startOfWeek(date, { locale: fr }),
  getDay: (date: Date) => getDay(date),
  locales
};

export const formatDate = (dateString: string) => {
  const date = new Date(dateString);
  return new Intl.DateTimeFormat('fr-FR', {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  }).format(date);
};

export const formatTime = (dateString: string) => {
  const date = new Date(dateString);
  return date.toLocaleTimeString('fr-FR', {
    hour: '2-digit',
    minute: '2-digit'
  });
};

export const formatDateTime = (dateString: string) => {
  const date = new Date(dateString);
  return {
    date: date.toISOString().split('T')[0],
    time: date.toLocaleTimeString('fr-FR', {
      hour: '2-digit',
      minute: '2-digit'
    })
  };
};

export const convertToCalendarEvents = (appointments: Appointment[]) => {
  return appointments.map((apt) => {
    const appointmentDate = new Date(apt.appointment_time);
    // Create end time (assuming 1 hour duration)
    const endDate = new Date(appointmentDate.getTime() + 60 * 60 * 1000);
    
    return {
      id: apt.id,
      title: `${apt.company.client_name}`,
      start: appointmentDate,
      end: endDate,
      resource: apt
    };
  });
};

export const getStatusColor = (status: string) => {
  const statusColors = {
    'a faire': 'bg-yellow-100 text-yellow-800 border-yellow-200',
    'fait': 'bg-green-100 text-green-800 border-green-200',
    'confirme': 'bg-blue-100 text-blue-800 border-blue-200',
    'annule': 'bg-red-100 text-red-800 border-red-200'
  };
  
  return statusColors[status as keyof typeof statusColors] || 'bg-gray-100 text-gray-800 border-gray-200';
};

export const getStatusLabel = (status: string) => {
  const statusLabels = {
    'a faire': 'À faire',
    'fait': 'Terminé',
    'confirme': 'Confirmé',
    'annule': 'Annulé'
  };
  
  return statusLabels[status as keyof typeof statusLabels] || status;
};

export const navigateCalendar = (action: string, currentDate: Date, view: View) => {
  if (action === 'TODAY') return new Date();
  
  let newDate;
  if (view === 'month') {
    newDate = action === 'PREV' ? subMonths(currentDate, 1) : addMonths(currentDate, 1);
  } else if (view === 'week') {
    newDate = action === 'PREV' ? subWeeks(currentDate, 1) : addWeeks(currentDate, 1);
  } else {
    newDate = action === 'PREV' ? subDays(currentDate, 1) : addDays(currentDate, 1);
  }
  
  return newDate;
};

export const getAppointmentsByDate = (appointments: Appointment[], date: Date) => {
  const targetDate = date.toISOString().split('T')[0];
  return appointments.filter(apt => {
    const appointmentDate = new Date(apt.appointment_time).toISOString().split('T')[0];
    return appointmentDate === targetDate;
  });
};

export const getAppointmentsByAgent = (appointments: Appointment[], agentId: number) => {
  return appointments.filter(apt => apt.agent.id === agentId);
};

export const getAppointmentsByStatus = (appointments: Appointment[], status: string) => {
  return appointments.filter(apt => apt.status === status);
};