from app import schema
import pytest
from jose import jwt 
from app.config import setting


# def test_root(client, session):
#     res = client.get("/")
#     print(res.json().get('message'))
#     assert res.json().get('message') ==  " HELLO USER!!! "
#     assert res.status_code == 200


def test_create_user(client):
    res = client.post("/users/", json={"email": "hello@gmail.com", "password": "password123"})
    new_user = schema.UserOut(** res.json())
    assert new_user.email == "hello@gmail.com"
    assert res.status_code == 201


def test_login_user(client, test_user):
    res = client.post("/login", data={"username": test_user['email'], "password": test_user['password']})
    login_res =schema.Token(**res.json())
    payload = jwt.decode(login_res.access_token, 
                         setting.secret_key, algorithms = [setting.algorithm])
    
    id = payload.get("user_id")
    assert id == test_user['id']
    assert login_res.token_type == "bearer"
    assert res.status_code == 200


@pytest.mark.parametrize("email, password, status_code", [
     ('wrongemail@gmail.com', 'password123', 403),
    ('hello@gmail.com', 'wrongpassword', 403),
    ('wrongemail@gmail.com', 'wrongpassword', 403),
    (None, 'password123', 422),
    ('hello@gmail.com', None, 422)
])
def test_incorrect_login(test_user, client, email, password, status_code):
    # Handle None values properly for form data
    form_data = {}
    if email is not None:
        form_data["username"] = email
    if password is not None:
        form_data["password"] = password
    
    res = client.post("/login", data=form_data) 
    assert res.status_code == status_code
    # assert res.json().get('detail') == 'Invalid Credentials'    