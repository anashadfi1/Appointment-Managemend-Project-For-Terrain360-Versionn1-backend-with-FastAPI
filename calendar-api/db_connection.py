from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Get database URLs from environment variables
STATISTICS_DATABASE_URL = os.getenv("STATISTICS_DATABASE_URL")
LISTS_DATABASE_URL = os.getenv("LISTS_DATABASE_URL")
CCA_DATABASE_URL = os.getenv("CCA_DATABASE_URL")

# Ensure none of the URLs are None
if not STATISTICS_DATABASE_URL or not LISTS_DATABASE_URL or not CCA_DATABASE_URL:
    raise ValueError("One or more database URLs are not set in .env")

# Create SQLAlchemy engines
statistics_engine = create_engine(STATISTICS_DATABASE_URL)
lists_engine = create_engine(LISTS_DATABASE_URL)
cca_engine = create_engine(CCA_DATABASE_URL)

# Create separate session factories for each database
SessionStatistics = sessionmaker(bind=statistics_engine, autoflush=False, autocommit=False)
SessionLists = sessionmaker(bind=lists_engine, autoflush=False, autocommit=False)
SessionCCA = sessionmaker(bind=cca_engine, autoflush=False, autocommit=False)

# Base classes for models (optional to separate)
BaseStatistics = declarative_base()
BaseLists = declarative_base()
BaseCCA = declarative_base()

# Dependency functions for FastAPI
def get_statistics_session():
    db = SessionStatistics()
    try:
        yield db
    finally:
        db.close()

def get_lists_session():
    db = SessionLists()
    try:
        yield db
    finally:
        db.close()

def get_cca_session():
    db = SessionCCA()
    try:
        yield db
    finally:
        db.close()
