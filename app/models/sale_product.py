from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from .sale import Sale

class SaleProduct(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    sale_id: int = Field(foreign_key="sale.id")
    product_id: int = Field(foreign_key="product.id")
    quantity: int
    sale: Optional["Sale"] = Relationship(back_populates="products")

Sale.update_forward_refs()

