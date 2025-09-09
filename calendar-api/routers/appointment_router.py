from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from db_connection import get_statistics_session
from models import Appointment
from schemas import AppointmentUpdate, AppointmentResponse

router = APIRouter(
    prefix="/appointments",
    tags=["Appointments"]
)




# Get all appointments
@router.get("/", response_model=List[AppointmentResponse])
def get_appointments(db: Session = Depends(get_statistics_session)):
    return db.query(Appointment).all()


# Get single appointment by ID
@router.get("/{appointment_id}", response_model=AppointmentResponse)
def get_appointment(appointment_id: int, db: Session = Depends(get_statistics_session)):
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appointment


# Update appointment
@router.put("/{appointment_id}", response_model=AppointmentResponse)
def update_appointment(appointment_id: int, appointment_update: AppointmentUpdate, db: Session = Depends(get_statistics_session)):
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")

    for field, value in appointment_update.dict(exclude_unset=True).items():
        setattr(appointment, field, value)

    db.commit()
    db.refresh(appointment)
    return appointment


# Delete appointment
@router.delete("/{appointment_id}")
def delete_appointment(appointment_id: int, db: Session = Depends(get_statistics_session)):
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")

    db.delete(appointment)
    db.commit()
    return {"detail": "Appointment deleted"}
