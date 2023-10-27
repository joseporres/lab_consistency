from fastapi import FastAPI,Depends,HTTPException
from starlette.middleware.cors import CORSMiddleware
from app.config.settings import api_settings
import uvicorn
from fastapi.responses import JSONResponse
from datetime import datetime
from app.database import SessionLocal
from sqlalchemy.orm import Session
import app.crud as crud
from app.schemas import Item


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI(
    title=api_settings.TITLE,
    openapi_url=f'{api_settings.PREFIX}/openapi.json',
    docs_url=f'{api_settings.PREFIX}/docs',
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# set prefix  all routes
app.router.prefix = api_settings.PREFIX

@app.get("/")
def root():
    return {"message": f"Welcome to {api_settings.TITLE}"}

#get all products /query?type=ALL
#query from db mysql with sqlalchemy
@app.get("/query")
def get_all_products(item_id: str = None, db: Session = Depends(get_db)):
    if item_id:
        resItem = crud.get_item(db, item_id)
        if resItem:
            return JSONResponse(
                status_code=200,
                content=resItem
            )
        else:
            raise HTTPException(status_code=404, detail="Item not found")
    else:
        items = crud.get_all_items(db)
        return JSONResponse(
            status_code=200,
            content=items
        )


@app.post("/buy-transaction")
def buy_transaction(
    item : Item,
    db: Session = Depends(get_db)):
    resItem = crud.buy_item_with_transation(db, item)
    if resItem:
        return JSONResponse(
            status_code=200,
            content=resItem
        )
    else:
        raise HTTPException(status_code=404, detail="Item not found")

# # buy item from shop /buy
# @app.post("/buy-pesimistic")
# def buy_pesimistic(
#     item : Item,
#     db: Session = Depends(get_db)):
#     resItem = crud.buy_item_pessimistic_locking(db, item)
#     if resItem:
#         return JSONResponse(
#             status_code=200,
#             content=resItem
#         )
#     else:
#         raise HTTPException(status_code=404, detail="Item not found")

@app.post("/buy-optimistic")
def buy_optimistic(
    item : Item,
    db: Session = Depends(get_db)):
    resItem = crud.buy_item_optimistic_locking(db, item)
    if resItem:
        return JSONResponse(
            status_code=200,
            content=resItem
        )
    else:
        raise HTTPException(status_code=404, detail="Item not found")
    


@app.post("/buy")
def buy(
    item : Item,
    db: Session = Depends(get_db)):
    resItem = crud.buy_item(db, item)
    if resItem:
        return JSONResponse(
            status_code=200,
            content=resItem
        )
    else:
        raise HTTPException(status_code=404, detail="Item not found")
    

@app.post('/insert')
def insert( 
    item : Item ,
    db: Session = Depends(get_db)):
    resItem = crud.add_item(db, item)
    return JSONResponse(
        status_code=200,
        content=resItem
    )

    
def run():
    uvicorn.run(app,
                host=api_settings.HOST,
                port=api_settings.PORT,
                )
