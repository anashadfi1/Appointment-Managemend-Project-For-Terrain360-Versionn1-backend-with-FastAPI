from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from db_connection import get_session  # your database session dependency
from models import AskCalls, Agent  # your SQLAlchemy models
from schemas import CallsByAgent, CallIDResponse # Pydantic schema for response

router = APIRouter(
    prefix="/calls",
    tags=["Calls"]
)

@router.get("/by-agent", response_model=list[CallsByAgent])
def get_calls_by_agent(db: Session = Depends(get_session)):
    try:
        results = (
            db.query(
                AskCalls.AgentID,
                Agent.Name.label("AgentName"),
                func.count(AskCalls.AgentID).label("TotalCalls")
            )
            .join(Agent, AskCalls.AgentID == Agent.AgentID)
            .group_by(AskCalls.AgentID, Agent.Name)
            .all()
        )

        return [
            CallsByAgent(
                AgentID=row.AgentID,
                AgentName=row.AgentName,
                TotalCalls=row.TotalCalls
            )
            for row in results
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/by-agent/{agent_id}", response_model=list[CallIDResponse])
def get_calls_by_agent_id(agent_id: int, db: Session = Depends(get_session)):
    try:
        calls = (
            db.query(AskCalls.CallID)
            .filter(AskCalls.AgentID == agent_id)
            .all()
        )

        if not calls:
            raise HTTPException(status_code=404, detail="No calls found for this AgentID")

        return [CallIDResponse(CallID=c.CallID) for c in calls]

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))