from passlib.context import CryptContext
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from auth.db import User

pwd_context = CryptContext(
    schemes=["bcrypt"], deprecated="auto"
)

def add_user(session: Session, username: str, password: str, email: str) -> User | None:
    db_user = User(username=username, email=email, hashed_password=pwd_context.hash(password))
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