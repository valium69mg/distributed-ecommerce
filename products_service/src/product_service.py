from sqlalchemy import text
from sqlalchemy.orm import Session
from schemas import ProductRead

def get_all_products(db: Session) -> list[ProductRead]:
    sql = text("SELECT id, name, description, price, stock, user_id FROM products")
    result = db.execute(sql)
    rows = result.fetchall()
    return [ProductRead(**dict(row)) for row in rows]
