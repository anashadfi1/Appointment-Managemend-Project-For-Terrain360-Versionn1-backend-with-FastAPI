from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from db_connection import get_statistics_session, get_cca_session
from models import Appointment as AppointmentModel, Agent  # <-- import Agent
from schemas import AppointmentResponse
from sqlalchemy.orm import joinedload


router = APIRouter(
    prefix="/appointments",
    tags=["Appointments"]
)

# Get all appointments

@router.get("/all", response_model=List[AppointmentResponse])
def get_appointments(db: Session = Depends(get_statistics_session)):
    appointments = db.query(AppointmentModel).all()
    return appointments


# Get single appointment by ID
@router.get("/{appointment_id}", response_model=AppointmentResponse)
def get_appointment(appointment_id: int, db: Session = Depends(get_statistics_session)):
    try:
        appointment = db.query(AppointmentModel).filter(AppointmentModel.StatsAppointmentID == appointment_id).first()
        if not appointment:
            raise HTTPException(status_code=404, detail="Appointment not found")
        return appointment
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Get appointments by agent
# @router.get("/by-agent/{agent_id}", response_model=AppointmentsByAgentResponse)
# def get_appointments_by_agent(agent_id: int, db: Session = Depends(get_cca_session)):
#     agent = db.query(Agent).filter(Agent.AgentID == agent_id).first()
#     if not agent:
#         raise HTTPException(status_code=404, detail="Agent not found")

#     appointments = db.query(AppointmentModel).filter(AppointmentModel.AgentID == agent_id).all()

#     return AppointmentsByAgentResponse(agent=agent, appointments=appointments)
