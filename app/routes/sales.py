from fastapi import APIRouter, HTTPException
from sqlmodel import Session, select
from models.sale import Sale
from database import session_dep

router = APIRouter()

@router.post("/sales/", response_model=Sale)
def create_sale(sale: Sale, session: session_dep):
    session.add(sale)
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
def update_sale(sale_id: int, sale: Sale, session: session_dep):
    db_sale = session.get(Sale, sale_id)
    if not db_sale:
        raise HTTPException(status_code=404, detail="Sale not found")
    db_sale.product_id = sale.product_id
    db_sale.client_id = sale.client_id
    db_sale.quantity = sale.quantity
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

docker push cristian9923/chainstore:latest 