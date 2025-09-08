'use client';

import React from 'react';
import { Calendar, dateFnsLocalizer, View } from 'react-big-calendar';
import { format, parse, startOfWeek, getDay } from 'date-fns';
import { fr } from 'date-fns/locale';
import { Appointment } from '../../types/appointment';

const locales = {
  'fr-FR': fr,
};

const localizer = dateFnsLocalizer({
  format,
  parse,
  startOfWeek,
  getDay,
  locales,
});

interface CalendarMainProps {
  events: any[];
  date: Date;
  view: View;
  appointments: Appointment[];
  onView: (view: View) => void;
  onNavigate: (date: Date) => void;
  onSelectEvent: (event: any) => void;
}

const getStatusColor = (status: string) => {
  const colors = {
    'a faire': '#F59E0B', // yellow
    'fait': '#10B981', // green
    'confirme': '#3B82F6', // blue
    'annule': '#EF4444' // red
  };
  return colors[status as keyof typeof colors] || '#6B7280';
};

const CalendarMain: React.FC<CalendarMainProps> = ({
  events,
  date,
  view,
  appointments, // Make sure this is destructured
  onView,
  onNavigate,
  onSelectEvent
}) => {
  const EventComponent = ({ event }: { event: any }) => {
    const appointment = event.resource as Appointment;
    return (
      <div 
        className="text-white text-xs p-1 rounded cursor-pointer hover:opacity-90 transition-opacity"
        style={{ 
          backgroundColor: getStatusColor(appointment.status),
          height: '100%',
          border: 'none',
          fontSize: '11px'
        }}
      >
        <div className="font-medium truncate" style={{ lineHeight: '1.2' }}>
          {appointment.company.client_name}
        </div>
        <div className="text-xs opacity-90 truncate" style={{ lineHeight: '1.1' }}>
          {appointment.company.location}
        </div>
        <div className="text-xs opacity-80" style={{ lineHeight: '1.1' }}>
          {new Date(appointment.appointment_time).toLocaleTimeString('fr-FR', {
            hour: '2-digit',
            minute: '2-digit'
          })}
        </div>
      </div>
    );
  };

  // Custom day format for better visibility
  const DayFormat = ({ date }: { date: Date }) => (
    <div className="text-center py-2">
      <div className="font-semibold text-gray-700 text-sm">
        {format(date, 'EEE', { locale: fr }).toUpperCase()}
      </div>
      <div className="text-lg font-bold text-gray-900">
        {format(date, 'd', { locale: fr })}
      </div>
    </div>
  );

  return (
    <div className="flex-1 bg-gray-50">
      <div className="p-6 h-full">
        <div className="bg-white rounded-lg shadow-sm border h-full overflow-hidden">
          <div className="p-4 border-b bg-gray-50">
            <div className="flex justify-between items-center">
              <div>
                <h1 className="text-2xl font-bold text-gray-900">Mon Calendrier</h1>
                <p className="text-gray-600">
                  {appointments?.length || 0} rendez-vous • {format(date, 'MMMM yyyy', { locale: fr })}
                </p>
              </div>
              <div className="flex items-center space-x-2">
                <div className="flex items-center space-x-1 text-xs">
                  <div className="w-3 h-3 bg-yellow-500 rounded"></div>
                  <span className="text-gray-600">À faire</span>
                </div>
                <div className="flex items-center space-x-1 text-xs">
                  <div className="w-3 h-3 bg-blue-500 rounded"></div>
                  <span className="text-gray-600">Confirmé</span>
                </div>
                <div className="flex items-center space-x-1 text-xs">
                  <div className="w-3 h-3 bg-green-500 rounded"></div>
                  <span className="text-gray-600">Terminé</span>
                </div>
                <div className="flex items-center space-x-1 text-xs">
                  <div className="w-3 h-3 bg-red-500 rounded"></div>
                  <span className="text-gray-600">Annulé</span>
                </div>
              </div>
            </div>
          </div>
          
          <div className="calendar-container" style={{ height: 'calc(100% - 100px)' }}>
            <Calendar
              localizer={localizer}
              events={events}
              date={date}
              view={view}
              onView={onView}
              onNavigate={onNavigate}
              onSelectEvent={onSelectEvent}
              startAccessor="start"
              endAccessor="end"
              style={{ 
                height: '100%',
                fontFamily: 'Inter, system-ui, sans-serif'
              }}
              components={{
                event: EventComponent,
                week: {
                  header: DayFormat
                },
                day: {
                  header: DayFormat
                }
              }}
              eventPropGetter={(event) => ({
                style: {
                  backgroundColor: getStatusColor(event.resource.status),
                  borderColor: getStatusColor(event.resource.status),
                  color: 'white',
                  border: 'none',
                  borderRadius: '4px',
                  fontSize: '11px',
                  padding: '2px 4px'
                }
              })}
              // Time constraints: 7 AM to 7 PM
              min={new Date(2025, 0, 1, 7, 0, 0)} // 7:00 AM
              max={new Date(2025, 0, 1, 19, 0, 0)} // 7:00 PM
              step={30}
              timeslots={2}
              popup
              popupOffset={20}
              views={['month', 'week', 'day']}
              showMultiDayTimes
              selectable={false}
              toolbar={true}
              scrollToTime={new Date(2025, 0, 1, 8, 0, 0)} // Scroll to 8:00 AM
              dayLayoutAlgorithm="no-overlap"
              messages={{
                next: "Suivant",
                previous: "Précédent",
                today: "Aujourd'hui",
                month: "Mois",
                week: "Semaine",
                day: "Jour",
                agenda: "Agenda",
                date: "Date",
                time: "Heure",
                event: "Événement",
                noEventsInRange: "Aucun rendez-vous dans cette période",
                allDay: "Toute la journée",
                tomorrow: "Demain",
                yesterday: "Hier"
              }}
              formats={{
                timeGutterFormat: (date: Date) => format(date, 'HH:mm', { locale: fr }),
                dayFormat: (date: Date) => format(date, 'dd/MM', { locale: fr }),
                dayHeaderFormat: (date: Date) => format(date, 'EEEE dd MMMM', { locale: fr }),
                monthHeaderFormat: (date: Date) => format(date, 'MMMM yyyy', { locale: fr }),
                dayRangeHeaderFormat: ({ start, end }: { start: Date; end: Date }) =>
                  `${format(start, 'dd MMM', { locale: fr })} - ${format(end, 'dd MMM yyyy', { locale: fr })}`
              }}
              culture="fr-FR"
            />
          </div>
        </div>
      </div>
    </div>
  );
};

export default CalendarMain;