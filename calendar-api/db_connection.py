# db_connection.py
from sqlmodel import Session, create_engine, SQLModel
from dotenv import load_dotenv
import os

# ---------------- Load environment variables ---------------- #
load_dotenv()

STATISTICS_DATABASE_URL = os.getenv("STATISTICS_DATABASE_URL")
LISTS_DATABASE_URL = os.getenv("LISTS_DATABASE_URL")
CCA_DATABASE_URL = os.getenv("CCA_DATABASE_URL")

if not STATISTICS_DATABASE_URL or not LISTS_DATABASE_URL or not CCA_DATABASE_URL:
    raise ValueError("❌ One or more database URLs are not set in .env")

# ---------------- Engines ---------------- #
statistics_engine = create_engine(STATISTICS_DATABASE_URL, echo=False)
lists_engine = create_engine(LISTS_DATABASE_URL, echo=False)
cca_engine = create_engine(CCA_DATABASE_URL, echo=False)

# ---------------- Session factories ---------------- #
def get_statistics_session():
    """Yield a SQLModel session for the Statistics DB."""
    with Session(statistics_engine) as session:
        yield session

def get_lists_session():
    """Yield a SQLModel session for the Lists DB."""
    with Session(lists_engine) as session:
        yield session

def get_cca_session():
    """Yield a SQLModel session for the CCA DB."""
    with Session(cca_engine) as session:
        yield session

# ---------------- Optional: Table creation ---------------- #
def init_db():
    """Call this once at startup if you want SQLModel to ensure tables exist."""
    SQLModel.metadata.create_all(statistics_engine)
    SQLModel.metadata.create_all(lists_engine)
    SQLModel.metadata.create_all(cca_engine)
