from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ProductBase(BaseModel):
    sku_base: str
    name: str
    description: Optional[str] = None
    is_active: Optional[bool] = True

class ProductCreate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: int
    created_at: Optional[datetime] = None   # 👈 opcional
    price: float = 0.0
    cost: float = 0.0

    class Config:
        from_attributes = True

