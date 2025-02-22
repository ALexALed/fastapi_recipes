from starlette import status

from . import db
from fastapi.testclient import TestClient
from main import app

db.DATABASE_URL = "sqlite:///./test_auth.db"

client = TestClient(app)


def test_register_user():
    response = client.post(
        '/auth/register/user',
        json={"username": "example", "email": "example@example.com", "password": "password"}
    )

    assert response.status_code == status.HTTP_201_CREATED
