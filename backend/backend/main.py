from typing import Union
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from os import getenv
from pydantic import BaseModel
from .models import Base, TextMessage, IPList, Customer
from .core.database import get_db, engine  # Move database setup to core/database.py
from .api.endpoints import text  # Import the text router
import random
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI(title="Anomal.AI")

# Include the text router
app.include_router(text.router, prefix="/api")

# Remove the /text endpoint as it's now handled by the router

@app.get("/is_blocked")
async def is_blocked(db: Session = Depends(get_db)):
    # Get real IP from request in production
    ip = f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
    blocked_ip = db.query(IPList).filter(IPList.ip_address == ip).first()
    return {"ip": ip, "is_blocked": blocked_ip.is_blocked if blocked_ip else False}

@app.get("/")
async def read_root(db: Session = Depends(get_db)):
    try:
        db.execute("SELECT 1")
        return {"msg": "Health Ok", "database": "connected"}
    except Exception as e:
        return {"msg": "Health Ok", "database": "not connected", "error": str(e)}

@app.post("/test")
async def test(db: Session = Depends(get_db)):
    pass
