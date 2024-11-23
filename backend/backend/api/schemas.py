from pydantic import BaseModel, Field
from typing import Dict, Optional
from datetime import datetime

class TextEventCreate(BaseModel):
    message: str = Field(..., description="Text message content")
    type: str = Field(..., description="Type of text event")

class MouseEventCreate(BaseModel):
    x: int = Field(..., description="X coordinate")
    y: int = Field(..., description="Y coordinate")
    viewport_x: int = Field(..., description="Viewport width")
    viewport_y: int = Field(..., description="Viewport height")

class NetworkEventCreate(BaseModel):
    headers: Dict = Field(..., description="Request headers")
    method: str = Field(..., description="HTTP method")
    body: Dict = Field(..., description="Request body")
    cookies: Dict = Field(..., description="Request cookies")
    url: str = Field(..., description="Request URL")
    status_code: int = Field(..., description="Response status code")

class DecisionResponse(BaseModel):
    ip_address: int
    is_malicious: bool
    event_id: int
