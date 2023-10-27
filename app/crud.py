from sqlalchemy.orm import Session
from app import models, schemas
from app.schemas import serialize_item
from sqlalchemy.orm.exc import StaleDataError


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

def get_item(db: Session, itemId:int):
    # query = db.query.(models.Item.id == itemId)
    query = db.query(models.Item).filter(models.Item.id == itemId).first()
    if query:
        return serialize_item(query)
    else:
        return None

def get_all_items(db: Session):
    # print("get_all_items")
    query = db.query(models.Item).all()
    # print(query)
    return [serialize_item(item) for item in query]

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
    try:
        db_item = db.query(models.Item).filter(models.Item.id == item.id).first()
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
    except StaleDataError:
        print("someone has changed the account, plz retry.")
    
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

