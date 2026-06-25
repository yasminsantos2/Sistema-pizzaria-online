from collections.abc import Generator

from fastapi import Depends
from sqlalchemy.orm import Session

from .database import SessionLocal
from .repositories.cliente_repository import ClienteRepository
from .services.cliente_service import ClienteService


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_cliente_service(db: Session = Depends(get_db)) -> ClienteService:
    return ClienteService(ClienteRepository(db))
