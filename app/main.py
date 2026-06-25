from fastapi import FastAPI

from . import models
from .controllers import cliente_router
from .database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Sistema Pizzaria Online")
app.include_router(cliente_router)


@app.get("/")
def root():
    return {"message": "API da pizzaria online"}
