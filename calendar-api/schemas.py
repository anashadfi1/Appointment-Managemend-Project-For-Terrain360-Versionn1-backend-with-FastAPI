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
    Email: Optional[EmailStr] = None
    UserName: Optional[str] = None


# Schema for creating a new Agent
class AgentCreate(AgentBase):
    Record: bool
    MaxChatSessions: int
    Deleted: bool
    CreationTime: datetime
    LastModificationTime: datetime
    SoftphoneTrace: bool
    RecordStereo: bool


# Schema for reading Agent data (includes AgentID instead of UserID)
class AgentRead(AgentBase):
    AgentID: int   # ✅ FIXED: was UserID before
    Record: bool
    MaxChatSessions: int
    Deleted: bool
    CreationTime: datetime
    LastModificationTime: datetime
    SoftphoneTrace: bool
    RecordStereo: bool

    class Config:
        orm_mode = True

# appointments schemas
class AppointmentBase(BaseModel):
    date: date
    hour: int
    minute: int
    description: str

class AppointmentCreate(AppointmentBase):
    user_id: Optional[int]

class Appointment(AppointmentBase):
    id: int
    user_id: Optional[int]

    class Config:
        from_attributes = True




class AppointmentBase(BaseModel):
    date: date
    hour: int
    minute: int

class AppointmentCreate(AppointmentBase):
    user_id: Optional[int]

class Appointment(AppointmentBase):
    id: int
    user_id: Optional[int]

    class Config:
        from_attributes = True

