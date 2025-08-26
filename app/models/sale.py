from sqlmodel import SQLModel, Field

class Sale(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    product_id: int = Field(default=None, foreign_key="product.id")
    client_id: int = Field(default=None, foreign_key="client.id")
    quantity: int
    canceled: bool = Field(default=False)
