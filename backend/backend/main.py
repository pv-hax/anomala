from typing import Union
from fastapi import FastAPI, HTTPException, Depends, Request
from sqlalchemy.orm import Session
from os import getenv
from pydantic import BaseModel
from .models import Base, TextMessage, IPList, Customer
from .core.database import get_db, engine 
from .api.endpoints import text  
import random
import logging
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI(title="Anomal.AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["127.0.0.1:5500", "localhost:5500", "127.0.0.1", "localhost", "http://127.0.0.1:5500"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
    expose_headers=["*"],
    max_age=600,
)

app.include_router(text.router, prefix="/api")

@app.options("/{full_path:path}")
async def options_handler(request: Request):
    return JSONResponse(
        content="OK",
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type, Authorization, Origin, Accept",
            "Access-Control-Max-Age": "600",
        }
    )

@app.get("/is_blocked")
async def is_blocked(db: Session = Depends(get_db)):
    # Get real IP from request in production
    ip = f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
    blocked_ip = True
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
