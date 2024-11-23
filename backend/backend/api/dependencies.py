from typing import Tuple
from fastapi import Request, HTTPException, Depends
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..models import IPList, Customer
from ipaddress import ip_address as validate_ip

def get_client_ip(
    request: Request, 
    db: Session,
    require_origin: bool = False
) -> Tuple[str, str]:
    """
    Get client IP and domain from request and ensure IP exists in database
    Returns:
        Tuple[str, str]: Tuple of (ip_address, domain)
    """
    # Get IP - check headers in priority order
    ip = None
    
    # Check common proxy headers
    if request.headers.get("CF-Connecting-IP"):  # Cloudflare
        ip = request.headers.get("CF-Connecting-IP")
    elif request.headers.get("X-Real-IP"):  # Nginx proxy
        ip = request.headers.get("X-Real-IP")
    elif request.headers.get("X-Forwarded-For"):  # Standard proxy header
        # X-Forwarded-For can contain multiple IPs, get the first one
        ip = request.headers.get("X-Forwarded-For").split(",")[0].strip()
    
    # Fallback to direct client IP
    if not ip:
        ip = request.client.host
    
    # Validate IP format
    try:
        validate_ip(ip)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid IP address format")
    
    # Validate IP
    if not ip:
        raise HTTPException(status_code=400, detail="Could not determine client IP")
    
    # Safely handle domain verification
    domain = request.headers.get("Origin", "")
    if domain:
        try:
            # Strip http:// or https:// if present
            domain = domain.replace("http://", "").replace("https://", "")
            # Remove port if present
            domain = domain.split(":")[0].strip()
            # Additional validation could go here
        except Exception:
            # If any error occurs during domain processing, set to empty string
            domain = ""
    
    if require_origin and not domain:
        raise HTTPException(status_code=400, detail="Valid Origin header is required")
    
    # Check if IP exists in database
    ip_entry = db.query(IPList).filter(IPList.ip_address == str(ip)).first()
    
    if not ip_entry:
        # Create new IP entry
        ip_entry = IPList(
            ip_address=str(ip),
            domain=domain,
            is_blocked=False  # Default to not blocked
        )
        db.add(ip_entry)
    else:
        # Update existing entry only if we have a new domain
        if domain and not ip_entry.domain:
            ip_entry.domain = domain
    
    try:
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to update IP database")
    
    return ip, domain