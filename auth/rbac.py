from typing import Annotated
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Status
)
from pydantic import BaseModel
from sqlalchemy.orm import Session
from db_connection import get_session
from models import Role
from security import (
    decode_access_token,
    oauth2_scheme
)


class Role(str, Enum):
    basic = "basic"
    premium = "premium"


class UserCreateRequestWithRole(BaseModel):
    username: str
    email: str
    role: Role

def get_current_user(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)) -> UserCreateRequestWithRole:
    user = decode_access_token(token)
    if not user:
        raise HTTPException(
            status_code=Status.HTTP_401_UNAUTHORIZED,
            detail="User not authorized",
            headers={"WWW-Authentificate": "Bearer"}
        )
    return UserCreateRequestWithRole(username=user.username, email=user.email, role=user.role)

def get_premium_user(current_user: Annotated[get_current_user, Depends()]):
    if current_user.role != Role.premium:
        raise HTTPException(
            status_code=Status.HTTP_401_UNAUTHORIZED,
            detail="User not authorized"
        )
    return current_user