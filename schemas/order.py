from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

# -------- Customer --------
class CustomerResponse(BaseModel):
    id: int
    full_name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    ig_username: Optional[str] = None
    national_id: Optional[str] = None

    class Config:
        orm_mode = True
        
# -------- Address --------
class AddressResponse(BaseModel):
    id: int
    street1: Optional[str] = None
    street2: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    country_code: Optional[str] = None

    class Config:
        orm_mode = True

# -------- Product --------
class ProductResponse(BaseModel):
    id: int
    sku_base: Optional[str] = None
    name: Optional[str] = None

    class Config:
        orm_mode = True

# -------- OrderItem --------
class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int
    unit_price: float
    unit_cost: float
    size: Optional[str] = None   # 👈 nuevo campo

class OrderItemResponse(BaseModel):
    id: int
    product_id: int
    quantity: int
    unit_price: float
    unit_cost: float
    size: Optional[str] = None
    product: Optional[ProductResponse] = None   # 👈 relación con product

    class Config:
        orm_mode = True

# -------- OrderEvent --------
class OrderEventResponse(BaseModel):
    id: int
    order_id: int
    event_type: str
    from_status: Optional[str] = None
    to_status: Optional[str] = None
    note: Optional[str] = None
    created_at: datetime

    class Config:
        orm_mode = True

# -------- Order --------
class OrderCreate(BaseModel):
    customer_id: int
    address_id: Optional[int] = None
    country_code: str
    currency_code: str
    shipping_fee: float = 0.0
    shipping_paid_by_customer: bool = True
    notes: Optional[str] = None
    provider_id: Optional[int] = None
    items: List[OrderItemCreate]

class OrderResponse(BaseModel):
    id: int
    customer_id: int
    address_id: Optional[int] = None
    country_code: str
    currency_code: str
    status_code: str
    items_count: int
    subtotal: float
    shipping_fee: float
    total_paid: float
    notes: Optional[str] = None
    created_at: datetime
    provider_id: Optional[int] = None   # 👈 nuevo campo

    # 👇 relaciones
    customer: Optional[CustomerResponse] = None
    address: Optional[AddressResponse] = None
    items: List[OrderItemResponse] = []
    events: List[OrderEventResponse] = []

    class Config:
        orm_mode = True
