import json

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from databases.connect_example.db import get_db, User

db_router = APIRouter(prefix="/db")

@db_router.get("/")
def home(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return {"hello": [{"name": user.name} for user in users]}
