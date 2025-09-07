# routers/auth_router.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from db_connection import get_session
from models import Agent as AgentModel
from schemas import AgentRead, LoginResponse
from utils.auth import verify_password, create_access_token, hash_password

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login", response_model=LoginResponse)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session)
):
    agent = session.query(AgentModel).filter(AgentModel.UserName == form_data.username).first()
    if not agent:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    if not verify_password(form_data.password, agent.Password):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    token = create_access_token({"sub": str(agent.AgentID)})
    return LoginResponse(
        access_token=token,
        token_type="bearer",
        agent=agent
    )


