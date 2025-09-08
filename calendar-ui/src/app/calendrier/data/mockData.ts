export interface Appointment {
  id: number;
  appointment_time: string; // ISO datetime string
  status: string; // "a faire", etc.
  company: {
    client_name: string;
    notes: string;
    location: string;
    contact_email: string;
    contact_phone: string;
    id: number;
  };
  agent: {
    username: string;
    email: string;
    id: number;
  };
}

// Legacy interface for backward compatibility
export interface LegacyAppointment {
  id: number;
  clientName: string;
  company: string;
  date: string;
  startTime: string;
  endTime: string;
  type: 'meeting' | 'call' | 'presentation' | 'consultation';
  status: 'confirmed' | 'pending' | 'completed' | 'cancelled';
  notes: string;
  agentId: number;
  agentName: string;
  location?: string;
  contactEmail?: string;
  contactPhone?: string;
}