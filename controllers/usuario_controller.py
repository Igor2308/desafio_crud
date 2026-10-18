from core.security import cria_hash_senha
from sqlmodel import Session, select

from entidades.models import Usuario, NivelAcesso

from sqlalchemy.exc import OperationalError, IntegrityError


# Cadastra um novo usuário no banco de dados
def cadastrar_usuario(
    usuario_data: Usuario,
    db: Session
):
    try:
        # Verifica se o nível de acesso informado existe
        nivel = db.get(
            NivelAcesso,
            usuario_data.nivel_acesso
        )

        if not nivel:
            raise KeyError(
                f"Nível de acesso de ID "
                f"{usuario_data.nivel_acesso} não encontrado."
            )

        # Cria um objeto do tipo Usuario
        dados_usuario = usuario_data.model_dump(
            exclude={"id_usuario"}
        )

        dados_usuario["senha"] = cria_hash_senha(
            dados_usuario["senha"]
        )

        usuario = Usuario(**dados_usuario)

        db.add(usuario)
        db.commit()
        db.refresh(usuario)

        return usuario

    except OperationalError as e:
        db.rollback()

        raise RuntimeError(
            "Falha na conexão com o banco de dados."
        ) from e

    except IntegrityError as e:
        db.rollback()

        raise ValueError(
            "Verifique os dados informados. "
            "E-mail ou CPF podem já estar cadastrados."
        ) from e


# Busca todos os usuários cadastrados
def buscar_usuarios(db: Session):
    try:
        statement = select(Usuario)
        usuarios = db.exec(statement).all()

        return usuarios

    except OperationalError as e:
        db.rollback()

        raise RuntimeError(
            "Falha na conexão com o banco de dados."
        ) from e


# Busca um usuário pelo ID
def buscar_usuario(
    db: Session,
    usuario_id: int
):
    try:
        usuario = db.get(
            Usuario,
            usuario_id
        )

        if not usuario:
            raise KeyError(
                f"Usuário de ID {usuario_id} não encontrado."
            )

        return usuario

    except OperationalError as e:
        db.rollback()

        raise RuntimeError(
            "Falha na conexão com o banco de dados."
        ) from e


# Atualiza um usuário existente
def atualizar_usuario(
    db: Session,
    usuario_id: int,
    dados_atualizados: Usuario
):
    try:
        # Busca o usuário pelo ID
        usuario = db.get(
            Usuario,
            usuario_id
        )

        if not usuario:
            raise KeyError(
                f"Usuário de ID {usuario_id} não encontrado."
            )

        usuario_data = dados_atualizados.model_dump(
            exclude_unset=True,
            exclude={"id_usuario"}
        )

        # Se o nível de acesso foi alterado,
        # verifica se o novo nível existe
        if "nivel_acesso" in usuario_data:
            nivel = db.get(
                NivelAcesso,
                usuario_data["nivel_acesso"]
            )

            if not nivel:
                raise KeyError(
                    f"Nível de acesso de ID "
                    f"{usuario_data['nivel_acesso']} não encontrado."
                )

        # Atualiza os campos recebidos
        # Criptografa a senha somente se ela foi enviada
        if "senha" in usuario_data:
            usuario_data["senha"] = cria_hash_senha(
                usuario_data["senha"]
            )

        # Atualiza os campos recebidos
        for key, value in usuario_data.items():
            setattr(usuario, key, value)

        db.add(usuario)
        db.commit()
        db.refresh(usuario)

        return usuario

    except IntegrityError as e:
        db.rollback()

        raise ValueError(
            "Erro de integridade. Verifique os dados informados."
        ) from e

    except OperationalError as e:
        db.rollback()

        raise RuntimeError(
            "Falha na conexão com o banco de dados."
        ) from e


# Deleta um usuário pelo ID
def deletar_usuario(
    db: Session,
    usuario_id: int
):
    try:
        usuario = db.get(
            Usuario,
            usuario_id
        )

        if not usuario:
            raise KeyError(
                f"Usuário de ID {usuario_id} não encontrado."
            )

        db.delete(usuario)
        db.commit()

    except IntegrityError as e:
        db.rollback()

        raise ValueError(
            "Não é possível excluir este usuário, "
            "pois existem registros vinculados a ele."
        ) from e

    except OperationalError as e:
        db.rollback()

        raise RuntimeError(
            "Falha na conexão com o banco de dados."
        ) from e
