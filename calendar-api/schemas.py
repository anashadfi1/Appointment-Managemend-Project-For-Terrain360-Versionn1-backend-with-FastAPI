from pydantic import BaseModel, EmailStr
from enum import Enum
from datetime import datetime
from typing import Optional, Literal


# -----------------------------
# ENUMS
# -----------------------------
class RoleEnum(str, Enum):
    supervisor = "superviseur"
    enqueteur = "enquêteur"


class StateEnum(str, Enum):
    confirmed = "confirmed"
    refused = "refused"
    inquee = "iquee"
    passed = "passed"
    actuallypassing = "actuallypassing"


# -----------------------------
# AGENT SCHEMAS
# -----------------------------
class AgentBase(BaseModel):
    Name: str
    # Password: str 


class AgentCreate(BaseModel):
    Name: str
    Password: str
    Email: Optional[str] = None
    Description: Optional[str] = None
    Role: RoleEnum = RoleEnum.enqueteur  # default
    Record: bool = False
    MaxChatSessions: int = 1
    Deleted: bool = False
    SoftphoneTrace: bool = False
    RecordStereo: bool = False

class AgentRead(AgentBase):
    AgentID: int
    Email: Optional[str] = None
    Description: Optional[str] = None
    Role: RoleEnum
    Record: bool
    MaxChatSessions: int
    Deleted: bool
    CreationTime: datetime
    LastModificationTime: datetime
    SoftphoneTrace: bool
    RecordStereo: bool

class AgentUpdate(AgentBase):
    AgentID: int
    Email: Optional[str] = None
    Description: Optional[str] = None 
    Record: bool
    MaxChatSessions: int
    Deleted: bool
    CreationTime: datetime
    LastModificationTime: datetime
    SoftphoneTrace: bool
    RecordStereo: bool
# -----------------------------
# AUTH SCHEMAS
# -----------------------------
class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    agent: AgentRead


# -----------------------------
# APPOINTMENT SCHEMAS
# -----------------------------
class AppointmentBase(BaseModel):
    StartTime: datetime
    EndTime: datetime
    state: StateEnum
    description: str
    user_id: Optional[int] = None


class AppointmentUpdate(BaseModel):
    StartTime: Optional[datetime] = None
    EndTime: Optional[datetime] = None
    state: Optional[StateEnum] = None
    description: Optional[str] = None
    user_id: Optional[int] = None


class AppointmentResponse(AppointmentBase):
    id: int

    class Config:
        from_attributes = True


# AgentSettings schema
class AgentSettingsBase(BaseModel):
    AgentID: int
    AppID: int
    Type: int   # 1 = supervisor, 2 = enqueteur
    Description: Optional[str] = None
    Value: int
    StringValue: Optional[str] = None
    DateTimeValue: Optional[datetime] = None


class AgentSettingsCreate(AgentSettingsBase):
    pass


class AgentSettingsResponse(AgentSettingsBase):
    ID: int

    class Config:
        orm_mode = True


# Agent schema
class AgentBase(BaseModel):
    Name: Optional[str] = None
    Email: Optional[str] = None
    Description: Optional[str] = None
    Record: bool
    MaxChatSessions: int
    Deleted: bool
    CreationTime: datetime
    LastModificationTime: datetime
    SoftphoneTrace: bool
    RecordStereo: bool


class AgentResponse(AgentBase):
    AgentID: int
    settings: Optional[AgentSettingsResponse] = None

    class Config:
        orm_mode = True