# routers/auth_router.py
from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from db_connection import get_session
from models import Agent as AgentModel, RoleEnum
from schemas import AgentRead, LoginResponse
from utils.auth import authenticate_user, verify_password, create_access_token, get_current_user, require_role

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_session)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )
    access_token = create_access_token(data={"sub": user.Name, "role": user.Role})
    return {"access_token": access_token, "token_type": "bearer"}
# @router.get("/admin-only")
# def admin_dashboard(current_user: dict = Depends(require_role(RoleEnum.supervisor))):
#     return {"message": f"Hello {current_user['username']}, you are a supervisor!"}