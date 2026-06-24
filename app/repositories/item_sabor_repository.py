from sqlalchemy import select
from sqlalchemy.orm import Session

from ..models import ItemSabor


class ItemSaborRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def adicionar_item_sabor(
        self,
        valor_item_sabor: float,
        pizza_id: int,
        sabor_id: int,
    ) -> ItemSabor:
        item = ItemSabor(
            valor_item_sabor=valor_item_sabor,
            pizza_id=pizza_id,
            sabor_id=sabor_id,
        )
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def buscar_por_id(self, item_id: int) -> ItemSabor | None:
        return self.db.get(ItemSabor, item_id)

    def listar_por_pizza(self, pizza_id: int) -> list[ItemSabor]:
        stmt = (
            select(ItemSabor)
            .where(ItemSabor.pizza_id == pizza_id)
            .order_by(ItemSabor.id)
        )
        return list(self.db.scalars(stmt).all())

    def listar_todos(self) -> list[ItemSabor]:
        stmt = select(ItemSabor).order_by(ItemSabor.id)
        return list(self.db.scalars(stmt).all())
