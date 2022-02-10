import pytest
from app import schemas


def test_create_user(client):
    res = client.post("/users/", json={
        "email": "example@gmail.com",
        "password": "123456"
        })
    new_user = schemas.UserResponse(**res.json())
    assert res.status_code == 201
    
    
def test_login_user(client, test_user):
    res = client.post("/auth/login", data={
        "username": test_user["email"],
        "password": test_user["password"]
        })
    
    login_res = schemas.Token(**res.json())
    assert res.status_code == 200
    
@pytest.mark.parametrize("email, passwd, status_code", [
    ("wrong_email", "123456", 403),
    ("ti5a@example.com", "wrong_passwd", 403),
    ("wrong_email", "wrongs_passwd", 403),
    ("wrong_email", None, 422),
    (None, "123456", 422)
])    
def test_incorrect_login(client, test_user, email, passwd, status_code):
    res = client.post("/auth/login", data={
        "username": email,
        "password": passwd
        })
    
    assert res.status_code == status_code