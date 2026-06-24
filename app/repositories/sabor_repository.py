from sqlalchemy import select
from sqlalchemy.orm import Session

from ..models import Sabor


class SaborRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def criar_sabor(self, nome_sabor: str, valor: float) -> Sabor:
        sabor = Sabor(nome_sabor=nome_sabor, valor=valor)
        self.db.add(sabor)
        self.db.commit()
        self.db.refresh(sabor)
        return sabor

    def buscar_por_id(self, sabor_id: int) -> Sabor | None:
        return self.db.get(Sabor, sabor_id)

    def consultar_por_nome(self, nome_sabor: str) -> Sabor | None:
        stmt = select(Sabor).where(Sabor.nome_sabor == nome_sabor)
        return self.db.scalars(stmt).first()

    def listar_todos(self) -> list[Sabor]:
        stmt = select(Sabor).order_by(Sabor.id)
        return list(self.db.scalars(stmt).all())
