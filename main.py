from fastapi import FastAPI

from routes.nivel_acesso_routes import nivel_acesso_router
from routes.categoria_equipamento_routes import categoria_equipamento_router
from routes.usuario_routes import usuario_router
from routes.equipamento_routes import equipamento_router
from routes.solicitacao_routes import solicitacao_router
from routes.emprestimo_routes import emprestimo_router
from routes.auth_routes import auth_routes

app = FastAPI()


# Inclui as rotas de cada entidade do sistema
app.include_router(nivel_acesso_router)
app.include_router(categoria_equipamento_router)
app.include_router(usuario_router)
app.include_router(equipamento_router)
app.include_router(solicitacao_router)
app.include_router(emprestimo_router)
app.include_router(auth_routes)
