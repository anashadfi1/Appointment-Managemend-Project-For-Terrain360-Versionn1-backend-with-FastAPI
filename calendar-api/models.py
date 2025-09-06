from enum import Enum
from sqlalchemy import Column, Integer, String, Enum as SQLEnum, Date, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class RoleEnum(str, Enum):
    supervisor = "supervisor"
    enqueteur = "enqueteur"

class StateEnum(str,Enum):
    confirmed="confirmed"
    refused="refused"
    inquee="iquee"
    passed="passed"
    actuallypassing="actuallypassing"

# class User(Base):
#     __tablename__ = "Agents"

#     id = Column(Integer, primary_key=True, index=True)
#     username = Column(String(50), unique=True, index=True, nullable=False)
#     password = Column(String(255), nullable=False)
#     email = Column(String(255), unique=True, index=True, nullable=False)
#     description = Column(String(255), nullable=True)
#     role = Column(SQLEnum(RoleEnum), nullable=False)
#     lastmodificationtine = Column(DateTime, nullable=False)
#     maxchatsessions = Column(Integer, nullable=True)


class Agent(Base):
    __tablename__ = "Agents"

    AgentID = Column(Integer, primary_key=True, autoincrement=True)
    Record = Column(Boolean, nullable=False)
    MaxChatSessions = Column(Integer, nullable=False)
    Deleted = Column(Boolean, nullable=False)
    CreationTime = Column(DateTime, nullable=False)
    LastModificationTime = Column(DateTime, nullable=False)
    SoftphoneTrace = Column(Boolean, nullable=False)
    RecordStereo = Column(Boolean, nullable=False)
    Email = Column(String(50), nullable=True)
    UserName = Column(String(255), nullable=True)

    def __repr__(self):
        return f"<Agent(AgentID={self.AgentID}, Email={self.Email}, UserName={self.UserName})>"

    # appointment = relationship("Appointment", back_populates="user", cascade="all, delete-orphan")

class Appointment(Base):
    __tablename__ = "appointment"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False)
    hour = Column(Integer, nullable=False)
    minute = Column(Integer, nullable=False) 
    state = Column(SQLEnum(RoleEnum),nullable=False)
    description =  Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    # user = relationship("User", back_populates="appointment")

