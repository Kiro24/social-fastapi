from fastapi import FastAPI


from . import models
from .database import engine
from .routers import user, post, auth, vote


# to make sa setup first db
# models.Base.metadata.create_all(bind=engine)

app = FastAPI() 


   


app.include_router(auth.router, prefix="/auth", tags=["Authentication"])        
app.include_router(user.router, prefix="/users", tags=["Users"])
app.include_router(post.router, prefix="/posts", tags=["Posts"])
app.include_router(vote.router, prefix="/vote", tags=["Votes"])