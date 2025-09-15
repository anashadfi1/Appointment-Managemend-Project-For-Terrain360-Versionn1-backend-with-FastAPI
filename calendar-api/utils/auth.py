# utils/auth.py
from datetime import datetime, timedelta
from typing import Optional, Dict
import os

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from jose.exceptions import ExpiredSignatureError
from sqlalchemy.orm import Session

from models import Agent
from db_connection import get_cca_session

# ---------------- ENV CONFIG ----------------
SECRET_KEY = os.getenv("SECRET_KEY", "super-secret-key")  # fallback for safety
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


# ---------------- PASSWORD UTILS ----------------
def verify_password(plain_password: str, stored_password: str) -> bool:
    """
    Verify password without hashing (plain comparison).
    ⚠️ Not secure for production — for demo/dev only.
    """
    return plain_password == stored_password


# ---------------- AUTHENTICATION ----------------
def authenticate_user(db: Session, username: str, password: str):
    """
    Authenticate agent by username + plain password.
    """
    user = db.query(Agent).filter(Agent.Name == username).first()
    if not user or not verify_password(password, user.Password):
        return None
    return user


# ---------------- JWT TOKEN UTILS ----------------
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create JWT with expiration.
    Payload must already contain required claims (sub, username, role).
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> dict:
    try:
        logger.debug(f"Decoding token: {token}")
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        logger.debug(f"Decoded payload: {payload}")
        return payload
    except ExpiredSignatureError:
        logger.error("Token has expired")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except JWTError as e:
        logger.error(f"JWT decode error: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


# ---------------- CURRENT USER ----------------
def get_current_agent(token: str = Depends(oauth2_scheme), db: Session = Depends(get_cca_session)) -> Agent:
    try:
        print("🔹 Raw token:", token)  # Debug
        payload = decode_access_token(token)
        print("🔹 Decoded payload:", payload)  # Debug

        agent_id = payload.get("sub")
        if agent_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        
        agent = db.query(Agent).filter(Agent.AgentID == int(agent_id)).first()
        if not agent:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
        return agent
    except Exception as e:
        print("❌ Exception in get_current_agent:", str(e))  # Debug
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"401: {str(e)}")





# ---------------- ROLE HELPERS ----------------
def get_role_name(role_type: int) -> str:
    role_mapping = {1: "supervisor", 2: "enqueteur"}
    return role_mapping.get(role_type, "unknown")


def require_role(allowed_roles: list[str]):
    """
    Dependency for role-based access control.
    Checks the role embedded in JWT payload.
    """
    def role_checker(agent: Agent = Depends(get_current_agent)):
        if agent.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough privileges",
            )
        return agent
    return role_checker
