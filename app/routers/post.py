from fastapi import APIRouter, Depends, Response, status, Depends
from sqlalchemy.orm import Session
from typing import List

from .. import models, schemas, utils, oauth2
from ..database import get_db

router = APIRouter()

@router.get("/", response_model=List[schemas.PostResponse])
def get_posts(db: Session=Depends(get_db), curr_user: int=Depends(oauth2.get_current_user)):
    # posts = cursor.execute(""" SELECT * FROM posts""")
    # posts = cursor.fetchall()
    
    posts = db.query(models.Post).all()
    
    return posts

@router.get("/{id}", response_model=schemas.PostResponse)
def get_post(id: int, res: Response, db: Session=Depends(get_db), curr_user: int=Depends(oauth2.get_current_user)):
    # cursor.execute(""" SELECT * FROM posts WHERE id = (%s) """, (str(id),))
    # post = cursor.fetchone()
    
    post = db.query(models.Post).filter(models.Post.id == id).first()
    utils.validate_not_empty(id, post)
        
    return post

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_posts(post: schemas.PostCreate, db: Session=Depends(get_db), curr_user: int=Depends(oauth2.get_current_user)):
    # to prevent SQLi
    # cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, 
    #                (post.title, post.content, post.published))
    # post = cursor.fetchone()
    # # saves item to db
    # conn.commit()
    print(curr_user.email)
    post = models.Post(**post.dict())
    db.add(post)
    db.commit()
    db.refresh(post)
    
    return post


@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(id: int, post: schemas.PostCreate, db: Session=Depends(get_db), curr_user: int=Depends(oauth2.get_current_user)):
        # cursor.execute(""" UPDATE posts SET title=%s, content=%s, published=%s WHERE id=%s RETURNING * """,
        #                (post.title, post.content, str(post.published), str(id)) )
        # updated_post = cursor.fetchone()
        # conn.commit()
        
        post_query = db.query(models.Post).filter(models.Post.id == id)
        
        utils.validate_not_empty(id, post_query.first())
        post_query.update(post.dict(), synchronize_session=False)
        db.commit()
        
        
        return post_query.first()
    



@router.delete("/{id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session=Depends(get_db), curr_user: int=Depends(oauth2.get_current_user)):
    # cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """, (str(id)), )
    # deleted_post = cursor.fetchone()
    # conn.commit()
    
    # post SQL query then executes it within validate post
    post_query = db.query(models.Post).filter(models.Post.id == id)
    utils.validate_not_empty(id, post_query.first())
    post_query.delete(synchronize_session=False)
    db.commit()


        
    

