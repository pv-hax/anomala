from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from os import getenv

# Direct database connection using docker network
SQLALCHEMY_DATABASE_URL = "postgresql://yourusername:yourpassword@db:5432/yourdbname"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
