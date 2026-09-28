from sqlmodel import Session, select

from entidades.models import (
    Solicitacao,
    Usuario,
    Equipamento
)

from sqlalchemy.exc import OperationalError, IntegrityError


# Cadastra uma nova solicitação no banco de dados

def cadastrar_solicitacao(
    solicitacao_data: Solicitacao,
    db: Session
):

    try:

        # Verifica se o equipamento existe
        equipamento = db.get(
            Equipamento,
            solicitacao_data.id_equipamento
        )

        if not equipamento:

            raise KeyError(
                f"Equipamento de ID "
                f"{solicitacao_data.id_equipamento} não encontrado."
            )

        # Verifica se o usuário solicitante existe
        usuario = db.get(
            Usuario,
            solicitacao_data.id_solicitante
        )

        if not usuario:

            raise KeyError(
                f"Usuário de ID "
                f"{solicitacao_data.id_solicitante} não encontrado."
            )

        # Cria a solicitação
        solicitacao = Solicitacao(
            **solicitacao_data.model_dump()
        )

        # Solicitações novas começam pendentes
        if solicitacao.situacao is None:

            solicitacao.situacao = "pendente"

        db.add(solicitacao)
        db.commit()
        db.refresh(solicitacao)

        return solicitacao

    except OperationalError as e:

        raise RuntimeError(
            "Falha na conexão com o banco de dados"
        ) from e

    except IntegrityError as e:

        db.rollback()

        raise ValueError(
            "Verifique os dados informados."
        ) from e


# Busca todas as solicitações cadastradas

def buscar_solicitacoes(db: Session):

    try:

        statement = select(Solicitacao)

        solicitacoes = db.exec(statement).all()

        return solicitacoes

    except OperationalError as e:

        raise RuntimeError(
            "Falha na conexão com o banco de dados"
        ) from e


# Busca uma solicitação pelo ID

def buscar_solicitacao(
    db: Session,
    solicitacao_id: int
):

    try:

        solicitacao = db.get(
            Solicitacao,
            solicitacao_id
        )

        if not solicitacao:

            raise KeyError(
                f"Solicitação de ID "
                f"{solicitacao_id} não encontrada."
            )

        return solicitacao

    except OperationalError as e:

        db.rollback()

        raise RuntimeError(
            "Falha na conexão com o banco de dados"
        ) from e


# Atualiza uma solicitação existente

def atualizar_solicitacao(
    db: Session,
    solicitacao_id: int,
    dados_atualizados: Solicitacao
):

    try:

        # Busca a solicitação pelo ID
        solicitacao = db.get(
            Solicitacao,
            solicitacao_id
        )

        if not solicitacao:

            raise KeyError(
                f"Solicitação de ID "
                f"{solicitacao_id} não encontrada."
            )

        solicitacao_data = dados_atualizados.model_dump(
            exclude_unset=True
        )

        # Verifica o novo equipamento, caso ele tenha sido alterado
        if "id_equipamento" in solicitacao_data:

            equipamento = db.get(
                Equipamento,
                solicitacao_data["id_equipamento"]
            )

            if not equipamento:

                raise KeyError(
                    f"Equipamento de ID "
                    f"{solicitacao_data['id_equipamento']} não encontrado."
                )

        # Verifica o novo solicitante, caso tenha sido alterado
        if "id_solicitante" in solicitacao_data:

            usuario = db.get(
                Usuario,
                solicitacao_data["id_solicitante"]
            )

            if not usuario:

                raise KeyError(
                    f"Usuário de ID "
                    f"{solicitacao_data['id_solicitante']} não encontrado."
                )

        # Verifica o autorizador, caso tenha sido informado
        if "id_usuario_autorizador" in solicitacao_data:

            autorizador_id = solicitacao_data[
                "id_usuario_autorizador"
            ]

            if autorizador_id is not None:

                autorizador = db.get(
                    Usuario,
                    autorizador_id
                )

                if not autorizador:

                    raise KeyError(
                        f"Usuário autorizador de ID "
                        f"{autorizador_id} não encontrado."
                    )

        # Atualiza os campos recebidos
        for key, value in solicitacao_data.items():

            if key != "id_solicitacao":
                setattr(solicitacao, key, value)

        db.add(solicitacao)
        db.commit()
        db.refresh(solicitacao)

        return solicitacao

    except IntegrityError as e:

        db.rollback()

        raise ValueError(
            "Erro de integridade. "
            "Verifique os dados informados."
        ) from e

    except OperationalError as e:

        db.rollback()

        raise RuntimeError(
            "Falha na conexão com o banco de dados"
        ) from e


# Deleta uma solicitação pelo ID

def deletar_solicitacao(
    db: Session,
    solicitacao_id: int
):

    try:

        solicitacao = db.get(
            Solicitacao,
            solicitacao_id
        )

        if not solicitacao:

            raise KeyError(
                f"Solicitação de ID "
                f"{solicitacao_id} não encontrada."
            )

        db.delete(solicitacao)
        db.commit()

    except IntegrityError as e:

        db.rollback()

        raise ValueError(
            "Não é possível excluir esta solicitação, "
            "pois existem empréstimos vinculados a ela."
        ) from e

    except OperationalError as e:

        db.rollback()

        raise RuntimeError(
            "Falha na conexão com o banco de dados"
        ) from e