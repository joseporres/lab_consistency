from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base


# item from item shop
class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True,
                autoincrement=True,
                index=True)
    quantity = Column(Integer, default=10)
