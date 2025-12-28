from sqlalchemy import Column, Integer, String, DateTime
from database import Base

class Attack(Base):
    __tablename__ = "attacks"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
