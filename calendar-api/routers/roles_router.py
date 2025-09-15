from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from db_connection import get_cca_session
from models import Agent, AgentSettings
from schemas import AgentResponse
from sqlalchemy.orm import joinedload
from fastapi import HTTPException, status

router = APIRouter(
    prefix="/roles",
    tags=["roles"]
)


@router.get("/agents/", response_model=List[AgentResponse])
def get_agents_by_role(role: str, db: Session = Depends(get_cca_session)):
    """
    Get agents filtered by role (supervisor / enqueteur).    
    Usage:
    - GET /agents/?role=supervisor  -> Returns agents with Type=1
    - GET /agents/?role=enqueteur   -> Returns agents with Type=2
    """
    
    # Map role string to numeric Type value
    role_mapping = {
        "supervisor": 1,
        "enqueteur": 2
    }
    
    # Validate role parameter
    if role not in role_mapping:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid role. Must be one of: {list(role_mapping.keys())}"
        )
    
    # Get the numeric Type value for the role
    role_type = role_mapping[role]
    
    # Query agents with the specified role type
    agents = (
        db.query(Agent)
        .join(Agent.settings)  # Join with AgentSettings
        .filter(AgentSettings.Type == role_type)  # Filter by numeric Type
        .options(joinedload(Agent.settings))
        .all()
    )
    
    return agents
