from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from product_service import get_all_products
from schemas import *

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/products/", response_model=list[ProductRead])
def read_products(db: Session = Depends(get_db)):
    return get_all_products(db)
