#  Things in this file is global for all in the package [or say test folder] so we don't have to
#  keep importing around 

from fastapi.testclient import TestClient
import pytest
from app.main import app
from app.oauth2 import create_access_token
from app.config import setting
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.database import get_db, Base
from app import model

# SQLALCHEMY_DATABASE_URL ='postgresql://<username>:<password>@<ip-address/hostname>/<database_name>'
SQLALCHEMY_DATABASE_URL = f'postgresql://{setting.database_username}:{setting.database_password}@{setting.database_hostname}:{setting.database_port}/{setting.database_name}_test'
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


@pytest.fixture
def test_user(client):
    user_data = {"email": "hello@gmail.com", "password": "password123"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201

    print(res.json())
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture
def token(test_user):
   return create_access_token({"user_id": test_user['id']})

@pytest.fixture
def authorized_client(client, token):
   client.headers = {
      **client.headers,
      "Authorization": f"Bearer {token}"
   }
   return client

@pytest.fixture
def test_posts(test_user, session):
    posts_data = [
        {
            "title": "first title",
            "content": "first content",
            "owner_id": test_user['id']
        },
        {
            "title": "2nd title",
            "content": "2nd content",
            "owner_id": test_user['id']
        },
        {
            "title": "3rd title",
            "content": "3rd content",
            "owner_id": test_user['id']
        }
    ]

    # instead of using the below method we can also use map function and convert into list and pass into session.add_all
    session.add_all([model.Post(title="first title", content="first content", owner_id=test_user['id']),
                   model.Post(title="2nd title", content="2nd content", owner_id=test_user['id']),
                    model.Post(title="3rd title", content="3rd content", owner_id=test_user['id'])])
    session.commit()
    posts = session.query(model.Post).all()
    return posts