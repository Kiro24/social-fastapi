import time
from typing import Optional, List
from fastapi import Depends, FastAPI, Response, status, HTTPException, Depends
from sqlalchemy.orm import Session

from . import models, schemas
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI() 


   
    
# while True:
#     try:
#         conn = psycopg2.connect(host="localhost",
#                                 database="fastapi-db",
#                                 user="postgres",
#                                 password="123465",
#                                 cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("DB connected successfully!")
#         break
#     except Exception as e:
#         print(f"DB Failed to connect: {e}")
#         time.sleep(2)
        
        
def validate_post_not_empty(id: int, post: schemas.PostCreate):
    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail= f"post with id: {id} was not found.")

     

@app.get("/posts")
def get_posts(db: Session=Depends(get_db), response_model=List[schemas.PostResponse]):
    # posts = cursor.execute(""" SELECT * FROM posts""")
    # posts = cursor.fetchall()
    
    posts = db.query(models.Post).all()
    
    return posts


@app.post("/posts", status_code= status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_posts(post: schemas.PostCreate, db: Session=Depends(get_db)):
    # to prevent SQLi
    # cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, 
    #                (post.title, post.content, post.published))
    # post = cursor.fetchone()
    # # saves item to db
    # conn.commit()
    
    post = models.Post(**post.dict())
    db.add(post)
    db.commit()
    db.refresh(post)
    
    return post



@app.get("/posts/{id}")
def get_post(id: int, res: Response, db: Session=Depends(get_db), response_model=schemas.PostResponse):
    # cursor.execute(""" SELECT * FROM posts WHERE id = (%s) """, (str(id),))
    # post = cursor.fetchone()
    
    post = db.query(models.Post).filter(models.Post.id == id).first()
    validate_post_not_empty(id, post)
        
    return post


@app.delete("/posts/{id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session=Depends(get_db)):
    # cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """, (str(id)), )
    # deleted_post = cursor.fetchone()
    # conn.commit()
    
    # post SQL query then executes it within validate post
    post_query = db.query(models.Post).filter(models.Post.id == id)
    validate_post_not_empty(id, post_query.first())
    post_query.delete(synchronize_session=False)
    db.commit()


        
    
@app.put("/posts/{id}")
def update_post(id: int, post: schemas.PostCreate, db: Session=Depends(get_db), response_model=schemas.PostResponse):
        # cursor.execute(""" UPDATE posts SET title=%s, content=%s, published=%s WHERE id=%s RETURNING * """,
        #                (post.title, post.content, str(post.published), str(id)) )
        # updated_post = cursor.fetchone()
        # conn.commit()
        
        post_query = db.query(models.Post).filter(models.Post.id == id)
        
        validate_post_not_empty(id, post_query.first())
        post_query.update(post.dict(), synchronize_session=False)
        db.commit()
        
        
        return post_query.first()