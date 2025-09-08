'use client';

import React from 'react';
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Appointment } from '../../types/appointment';
import { formatDate, formatTime, getStatusLabel, getStatusColor } from '../../utils/calendarUtils';
import { Calendar, MapPin, Mail, Phone, User, Clock, FileText, X } from 'lucide-react';

interface AppointmentModalProps {
  appointment: Appointment;
  onClose: () => void;
  onDelete: (id: number) => void;
  open: boolean;
}

const AppointmentModal: React.FC<AppointmentModalProps> = ({
  appointment,
  onClose,
  onDelete,
  open
}) => {
  return (
    <Dialog open={open} onOpenChange={onClose}>
      <DialogContent className="max-w-2xl max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle className="flex items-center space-x-2 text-lg">
            <Calendar className="h-5 w-5" />
            Détails du rendez-vous
          </DialogTitle>
        </DialogHeader>
        
        <div className="space-y-6">
          {/* Client Information */}
          <div className="bg-gray-50 rounded-lg p-4">
            <div className="flex items-center space-x-2 mb-3">
              <User className="h-4 w-4" />
              Informations client
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-1">
                <label className="text-sm font-medium text-muted-foreground">
                  Nom du client
                </label>
                <p className="font-medium">{appointment.company.client_name}</p>
              </div>
              <div className="space-y-1">
                <div className="flex items-center space-x-1">
                  <MapPin className="h-3 w-3" />
                  Lieu
                </div>
                <p>{appointment.company.location}</p>
              </div>
              <div className="space-y-1">
                <div className="flex items-center space-x-1">
                  <Mail className="h-3 w-3" />
                  Email
                </div>
                <p className="text-blue-600">
                  <a href={`mailto:${appointment.company.contact_email}`}>
                    {appointment.company.contact_email}
                  </a>
                </p>
              </div>
              <div className="space-y-1">
                <div className="flex items-center space-x-1">
                  <Phone className="h-3 w-3" />
                  Téléphone
                </div>
                <p className="text-blue-600">
                  <a href={`tel:${appointment.company.contact_phone}`}>
                    {appointment.company.contact_phone}
                  </a>
                </p>
              </div>
            </div>
          </div>

          {/* Appointment Details */}
          <div className="bg-gray-50 rounded-lg p-4">
            <div className="flex items-center space-x-2 mb-3">
              <Clock className="h-4 w-4" />
              Détails du rendez-vous
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-1">
                <label className="text-sm font-medium text-muted-foreground">
                  Date et heure
                </label>
                <p className="font-medium">
                  {formatDate(appointment.appointment_time)} à {formatTime(appointment.appointment_time)}
                </p>
              </div>
              <div className="space-y-1">
                <label className="text-sm font-medium text-muted-foreground">
                  Statut
                </label>
                <span className={`inline-block px-3 py-1 text-sm rounded-full border ${getStatusColor(appointment.status)}`}>
                  {getStatusLabel(appointment.status)}
                </span>
              </div>
            </div>
          </div>

          {/* Agent Information */}
          <div className="bg-gray-50 rounded-lg p-4">
            <div className="flex items-center space-x-2 mb-3">
              <User className="h-4 w-4" />
              Informations agent
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-1">
                <label className="text-sm font-medium text-muted-foreground">
                  Agent assigné
                </label>
                <p className="font-medium">{appointment.agent.username}</p>
              </div>
              <div className="space-y-1">
                <label className="text-sm font-medium text-muted-foreground">
                  Email de l'agent
                </label>
                <p className="text-blue-600">{appointment.agent.email}</p>
              </div>
            </div>
          </div>

          {/* Notes */}
          {appointment.company.notes && (
            <div className="bg-gray-50 rounded-lg p-4">
              <div className="flex items-center space-x-2 mb-3">
                <FileText className="h-4 w-4" />
                Notes
              </div>
              <div className="space-y-1">
                <p className="text-muted-foreground whitespace-pre-wrap">
                  {appointment.company.notes}
                </p>
              </div>
            </div>
          )}

          {/* Actions */}
          <div className="flex justify-between pt-4 border-t">
            <Button variant="outline" onClick={onClose}>
              Fermer
            </Button>
            <Button 
              variant="destructive" 
              onClick={() => onDelete(appointment.id)}
            >
              Supprimer
            </Button>
          </div>
        </div>
      </DialogContent>
    </Dialog>
  );
};

export default AppointmentModal;