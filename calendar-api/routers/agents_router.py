# agents_router.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from db_connection import get_session
from models import Agent as AgentModel  # SQLAlchemy model
from schemas import AgentRead# Pydantic schemas

router = APIRouter(prefix="/agents", tags=["Agents"])


# List all agents
@router.get("/", response_model=List[AgentRead])
def list_agents(session: Session = Depends(get_session)):
    agents = session.query(AgentModel).all()
    return agents


# Get agent by ID
@router.get("/{agent_id}", response_model=AgentRead)
def get_agent(agent_id: int, session: Session = Depends(get_session)):
    agent = session.query(AgentModel).filter(AgentModel.AgentID == agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent



