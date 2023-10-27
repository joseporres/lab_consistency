from pydantic import BaseModel
from pydantic.fields import Field
from typing import Annotated

class Item(BaseModel):
    id: Annotated[int, Field(..., description="Id del item")]
    quantity: Annotated[int, Field(..., description="quantity del item")] 

    # class Config:
    #     orm_mode = True


def serialize_item(item):
    return {
        "id": item.id,
        "quantity": item.quantity
    }

class ResponseItem(BaseModel):
    id: int
    quantity: int

def serialize_response_item(item):
    return {
        "id": item.id,
        "quantity": item.quantity
    }