import time
from distutils.sysconfig import customize_compiler
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor

from app import database

app = FastAPI()

    
    
while True:
    try:
        conn = psycopg2.connect(host="localhost",
                                database="fastapi-db",
                                user="postgres",
                                password="123465",
                                cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("DB connected successfully!")
        break
    except Exception as e:
        print(f"DB Failed to connect: {e}")
        time.sleep(2)
        
        
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] 


def validate_post_not_empty(id: int, post: Post):
    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail= f"post with id: {id} was not found.")
    

@app.get("/posts")
async def get_posts():
    posts = cursor.execute(""" SELECT * FROM posts""")
    posts = cursor.fetchall()
    print(posts)
    return {"data": posts}


@app.post("/posts", status_code= status.HTTP_201_CREATED)
def create_posts(post: Post):
    # to prevent SQLi
    cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, 
                   (post.title, post.content, post.published))
    post = cursor.fetchone()
    # saves item to db
    conn.commit()
    return {"data": post}



@app.get("/posts/{id}")
def get_post(id: int, res: Response):
    cursor.execute(""" SELECT * FROM posts WHERE id = (%s) """, (str(id),))
    post = cursor.fetchone()
    validate_post_not_empty(id, post)
        
    return {"data": post}


@app.delete("/posts/{id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """, (str(id)), )
    deleted_post = cursor.fetchone()
    validate_post_not_empty(id, deleted_post)
    
    conn.commit()
    
    return {"data": deleted_post}

        
    
@app.put("/posts/{id}")
def update_post(id: int, post: Post):
        cursor.execute(""" UPDATE posts SET title=%s, content=%s, published=%s WHERE id=%s RETURNING * """,
                       (post.title, post.content, str(post.published), str(id)) )
        updated_post = cursor.fetchone()
        conn.commit()
        
        validate_post_not_empty(id, updated_post)
        return {"data": updated_post}