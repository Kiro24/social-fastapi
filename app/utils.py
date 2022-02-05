import pwd
from fastapi import HTTPException, status
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def validate_not_empty(id: int, res):
    if not res:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail= f"resource with id: {id} was not found.")

def hash(password: str):
    return pwd_context.hash(password)

def verify(plain_passwd, hashed_passwd):
    return pwd_context.verify(plain_passwd, hashed_passwd)