from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List

class Sale(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    client_id: int = Field(foreign_key="client.id")
    canceled: bool = Field(default=False)
    products: List["SaleProduct"] = Relationship(back_populates="sale")

from .sale_product import SaleProduct
SaleProduct.update_forward_refs()
