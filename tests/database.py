from fastapi.testclient import TestClient
import pytest
from app.main import app

from app.config import setting
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.database import get_db, Base

# SQLALCHEMY_DATABASE_URL ='postgresql://<username>:<password>@<ip-address/hostname>/<database_name>'
SQLALCHEMY_DATABASE_URL = f'postgresql://{setting.database_username}:{setting.
                database_password}@{setting.database_hostname}:{setting.database_port}/{setting.database_name}_test'
# by adding _test we can pull db password etc from env variable


engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base.metadata.create_all(bind = engine)
    
# client = TestClient(app)

# we can define the scope of fixture 
@pytest.fixture()
def session():
    print("my session fixture ran")
    Base.metadata.drop_all(bind = engine)
    Base.metadata.create_all(bind = engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()    

# Fixture is like a function that runs before test
@pytest.fixture()
def client(session):
    def override_get_db():
    
     try:
        yield session
     finally:
        session.close()    

    app.dependency_overrides[get_db] = override_get_db   
    yield TestClient(app)