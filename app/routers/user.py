from fastapi import Depends, status, Depends, APIRouter
from sqlalchemy.orm import Session

from .. import models, schemas, utils
from ..database import get_db

router = APIRouter()

@router.get("/{id}", status_code= status.HTTP_200_OK, response_model=schemas.UserResponse)
def get_user(id:int, db: Session=Depends(get_db)):

    user = db.query(models.User).filter(models.User.id == id).first()
    utils.validate_not_empty(id, user)
    return user
    
    
@router.post("/", status_code= status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session=Depends(get_db)):
    # hash psswd
    user.password = utils.hash(user.password)
    
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user