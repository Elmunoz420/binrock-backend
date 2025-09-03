from sqlalchemy import Column, String, CHAR
from db import Base

class Country(Base):
    __tablename__ = "country"

    code = Column(CHAR(3), primary_key=True, index=True)
    name = Column(String(100), nullable=False)
