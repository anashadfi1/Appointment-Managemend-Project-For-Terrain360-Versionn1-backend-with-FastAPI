from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from db_connection import get_lists_session
from models import Appointment, AskCalls
from schemas import AppointmentUpdate, CallIDResponse, CallsByAgent

router = APIRouter(
    prefix="/appointments",
    tags=["Appointments"]
)




# Get all appointments
@router.get("/", response_model=List[CallIDResponse])
def get_appointments(db: Session = Depends(get_lists_session)):
    return db.query(AskCalls).all()


# Get single appointment by ID
@router.get("/{call_id}", response_model=CallIDResponse)
def get_appointment(call_id: int, db: Session = Depends(get_lists_session)):
    try:
        call = db.query(AskCalls).filter(AskCalls.CallID == call_id).first()
        if not call:
            raise HTTPException(status_code=404, detail="Appointment not found")
        return call
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
