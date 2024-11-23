from typing import Tuple
from fastapi import Request, HTTPException, Depends
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..models import IPList, Customer

def get_client_ip(
    request: Request, 
    db: Session = Depends(get_db),
    require_origin: bool = True
) -> Tuple[str, str]:
    """
    Get client IP and domain from request and ensure IP exists in database
    Returns:
        Tuple[str, str]: Tuple of (ip_address, domain)
    """
    # Get IP
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        ip = forwarded.split(",")[0].strip()
    else:
        ip = request.client.host or ""
    
    # Validate IP
    if not ip:
        raise HTTPException(status_code=400, detail="Could not determine client IP")
    
    # Always get domain since we're changing the default behavior
    domain = request.headers.get("Origin")
    if not domain and require_origin:
        raise HTTPException(status_code=400, detail="Origin header is required")
    
    domain = domain or ""
    # Strip http:// or https:// if present
    domain = domain.replace("http://", "").replace("https://", "")
    # Remove port if present
    domain = domain.split(":")[0]
    
    # Check if IP exists in database
    ip_entry = db.query(IPList).filter(IPList.ip_address == str(ip)).first()
    
    if not ip_entry:
        # Create new IP entry
        ip_entry = IPList(
            ip_address=str(ip),
            domain=domain,
            is_blocked=False,  # Default to not blocked
            request_count=1
        )
        db.add(ip_entry)
    else:
        # Update existing entry
        ip_entry.request_count += 1
        if domain and not ip_entry.domain:
            ip_entry.domain = domain
    
    try:
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to update IP database")
    
    return ip, domain