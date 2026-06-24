from sqlalchemy import select
from sqlalchemy.orm import Session

from ..models import ItemBebida


class ItemBebidaRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def adicionar_item_bebida(
        self,
        valor_item_bebida: float,
        pedido_id: int,
        bebida_id: int,
    ) -> ItemBebida:
        item = ItemBebida(
            valor_item_bebida=valor_item_bebida,
            pedido_id=pedido_id,
            bebida_id=bebida_id,
        )
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def buscar_por_id(self, item_id: int) -> ItemBebida | None:
        return self.db.get(ItemBebida, item_id)

    def listar_por_pedido(self, pedido_id: int) -> list[ItemBebida]:
        stmt = (
            select(ItemBebida)
            .where(ItemBebida.pedido_id == pedido_id)
            .order_by(ItemBebida.id)
        )
        return list(self.db.scalars(stmt).all())

    def listar_todos(self) -> list[ItemBebida]:
        stmt = select(ItemBebida).order_by(ItemBebida.id)
        return list(self.db.scalars(stmt).all())
