from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select

from db_connection import get_cca_session
from models import Agent
from utils.auth import authenticate_user, create_access_token, get_current_agent, require_role

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_cca_session),
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    role_map = {1: "supervisor", 2: "enqueteur"}
    role_setting = next(iter(user.settings), None)
    role = role_map.get(role_setting.Type) if role_setting else None

    access_token = create_access_token(
        data={"sub": str(user.AgentID), "username": user.Name, "role": role}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "agent_id": user.AgentID,
        "username": user.Name,
        "email": user.Email,
        "role": role,
    }


@router.get("/me")
def read_current_agent(current_agent: Agent = Depends(get_current_agent)):
    return current_agent


@router.get("/supervisor-only", dependencies=[Depends(require_role(["supervisor"]))])
def supervisor_area():
    return {"message": "Welcome Supervisor! 🎩"}
