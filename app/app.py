from fastapi import FastAPI, Request,Header, Response
from starlette.middleware.cors import CORSMiddleware
from app.config.settings import api_settings
import uvicorn
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from datetime import datetime
import requests

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
def get_all_products(type: str):
    try:
        +

# buy item from shop /buy
@app.post("/buy")


def run():
    uvicorn.run(app,
                host=api_settings.HOST,
                port=api_settings.PORT,
                )
