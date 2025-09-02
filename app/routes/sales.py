from fastapi import APIRouter, HTTPException, Body
from sqlmodel import Session, select
from models.sale import Sale
from models.client import Client
from models.product import Product
from models.sale_product import SaleProduct
from database import session_dep, engine
from typing import List

router = APIRouter()

@router.post("/sales/", response_model=Sale)
def create_sale(client_id: int = Body(...), products: List[dict] = Body(...), session: session_dep = None):
    client = session.get(Client, client_id)
    if not client or not client.active:
        raise HTTPException(status_code=400, detail="Client is not active or does not exist")
    sale = Sale(client_id=client_id)
    session.add(sale)
    session.commit()
    session.refresh(sale)
    for prod in products:
        product = session.get(Product, prod["product_id"])
        if not product or not product.active:
            raise HTTPException(status_code=400, detail=f"Product {prod['product_id']} is not active or does not exist")
        sale_product = SaleProduct(sale_id=sale.id, product_id=prod["product_id"], quantity=prod["quantity"])
        session.add(sale_product)
    session.commit()
    session.refresh(sale)
    return sale

@router.get("/sales/{sale_id}", response_model=Sale)
def read_sale(sale_id: int, session: session_dep):
    sale = session.get(Sale, sale_id)
    if not sale:
        raise HTTPException(status_code=404, detail="Sale not found")
    return sale

@router.get("/sales/", response_model=list[Sale])
def read_sales(session: session_dep):
    sales = session.exec(select(Sale)).all()
    return sales

@router.put("/sales/{sale_id}", response_model=Sale)
def update_sale(sale_id: int, client_id: int = Body(...), products: List[dict] = Body(...), session: session_dep = None):
    db_sale = session.get(Sale, sale_id)
    if not db_sale:
        raise HTTPException(status_code=404, detail="Sale not found")
    client = session.get(Client, client_id)
    if not client or not client.active:
        raise HTTPException(status_code=400, detail="Client is not active or does not exist")
    db_sale.client_id = client_id
    # Eliminar productos anteriores
    old_products = session.exec(select(SaleProduct).where(SaleProduct.sale_id == sale_id)).all()
    for op in old_products:
        session.delete(op)
    # Agregar nuevos productos
    for prod in products:
        product = session.get(Product, prod["product_id"])
        if not product or not product.active:
            raise HTTPException(status_code=400, detail=f"Product {prod['product_id']} is not active or does not exist")
        sale_product = SaleProduct(sale_id=sale_id, product_id=prod["product_id"], quantity=prod["quantity"])
        session.add(sale_product)
    session.commit()
    session.refresh(db_sale)
    return db_sale

@router.put("/sales/{sale_id}/cancel", response_model=Sale)
def cancel_sale(sale_id: int, session: session_dep):
    db_sale = session.get(Sale, sale_id)
    if not db_sale:
        raise HTTPException(status_code=404, detail="Sale not found")
    db_sale.canceled = True
    session.commit()
    session.refresh(db_sale)
    return db_sale

@router.delete("/sales/{sale_id}")
def delete_sale(sale_id: int):
    with Session(engine) as session:
        sale = session.get(Sale, sale_id)
        if not sale:
            raise HTTPException(status_code=404, detail="Sale not found")
        session.delete(sale)
        session.commit()
        return {"ok": True}

