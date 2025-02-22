import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from auth.db import Base

import pytest


@pytest.fixture(scope='function')
def create_session():
    engine = create_engine('sqlite:///test_auth.db')

    Base.metadata.create_all(engine)

    session_ = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

    yield session_

    session_.rollback()
    session_.close()
    os.remove('test_auth.db')
