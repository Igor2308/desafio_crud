from fastapi import APIRouter, Depends, HTTPException, status

from sqlmodel import Session

from db.db import get_db

from entidades.models import Solicitacao

from controllers.solicitacao_controller import (
    cadastrar_solicitacao,
    buscar_solicitacoes,
    buscar_solicitacao,
    atualizar_solicitacao,
    deletar_solicitacao
)

solicitacao_router = APIRouter()


# Cadastra uma nova solicitação

@solicitacao_router.post("/solicitacoes")
def cadastro_solicitacao(
    solicitacao: Solicitacao,
    db: Session = Depends(get_db)
):
    try:
        return cadastrar_solicitacao(
            solicitacao,
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


# Busca todas as solicitações

@solicitacao_router.get("/solicitacoes")
def buscar_solicitacoes_route(
    db: Session = Depends(get_db)
):
    try:
        return buscar_solicitacoes(db)

    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


# Busca uma solicitação pelo ID

@solicitacao_router.get("/solicitacoes/{solicitacao_id}")
def buscar_solicitacao_route(
    solicitacao_id: int,
    db: Session = Depends(get_db)
):
    try:
        return buscar_solicitacao(
            db,
            solicitacao_id
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


# Atualiza uma solicitação

@solicitacao_router.put("/solicitacoes/{solicitacao_id}")
def atualizar_solicitacao_route(
    solicitacao_id: int,
    solicitacao: Solicitacao,
    db: Session = Depends(get_db)
):
    try:
        return atualizar_solicitacao(
            db,
            solicitacao_id,
            solicitacao
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


# Deleta uma solicitação

@solicitacao_router.delete("/solicitacoes/{solicitacao_id}")
def deletar_solicitacao_route(
    solicitacao_id: int,
    db: Session = Depends(get_db)
):
    try:
        deletar_solicitacao(
            db,
            solicitacao_id
        )

        return {
            "mensagem": "Solicitação deletada com sucesso."
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