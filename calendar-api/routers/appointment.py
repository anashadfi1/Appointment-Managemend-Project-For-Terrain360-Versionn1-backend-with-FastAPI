# routers/appointment.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from db_connection import get_session
from models import Agent as AgentModel
from schemas import AgentRead

router = APIRouter(prefix="/appointments", tags=["Appointments"])


# Example: Get all appointments for a specific agent
@router.get("/agent/{agent_id}", response_model=AgentRead)
def get_agent_appointments(agent_id: int, session: Session = Depends(get_session)):
    agent = session.query(AgentModel).filter(AgentModel.AgentID == agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    # ⚠️ Replace with actual appointment query once you have Appointment model
    return agent
