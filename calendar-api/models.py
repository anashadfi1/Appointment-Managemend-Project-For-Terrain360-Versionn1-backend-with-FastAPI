from enum import Enum
from typing import Optional, List
from datetime import datetime

from sqlmodel import SQLModel, Field, Relationship


# ---------------- ENUMS ---------------- #

class RoleEnum(str, Enum):
    supervisor = "superviseur"
    enqueteur = "enquêteur"


class StateEnum(str, Enum):
    confirmed = "confirmed"
    refused = "refused"
    inquee = "iquee"
    passed = "passed"
    actuallypassing = "actuallypassing"


# ---------------- MODELS ---------------- #

class StatisticAgent(SQLModel, table=True):
    __tablename__ = "Statistic_Agent"

    StatAgendID: Optional[int] = Field(default=None, primary_key=True, index=True)
    Inbound: bool
    DiversionOnBusy: bool
    DiversionOnNoAnswer: bool
    DiversionOnAgentPaused: bool
    OverflowNoMember: bool
    AgentDisconnected: bool

    # one-to-many
    appointments: List["Appointment"] = Relationship(back_populates="stat_agent")


class Appointment(SQLModel, table=True):
    __tablename__ = "Statistic_Appointment"

    StatsAppointmentID: Optional[int] = Field(default=None, primary_key=True, index=True)
    ListID: int
    ContactID: int
    CallID: int
    TimeUTC: datetime
    AppointmentTimeUTC: datetime

    AgentID: Optional[int] = Field(default=None, foreign_key="Statistic_Agent.StatAgendID")

    AppointmentOnlyForAgent: bool = Field(default=False)
    AppointmentMessage: Optional[str] = None
    AppointmentAckMessage: Optional[str] = None
    Importance: Optional[int] = None
    CallResult: Optional[int] = None
    CallSubResult: Optional[int] = None

    # many-to-one
    stat_agent: Optional[StatisticAgent] = Relationship(back_populates="appointments")

    def __repr__(self):
        return f"<Appointment(StatsAppointmentID={self.StatsAppointmentID}, AgentID={self.AgentID})>"


# models.py
class Agent(SQLModel, table=True):
    __tablename__ = "Agents"

    AgentID: Optional[int] = Field(default=None, primary_key=True)
    Name: Optional[str] = Field(default=None, max_length=255, unique=True)
    Email: Optional[str] = Field(default=None, max_length=50, unique=True)
    Password: str
    Description: str
    Record: bool
    MaxChatSessions: int
    Deleted: bool
    CreationTime: datetime
    LastModificationTime: datetime
    SoftphoneTrace: bool
    RecordStereo: bool

    settings: Optional["AgentSettings"] = Relationship(
        back_populates="agent", sa_relationship_kwargs={"uselist": False}  # ← key for one-to-one
    )


class AgentSettings(SQLModel, table=True):
    __tablename__ = "AgentSettings"

    ID: Optional[int] = Field(default=None, primary_key=True)
    AgentID: int = Field(foreign_key="Agents.AgentID")
    Type: int  
    Description: Optional[str] = Field(default=None, max_length=50)
    Value: int
    StringValue: Optional[str] = None
    DateTimeValue: Optional[datetime] = None

    agent: Optional[Agent] = Relationship(back_populates="settings")




class AgentsLoggedOn(SQLModel, table=True):
    __tablename__ = "AgentsLoggedOn"
    __table_args__ = {"schema": "dbo"}

    AgentID: Optional[int] = Field(default=None, primary_key=True)
    OutboundTaskID: Optional[int] = None

    calls: List["AskCalls"] = Relationship(back_populates="agent")

    def __repr__(self):
        return f"<AgentsLoggedOn(AgentID={self.AgentID}, OutboundTaskID={self.OutboundTaskID})>"


class AskCalls(SQLModel, table=True):
    __tablename__ = "AskCall10"
    __table_args__ = {"schema": "dbo"}

    AskInterview: int = Field(primary_key=True, index=True)
    AskTimeUTC: datetime = Field(primary_key=True, index=True)
    CallID: int
    AgentID: Optional[int] = Field(default=None, foreign_key="dbo.AgentsLoggedOn.AgentID")
    AskState: Optional[int] = None

    agent: Optional[AgentsLoggedOn] = Relationship(back_populates="calls")
