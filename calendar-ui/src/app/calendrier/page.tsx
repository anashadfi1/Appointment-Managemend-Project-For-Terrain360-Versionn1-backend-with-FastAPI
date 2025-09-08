'use client';

import { useState } from 'react';
import { View } from 'react-big-calendar';
import CalendarMain from './components/Calendar/CalendarMain';
import CalendarSidebar from './components/Calendar/CalendarSidebar';
import AppointmentModal from './components/Appointments/AppointmentModal';
import UserHeader from '@/components/layout/UserHeader';
import ProtectedRoute from '@/components/auth/ProtectedRoute';
import { Appointment } from './types/appointment';
import { convertToCalendarEvents } from './utils/calendarUtils';
import { useAppointments } from './hooks/useAppointments';
import { useAuth } from '@/context/AuthContext';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { RefreshCw, AlertCircle, Calendar as CalendarIcon } from 'lucide-react';
import 'react-big-calendar/lib/css/react-big-calendar.css';
import './styles/calendar.css';

function CalendarContent() {
  const { appointments, loading, error, refreshAppointments } = useAppointments();
  const { user } = useAuth();
  const [selectedAppointment, setSelectedAppointment] = useState<Appointment | null>(null);
  const [date, setDate] = useState(new Date());
  const [view, setView] = useState<View>('month');
  const [showSidebar, setShowSidebar] = useState(true);

  const calendarEvents = convertToCalendarEvents(appointments);

  const handleEventClick = (event: any) => {
    const appointment = event.resource;
    setSelectedAppointment(appointment);
  };

  const handleDeleteAppointment = async (id: number) => {
    try {
      console.log('Suppression du rendez-vous ID:', id);
      setSelectedAppointment(null);
      await refreshAppointments();
    } catch (error) {
      console.error('Erreur lors de la suppression:', error);
    }
  };

  const handleCloseModal = () => {
    setSelectedAppointment(null);
  };

  if (loading) {
    return (
      <div className="flex flex-col h-screen bg-gray-50">
        <UserHeader />
        <div className="flex-1 flex items-center justify-center">
          <Card className="p-8">
            <CardContent className="text-center">
              <div className="calendar-loading">
                <div className="spinner"></div>
              </div>
              <p className="mt-4 text-gray-700 font-medium">Chargement des rendez-vous...</p>
              <p className="text-sm text-gray-500">Récupération des données depuis le serveur</p>
            </CardContent>
          </Card>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex flex-col h-screen bg-gray-50">
        <UserHeader onRefresh={refreshAppointments} />
        <div className="flex-1 flex items-center justify-center p-4">
          <Card className="p-8 max-w-md">
            <CardContent className="text-center">
              <AlertCircle className="h-12 w-12 text-red-500 mx-auto mb-4" />
              <h2 className="text-lg font-semibold text-gray-900 mb-2">Erreur de chargement</h2>
              <p className="text-red-600 mb-6 text-sm">{error}</p>
              <div className="flex flex-col sm:flex-row gap-2 justify-center">
                <Button 
                  onClick={refreshAppointments}
                  className="flex items-center space-x-2"
                >
                  <RefreshCw className="h-4 w-4" />
                  <span>Réessayer</span>
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    );
  }

  return (
    <div className="flex flex-col h-screen bg-gray-50">
      <UserHeader onRefresh={refreshAppointments} />
      
      <div className="flex flex-1 overflow-hidden">
        <CalendarSidebar 
          appointments={appointments}
          showSidebar={showSidebar}
          onToggleSidebar={() => setShowSidebar(!showSidebar)}
        />
        
        <CalendarMain
          events={calendarEvents}
          date={date}
          view={view}
          appointments={appointments}
          onView={setView}
          onNavigate={setDate}
          onSelectEvent={handleEventClick}
        />
      </div>

      {selectedAppointment && (
        <AppointmentModal
          appointment={selectedAppointment}
          onClose={handleCloseModal}
          onDelete={handleDeleteAppointment}
          open={!!selectedAppointment}
        />
      )}
    </div>
  );
}

export default function CalendarApp() {
  return (
    <ProtectedRoute>
      <CalendarContent />
    </ProtectedRoute>
  );
}