class ClienteError(Exception):
    """Erro base da regra de negócio de Cliente."""


class LoginJaExisteError(ClienteError):
    """Login já cadastrado."""


class CredenciaisInvalidasError(ClienteError):
    """Login ou senha incorretos."""


class ClienteNaoEncontradoError(ClienteError):
    """Cliente não encontrado."""


class DadosInvalidosError(ClienteError):
    """Dados obrigatórios inválidos ou incompletos."""
