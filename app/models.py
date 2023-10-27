from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base


# item from item shop
class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True,
                index=True)
    quantity = Column(Integer, default=10)
    version = Column(Integer, default=0)

    __mapper_args__ = {"version_id_col": version}
    
