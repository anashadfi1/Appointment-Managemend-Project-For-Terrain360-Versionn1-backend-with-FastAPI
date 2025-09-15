import jwt   # this is PyJWT
import sys

SECRET_KEY = "your-secret-key"  # must match the one in your FastAPI app
ALGORITHM = "HS256"

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJBZ2VudCIsImV4cCI6MTc1Nzk0MjA4Nn0.ENaLJSNjQt4WI9Lw8xLFcIZAiEWs27N55v643NkBOA8"

try:
    decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    print("Decoded payload:", decoded)
except Exception as e:
    print("Error:", str(e))
