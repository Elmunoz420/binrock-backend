from sqlalchemy import Column, String, Integer
from db import Base

class OrderStatus(Base):
    __tablename__ = "order_status"

    code = Column(String(20), primary_key=True, index=True)
    sort_order = Column(Integer, nullable=False)
