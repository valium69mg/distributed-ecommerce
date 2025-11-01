from sqlalchemy import text, bindparam
from sqlalchemy.orm import Session
from dtos import *
from fastapi import UploadFile, HTTPException
import kafka_client
import json
from fastapi import File
import uuid
import os
from sqlalchemy import select
from models import Photo

async def get_all_products(db: Session) -> list[ProductRead]:
    sql = text("SELECT id, name, description, price, stock, user_id FROM products")
    result = db.execute(sql)
    rows = result.mappings().all()
    return [ProductRead(**dict(row)) for row in rows]


async def get_product_by_id(db: Session, id: int) -> ProductRead:
    sql = text("""
        SELECT id, name, description, price, stock, user_id
        FROM products
        WHERE id = :id
    """)
    result = db.execute(sql, {"id": id})
    row = result.fetchone()

    if row is None:
        raise HTTPException(status_code=404, detail="Product not found")

    return ProductRead(
        id=row.id,
        name=row.name,
        description=row.description,
        price=row.price,
        stock=row.stock,
        user_id=row.user_id
    )

async def get_products_by_ids(db: Session, ids: list[int]) -> list[ProductRead]:
    sql = text("""
        SELECT id, name, description, price, stock, user_id
        FROM products
        WHERE id IN :ids
    """).bindparams(bindparam("ids", expanding=True))
    result = db.execute(sql, {"ids": ids})
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

async def upload_photos(db: Session, product_id: int, files: List[UploadFile], dir: str) -> None:
    os.makedirs(dir, exist_ok=True)
    photo_paths = []
    for file in files:
        ext = os.path.splitext(file.filename)[1].lower()
        unique_name = f"{uuid.uuid4()}{ext}"
        file_path = os.path.abspath(os.path.join(dir, unique_name))
        content = await file.read()
        with open(file_path, "wb") as f:
            f.write(content)
        photo_paths.append(file_path)
    try:
        insert_photos_sql = text("""
            INSERT INTO photos (path)
            VALUES (:path)
            RETURNING id
        """)
        photo_ids = []
        for path in photo_paths:
            result = db.execute(insert_photos_sql, {"path": path})
            photo_id = result.scalar()
            photo_ids.append(photo_id)
        insert_links_sql = text("""
            INSERT INTO product_photos (product_id, photo_id)
            VALUES (:product_id, :photo_id)
        """)
        db.execute(
            insert_links_sql,
            [{"product_id": product_id, "photo_id": pid} for pid in photo_ids]
        )
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    
def get_photo_path_by_id(db: Session, photo_id: int) -> str | None:
    photo = db.execute(select(Photo).where(Photo.id == photo_id)).scalar_one_or_none()
    return photo.path if photo else None
            
async def validate_photos_format(files: List[File]) -> None:
    allowed_extensions = {ext.value for ext in PhotoExtensions}
    invalid_files = []

    for file in files:
        try:
            filename = file.filename
            _, extension = os.path.splitext(filename)
            extension = extension.lower().strip(".")
            if extension not in allowed_extensions:
                invalid_files.append(filename)
        except Exception:
            raise HTTPException(status_code=400, detail=f"Could not extract image format from: {file.filename}")

    if invalid_files:
        raise HTTPException(
            status_code=415,
            detail=f"Unsupported file formats: {', '.join(invalid_files)}. Allowed formats are: {', '.join(allowed_extensions)}"
        )
    

async def excecuteOrderEvent(db: Session, json: OrderEventDTO):
    if json.type == EventType.CREATE:
        try:
            with db.begin(): 
                for product in json.products:
                    check_sql = text("SELECT stock FROM products WHERE id = :id FOR UPDATE")
                    result = db.execute(check_sql, {"id": product.productId})
                    row = result.fetchone()

                    if row is None:
                        raise HTTPException(status_code=404, detail=f"Product {product.productId} not found")

                    result = db.execute(check_sql, {"id": product.productId}).mappings()
                    row = result.fetchone()
                    available_stock = row["stock"]

                    if available_stock < product.units:
                        raise HTTPException(
                            status_code=400,
                            detail=f"Insufficient stock for product {product.productId}: requested {product.units}, available {available_stock}"
                        )

                    # Subtract stock
                    update_sql = text("""
                        UPDATE products
                        SET stock = stock - :units
                        WHERE id = :id
                    """)
                    db.execute(update_sql, {
                        "units": product.units,
                        "id": product.productId
                    })

            approved_event = OrderEventDTO(
                orderId=json.orderId,
                type=EventType.APPROVED_STOCK,
                products=json.products
            )
            print("Sending APPROVED_STOCK event for order", json.orderId)
            await send_order_event(approved_event)

        except Exception as e:
            db.rollback()
            no_stock_event = OrderEventDTO(
                orderId=json.orderId,
                type=EventType.NO_STOCK,
                products=json.products
            )
            await send_order_event(no_stock_event)
            raise HTTPException(status_code=500, detail=f"Stock update failed: {str(e)}")

async def send_order_event(event: OrderEventDTO):
    if kafka_client.producer is None:
        raise RuntimeError("Kafka producer is not initialized")

    payload = event.model_dump()
    payload["type"] = event.type.value 

    message = json.dumps(payload).encode("utf-8")
    await kafka_client.producer.send_and_wait("product-events", message)
    print("Kafka event sent:", message)
