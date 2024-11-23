from sqlalchemy import Boolean, Column, Integer, String, BigInteger, DateTime, ForeignKey, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from datetime import datetime

Base = declarative_base()

class Customer(Base):
    __tablename__ = "customers"
    
    id = Column(Integer, primary_key=True, index=True)
    domain = Column(String(255), unique=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class IPList(Base):
    __tablename__ = "ip_lists"
    
    id = Column(Integer, primary_key=True, index=True)
    ip_address = Column(BigInteger, unique=True, nullable=False)
    is_blocked = Column(Boolean, default=False)
    domain = Column(String(255), ForeignKey("customers.domain"), nullable=False)

class TextMessage(Base):
    __tablename__ = "text_messages"
    
    id = Column(Integer, primary_key=True, index=True)
    domain = Column(String(255), ForeignKey("customers.domain"), nullable=False)
    ip_address = Column(BigInteger, nullable=False)
    message = Column(String(1000), nullable=False)
    type = Column(String(255), nullable=False)
    is_malicious = Column(Boolean, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    blocked_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class MouseEvent(Base):
    __tablename__ = "mouse_events"
    
    id = Column(Integer, primary_key=True, index=True)
    domain = Column(String(255), ForeignKey("customers.domain"), nullable=False)
    ip_address = Column(BigInteger, nullable=False)
    x = Column(Integer, nullable=False)
    y = Column(Integer, nullable=False)
    viewport_x = Column(Integer, nullable=False)
    viewport_y = Column(Integer, nullable=False)
    is_malicious = Column(Boolean, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    blocked_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class NetworkEvent(Base):
    __tablename__ = "network_events"
    
    id = Column(Integer, primary_key=True, index=True)
    domain = Column(String(255), ForeignKey("customers.domain"), nullable=False)
    ip_address = Column(BigInteger, nullable=False)
    headers = Column(JSON, nullable=False)
    method = Column(String(255), nullable=False)
    body = Column(JSON, nullable=False)
    cookies = Column(JSON, nullable=False)
    url = Column(String(2048), nullable=False)
    status_code = Column(Integer, nullable=False)
    is_malicious = Column(Boolean, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    blocked_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
