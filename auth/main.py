from contextlib import asynccontextmanager

from fastapi import APIRouter, FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette import status

from auth.db import Base, engine, get_session
from auth.jwt_security import decode_token, Token, authenticate_user, create_access_token
from auth.operations import add_user
from auth.rbac import Role
from auth.responses import ResponseCreateUser, UserCreateBody, UserCreateResponse


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


auth_router = APIRouter(prefix='/auth', lifespan=lifespan, tags=["Auth"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


@auth_router.post('/register/user', status_code=status.HTTP_201_CREATED, response_model=ResponseCreateUser,
                  responses={status.HTTP_409_CONFLICT: {"description": "The user already exists"}})
def register(user: UserCreateBody, session: Session = Depends(get_session)) -> dict[str, UserCreateResponse]:
    user = add_user(
        session=session,
        **user.model_dump()
    )
    if not user:
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            "username or email already exists"
        )
    user_response = UserCreateResponse(
        username=user.username,
        email=user.email
    )
    return {"message": "user created", "user": user_response}


@auth_router.post('/register/premium-user', status_code=status.HTTP_201_CREATED, response_model=ResponseCreateUser,
                  responses={status.HTTP_409_CONFLICT: {"description": "The user already exists"}})
def register(user: UserCreateBody, session: Session = Depends(get_session)) -> dict[str, UserCreateResponse]:
    user = add_user(
        session=session,
        **user.model_dump(),
        role=Role.premium
    )
    if not user:
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            "username or email already exists"
        )
    user_response = UserCreateResponse(
        username=user.username,
        email=user.email
    )
    return {"message": "user created", "user": user_response}


@auth_router.get("/users/me")
def read_users_me(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)):
    user = decode_token(token, session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authentificate": "Bearer"}
        )
    return {
        "description": f"{user.username} authorized",
    }


@auth_router.post("/token", response_model=Token, include_in_schema=False)
def get_user_access_token(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends()):
    user = authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")

    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
