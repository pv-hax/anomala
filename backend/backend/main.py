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
from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session
from typing import Dict
from pydantic import BaseModel


logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
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
        },
    )


@app.get("/is_blocked")
async def is_blocked(request: Request, db: Session = Depends(get_db)):
    ip, domain = get_client_ip(request, db=db)

    with db.begin():
        # Check if domain exists
        customer = db.query(Customer).filter(Customer.domain == domain).first()
        if not customer:
            customer = Customer(domain=domain)
            db.add(customer)
            db.flush()
    
        logger.info(f"Checking IP: {ip}, Domain: {domain}")
        ip_blocked = (
            db.query(IPList)
            .filter(IPList.ip_address == ip, IPList.is_blocked == True)
            .first()
        )
    
    if ip_blocked:
        logger.info(f"IP blocked: {ip_blocked}")
        raise HTTPException(status_code=403, detail="IP is blocked")
    logger.info(f"IP not blocked: {ip_blocked}")
    return {"ip": ip, "domain": domain, "is_blocked": bool(ip_blocked)}


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
        db.query(TextMessage).order_by(desc(TextMessage.created_at)).limit(850).all()
    )

    # Transform the database records into the response format
    logs = [
        AttackLog(
            ip=message.ip_address,
            type_of_attack=message.type,
            timestamp=message.created_at,
            blocked=message.caused_block if message.caused_block is not None else False,
        )
        for message in messages
    ]

    return AttackLogsResponse(timestamp=current_time, logs=logs)


@app.post("/unban-all")
async def unban_all(db: Session = Depends(get_db)):
    with db.begin():
        db.query(IPList).filter(IPList.is_blocked == True).update(
            {IPList.is_blocked: False}
        )
        db.flush()
    return {"msg": "All IPs unbanned"}


class AttackStats(BaseModel):
    total_attacks: int
    types_of_attacks: Dict[str, int]
    average_malicious_confidence: float
    total_blocked: int


@app.get("/stats", response_model=AttackStats)
async def get_attack_stats(db: Session = Depends(get_db)):
    # Get total number of attacks
    total_attacks = db.query(TextMessage).count()

    # Get counts of different types of attacks using group by
    type_counts = (
        db.query(TextMessage.type, func.count(TextMessage.id).label("count"))
        .group_by(TextMessage.type)
        .all()
    )

    # Convert the query results into a dictionary
    types_of_attacks = {attack_type: count for attack_type, count in type_counts}

    # Calculate average confidence score for malicious messages only
    avg_malicious_confidence = (
        db.query(func.avg(TextMessage.confidence_score))
        .filter(
            TextMessage.is_malicious is True, TextMessage.confidence_score.isnot(None)
        )
        .scalar()
        or 0.0
    )

    # Get total number of blocked attacks
    total_blocked = db.query(TextMessage).filter(TextMessage.caused_block == True).count()

    return AttackStats(
        total_attacks=total_attacks,
        types_of_attacks=types_of_attacks,
        average_malicious_confidence=round(avg_malicious_confidence, 2),
        total_blocked=total_blocked
    )
