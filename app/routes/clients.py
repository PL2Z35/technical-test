from fastapi import APIRouter, HTTPException
from sqlmodel import Session, select
from models.client import Client
from database import session_dep

router = APIRouter()

@router.post("/clients/", response_model=Client)
def create_client(client: Client, session: session_dep):
    session.add(client)
    session.commit()
    session.refresh(client)
    return client

@router.get("/clients/{client_id}", response_model=Client)
def read_client(client_id: int, session: session_dep):
    client = session.get(Client, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client

@router.get("/clients/", response_model=list[Client])
def read_clients(session: session_dep):
    clients = session.exec(select(Client)).all()
    return clients

@router.put("/clients/{client_id}", response_model=Client)
def update_client(client_id: int, client: Client, session: session_dep):
    db_client = session.get(Client, client_id)
    if not db_client:
        raise HTTPException(status_code=404, detail="Client not found")
    db_client.name = client.name
    db_client.email = client.email
    session.commit()
    session.refresh(db_client)
    return db_client

@router.put("/clients/{client_id}/deactivate", response_model=Client)
def deactivate_client(client_id: int, session: session_dep):
    db_client = session.get(Client, client_id)
    if not db_client:
        raise HTTPException(status_code=404, detail="Client not found")
    db_client.active = False
    session.commit()
    session.refresh(db_client)
    return db_client

@router.delete("/clients/{client_id}")
def delete_client(client_id: int):
    with Session(engine) as session:
        client = session.get(Client, client_id)
        if not client:
            raise HTTPException(status_code=404, detail="Client not found")
        session.delete(client)
        session.commit()
        return {"ok": True}
