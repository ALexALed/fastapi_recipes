from http.client import HTTPException

from pydantic import BaseModel
from fastapi import Depends, status
from fastapi.security import OAuth2PasswordBearer

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "hashed_password": "hashedsecret"
    },
    "janedoe": {
        "username": "johndoe",
        "hashed_password": "hashedsecret2"
    }
}


def fakely_hash_password(password: str):
    return f"hashed{password}"


class User(BaseModel):
    username: str


class UserInDB(User):
    hashed_password: str


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def fake_token_generator(user: UserInDB) -> str:
    return f"token{user.username}"


def fake_token_resolver(token: str) -> UserInDB | None:
    if token.startswith("tokenized"):
        user_id = token.removeprefix("tokenized")
        user = get_user(fake_users_db, user_id)
        return user


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_user_from_token(token: str = Depends(oauth2_scheme)) -> UserInDB:
    user = fake_token_resolver(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_410_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authentificate": "Bearer"}
        )
    return user