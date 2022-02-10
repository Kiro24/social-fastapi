import json
from turtle import update
from venv import create
import pytest
from app import schemas
from app.routers.post import update_post


def test_get_all_posts(auth_client, test_posts):
    res =auth_client.get("/posts/")
    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200
    
def test_unauth_user_get_all_posts(client, test_posts):
    res = client.get("/posts/")
    assert res.status_code == 401
    
def test_unauth_user_get_one_posts(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401
    
    
def test_get_one_post_dont_exist(auth_client, test_posts):
    res = auth_client.get(f"/posts/8888888")
    assert res.status_code == 404
    
    
def test_get_one_post(auth_client, test_posts):
    res = auth_client.get(f"/posts/{test_posts[0].id}")
    post = schemas.PostResponse(** res.json())
    assert post.Post.id == test_posts[0].id
    assert post.Post.title == test_posts[0].title
    assert post.Post.content == test_posts[0].content
    

@pytest.mark.parametrize("title, content, published", [
    ("first new title", "first new content", True),
    ("second new title", "second new content", False),
    ("newwset new title", "newwset new content", True),
])
def test_create_post(auth_client, test_user, test_posts, title, content, published):
    res = auth_client.post("/posts/", json={
        "title": title,
        "content": content,
        "published": published
    })
    created_post = schemas.PostIntermediate(**res.json())
    
    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.user.id == test_user["id"]
    
    
def test_default_published_value(auth_client, test_user, test_posts):
    res = auth_client.post("/posts/", json={
        "title": "test title",
        "content": "test content",
    })
    created_post = schemas.PostIntermediate(**res.json())
    
    assert res.status_code == 201
    assert created_post.title == "test title"
    assert created_post.content == "test content"
    assert created_post.published == True
    assert created_post.user.id == test_user["id"]
    
def test_unauth_user_create_posts(client, test_posts):
    res = client.post("/posts/", json={
        "title": "test title",
        "content": "test content",
    })
    assert res.status_code == 401
    
    
def test_delete_post(auth_client, test_posts):
    res = auth_client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 204
    
def test_delete_post_nonexist(auth_client, test_posts):
    res = auth_client.delete(f"/posts/4000000")
    assert res.status_code == 404
    
def test_unauth_user_delete_post(client, test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

def test_delete_other_user_post(auth_client, test_posts):
    res = auth_client.delete(f"/posts/{test_posts[3].id}")
    assert res.status_code == 403
    
    
def test_update_post(auth_client,test_user, test_posts):
    data = {
        "title": "updated post",
        "content": "updated content",
        "id": test_posts[0].id
    }
    res = auth_client.put(f"/posts/{test_posts[0].id}", json=data)
    
    updated_post = schemas.PostIntermediate(** res.json())
    assert res.status_code == 200
    assert updated_post.title == data["title"]
    assert updated_post.content == data["content"]
    assert updated_post.id == data["id"]
    
def test_update_other_user_post(auth_client, test_posts):
    data = {
        "title": "updated post",
        "content": "updated content",
        "id": test_posts[3].id
    }
    res = auth_client.put(f"/posts/{test_posts[3].id}", json=data)
    assert res.status_code == 403
    
def test_unauth_user_update_post(client, test_posts):
    data = {
        "title": "updated post",
        "content": "updated content",
        "id": test_posts[3].id
    }
    res = client.put(f"/posts/{test_posts[3].id}", json=data)
    assert res.status_code == 401
    
def test_update_post_nonexist(auth_client, test_posts):
    data = {
        "title": "updated post",
        "content": "updated content",
        "id": test_posts[3].id
    }
    res = auth_client.put(f"/posts/4000000", json=data)
    assert res.status_code == 404