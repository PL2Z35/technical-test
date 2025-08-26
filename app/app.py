from fastapi import FastAPI
from sqlmodel import SQLModel
from routes.products import router as products_router
from routes.clients import router as clients_router
from routes.sales import router as sales_router

from database import engine, create_db_and_tables

create_db_and_tables()

app = FastAPI()

app.include_router(products_router)
app.include_router(clients_router)
app.include_router(sales_router)

@app.get("/")
def read_root():
    return {"Hello": "World"}