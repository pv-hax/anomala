from typing import Union
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from os import getenv
from pydantic import BaseModel
from .models import Base, TextMessage, BlockedIP, Customer
import random

app = FastAPI(title="Anomal.AI")

# Get database URL from environment variable
DATABASE_URL = getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class MessageRequest(BaseModel):
    message: str

@app.post("/text")
async def save_text(message_req: MessageRequest, db: Session = Depends(get_db)):
    try:
        new_message = TextMessage(
            message=message_req.message,
            ip_address=3232235777  # You'll want to get this from the request
        )
        db.add(new_message)
        db.commit()
        db.refresh(new_message)
        return {"status": "success", "message": "Text saved successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/is_blocked")
async def is_blocked(db: Session = Depends(get_db)):
    # Get real IP from request in production
    ip = f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
    blocked_ip = db.query(BlockedIP).filter(BlockedIP.ip_address == ip).first()
    return {"ip": ip, "is_blocked": blocked_ip.is_blocked if blocked_ip else False}

@app.get("/")
async def read_root(db: Session = Depends(get_db)):
    try:
        db.execute("SELECT 1")
        return {"msg": "Health Ok", "database": "connected"}
    except Exception as e:
        return {"msg": "Health Ok", "database": "not connected", "error": str(e)}