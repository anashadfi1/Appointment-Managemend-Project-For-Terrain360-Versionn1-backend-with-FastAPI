from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List

from db_connection import get_cca_session
from models import Agent, AgentSettings

router = APIRouter(prefix="/roles", tags=["Roles"])


@router.get("/agents/", response_model=List[Agent])
def get_agents_by_role(role: str, db: Session = Depends(get_cca_session)):
    role_mapping = {"supervisor": 1, "enqueteur": 2}
    role_type = role_mapping.get(role)

    if not role_type:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid role. Must be one of: {list(role_mapping.keys())}"
        )

    statement = (
        select(Agent)
        .join(Agent.settings)
        .where(AgentSettings.Type == role_type)
    )
    return db.exec(statement).all()
