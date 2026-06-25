from fastapi import APIRouter, Depends, HTTPException, status

from ..dependencies import get_cliente_service
from ..schemas.cliente import ClienteLogin, ClienteRegistro, ClienteResponse
from ..services.cliente_service import ClienteService
from ..services.exceptions import (
    ClienteError,
    ClienteNaoEncontradoError,
    CredenciaisInvalidasError,
    DadosInvalidosError,
    LoginJaExisteError,
)

router = APIRouter(prefix="/clientes", tags=["Clientes"])


def _http_exception_from_cliente_error(error: ClienteError) -> HTTPException:
    if isinstance(error, DadosInvalidosError):
        status_code = status.HTTP_400_BAD_REQUEST
    elif isinstance(error, LoginJaExisteError):
        status_code = status.HTTP_409_CONFLICT
    elif isinstance(error, CredenciaisInvalidasError):
        status_code = status.HTTP_401_UNAUTHORIZED
    elif isinstance(error, ClienteNaoEncontradoError):
        status_code = status.HTTP_404_NOT_FOUND
    else:
        status_code = status.HTTP_400_BAD_REQUEST

    return HTTPException(status_code=status_code, detail=str(error))


@router.post("/registrar", response_model=ClienteResponse, status_code=status.HTTP_201_CREATED)
def registrar_cliente(
    dados: ClienteRegistro,
    service: ClienteService = Depends(get_cliente_service),
) -> ClienteResponse:
    try:
        cliente = service.registrar_cliente(dados.login, dados.senha, dados.nome)
    except ClienteError as error:
        raise _http_exception_from_cliente_error(error) from error
    return ClienteResponse.model_validate(cliente)


@router.post("/login", response_model=ClienteResponse)
def logar_cliente(
    dados: ClienteLogin,
    service: ClienteService = Depends(get_cliente_service),
) -> ClienteResponse:
    try:
        cliente = service.logar_cliente(dados.login, dados.senha)
    except ClienteError as error:
        raise _http_exception_from_cliente_error(error) from error
    return ClienteResponse.model_validate(cliente)


@router.get("/", response_model=list[ClienteResponse])
def listar_clientes(
    service: ClienteService = Depends(get_cliente_service),
) -> list[ClienteResponse]:
    clientes = service.listar_todos()
    return [ClienteResponse.model_validate(cliente) for cliente in clientes]


@router.get("/{cliente_id}", response_model=ClienteResponse)
def buscar_cliente(
    cliente_id: int,
    service: ClienteService = Depends(get_cliente_service),
) -> ClienteResponse:
    try:
        cliente = service.buscar_por_id(cliente_id)
    except ClienteError as error:
        raise _http_exception_from_cliente_error(error) from error
    return ClienteResponse.model_validate(cliente)
