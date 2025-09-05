from sqlalchemy import Column, Integer, String, TIMESTAMP, func
from sqlalchemy.orm import relationship
from db import Base

class Customer(Base):
    __tablename__ = "customer"

    id = Column(Integer, primary_key=True, index=True)
    ig_username = Column(String(100))
    phone = Column(String(50))
    national_id = Column(String(50))
    email = Column(String(255), unique=True)
    full_name = Column(String(160), nullable=False)

    # Ahora sí con default de Postgres
    created_at = Column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    # 👇 relación inversa para que funcione Order.customer
    orders = relationship("Order", back_populates="customer")
