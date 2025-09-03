from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AddressCreate(BaseModel):
    street1: str
    street2: Optional[str] = None
    city: str
    state: Optional[str] = None
    postal_code: Optional[str] = None
    country_code: str
    label: Optional[str] = None

class AddressResponse(AddressCreate):
    id: int
    customer_id: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
