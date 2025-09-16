from fastapi import FastAPI
from sqlmodel import SQLModel
# from db_connection import engine
from routers import agents_router, appointment_router, auth_router, roles_router, calls_by_agents_router
from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost:3000",  # your Next.js dev server
    "http://127.0.0.1:3000"
]



app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# @app.on_event("startup")
# def on_startup():
#     SQLModel.metadata.create_all(engine)

app.include_router(agents_router.router)
app.include_router(appointment_router.router)
app.include_router(auth_router.router)
app.include_router(roles_router.router)
app.include_router(calls_by_agents_router.router)


