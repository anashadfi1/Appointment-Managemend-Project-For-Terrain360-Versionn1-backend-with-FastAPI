# test_db_connections.py
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv
from pathlib import Path
import os

# Load .env explicitly
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

# Get database URLs
STATISTICS_DATABASE_URL = os.getenv("STATISTICS_DATABASE_URL")
LISTS_DATABASE_URL = os.getenv("LISTS_DATABASE_URL")
CCA_DATABASE_URL = os.getenv("CCA_DATABASE_URL")

# Check if any URL is None
if not STATISTICS_DATABASE_URL or not LISTS_DATABASE_URL or not CCA_DATABASE_URL:
    raise ValueError("One or more database URLs are not set in .env")

# Dictionary to iterate
databases = {
    "Statistics": STATISTICS_DATABASE_URL,
    "Lists": LISTS_DATABASE_URL,
    "CCA": CCA_DATABASE_URL
}

# Test connections
for name, url in databases.items():
    try:
        engine = create_engine(url)
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))  # Use sqlalchemy.text()
        print(f"[SUCCESS] Connection to {name} database succeeded.")
    except SQLAlchemyError as e:
        print(f"[FAILURE] Connection to {name} database failed!")
        print(f"Error: {e}")
