from datetime import date, time

from sqlalchemy import BigInteger, Date, Float, ForeignKey, Integer, String, Time
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


class Cliente(Base):
    __tablename__ = "clientes"

    id: Mapped[int] = mapped_column(primary_key=True)
    login: Mapped[str] = mapped_column(String(100), unique=True)
    senha: Mapped[str] = mapped_column(String(255))
    nome: Mapped[str] = mapped_column(String(100))

    pedidos: Mapped[list["Pedido"]] = relationship(back_populates="cliente")


class Pedido(Base):
    __tablename__ = "pedidos"

    id: Mapped[int] = mapped_column(primary_key=True)
    numero_pedido: Mapped[int] = mapped_column(BigInteger, unique=True)
    hora_pedido: Mapped[time] = mapped_column(Time)
    data_pedido: Mapped[date] = mapped_column(Date)
    situacao_pedido: Mapped[int] = mapped_column(Integer)
    cliente_id: Mapped[int] = mapped_column(ForeignKey("clientes.id"))

    cliente: Mapped["Cliente"] = relationship(back_populates="pedidos")
    pizzas: Mapped[list["Pizza"]] = relationship(back_populates="pedido")
    itens_bebida: Mapped[list["ItemBebida"]] = relationship(back_populates="pedido")


class Pizza(Base):
    __tablename__ = "pizzas"

    id: Mapped[int] = mapped_column(primary_key=True)
    quantidade_sabores: Mapped[int] = mapped_column(Integer)
    valor_pizza: Mapped[float] = mapped_column(Float)
    pedido_id: Mapped[int] = mapped_column(ForeignKey("pedidos.id"))

    pedido: Mapped["Pedido"] = relationship(back_populates="pizzas")
    itens_sabor: Mapped[list["ItemSabor"]] = relationship(back_populates="pizza")


class Sabor(Base):
    __tablename__ = "sabores"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome_sabor: Mapped[str] = mapped_column(String(100))
    valor: Mapped[float] = mapped_column(Float)

    itens_sabor: Mapped[list["ItemSabor"]] = relationship(back_populates="sabor")


class ItemSabor(Base):
    __tablename__ = "item_sabores"

    id: Mapped[int] = mapped_column(primary_key=True)
    valor_item_sabor: Mapped[float] = mapped_column(Float)
    pizza_id: Mapped[int] = mapped_column(ForeignKey("pizzas.id"))
    sabor_id: Mapped[int] = mapped_column(ForeignKey("sabores.id"))

    pizza: Mapped["Pizza"] = relationship(back_populates="itens_sabor")
    sabor: Mapped["Sabor"] = relationship(back_populates="itens_sabor")


class Bebida(Base):
    __tablename__ = "bebidas"

    id: Mapped[int] = mapped_column(primary_key=True)
    descricao: Mapped[str] = mapped_column(String(255))
    valor: Mapped[float] = mapped_column(Float)

    itens_bebida: Mapped[list["ItemBebida"]] = relationship(back_populates="bebida")


class ItemBebida(Base):
    __tablename__ = "item_bebidas"

    id: Mapped[int] = mapped_column(primary_key=True)
    valor_item_bebida: Mapped[float] = mapped_column(Float)
    pedido_id: Mapped[int] = mapped_column(ForeignKey("pedidos.id"))
    bebida_id: Mapped[int] = mapped_column(ForeignKey("bebidas.id"))

    pedido: Mapped["Pedido"] = relationship(back_populates="itens_bebida")
    bebida: Mapped["Bebida"] = relationship(back_populates="itens_bebida")
