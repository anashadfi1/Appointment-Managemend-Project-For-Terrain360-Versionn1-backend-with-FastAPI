from fastapi import FastAPI
from sqlmodel import SQLModel
# from db_connection import engine
from routers import agents_router, appointment_router, auth_router, roles_router, calls_by_agents_router

app = FastAPI()

# @app.on_event("startup")
# def on_startup():
#     SQLModel.metadata.create_all(engine)

app.include_router(agents_router.router)
app.include_router(appointment_router.router)
app.include_router(auth_router.router)
app.include_router(roles_router.router)
app.include_router(calls_by_agents_router.router)


