from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from typing import List

from db_connection import get_cca_session
from models import Agent, AgentSettings
from schemas import AgentResponse
from schemas import AppointmentResponse

router = APIRouter(
    prefix="/roles",
    tags=["roles"]
)


@router.get("/agents/", response_model=List[AgentResponse])
def get_agents_by_role(role: str, db: Session = Depends(get_cca_session)):
    """
    Get agents filtered by role (supervisor / enqueteur).    
    Usage:
    - GET /roles/agents/?role=supervisor  -> Returns agents with Type=1
    - GET /roles/agents/?role=enqueteur   -> Returns agents with Type=2
    """
    
    # Map role string to numeric Type value
    role_mapping = {
        "supervisor": 1,
        "enqueteur": 2
    }
    
    # Validate role parameter
    role_type = role_mapping.get(role)
    if not role_type:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid role. Must be one of: {list(role_mapping.keys())}"
        )
    
    # Query agents with the specified role type
    agents = (
        db.query(Agent)
        .join(Agent.settings)  # Ensure Agent.settings relationship exists
        .filter(AgentSettings.Type == role_type)
        .options(joinedload(Agent.settings))
        .all()
    )
    
    return agents
