from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List

from db_connection import get_statistics_session
from models import Appointment

router = APIRouter(prefix="/appointments", tags=["Appointments"])


@router.get("/", response_model=List[Appointment])
def list_appointments(db: Session = Depends(get_statistics_session)):
    return db.exec(select(Appointment)).all()


@router.get("/{appointment_id}", response_model=Appointment)
def get_appointment(appointment_id: int, db: Session = Depends(get_statistics_session)):
    appointment = db.exec(select(Appointment).where(Appointment.StatsAppointmentID == appointment_id)).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appointment


@router.post("/", response_model=Appointment)
def create_appointment(appointment: Appointment, db: Session = Depends(get_statistics_session)):
    db.add(appointment)
    db.commit()
    db.refresh(appointment)
    return appointment
