# routers/auth_router.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from db_connection import get_cca_session
from models import Agent as AgentModel
from schemas import AgentRead
from utils.auth import authenticate_user, create_access_token, get_current_agent, require_role

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_cca_session),
):
    """
    Authenticate the agent and return a JWT access token containing:
    - AgentID (sub)
    - Username (Name)
    - Role (from AgentSettings.Type)
    """
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Map Type → Role string
    role_map = {1: "supervisor", 2: "enqueteur"}

    # Some agents may have multiple settings, just take the first
    role_setting = next(iter(user.settings), None)
    role = role_map.get(role_setting.Type) if role_setting else None

    # Create token with sub, username, role
    access_token = create_access_token(
        data={
            "sub": str(user.AgentID),  # unique ID
            "username": user.Name,
            "role": role,
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "agent_id": user.AgentID,
        "username": user.Name,
        "email": user.Email,
        "role": role,
    }


@router.get("/me", response_model=AgentRead)
def read_current_agent(current_agent: AgentModel = Depends(get_current_agent)):
    """Return the currently authenticated agent based on JWT token."""
    return current_agent


@router.get("/supervisor-only", dependencies=[Depends(require_role(["supervisor"]))])
def supervisor_area():
    return {"message": "Welcome Supervisor! 🎩"}

# @router.get("/secure")
# def secure_route(current_user: Agent = Depends(get_current_agent)):
#     return {"msg": f"Hello {current_user.Name}, role={current_user.role}"}
