from sqlalchemy import select

from auth.conftest import create_session
from auth.db import User
from auth.operations import add_user


def test_create_user(create_session):
    add_user(create_session, 'test_name', 'password', 'test_name@example.com')
    [user_from_db] = create_session.execute(select(User)).scalars().all()

    assert user_from_db.username == 'test_name'


def test_create_user_integrity_error(create_session):
    add_user(create_session, 'test_name', 'password', 'test_name@example.com')
    result = add_user(create_session, 'test_name', 'password', 'test_name@example.com')

    assert result is None
