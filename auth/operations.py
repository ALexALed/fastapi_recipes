from passlib.context import CryptContext
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from auth.db import User
from auth.rbac import Role

pwd_context = CryptContext(
    schemes=["bcrypt"], deprecated="auto"
)

def add_user(session: Session, username: str, password: str, email: str, role: Role = Role.basic) -> User | None:
    db_user = User(username=username, email=email, hashed_password=pwd_context.hash(password), role=role)
    session.add(db_user)
    try:
        session.commit()
        session.refresh(db_user)
        return db_user
    except IntegrityError:
        session.rollback()
        return None


def get_user(session: Session, username: str) -> User | None:
    return session.query(User).filter(User.username == username).first()