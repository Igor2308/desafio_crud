from fastapi import APIRouter, Depends, HTTPException, status

from sqlmodel import Session

from db.db import get_db

from entidades.models import Usuario

from entidades.schemas import UsuarioResposta

from controllers.usuario_controller import (
    cadastrar_usuario,
    buscar_usuarios,
    buscar_usuario,
    atualizar_usuario,
    deletar_usuario
)

usuario_router = APIRouter()


# Cadastra um novo usuário

@usuario_router.post(
    "/usuarios",
    response_model=UsuarioResposta
)
def cadastro_usuario(
    usuario: Usuario,
    db: Session = Depends(get_db)
):
    try:
        return cadastrar_usuario(
            usuario,
            db
        )

    except KeyError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


# Busca todos os usuários

@usuario_router.get(
    "/usuarios",
    response_model=list[UsuarioResposta]
)
def buscar_usuarios_route(
    db: Session = Depends(get_db)
):
    try:
        return buscar_usuarios(db)

    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


# Busca um usuário pelo ID

@usuario_router.get(
    "/usuarios/{usuario_id}",
    response_model=UsuarioResposta
)
def buscar_usuario_route(
    usuario_id: int,
    db: Session = Depends(get_db)
):
    try:
        return buscar_usuario(
            db,
            usuario_id
        )

    except KeyError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


# Atualiza um usuário

@usuario_router.put(
    "/usuarios/{usuario_id}",
    response_model=UsuarioResposta
)
def atualizar_usuario_route(
    usuario_id: int,
    usuario: Usuario,
    db: Session = Depends(get_db)
):
    try:
        return atualizar_usuario(
            db,
            usuario_id,
            usuario
        )

    except KeyError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


# Deleta um usuário

@usuario_router.delete("/usuarios/{usuario_id}")
def deletar_usuario_route(
    usuario_id: int,
    db: Session = Depends(get_db)
):
    try:
        deletar_usuario(
            db,
            usuario_id
        )

        return {
            "mensagem": "Usuário deletado com sucesso."
        }

    except KeyError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )

    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )