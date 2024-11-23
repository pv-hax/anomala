from fastapi import FastAPI, HTTPException, Depends, Request
from sqlalchemy.orm import Session
from .models import Base, TextMessage, IPList, Customer
from .core.database import get_db, engine 
from .api.endpoints import text  
import logging
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

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
async def is_blocked(request: Request, db: Session = Depends(get_db)):
    forwarded_for = request.headers.get("X-Forwarded-For")
    if forwarded_for:
        ip = forwarded_for.split(",")[0].strip()
    else:
        ip = request.client.host
    
    blocked_ip = db.query(IPList).filter(IPList.ip == ip).first()
    
    return {
        "ip": ip,
        "is_blocked": blocked_ip.is_blocked if blocked_ip else False
    }

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
