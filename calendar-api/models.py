from enum import Enum
from sqlalchemy import Column, Integer, String, Enum as SQLEnum, Date, ForeignKey, DateTime, Boolean
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
    Role = Column(String(50), nullable=False)  # Store enum as string

    def __repr__(self):
        return f"<Agent(AgentID={self.AgentID}, Email={self.Email}, Name={self.Name}, Role={self.Role})>"

    def set_role(self, role: RoleEnum):
        if role.value not in [r.value for r in RoleEnum]:
            raise ValueError(f"Invalid role: {role}")
        self.Role = role.value
    def __repr__(self):
        return f"<Agent(AgentID={self.AgentID}, Email={self.Email}, UserName={self.UserName})>"

    # appointment = relationship("Appointment", back_populates="Agents", cascade="all, delete-orphan")

class Appointment(Base):
    __tablename__ = "Statistic_WebInterview"
    __table_args__ = {"schema": "dbo"} 

    WebInterviewId = Column(Integer, primary_key=True, index=True)
    StartTime = Column(DateTime, nullable=True)
    EndTime = Column(DateTime, nullable=True)

    # Optional: you can map "LastState" if you want a state-like field
    LastState = Column(Integer, nullable=True)

    # user = relationship("User", back_populates="appointment")

