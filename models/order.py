from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Numeric, TIMESTAMP, Boolean
from sqlalchemy.orm import relationship
from db import Base

class Order(Base):
    __tablename__ = "order"

    id = Column(Integer, primary_key=True, index=True)
    order_code = Column(String(30), unique=True, nullable=True)
    customer_id = Column(Integer, ForeignKey("customer.id"), nullable=False)
    address_id = Column(Integer, ForeignKey("address.id"), nullable=True)
    country_code = Column(String(3), ForeignKey("country.code"), nullable=False)
    currency_code = Column(String(3), ForeignKey("currency.code"), nullable=False, default="USD")
    channel = Column(String(30), default="instagram_dm")
    status_code = Column(String(20), ForeignKey("order_status.code"), nullable=False)
    items_count = Column(Integer, default=0)
    subtotal = Column(Numeric(10, 2), default=0.00)
    shipping_fee = Column(Numeric(10, 2), default=0.00)
    shipping_paid_by_customer = Column(Boolean, default=True)
    shipping_policy_applied = Column(String(120), nullable=True)
    total_paid = Column(Numeric(10, 2), default=0.00)
    paid_at = Column(DateTime, nullable=True)
    notes = Column(String(255), nullable=True)
    created_at = Column(TIMESTAMP)
    provider_id = Column(Integer, ForeignKey("providers.id"), nullable=True)
    

    # Relaciones
    items = relationship("OrderItem", back_populates="order")
    events = relationship("OrderEvent", back_populates="order")

    # 👇 Agrega estas relaciones
    customer = relationship("Customer", back_populates="orders")
    address = relationship("Address", back_populates="orders")
    provider = relationship("Provider", back_populates="orders")  # relación con proveedor


class OrderItem(Base):
    __tablename__ = "order_item"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("order.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("product.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Numeric(10, 2), nullable=False)
    unit_cost = Column(Numeric(10, 2), nullable=False)
    size = Column(String(10))

    order = relationship("Order", back_populates="items")
    product = relationship("Product", back_populates="items")   # 👈 NUEVO


class OrderEvent(Base):
    __tablename__ = "order_event"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("order.id"), nullable=False)
    event_type = Column(String(40), nullable=False)
    from_status = Column(String(20), nullable=True)
    to_status = Column(String(20), nullable=True)
    note = Column(String(255), nullable=True)
    created_at = Column(TIMESTAMP)

    order = relationship("Order", back_populates="events")
