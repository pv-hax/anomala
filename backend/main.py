from typing import Union
from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from os import getenv
from pydantic import BaseModel
from models import Base, TextMessage
import random

app = FastAPI(title="Anomal.AI")

# Get database URL from environment variable
DATABASE_URL = getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

# Create tables
Base.metadata.create_all(bind=engine)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class MessageRequest(BaseModel):
    message: str

@app.post("/text")
async def save_text(message_req: MessageRequest):
    try:
        db = SessionLocal()
        new_message = TextMessage(message=message_req.message)
        db.add(new_message)
        db.commit()
        db.refresh(new_message)
        db.close()
        return {"status": "success", "message": "Text saved successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/is_blocked")
async def is_blocked():
    # Generate a random IP address for demonstration
    ip = f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
    return {"ip": ip, "is_blocked": True}

# Keep your existing health check endpoint
@app.get("/")
async def read_root():
    try:
        with engine.connect() as connection:
            connection.execute("SELECT 1")
        return {"msg": "Health Ok", "database": "connected"}
    except Exception as e:
        return {"msg": "Health Ok", "database": "not connected", "error": str(e)}