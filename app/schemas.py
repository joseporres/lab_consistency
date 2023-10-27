from pydantic import BaseModel
from pydantic.fields import Field
from typing import Annotated

class Item(BaseModel):
    id: Annotated[int, Field(..., description="Id del item")]
    quantity: Annotated[int, Field(..., description="quantity del item")] 
    version: Annotated[int, Field(..., description="version del item")]
    # class Config:
    #     orm_mode = True


def serialize_item(item):
    return {
        "id": item.id,
        "quantity": item.quantity,
        "version": item.version
    }

class ResponseItem(BaseModel):
    id: int
    quantity: int
    version: int

def serialize_response_item(item):
    return {
        "id": item.id,
        "quantity": item.quantity,
        "version": item.version
    }