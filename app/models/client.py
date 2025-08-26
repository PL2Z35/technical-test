from sqlmodel import SQLModel, Field

class Client(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    email: str
    active: bool = Field(default=True)
