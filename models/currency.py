from sqlalchemy import Column, String
from db import Base

class Currency(Base):
    __tablename__ = "currency"   # exactamente el mismo nombre que en MySQL
    code = Column(String(3), primary_key=True, index=True)
    name = Column(String(60), nullable=False)
    symbol = Column(String(6), nullable=True)
