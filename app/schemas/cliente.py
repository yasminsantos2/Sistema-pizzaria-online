from pydantic import BaseModel, ConfigDict, Field


class ClienteRegistro(BaseModel):
    login: str = Field(min_length=1, max_length=100)
    senha: str = Field(min_length=6, max_length=255)
    nome: str = Field(min_length=1, max_length=100)


class ClienteLogin(BaseModel):
    login: str = Field(min_length=1, max_length=100)
    senha: str = Field(min_length=1, max_length=255)


class ClienteResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    login: str
    nome: str
