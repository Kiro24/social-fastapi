from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
import pytest

from app.main import app
from app.config import settings
from app.database import get_db, Base



SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.db_username}:{settings.db_passwd}@{settings.db_hostname}:{settings.db_port}/fastapi_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)



@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close() 

@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close() 
    # run code before test
    # create all tables
    # dependancy override
    app.dependency_overrides[get_db] = override_get_db  
    yield TestClient(app)
    