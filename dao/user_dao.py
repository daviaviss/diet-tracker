import bcrypt

from mvc.models import User
from dao import use_session


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())


def create_user(name: str, email: str, password: str, **kwargs) -> User:
    with use_session(commit=True) as session:
        user = User(name=name, email=email, password=hash_password(password), **kwargs)
        session.add(user)
        session.flush()
        session.refresh(user)
        return user


def get_user_by_id(user_id: int) -> User | None:
    with use_session() as session:
        return session.get(User, user_id)


def get_user_by_email(email: str) -> User | None:
    with use_session() as session:
        return session.query(User).filter_by(email=email).first()


def get_all_users() -> list[User]:
    with use_session() as session:
        return session.query(User).all()


def delete_user(user_id: int) -> bool:
    with use_session(commit=True) as session:
        user = session.get(User, user_id)
        if user is None:
            return False
        session.delete(user)
        return True
