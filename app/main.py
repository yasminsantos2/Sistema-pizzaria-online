from fastapi import FastAPI

from . import models
from .database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Sistema Pizzaria Online")


@app.get("/")
def root():
    return {"message": "API da pizzaria online"}
