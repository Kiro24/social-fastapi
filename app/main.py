from fastapi import FastAPI

from . import models, schemas, utils
from .database import engine
from .routers import user, post, auth



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

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])        
app.include_router(user.router, prefix="/users", tags=["Users"])
app.include_router(post.router, prefix="/posts", tags=["Posts"])
