# # test_db_connections.py
# from sqlalchemy import create_engine, text
# from sqlalchemy.exc import SQLAlchemyError
# from dotenv import load_dotenv
# from pathlib import Path
# import os

# # Load .env explicitly
# env_path = Path(__file__).parent / ".env"
# load_dotenv(dotenv_path=env_path)

# # Get database URLs
# STATISTICS_DATABASE_URL = os.getenv("STATISTICS_DATABASE_URL")
# LISTS_DATABASE_URL = os.getenv("LISTS_DATABASE_URL")
# CCA_DATABASE_URL = os.getenv("CCA_DATABASE_URL")

# # Check if any URL is None
# if not STATISTICS_DATABASE_URL or not LISTS_DATABASE_URL or not CCA_DATABASE_URL:
#     raise ValueError("One or more database URLs are not set in .env")

# # Dictionary to iterate
# databases = {
#     "Statistics": STATISTICS_DATABASE_URL,
#     "Lists": LISTS_DATABASE_URL,
#     "CCA": CCA_DATABASE_URL
# }

# # Test connections
# for name, url in databases.items():
#     try:
#         engine = create_engine(url)
#         with engine.connect() as conn:
#             conn.execute(text("SELECT 1"))  # Use sqlalchemy.text()
#         print(f"[SUCCESS] Connection to {name} database succeeded.")
#     except SQLAlchemyError as e:
#         print(f"[FAILURE] Connection to {name} database failed!")
#         print(f"Error: {e}")

# import logging
# from jose import jwt, JWTError, ExpiredSignatureError
# from fastapi import HTTPException, status

# # Setup logging
# logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")
# logger = logging.getLogger(__name__)

# # Config (you should import these from your settings or utils)
# SECRET_KEY = "supersecret"
# ALGORITHM = "HS256"


# def decode_access_token(token: str):
#     logger.debug("Decoding access token...")

#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         logger.debug(f"Token decoded successfully: {payload}")
#         return payload

#     except ExpiredSignatureError:
#         logger.warning("Token has expired.")
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Token has expired",
#             headers={"WWW-Authenticate": "Bearer"},
#         )

#     except JWTError as e:
#         logger.error(f"JWT error while decoding token: {str(e)}")
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Could not validate credentials",
#             headers={"WWW-Authenticate": "Bearer"},
#         )


# if __name__ == '__main__':
#     # Example usage
#     fake_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIzIiwidXNlcm5hbWUiOiJBZ2VudCIsInJvbGUiOiJzdXBlcnZpc29yIiwiZXhwIjoxNzU3ODY4NDc2fQ.tNEfR-Y0hocLVUFiAtMSx95e2wwF6XfsOQB41NFTYTk"
#     try:
#         decode_access_token(fake_token)
#     except Exception as e:
#         logger.exception("Error while decoding token")

from utils.auth import create_access_token
from utils.auth import decode_access_token, SECRET_KEY
token = create_access_token( {
"sub":"Agent",
"username":"Agent",
"role":"supervisor"
})
print("Generated token:", token)
print("Decoded token:", decode_access_token(token))
print(repr(SECRET_KEY))

# test_script.py
# from utils.auth import create_access_token, decode_access_token, SECRET_KEY

# # --- Step 1: Create a token ---
# payload = {
#     "sub": "Agent",  # this can be any identifier, e.g., AgentID
#     "role": "supervisor"  # optional, add role to test role-based access
# }
# token = create_access_token(payload)

# print("✅ Generated token:")
# print(token)

# # --- Step 2: Decode the token ---
# decoded_payload = decode_access_token(token)
# print("\n✅ Decoded token payload:")
# print(decoded_payload)

# # --- Step 3: Show the secret key being used ---
# print("\n🔑 SECRET_KEY used for encoding/decoding:")
# print(repr(SECRET_KEY))
