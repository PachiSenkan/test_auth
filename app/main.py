from fastapi import FastAPI
from app.api.main import api_router
from app.models import Base
from app.core.db import engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(api_router, prefix="/api/v1")
