from enum import Enum
from sqlalchemy import Column, Integer, String, Enum as SQLEnum, Date, ForeignKey, DateTime, Boolean, SmallInteger
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class RoleEnum(str, Enum):
    supervisor = "superviseur"
    enqueteur = "enquêteur"

class StateEnum(str,Enum):
    confirmed="confirmed"
    refused="refused"
    inquee="iquee"
    passed="passed"
    actuallypassing="actuallypassing"





class Agent(Base):
    __tablename__ = "Agents"

    AgentID = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String(255), nullable=True, unique=True)
    Email = Column(String(50), nullable=True, unique=True)
    Password = Column(String(255), nullable=False)
    Description = Column(String(255), nullable=False)
    Record = Column(Boolean, nullable=False)
    MaxChatSessions = Column(Integer, nullable=False)
    Deleted = Column(Boolean, nullable=False)
    CreationTime = Column(DateTime, nullable=False)
    LastModificationTime = Column(DateTime, nullable=False)
    SoftphoneTrace = Column(Boolean, nullable=False)
    RecordStereo = Column(Boolean, nullable=False)
    # ⚠️ Remove Role column because role comes from AgentSettings.Type
    # Role = Column(String(50), nullable=False)

    settings = relationship("AgentSettings", back_populates="agent")

    def __repr__(self):
        return f"<Agent(AgentID={self.AgentID}, Email={self.Email}, Name={self.Name})>"


class AgentSettings(Base):
    __tablename__ = "AgentSettings"

    ID = Column(Integer, primary_key=True, autoincrement=True)
    AgentID = Column(Integer, ForeignKey("Agents.AgentID"), nullable=False)
    AppID = Column(Integer, nullable=False)
    Type = Column(Integer, nullable=False)  # 1 = supervisor, 2 = enqueteur
    Description = Column(String(50), nullable=True)
    Value = Column(Integer, nullable=False)
    StringValue = Column(String, nullable=True)
    DateTimeValue = Column(DateTime, nullable=True)

    agent = relationship("Agent", back_populates="settings")

    def __repr__(self):
        return f"<AgentSettings(ID={self.ID}, AgentID={self.AgentID}, Type={self.Type})>"

class Appointment(Base):
    __tablename__ = "Statistic_WebInterview"
    __table_args__ = {"schema": "dbo"} 

    WebInterviewId = Column(Integer, primary_key=True, index=True)
    StartTime = Column(DateTime, nullable=True)
    EndTime = Column(DateTime, nullable=True)

    # Optional: you can map "LastState" if you want a state-like field
    LastState = Column(Integer, nullable=True)

    # user = relationship("User", back_populates="appointment")

class AskCalls(Base):
    __tablename__ = "AskCalls10"
    AskInterview = Column(Integer, primary_key=True, index=True, nullable=False)
    AskTimeUTC = Column(DateTime, primary_key=True, index=True, nullable=False)
    CallID = Column(Integer, nullable=False)
    AgentID = Column(Integer, ForeignKey("Agents.AgentID"), nullable=True)
    AskState = Column(SmallInteger, nullable=True)

    # other columns...

