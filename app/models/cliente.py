from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from ..database import Base


class Cliente(Base):
    __tablename__ = "clientes"

    id: Mapped[int] = mapped_column(primary_key=True)
    login: Mapped[str] = mapped_column(String(100), unique=True)
    senha: Mapped[str] = mapped_column(String(255))
    nome: Mapped[str] = mapped_column(String(100))
