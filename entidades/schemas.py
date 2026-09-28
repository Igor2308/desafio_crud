from datetime import datetime
from pydantic import BaseModel, ConfigDict

# Schema utilizado para devolver um usuário pela API
# A senha não faz parte deste schema
class UsuarioResposta(BaseModel):

    id_usuario: int
    nome: str
    email: str
    cpf: str
    nivel_acesso: int
    status_usuario: str
    data_criacao: datetime | None = None

    model_config = ConfigDict(from_attributes=True)