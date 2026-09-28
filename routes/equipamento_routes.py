from fastapi import APIRouter, Depends, HTTPException, status

from sqlmodel import Session

from db.db import get_db

from entidades.models import Equipamento

from controllers.equipamento_controller import (
    cadastrar_equipamento,
    buscar_equipamentos,
    buscar_equipamento,
    atualizar_equipamento,
    deletar_equipamento
)

equipamento_router = APIRouter()


# Cadastra um novo equipamento

@equipamento_router.post("/equipamentos")
def cadastro_equipamento(
    equipamento: Equipamento,
    db: Session = Depends(get_db)
):
    try:
        return cadastrar_equipamento(
            equipamento,
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


# Busca todos os equipamentos

@equipamento_router.get("/equipamentos")
def buscar_equipamentos_route(
    db: Session = Depends(get_db)
):
    try:
        return buscar_equipamentos(db)

    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


# Busca um equipamento pelo ID

@equipamento_router.get("/equipamentos/{equipamento_id}")
def buscar_equipamento_route(
    equipamento_id: int,
    db: Session = Depends(get_db)
):
    try:
        return buscar_equipamento(
            db,
            equipamento_id
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


# Atualiza um equipamento

@equipamento_router.put("/equipamentos/{equipamento_id}")
def atualizar_equipamento_route(
    equipamento_id: int,
    equipamento: Equipamento,
    db: Session = Depends(get_db)
):
    try:
        return atualizar_equipamento(
            db,
            equipamento_id,
            equipamento
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


# Deleta um equipamento

@equipamento_router.delete("/equipamentos/{equipamento_id}")
def deletar_equipamento_route(
    equipamento_id: int,
    db: Session = Depends(get_db)
):
    try:
        deletar_equipamento(
            db,
            equipamento_id
        )

        return {
            "mensagem": "Equipamento deletado com sucesso."
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