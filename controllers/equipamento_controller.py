from sqlmodel import Session, select

from entidades.models import Equipamento, CategoriaEquipamento

from sqlalchemy.exc import OperationalError, IntegrityError


# Cadastra um novo equipamento no banco de dados

def cadastrar_equipamento(
    equipamento_data: Equipamento,
    db: Session
):

    try:

        # Verifica se a categoria informada existe
        categoria = db.get(
            CategoriaEquipamento,
            equipamento_data.id_categoria
        )

        if not categoria:

            raise KeyError(
                f"Categoria de equipamento de ID "
                f"{equipamento_data.id_categoria} não encontrada."
            )

        # Cria um objeto do tipo Equipamento
        equipamento = Equipamento(
            **equipamento_data.model_dump()
        )

        db.add(equipamento)
        db.commit()
        db.refresh(equipamento)

        return equipamento

    except OperationalError as e:

        raise RuntimeError(
            "Falha na conexão com o banco de dados"
        ) from e

    except IntegrityError as e:

        db.rollback()

        raise ValueError(
            "Verifique os dados informados. "
            "O número de patrimônio pode já estar cadastrado."
        ) from e


# Busca todos os equipamentos cadastrados

def buscar_equipamentos(db: Session):

    try:

        statement = select(Equipamento)

        equipamentos = db.exec(statement).all()

        return equipamentos

    except OperationalError as e:

        raise RuntimeError(
            "Falha na conexão com o banco de dados"
        ) from e


# Busca um equipamento pelo ID

def buscar_equipamento(
    db: Session,
    equipamento_id: int
):

    try:

        equipamento = db.get(
            Equipamento,
            equipamento_id
        )

        if not equipamento:

            raise KeyError(
                f"Equipamento de ID "
                f"{equipamento_id} não encontrado."
            )

        return equipamento

    except OperationalError as e:

        db.rollback()

        raise RuntimeError(
            "Falha na conexão com o banco de dados"
        ) from e


# Atualiza um equipamento existente

def atualizar_equipamento(
    db: Session,
    equipamento_id: int,
    dados_atualizados: Equipamento
):

    try:

        # Busca o equipamento pelo ID
        equipamento = db.get(
            Equipamento,
            equipamento_id
        )

        if not equipamento:

            raise KeyError(
                f"Equipamento de ID "
                f"{equipamento_id} não encontrado."
            )

        equipamento_data = dados_atualizados.model_dump(
            exclude_unset=True
        )

        # Se a categoria foi alterada,
        # verifica se a nova categoria existe
        if "id_categoria" in equipamento_data:

            categoria = db.get(
                CategoriaEquipamento,
                equipamento_data["id_categoria"]
            )

            if not categoria:

                raise KeyError(
                    f"Categoria de equipamento de ID "
                    f"{equipamento_data['id_categoria']} não encontrada."
                )

        # Atualiza os campos recebidos
        for key, value in equipamento_data.items():

            if key != "id_equipamento":
                setattr(equipamento, key, value)

        db.add(equipamento)
        db.commit()
        db.refresh(equipamento)

        return equipamento

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


# Deleta um equipamento pelo ID

def deletar_equipamento(
    db: Session,
    equipamento_id: int
):

    try:

        equipamento = db.get(
            Equipamento,
            equipamento_id
        )

        if not equipamento:

            raise KeyError(
                f"Equipamento de ID "
                f"{equipamento_id} não encontrado."
            )

        db.delete(equipamento)
        db.commit()

    except IntegrityError as e:

        db.rollback()

        raise ValueError(
            "Não é possível excluir este equipamento, "
            "pois existem solicitações ou empréstimos vinculados a ele."
        ) from e

    except OperationalError as e:

        db.rollback()

        raise RuntimeError(
            "Falha na conexão com o banco de dados"
        ) from e