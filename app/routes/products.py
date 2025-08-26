from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from models.product import Product
from database import session_dep

router = APIRouter()

@router.post("/products/", response_model=Product)
def create_product(product: Product, session: session_dep):
    session.add(product)
    session.commit()
    session.refresh(product)
    return product

@router.get("/products/{product_id}", response_model=Product)
def read_product(product_id: int, session: session_dep):
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.get("/products/", response_model=list[Product])
def read_products(session: session_dep):
    products = session.exec(select(Product)).all()
    return products

@router.put("/products/{product_id}", response_model=Product)
def update_product(product_id: int, product: Product, session: session_dep):
    db_product = session.get(Product, product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    db_product.name = product.name
    db_product.price = product.price
    session.commit()
    session.refresh(db_product)
    return db_product

# Desactivar producto
@router.put("/products/{product_id}/deactivate", response_model=Product)
def deactivate_product(product_id: int, session: session_dep):
    db_product = session.get(Product, product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    db_product.active = False
    session.commit()
    session.refresh(db_product)
    return db_product

@router.delete("/products/{product_id}")
def delete_product(product_id: int):
    with Session(engine) as session:
        product = session.get(Product, product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        session.delete(product)
        session.commit()
        return {"ok": True}
