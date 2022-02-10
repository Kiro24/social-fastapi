import pytest
from app import models

@pytest.fixture
def test_vote(test_posts, session, test_user):
    new_vote = models.Vote(post_id=test_posts[3].id, user_id=test_user["id"])
    session.add(new_vote)
    session.commit()



def test_vote_on_post(auth_client, test_posts):
    res =auth_client.post("/vote/", json={"post_id": test_posts[3].id, "dir": 1})
    
    assert res.status_code == 201
    
    

def test_vote_twice_on_post(auth_client, test_posts, test_vote):
    res =auth_client.post("/vote/", json={"post_id": test_posts[3].id, "dir": 1})
    
    assert res.status_code == 409
    

def test_unvote_on_post(auth_client, test_posts, test_vote):
    res =auth_client.post("/vote/", json={"post_id": test_posts[3].id, "dir": 0})
    
    assert res.status_code == 201
    
def test_unvote_twice_on_post(auth_client, test_posts):
    res =auth_client.post("/vote/", json={"post_id": test_posts[3].id, "dir": 0})
    
    assert res.status_code == 404
    
def test_vote_on_nonexist_post(auth_client, test_posts):
    res =auth_client.post("/vote/", json={"post_id": 20000, "dir": 1})
    
    assert res.status_code == 404
    
def test_unvote_on_nonexist_post(auth_client, test_posts):
    res =auth_client.post("/vote/", json={"post_id": 20000, "dir": 0})
    
    assert res.status_code == 404
    
def test_unauth_vote(client, test_posts):
    res =client.post("/vote/", json={"post_id": test_posts[3].id, "dir": 1})
    
    assert res.status_code == 401
    
def test_unauth_unvote(client, test_posts):
    res =client.post("/vote/", json={"post_id": test_posts[3].id, "dir": 0})
    
    assert res.status_code == 401