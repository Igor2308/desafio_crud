from fastapi import APIRouter, Depends, HTTPException, status

from sqlmodel import Session

from db.db import get_db

from entidades.models import Emprestimo

from controllers.emprestimo_controller import (
    cadastrar_emprestimo,
    buscar_emprestimos,
    buscar_emprestimo,
    atualizar_emprestimo,
    deletar_emprestimo
)

emprestimo_router = APIRouter()


# Cadastra um novo empréstimo

@emprestimo_router.post("/emprestimos")
def cadastro_emprestimo(
    emprestimo: Emprestimo,
    db: Session = Depends(get_db)
):
    try:
        return cadastrar_emprestimo(
            emprestimo,
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


# Busca todos os empréstimos

@emprestimo_router.get("/emprestimos")
def buscar_emprestimos_route(
    db: Session = Depends(get_db)
):
    try:
        return buscar_emprestimos(db)

    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


# Busca um empréstimo pelo ID

@emprestimo_router.get("/emprestimos/{emprestimo_id}")
def buscar_emprestimo_route(
    emprestimo_id: int,
    db: Session = Depends(get_db)
):
    try:
        return buscar_emprestimo(
            db,
            emprestimo_id
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


# Atualiza um empréstimo

@emprestimo_router.put("/emprestimos/{emprestimo_id}")
def atualizar_emprestimo_route(
    emprestimo_id: int,
    emprestimo: Emprestimo,
    db: Session = Depends(get_db)
):
    try:
        return atualizar_emprestimo(
            db,
            emprestimo_id,
            emprestimo
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


# Deleta um empréstimo

@emprestimo_router.delete("/emprestimos/{emprestimo_id}")
def deletar_emprestimo_route(
    emprestimo_id: int,
    db: Session = Depends(get_db)
):
    try:
        deletar_emprestimo(
            db,
            emprestimo_id
        )

        return {
            "mensagem": "Empréstimo deletado com sucesso."
        }

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