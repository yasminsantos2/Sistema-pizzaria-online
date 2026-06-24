from sqlalchemy import select
from sqlalchemy.orm import Session

from ..models import Pizza


class PizzaRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def adicionar_pizza(
        self,
        quantidade_sabores: int,
        valor_pizza: float,
        pedido_id: int,
    ) -> Pizza:
        pizza = Pizza(
            quantidade_sabores=quantidade_sabores,
            valor_pizza=valor_pizza,
            pedido_id=pedido_id,
        )
        self.db.add(pizza)
        self.db.commit()
        self.db.refresh(pizza)
        return pizza

    def excluir_pizza(self, pizza_id: int) -> bool:
        pizza = self.buscar_por_id(pizza_id)
        if pizza is None:
            return False
        self.db.delete(pizza)
        self.db.commit()
        return True

    def buscar_por_id(self, pizza_id: int) -> Pizza | None:
        return self.db.get(Pizza, pizza_id)

    def listar_por_pedido(self, pedido_id: int) -> list[Pizza]:
        stmt = select(Pizza).where(Pizza.pedido_id == pedido_id).order_by(Pizza.id)
        return list(self.db.scalars(stmt).all())

    def listar_todos(self) -> list[Pizza]:
        stmt = select(Pizza).order_by(Pizza.id)
        return list(self.db.scalars(stmt).all())
