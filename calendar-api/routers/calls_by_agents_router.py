from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from db_connection import get_lists_session
from models import AskCalls, AgentsLoggedOn
from schemas import CallsByAgent, CallIDResponse

router = APIRouter(
    prefix="/calls",
    tags=["Calls"]
)



@router.get("/by-agent/{agent_id}", response_model=list[CallIDResponse])
def get_calls_by_agent_id(agent_id: int, db: Session = Depends(get_lists_session)):
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
