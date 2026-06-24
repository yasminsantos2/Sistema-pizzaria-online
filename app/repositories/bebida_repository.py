from sqlalchemy import select
from sqlalchemy.orm import Session

from ..models import Bebida


class BebidaRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def criar_bebida(self, descricao: str, valor: float) -> Bebida:
        bebida = Bebida(descricao=descricao, valor=valor)
        self.db.add(bebida)
        self.db.commit()
        self.db.refresh(bebida)
        return bebida

    def buscar_por_id(self, bebida_id: int) -> Bebida | None:
        return self.db.get(Bebida, bebida_id)

    def atualizar_bebida(
        self,
        bebida_id: int,
        descricao: str | None = None,
        valor: float | None = None,
    ) -> Bebida | None:
        bebida = self.buscar_por_id(bebida_id)
        if bebida is None:
            return None
        if descricao is not None:
            bebida.descricao = descricao
        if valor is not None:
            bebida.valor = valor
        self.db.commit()
        self.db.refresh(bebida)
        return bebida

    def listar_todos(self) -> list[Bebida]:
        stmt = select(Bebida).order_by(Bebida.id)
        return list(self.db.scalars(stmt).all())
