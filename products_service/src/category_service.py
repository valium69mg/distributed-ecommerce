from sqlalchemy import text
from sqlalchemy.orm import Session
from dtos import CategoryRead

async def get_all_categories(db: Session) -> list[CategoryRead]:
    sql = text("SELECT * FROM categories")
    result = db.execute(sql)
    rows = result.mappings().all()
    return [CategoryRead(**dict(row)) for row in rows]