from sqlalchemy import Column, Integer, ForeignKey, Numeric, String, TIMESTAMP
from db import Base

class ProductCost(Base):
    __tablename__ = "product_cost"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("product.id"), nullable=False)
    country_code = Column(String(3), nullable=False)
    cost = Column(Numeric(10, 2), nullable=False)
    effective_from = Column(TIMESTAMP, nullable=True)
