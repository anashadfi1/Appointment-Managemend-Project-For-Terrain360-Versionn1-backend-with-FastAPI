from pydantic import BaseModel
from enum import Enum
from datetime import datetime
from typing import Optional, List

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


class AgentCreate(BaseModel):
    Name: str
    Password: str
    Email: Optional[str] = None
    Description: Optional[str] = None
    Record: bool = False
    MaxChatSessions: int = 1
    Deleted: bool = False
    SoftphoneTrace: bool = False
    RecordStereo: bool = False


class AgentRead(AgentBase):
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

    class Config:
        from_attributes = True


class AgentResponse(BaseModel):
    AgentID: int
    Name: Optional[str]
    Email: Optional[str]

    class Config:
        from_attributes = True


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
    ListID: int
    ContactID: int
    CallID: int
    TimeUTC: datetime
    AgentID: int  # FK to StatisticAgent
    AppointmentOnlyForAgent: bool
    AppointmentTimeUTC: datetime
    AppointmentMessage: str
    AppointmentAckMessage: str
    Importance: int
    CallResult: int
    CallSubResult: int


class AppointmentResponse(AppointmentBase):
    StatsAppointmentID: int  # PK
    class Config:
        from_attributes = True


# Grouped appointments by StatisticAgent
class AppointmentsByStatisticAgentResponse(BaseModel):
    StatAgentID: int
    appointments: List[AppointmentResponse]
    class Config:
        from_attributes = True


# -----------------------------
# AGENT SETTINGS
# -----------------------------
class AgentSettingsBase(BaseModel):
    AgentID: int
    AppID: int
    Type: int   # 1 = supervisor, 2 = enqueteur
    Description: Optional[str] = None
    Value: int
    StringValue: Optional[str] = None
    DateTimeValue: Optional[datetime] = None


class AgentSettingsResponse(AgentSettingsBase):
    ID: int

    class Config:
        from_attributes = True


# -----------------------------
# STATISTIC AGENT SCHEMAS
# -----------------------------
class StatisticAgentBase(BaseModel):
    Inbound: bool
    DiversionOnBusy: bool
    DiversionOnNoAnswer: bool
    DiversionOnAgentPaused: bool
    OverflowNoMember: bool
    AgentDisconnected: bool


class StatisticAgentResponse(StatisticAgentBase):
    StatAgentID: int
    appointments: List[AppointmentResponse] = []  # One-to-Many

    class Config:
        from_attributes = True
