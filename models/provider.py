from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from db import Base

class Provider(Base):
    __tablename__ = "providers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), nullable=False)
    contact_email = Column(String(120))
    contact_phone = Column(String(50))
    is_active = Column(Boolean, default=True)

    orders = relationship("Order", back_populates="provider")
