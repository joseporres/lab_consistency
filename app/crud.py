from sqlalchemy.orm import Session
from app import models, schemas
from app.schemas import serialize_item

##################################################################
############## PRIVATE FUNCTIONS #################################
##################################################################
def add_item(db: Session, item: schemas.Item):
    db_item = models.Item(id=item.id, quantity=item.quantity)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return serialize_item(item)

##################################################################
##################################################################
##################################################################

##################################################################
############## SIMPLE CRUD #######################################
##################################################################

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

def get_all_items(db: Session):
    return db.query(models.Item).all()

def buy_item(db: Session, item: schemas.Item):
    db_item = db.query(models.Item).filter(models.Item.id == item.id).first()
    if db_item:
        db_item.quantity -= item.quantity
        db.commit()
        db.refresh(db_item)
        return serialize_item(db_item)
    else:
        return None
    
# ##################################################################
# ##################################################################
# ##################################################################


# ##################################################################
# ############## Concurrency Control ###############################
# ##################################################################

def buy_item_with_transation(db:Session, item:schemas.Item):
    db_item = db.query(models.Item).filter(models.Item.id == item.id).with_for_update().first()
    if db_item:
        if db_item.quantity >= item.quantity:
            db_item.quantity -= item.quantity
            db.commit()
            db.refresh(db_item)
            return serialize_item(db_item)
        else:
            raise Exception("Not enough items in stock")
    else:
        return None

    
def buy_item_optimistic_locking(db: Session, item: schemas.Item):
    db_item = db.query(models.Item).filter(models.Item.id == item.id).first()
    if db_item:
        if db_item.quantity >= item.quantity:
            db_item.quantity -= item.quantity
            db_item.version += 1  # Increment the version to indicate the change
            db.commit()
            db.refresh(db_item)
            return serialize_item(db_item)
        else:
            raise Exception("Not enough items in stock")
    else:
        return None
    
def buy_item_pessimistic_locking(db: Session, item: schemas.Item):
    db_item = db.query(models.Item).filter(models.Item.id == item.id).with_for_update().first()
    if db_item:
        if db_item.quantity >= item.quantity:
            db_item.quantity -= item.quantity
            db.commit()
            db.refresh(db_item)
            return serialize_item(db_item)
        else:
            raise Exception("Not enough items in stock")
    else:
        return None
    
##################################################################
##################################################################
##################################################################

