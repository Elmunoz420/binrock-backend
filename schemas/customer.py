from pydantic import BaseModel
from datetime import datetime
from typing import Optional


# Schema para crear un cliente
class CustomerCreate(BaseModel):
    full_name: str
    email: Optional[str] = None
    ig_username: Optional[str] = None
    phone: Optional[str] = None
    national_id: Optional[str] = None


# Schema para devolver un cliente
class CustomerResponse(BaseModel):
    id: int
    full_name: str
    email: Optional[str] = None
    ig_username: Optional[str] = None
    phone: Optional[str] = None
    national_id: Optional[str] = None

    class Config:
        orm_mode = True