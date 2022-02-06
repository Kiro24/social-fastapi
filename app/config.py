from pydantic import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    db_hostname: str
    db_port: str
    db_name: str
    db_username: str
    db_passwd: str
    
    secret_key: str
    algorithm: str
    access_token_expire_mins: int
    
    class Config:
        env_file = ".env"
    
settings = Settings()

@lru_cache()
def get_settings():
    """Acts as a dependancy
    easier for testitng
    """
    return Settings()