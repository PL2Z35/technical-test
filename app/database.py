import os
from dotenv import load_dotenv
from sqlmodel import SQLModel, create_engine, Session
from typing import Annotated
from fastapi import Depends

load_dotenv()

db_username = os.getenv('USER_DB')
db_password = os.getenv('PASSWORD_DB')
db_host = os.getenv('HOST_DB')
db_name = os.getenv('NAME_DB')

ssl_args = {
    "ssl": {
        "fake_flag_to_enable_tls": True  # Required to trigger TLS, even if no CA certs are provided
    }
}

url_connection = f"mysql+pymysql://{db_username}:{db_password}@{db_host}:3306/{db_name}"
engine = create_engine(url_connection, pool_size=5, max_overflow=10, connect_args=ssl_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def drop_and_create_tables():
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

session_dep = Annotated[Session, Depends(get_session)]

if __name__ == "__main__":
    drop_and_create_tables()