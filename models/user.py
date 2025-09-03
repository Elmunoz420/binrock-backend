from sqlalchemy import Column, Integer, String, Enum, DateTime
from datetime import datetime
import enum

from db import Base

# Enum para roles
class Role(enum.Enum):
    ADMIN = "ADMIN"
    OPERACIONES = "OPERACIONES"
    PROVEEDOR = "PROVEEDOR"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(120), nullable=False)
    email = Column(String(120), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(Enum(Role), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
