from fastapi import Request, HTTPException
from typing import Tuple
import ipaddress

# def get_client_ip(request: Request) -> Tuple[int, str]:
#     """
#     Get client IP and domain from request
#     Returns: (ip_as_int, domain)
#     """
#     # Get IP
#     forwarded = request.headers.get("X-Forwarded-For")
#     if forwarded:
#         ip = forwarded.split(",")[0]
#     else:
#         ip = request.client.host
    
#     # Convert IP to integer
#     ip_int = int(ipaddress.ip_address(ip))
    
#     # Get domain from Origin header
#     domain = request.headers.get("Origin")
#     if domain:
#         # Strip http:// or https:// if present
#         domain = domain.replace("http://", "").replace("https://", "")
#         # Remove port if present
#         domain = domain.split(":")[0]
#     else:
#         raise HTTPException(status_code=400, detail="Origin header is required")
    
#     print(f"Debug - IP: {ip} ({ip_int}), Domain: {domain}")  # Debug line
#     return ip_int, domain


def get_client_ip(request: Request) -> Tuple[int, str]:
    """
    Mock function that returns a hardcoded IP and domain for testing
    Returns: (ip_as_int, domain)
    """
    # Mock values matching our seed data
    ip = "192.168.1.1"  # This converts to 3232235777
    domain = "example.com"
    
    ip_int = int(ipaddress.ip_address(ip))
    
    print(f"Debug - Using mock IP: {ip} ({ip_int}), Domain: {domain}")
    return ip_int, domain
