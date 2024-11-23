from fastapi import Request, HTTPException
from typing import Tuple
import ipaddress

def get_client_ip(request: Request) -> Tuple[int, str]:
    """
    Get client IP and domain from request
    Returns: (ip_as_int, domain)
    """
    # Get IP
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        ip = forwarded.split(",")[0]
    else:
        ip = request.client.host
    
    # Get domain from Origin header
    domain = request.headers.get("Origin")
    if domain:
        # Strip http:// or https:// if present
        domain = domain.replace("http://", "").replace("https://", "")
        # Remove port if present
        domain = domain.split(":")[0]
    else:
        raise HTTPException(status_code=400, detail="Origin header is required")
    
    print(f"Debug - IP: {ip} ({ip}), Domain: {domain}")  # Debug line
    return ip, domain