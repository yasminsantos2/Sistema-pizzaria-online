from datetime import date, time
from enum import IntEnum

from sqlalchemy import select
from sqlalchemy.orm import Session

from ..models import Pedido


class SituacaoPedido(IntEnum):
    PENDENTE = 1
    CONFIRMADO = 2
    FINALIZADO = 3


class PedidoRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def criar_pedido(
        self,
        numero_pedido: int,
        hora_pedido: time,
        data_pedido: date,
        cliente_id: int,
        situacao_pedido: int = SituacaoPedido.PENDENTE,
    ) -> Pedido:
        pedido = Pedido(
            numero_pedido=numero_pedido,
            hora_pedido=hora_pedido,
            data_pedido=data_pedido,
            situacao_pedido=situacao_pedido,
            cliente_id=cliente_id,
        )
        self.db.add(pedido)
        self.db.commit()
        self.db.refresh(pedido)
        return pedido

    def buscar_por_id(self, pedido_id: int) -> Pedido | None:
        return self.db.get(Pedido, pedido_id)

    def buscar_por_numero(self, numero_pedido: int) -> Pedido | None:
        stmt = select(Pedido).where(Pedido.numero_pedido == numero_pedido)
        return self.db.scalars(stmt).first()

    def listar_todos(self) -> list[Pedido]:
        stmt = select(Pedido).order_by(Pedido.id)
        return list(self.db.scalars(stmt).all())

    def listar_por_cliente(self, cliente_id: int) -> list[Pedido]:
        stmt = (
            select(Pedido)
            .where(Pedido.cliente_id == cliente_id)
            .order_by(Pedido.id)
        )
        return list(self.db.scalars(stmt).all())

    def confirmar_pedido(self, pedido_id: int) -> Pedido | None:
        return self._atualizar_situacao(pedido_id, SituacaoPedido.CONFIRMADO)

    def finalizar_pedido(self, pedido_id: int) -> Pedido | None:
        return self._atualizar_situacao(pedido_id, SituacaoPedido.FINALIZADO)

    def _atualizar_situacao(self, pedido_id: int, situacao: SituacaoPedido) -> Pedido | None:
        pedido = self.buscar_por_id(pedido_id)
        if pedido is None:
            return None
        pedido.situacao_pedido = situacao
        self.db.commit()
        self.db.refresh(pedido)
        return pedido
