from db_connection import engine
from sqlalchemy import text

try:
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        print("✅ Database connected successfully:", result.scalar())
except Exception as e:
    print("❌ Database connection failed:", e)

with engine.connect() as conn:
    result = conn.execute(text("SELECT TOP 5 * FROM Agents"))
    for row in result:
        print(row)