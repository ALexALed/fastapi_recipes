from http.client import HTTPException

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from databases.connect_example.db import get_db, User
from databases.connect_example.models import UserBody, UserResponse

db_router = APIRouter(prefix="/db")

@db_router.post("/user")
def add_user(user: UserBody, db: Session = Depends(get_db)):
    user_object = User(name=user.name, email=user.email)
    db.add(user_object)
    db.commit()
    db.refresh(user_object)
    return user_object


@db_router.get('/user')
def get_user(user_id: int, db: Session = Depends(get_db)) -> UserResponse:
    user = db.query(User).filter(User.id==user_id).first()
    if user is None:
        raise HTTPException(status_code=404, details="User not found")
    return user

@db_router.patch('/user/{user_id}')
def update_user(user_id: int, user: UserBody, db: Session = Depends(get_db)):
    user_to_update = db.query(User).filter(User.id == user_id).first()
    if not user_to_update:
        raise HTTPException(status_code=404, details="User not found")
    user_to_update.name = user.name
    user_to_update.email = user.email
    db.commit()
    db.refresh(user_to_update)
    return user_to_update

@db_router.delete('/user/{user_id')
def delete_user(user_id, db: Session = Depends(get_db)):
    user_to_delete = db.query(User).filter(User.id == user_id).first()
    if not user_to_delete:
        raise HTTPException(status_code=404, details="User not found")

    db.delete(user_to_delete)
    db.commit()
    return {"detail": "User deleted"}
