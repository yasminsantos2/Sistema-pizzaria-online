from fastapi import Depends, FastAPI
from sqlalchemy import select
from sqlalchemy.orm import Session

from . import models
from .database import Base, engine, get_db

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Sistema Pizzaria Online")

@app.get("/")
def root():
    return {"message": "API da pizzaria online"}

@app.get("/users")
def list_users(db: Session = Depends(get_db)):
    users = db.scalars(select(models.User)).all()
    return users