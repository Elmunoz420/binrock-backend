from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from db import Base

class Address(Base):
    __tablename__ = "address"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customer.id"), nullable=False)
    label = Column(String(60))
    street1 = Column(String(160), nullable=False)
    street2 = Column(String(160))
    city = Column(String(100), nullable=False)
    state = Column(String(100))
    postal_code = Column(String(20))
    country_code = Column(String(3), ForeignKey("country.code"), nullable=False)
    created_at = Column(TIMESTAMP)

    # 👇 relación inversa
    orders = relationship("Order", back_populates="address")
