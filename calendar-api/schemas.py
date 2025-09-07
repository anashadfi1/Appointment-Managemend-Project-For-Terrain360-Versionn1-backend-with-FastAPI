from pydantic import BaseModel,EmailStr
from enum import Enum
from datetime import date, datetime
from typing import List, Optional
from datetime import date


#Creating Enums schemas, used on our models

class RoleEnum(str, Enum):
    supervisor = "supervisor"
    enqueteur = "enqueteur"

class StateEnum(str,Enum):
    confirmed="confirmed"
    refused="refused"
    inquee="iquee"
    passed="passed"
    actuallypassing="actuallypassing"


#User Schemas

# Base schema (shared)
class AgentBase(BaseModel):
    UserName: Optional[str] = None
    Email: Optional[EmailStr] = None

#Agents schemas
class AgentRead(AgentBase):
    AgentID: int
    Record: bool
    MaxChatSessions: int
    Deleted: bool
    CreationTime: datetime
    LastModificationTime: datetime
    SoftphoneTrace: bool
    RecordStereo: bool

    class Config:
        from_attributes = True

# 🔑 Login response schema
class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    agent: AgentRead
    


# Base schema (shared properties)
class AppointmentBase(BaseModel):
    StartTime: datetime
    EndTime: datetime
    state: StateEnum
    description: str
    user_id: Optional[int] = None



# For updating existing appointment (all fields optional)
class AppointmentUpdate(BaseModel):
    StartTime: Optional[datetime] = None
    EndTime: Optional[datetime] = None
    state: Optional[StateEnum] = None
    description: Optional[str] = None
    user_id: Optional[int] = None


# For response (includes id)
class AppointmentResponse(AppointmentBase):
    id: int

    class Config:
        from_attributes = True