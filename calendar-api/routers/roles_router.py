from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from db_connection import get_cca_session
from models import Agent, AgentSettings
from schemas import AgentResponse

router = APIRouter(
    prefix="/roles",
    tags=["roles"]
)


@router.get("/agents/", response_model=List[AgentResponse])
def get_agents_by_role(role: str, db: Session = Depends(get_cca_session)):
    """
    Get agents filtered by role (supervisor / enqueteur).
    Role is defined by AgentSettings.Type:
    - 1 = supervisor
    - 2 = enqueteur
    """
    type_mapping = {"supervisor": 1, "enqueteur": 2}
    role_type = type_mapping.get(role.lower())
    if role_type is None:
        return []  # return empty list instead of error for invalid role

    agents = (
        db.query(Agent)
        .join(AgentSettings, Agent.AgentID == AgentSettings.AgentID)
        .filter(AgentSettings.Type == role_type)
        .all()
    )

    return agents
