from pydantic.v1 import BaseModel


class Item(BaseModel):
    id: int
    quantity: int

    class Config:
        orm_mode = True


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