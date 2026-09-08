from fastapi import FastAPI
from app.database import Base,engine
from app.models import User
from app.routers import auth


app=FastAPI()

Base.metadata.create_all(bind=engine)
app.include_router(auth.router)