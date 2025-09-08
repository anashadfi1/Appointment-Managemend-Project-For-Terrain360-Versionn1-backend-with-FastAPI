# agents_router.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from db_connection import get_session
from models import Agent as AgentModel  # SQLAlchemy model
from schemas import AgentRead, AgentCreate, AgentUpdate # Pydantic schemas

router = APIRouter(prefix="/agents", tags=["Agents"])


# ✅ List all agents
@router.get("/", response_model=List[AgentRead])
def list_agents(session: Session = Depends(get_session)):
    agents = session.query(AgentModel).all()
    return agents


# ✅ Get agent by ID
@router.get("/{agent_id}", response_model=AgentRead)
def get_agent(agent_id: int, session: Session = Depends(get_session)):
    agent = session.query(AgentModel).filter(AgentModel.AgentID == agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent


# ✅ Create new agent
@router.post("/", response_model=AgentRead)
def create_agent(agent: AgentCreate, session: Session = Depends(get_session)):
    # check if name already exists
    db_agent = session.query(AgentModel).filter(AgentModel.Name == agent.Name).first()
    if db_agent:
        raise HTTPException(status_code=400, detail="Agent with this name already exists")

    # create description as "Name1234"
    description = f"{agent.Name}1234"

    new_agent = AgentModel(
    Name=agent.Name,
    Password=f"{agent.Name}1234",  # default password
    Email=agent.Email,
    Description=description,
    Record=agent.Record,
    MaxChatSessions=agent.MaxChatSessions,
    Deleted=agent.Deleted,
    CreationTime=datetime.utcnow(),
    LastModificationTime=datetime.utcnow(),
    SoftphoneTrace=agent.SoftphoneTrace,
    RecordStereo=agent.RecordStereo,
    )


    session.add(new_agent)
    session.commit()
    session.refresh(new_agent)

    return new_agent


# ✅ Update all agents → set Password & Description = Name1234
@router.put("/update_all")
def update_all_agents(session: Session = Depends(get_session)):
    agents = session.query(AgentModel).all()

    if not agents:
        return {"message": "No agents found to update"}

    for agent in agents:
        new_value = f"{agent.Name}1234"
        agent.Description = new_value
        agent.Password = new_value
        agent.LastModificationTime = datetime.utcnow()

    session.commit()

    return {"message": f"✅ Updated {len(agents)} agents with Name1234 as password & description"}
