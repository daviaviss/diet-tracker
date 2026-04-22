import bcrypt

from mvc.models import User
from dao import use_session


# Gera um hash seguro da senha usando bcrypt com salt aleatório
def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


# Compara a senha digitada com o hash armazenado no banco
# Retorna True se a senha estiver correta, False caso contrário
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())


# Cria um novo usuário no banco, já salvando a senha como hash
def create_user(name: str, email: str, password: str, **kwargs) -> User:
    with use_session(commit=True) as session:
        user = User(name=name, email=email, password=hash_password(password), **kwargs)
        session.add(user)
        # flush envia o INSERT antes do commit para que o id seja gerado
        session.flush()
        # refresh carrega os dados do banco de volta para o objeto (ex: id gerado)
        session.refresh(user)
        return user


# Busca um usuário pelo id — retorna None se não encontrado
def get_user_by_id(user_id: int) -> User | None:
    with use_session() as session:
        return session.get(User, user_id)


# Busca um usuário pelo e-mail — usado no login para localizar a conta
def get_user_by_email(email: str) -> User | None:
    with use_session() as session:
        return session.query(User).filter_by(email=email).first()


# Retorna todos os usuários cadastrados no banco
def get_all_users() -> list[User]:
    with use_session() as session:
        return session.query(User).all()


# Remove um usuário pelo id — retorna False se o usuário não existir
def delete_user(user_id: int) -> bool:
    with use_session(commit=True) as session:
        user = session.get(User, user_id)
        if user is None:
            return False
        session.delete(user)
        return True
