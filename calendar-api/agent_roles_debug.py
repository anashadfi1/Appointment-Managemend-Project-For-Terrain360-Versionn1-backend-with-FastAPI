# debug_agents.py

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, joinedload
from models import Agent, AgentSettings  # import your models

# Load environment variables from .env
load_dotenv()

# Get DB URL from .env
DATABASE_URL = os.getenv("CCA_DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("❌ CCA_DATABASE_URL is not set in .env file")

# Create engine
engine = create_engine(DATABASE_URL, echo=True)  # echo=True prints SQL
SessionLocal = sessionmaker(bind=engine)

# def debug_agents_by_role(role: str):
#     type_mapping = {"supervisor": 1, "enqueteur": 2}
#     role_type = type_mapping.get(role.lower())
#     if role_type is None:
#         print(f"Invalid role: {role}")
#         return []

#     with SessionLocal() as db:
#         agents = (
#             db.query(Agent)
#             .join(Agent.settings)  # join via relationship
#             .options(joinedload(Agent.settings))
#             .filter(AgentSettings.Type == role_type)
#             .all()
#         )

#         print(f"\n=== Agents with role '{role}' (Type={role_type}) ===")
#         for agent in agents:
#             print(
#                 f"AgentID={agent.AgentID}, "
#                 f"Name={agent.Name}, "
#                 f"Settings={[s.Type for s in agent.settings]}"
#             )

#         return agents

// Complete test - replace with your actual username and password
fetch('http://localhost:8000/auth/login', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/x-www-form-urlencoded',
  },
  body: 'username=Administrator&password=Administrator1234'
})
.then(response => response.json())
.then(loginData => {
  console.log('Login response:', loginData);
  
  if (loginData.access_token) {
    const token = loginData.access_token;
    console.log('Token received:', token);
    
    // Test the token with test-auth endpoint
    return fetch('http://localhost:8000/auth/test-auth', {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
  } else {
    throw new Error('No access token received');
  }
})
.then(response => response.json())
.then(testData => {
  console.log('Test auth response:', testData);
  
  // If test-auth works, try the actual /me endpoint
  if (testData.status === 'success') {
    // Get the token again for the /me request
    return fetch('http://localhost:8000/auth/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: 'username=YOUR_ACTUAL_USERNAME&password=YOUR_ACTUAL_PASSWORD'
    })
    .then(response => response.json())
    .then(loginData => {
      return fetch('http://localhost:8000/auth/me', {
        headers: {
          'Authorization': `Bearer ${loginData.access_token}`
        }
      });
    });
  }
})
.then(response => {
  console.log('/me response status:', response.status);
  return response.json();
})
.then(meData => {
  console.log('/me response data:', meData);
})
.catch(error => {
  console.error('Error:', error);
});
if __name__ == "__main__":
    # Test both roles
    debug_agents_by_role("supervisor")
    debug_agents_by_role("enqueteur")
