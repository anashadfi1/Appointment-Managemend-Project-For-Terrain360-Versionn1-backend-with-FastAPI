from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from datetime import datetime

from db_connection import get_cca_session
from models import Agent

router = APIRouter(prefix="/agents", tags=["Agents"])


@router.get("/all", response_model=List[Agent])
def list_agents(db: Session = Depends(get_cca_session)):
    return db.exec(select(Agent)).all()


@router.get("/{agent_id}", response_model=Agent)
def get_agent(agent_id: int, db: Session = Depends(get_cca_session)):
    agent = db.exec(select(Agent).where(Agent.AgentID == agent_id)).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent


@router.post("/", response_model=Agent)
def create_agent(agent: Agent, db: Session = Depends(get_cca_session)):
    existing = db.exec(select(Agent).where(Agent.Name == agent.Name)).first()
    if existing:
        raise HTTPException(status_code=400, detail="Agent with this name already exists")

    agent.Description = f"{agent.Name}1234"
    agent.Password = f"{agent.Name}1234"  # default password
    agent.CreationTime = datetime.utcnow()
    agent.LastModificationTime = datetime.utcnow()

    db.add(agent)
    db.commit()
    db.refresh(agent)
    return agent


@router.put("/update_all")
def update_all_agents(db: Session = Depends(get_cca_session)):
    agents = db.exec(select(Agent)).all()

    if not agents:
        return {"message": "No agents found to update"}

    for agent in agents:
        new_value = f"{agent.Name}1234"
        agent.Description = new_value
        agent.Password = new_value
        agent.LastModificationTime = datetime.utcnow()

    db.add_all(agents)
    db.commit()
    return {"message": f"✅ Updated {len(agents)} agents"}
