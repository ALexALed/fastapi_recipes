from dataclasses import Field

from fastapi import APIRouter

models_router = APIRouter(prefix='/models')

from pydantic import BaseModel, Field

class Book(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    author: str
    year: int

@models_router.post('/book')
async def create_book(book: Book):
    return { 'book': book }
