from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .config import settings

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.db_username}:{settings.db_passwd}@{settings.db_hostname}:{settings.db_port}/{settings.db_name}"
# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:123465@localhost/fastapi-db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

#dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 
        
        
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