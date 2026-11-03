import os
from urllib.parse import quote_plus
from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker , DeclarativeBase
from dotenv import load_dotenv

load_dotenv()

user = os.getenv("db_user")
password =os.getenv("db_pass")
host=os.getenv("db_host")
port=os.getenv("db_port")
database=os.getenv("data_base")

password_ = quote_plus(password)

db_URL = f"mysql+mysqlconnector://{user}:{password_}@{host}:{port}/{database}"
engine = create_engine(db_URL,echo=True)

SessionLocal = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass

def get_db():
    db = SessionLocal()
    try:
        yield db
        
    finally:
        db.close()

