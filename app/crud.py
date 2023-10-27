from sqlalchemy.orm import Session
from app import models, schemas

def get_item(db: Session, itemId: str = None, page: int = 1, size: int = 10):
    skip = (page - 1) * size
    query = db.query(models.Item)

    if itemId:
        query = query.filter(models.Item.id == itemId)
    
    total = query.count()
    data = query.offset(skip).limit(size).all()
    data = [schemas.Item.from_orm(item) for item in data]
    return {
        "data": data,
        "total": total,
        "page": page,
        "pages": total // size + 1 if total % size > 0 else total // size,
        "size": size
    }
