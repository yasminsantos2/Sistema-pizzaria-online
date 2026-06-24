from sqlalchemy import select
from sqlalchemy.orm import Session

from ..models import Cliente


class ClienteRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def registrar_cliente(self, login: str, senha: str, nome: str) -> Cliente:
        cliente = Cliente(login=login, senha=senha, nome=nome)
        self.db.add(cliente)
        self.db.commit()
        self.db.refresh(cliente)
        return cliente

    def logar_cliente(self, login: str, senha: str) -> Cliente | None:
        cliente = self.buscar_por_login(login)
        if cliente and cliente.senha == senha:
            return cliente
        return None

    def buscar_por_id(self, cliente_id: int) -> Cliente | None:
        return self.db.get(Cliente, cliente_id)

    def buscar_por_login(self, login: str) -> Cliente | None:
        stmt = select(Cliente).where(Cliente.login == login)
        return self.db.scalars(stmt).first()

    def listar_todos(self) -> list[Cliente]:
        stmt = select(Cliente).order_by(Cliente.id)
        return list(self.db.scalars(stmt).all())
