from sqlalchemy import text
from sqlalchemy.orm import Session
from dtos import ProductRead, ProductCreate

async def get_all_products(db: Session) -> list[ProductRead]:
    sql = text("SELECT id, name, description, price, stock, user_id FROM products")
    result = db.execute(sql)
    rows = result.mappings().all()
    return [ProductRead(**dict(row)) for row in rows]

async def create_product(db: Session, product: ProductCreate, user_id: str) -> None:
    sql = text("""
        INSERT INTO products (name, description, price, stock, user_id, category_id)
        VALUES (:name, :description, :price, :stock, :user_id, :category_id)
    """)
    db.execute(sql, {
        "name": product.name,
        "description": product.description,
        "price": product.price,
        "stock": product.stock,
        "user_id": user_id,
        "category_id": product.category_id
    })
    db.commit()

async def search_products_by_name(db: Session, query: str) -> list[ProductRead]:
    sql = text("""
        SELECT id, name, description, price, stock, user_id
        FROM products
        WHERE name ILIKE :pattern
        ORDER BY similarity(name, :query) DESC
    """)
    result = db.execute(sql, {"pattern": f"%{query}%", "query": query})
    rows = result.mappings().all()
    return [ProductRead(**dict(row)) for row in rows]