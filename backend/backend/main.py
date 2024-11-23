from fastapi import FastAPI, HTTPException, Depends, Request
from pydantic import BaseModel
from sqlalchemy.orm import Session
from datetime import datetime
from zoneinfo import ZoneInfo
from sqlalchemy import desc
from typing import List
from .models import Base, TextMessage, IPList, Customer
from .core.database import get_db, engine 
from .api.endpoints import text  
import logging
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from .api.dependencies import get_client_ip

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI(title="Anomal.AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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
            "Access-Control-Allow-Methods": "*",
            "Access-Control-Allow-Headers": "Content-Type, Authorization, Origin, Accept",
            "Access-Control-Max-Age": "600",
        }
    )

@app.get("/is_blocked")
async def is_blocked(
    request: Request, 
    db: Session = Depends(get_db)
):
    try:
        ip, domain = get_client_ip(request, db=db)
        
        logger.info(f"Checking IP: {ip}, Domain: {domain}")
        
        ip_blocked = (
            db.query(IPList)
            .filter(
                IPList.ip_address == ip,
                IPList.domain == domain,
                IPList.is_blocked == True
            )
            .first()
        )
        
        return {
            "ip": ip,
            "domain": domain,
            "is_blocked": bool(ip_blocked)
        }
        
    except Exception as e:
        logger.error(f"Error in is_blocked: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/")
async def read_root(db: Session = Depends(get_db)):
    try:
        db.execute("SELECT 1")
        return {"msg": "Health Ok", "database": "connected"}
    except Exception as e:
        return {"msg": "Health Ok", "database": "not connected", "error": str(e)}


# Pydantic models for response
class AttackLog(BaseModel):
    ip: str
    type_of_attack: str
    timestamp: datetime | None = None
    blocked: bool

class AttackLogsResponse(BaseModel):
    timestamp: datetime
    logs: List[AttackLog]

@app.get("/attack-logs", response_model=AttackLogsResponse)
async def get_attack_logs(db: Session = Depends(get_db)):
    # Get the current timestamp in UTC
    current_time = datetime.now(ZoneInfo("UTC"))

    # Query the most recent 850 text messages, ordered by newest first
    messages = (
        db.query(TextMessage)
        .order_by(desc(TextMessage.created_at))
        .limit(850)
        .all()
    )

    # Transform the database records into the response format
    logs = [
        AttackLog(
            ip=message.ip_address,
            type_of_attack="sqlinjection",  # Since we're only dealing with TextMessage
            timestamp=message.created_at,
            blocked=message.caused_block if message.caused_block is not None else False
        )
        for message in messages
    ]

    return AttackLogsResponse(
        timestamp=current_time,
        logs=logs
    )
