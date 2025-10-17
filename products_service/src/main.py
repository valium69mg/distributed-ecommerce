from fastapi import FastAPI, Depends, Request, Query
from sqlalchemy.orm import Session
from database import SessionLocal
from product_service import get_all_products, create_product, search_products_by_name
from dtos import *
from auth_service import verify_token  
from category_service import get_all_categories
app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/products/", response_model=list[ProductRead])
async def read_products(
    request: Request,
    db: Session = Depends(get_db),
    user: UserRoles = Depends(verify_token)
    ):
    return await get_all_products(db)

@app.post('/products/')
async def create_product_endpoint(product: ProductCreate, db: Session = Depends(get_db), user: UserRoles = Depends(verify_token)):
    user_id = user.userId
    await create_product(db, product, user_id)
    return {"message": "Product created successfully"}

@app.get("/products/search", response_model=list[ProductRead])
async def search_products(query: str = Query(..., min_length=2), db: Session = Depends(get_db), user: UserRoles = Depends(verify_token)):
    return await search_products_by_name(db, query)

@app.get("/categories/", response_model=list[CategoryRead])
async def read_categories(
    request: Request,
    db: Session = Depends(get_db),
    user: UserRoles = Depends(verify_token)
    ):
    return await get_all_categories(db)

