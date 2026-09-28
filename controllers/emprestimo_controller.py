from sqlmodel import Session, select

from entidades.models import (
    Emprestimo,
    Usuario,
    Solicitacao,
    Equipamento
)

from sqlalchemy.exc import OperationalError, IntegrityError


# Cadastra um novo empréstimo no banco de dados

def cadastrar_emprestimo(
    emprestimo_data: Emprestimo,
    db: Session
):

    try:

        # Verifica se o usuário existe
        usuario = db.get(
            Usuario,
            emprestimo_data.id_usuario
        )

        if not usuario:

            raise KeyError(
                f"Usuário de ID "
                f"{emprestimo_data.id_usuario} não encontrado."
            )

        # Verifica se a solicitação existe
        solicitacao = db.get(
            Solicitacao,
            emprestimo_data.id_solicitacao
        )

        if not solicitacao:

            raise KeyError(
                f"Solicitação de ID "
                f"{emprestimo_data.id_solicitacao} não encontrada."
            )

        # O empréstimo só pode ser criado para uma solicitação aprovada
        if solicitacao.situacao != "aprovado":

            raise ValueError(
                "Não é possível criar o empréstimo, "
                "pois a solicitação não está aprovada."
            )

        # Verifica se o equipamento existe
        equipamento = db.get(
            Equipamento,
            emprestimo_data.id_equipamento
        )

        if not equipamento:

            raise KeyError(
                f"Equipamento de ID "
                f"{emprestimo_data.id_equipamento} não encontrado."
            )

        # Verifica se o equipamento está disponível
        if equipamento.status_equipamento != "disponivel":

            raise ValueError(
                "Não é possível realizar o empréstimo, "
                "pois o equipamento não está disponível."
            )

        # Verifica se o equipamento do empréstimo
        # é o mesmo equipamento da solicitação
        if solicitacao.id_equipamento != emprestimo_data.id_equipamento:

            raise ValueError(
                "O equipamento informado no empréstimo "
                "não corresponde ao equipamento da solicitação."
            )

        # Cria o empréstimo
        emprestimo = Emprestimo(
            **emprestimo_data.model_dump()
        )

        db.add(emprestimo)

        # Atualiza o status do equipamento
        equipamento.status_equipamento = "emprestado"

        db.add(equipamento)

        db.commit()

        db.refresh(emprestimo)

        return emprestimo

    except OperationalError as e:

        db.rollback()

        raise RuntimeError(
            "Falha na conexão com o banco de dados"
        ) from e

    except IntegrityError as e:

        db.rollback()

        raise ValueError(
            "Verifique os dados informados."
        ) from e


# Busca todos os empréstimos cadastrados

def buscar_emprestimos(db: Session):

    try:

        statement = select(Emprestimo)

        emprestimos = db.exec(statement).all()

        return emprestimos

    except OperationalError as e:

        raise RuntimeError(
            "Falha na conexão com o banco de dados"
        ) from e


# Busca um empréstimo pelo ID

def buscar_emprestimo(
    db: Session,
    emprestimo_id: int
):

    try:

        emprestimo = db.get(
            Emprestimo,
            emprestimo_id
        )

        if not emprestimo:

            raise KeyError(
                f"Empréstimo de ID "
                f"{emprestimo_id} não encontrado."
            )

        return emprestimo

    except OperationalError as e:

        db.rollback()

        raise RuntimeError(
            "Falha na conexão com o banco de dados"
        ) from e


# Atualiza um empréstimo existente

def atualizar_emprestimo(
    db: Session,
    emprestimo_id: int,
    dados_atualizados: Emprestimo
):

    try:

        # Busca o empréstimo pelo ID
        emprestimo = db.get(
            Emprestimo,
            emprestimo_id
        )

        if not emprestimo:

            raise KeyError(
                f"Empréstimo de ID "
                f"{emprestimo_id} não encontrado."
            )

        emprestimo_data = dados_atualizados.model_dump(
            exclude_unset=True
        )

        # Verifica o usuário caso ele tenha sido alterado
        if "id_usuario" in emprestimo_data:

            usuario = db.get(
                Usuario,
                emprestimo_data["id_usuario"]
            )

            if not usuario:

                raise KeyError(
                    f"Usuário de ID "
                    f"{emprestimo_data['id_usuario']} não encontrado."
                )

        # Verifica a solicitação caso tenha sido alterada
        if "id_solicitacao" in emprestimo_data:

            solicitacao = db.get(
                Solicitacao,
                emprestimo_data["id_solicitacao"]
            )

            if not solicitacao:

                raise KeyError(
                    f"Solicitação de ID "
                    f"{emprestimo_data['id_solicitacao']} não encontrada."
                )

            if solicitacao.situacao != "aprovado":

                raise ValueError(
                    "A solicitação informada não está aprovada."
                )

        # Verifica o equipamento caso tenha sido alterado
        if "id_equipamento" in emprestimo_data:

            equipamento = db.get(
                Equipamento,
                emprestimo_data["id_equipamento"]
            )

            if not equipamento:

                raise KeyError(
                    f"Equipamento de ID "
                    f"{emprestimo_data['id_equipamento']} não encontrado."
                )

        # Atualiza os campos recebidos
        for key, value in emprestimo_data.items():

            if key != "id_emprestimo":
                setattr(emprestimo, key, value)

        # Se foi informada uma devolução,
        # o equipamento volta a ficar disponível
        if (
            "data_devolucao" in emprestimo_data
            and emprestimo_data["data_devolucao"] is not None
        ):

            equipamento = db.get(
                Equipamento,
                emprestimo.id_equipamento
            )

            if equipamento:

                equipamento.status_equipamento = "disponivel"

                db.add(equipamento)

        db.add(emprestimo)

        db.commit()

        db.refresh(emprestimo)

        return emprestimo

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


# Deleta um empréstimo pelo ID

def deletar_emprestimo(
    db: Session,
    emprestimo_id: int
):

    try:

        # Busca o empréstimo pelo ID
        emprestimo = db.get(
            Emprestimo,
            emprestimo_id
        )

        if not emprestimo:

            raise KeyError(
                f"Empréstimo de ID "
                f"{emprestimo_id} não encontrado."
            )

        # Busca o equipamento relacionado
        equipamento = db.get(
            Equipamento,
            emprestimo.id_equipamento
        )

        # Exclui o empréstimo
        db.delete(emprestimo)

        # Caso o equipamento esteja emprestado,
        # volta para disponível
        if equipamento:

            equipamento.status_equipamento = "disponivel"

            db.add(equipamento)

        db.commit()

    except IntegrityError as e:

        db.rollback()

        raise ValueError(
            "Não é possível excluir este empréstimo, "
            "pois existem registros vinculados a ele."
        ) from e

    except OperationalError as e:

        db.rollback()

        raise RuntimeError(
            "Falha na conexão com o banco de dados"
        ) from e