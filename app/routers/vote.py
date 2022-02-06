from pyexpat import model
from fastapi import Response, APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, database, models, oauth2


router = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, 
         db: Session=Depends(database.get_db), 
         curr_user: models.User=Depends(oauth2.get_current_user)):
    
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Post {vote.post_id} does not exist.")
    
    vote_q = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id,
        models.Vote.user_id == curr_user.id)
    found_vote = vote_q.first() 
    
    
    if vote.dir == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"user {curr_user.id} has already voted on post {vote.post_id}.")
            
        new_vote = models.Vote(post_id=vote.post_id, user_id=curr_user.id)
        db.add(new_vote)
        db.commit()
        
        return {"detail": "successfully added vote"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Vote does not exist.")
    
        vote_q.delete(synchronize_session=False)
        db.commit()
        
        return {"detail": "successfully deleted vote"}
        
        