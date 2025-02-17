from pydantic import BaseModel, EmailStr, field_validator


class InputModel(BaseModel):
    email: EmailStr
    name: str
    age: int
    tags: list[str] = []

    @field_validator("age")
    def validate_age(cls, v):
        if v < 18 or v > 100:
            raise ValueError("Age must be between 18 and 100")
        return v
