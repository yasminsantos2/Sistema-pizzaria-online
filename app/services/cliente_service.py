from ..models.cliente import Cliente
from ..repositories.cliente_repository import ClienteRepository
from .exceptions import (
    ClienteNaoEncontradoError,
    CredenciaisInvalidasError,
    DadosInvalidosError,
    LoginJaExisteError,
)


class ClienteService:
    def __init__(self, repository: ClienteRepository) -> None:
        self.repository = repository

    def registrar_cliente(self, login: str, senha: str, nome: str) -> Cliente:
        login = login.strip()
        nome = nome.strip()

        if not login or not nome or not senha:
            raise DadosInvalidosError("Login, senha e nome são obrigatórios.")

        if len(senha) < 6:
            raise DadosInvalidosError("A senha deve ter no mínimo 6 caracteres.")

        if self.repository.buscar_por_login(login):
            raise LoginJaExisteError("Login já cadastrado.")

        return self.repository.registrar_cliente(login=login, senha=senha, nome=nome)

    def logar_cliente(self, login: str, senha: str) -> Cliente:
        login = login.strip()

        if not login or not senha:
            raise DadosInvalidosError("Login e senha são obrigatórios.")

        cliente = self.repository.buscar_por_login(login)
        if cliente is None or cliente.senha != senha:
            raise CredenciaisInvalidasError("Login ou senha inválidos.")

        return cliente

    def buscar_por_id(self, cliente_id: int) -> Cliente:
        cliente = self.repository.buscar_por_id(cliente_id)
        if cliente is None:
            raise ClienteNaoEncontradoError("Cliente não encontrado.")
        return cliente

    def listar_todos(self) -> list[Cliente]:
        return self.repository.listar_todos()
