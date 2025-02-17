from pydantic import BaseModel, EmailStr


class UserBody(BaseModel):
    name: str
    email: EmailStr


class UserResponse(BaseModel):
    id: int
