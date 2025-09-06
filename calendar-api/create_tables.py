# create_tables.py
from models import Base
from db_connection import engine  # your SQLAlchemy engine

Base.metadata.create_all(bind=engine)
print("Tables created successfully")
