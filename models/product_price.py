from sqlalchemy import Column, Integer, ForeignKey, Numeric, String, TIMESTAMP
from db import Base

class ProductPrice(Base):
    __tablename__ = "product_price"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("product.id"), nullable=False)
    country_code = Column(String(3), nullable=False)
    currency_code = Column(String(3), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    effective_from = Column(TIMESTAMP, nullable=True)
