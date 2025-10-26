from sqlalchemy import text, bindparam
from sqlalchemy.orm import Session
from dtos import *
from fastapi import HTTPException
import kafka_client
import json

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

async def excecuteOrderEvent(db: Session, json: OrderEventDTO):
    if json.type == OrderEventType.CREATE:
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
                type=OrderEventType.APPROVED_STOCK,
                products=json.products
            )
            print("Sending APPROVED_STOCK event for order", json.orderId)
            await send_order_event(approved_event)

        except Exception as e:
            db.rollback()
            no_stock_event = OrderEventDTO(
                orderId=json.orderId,
                type=OrderEventType.NO_STOCK,
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
    await kafka_client.producer.send_and_wait("order-events", message)
    print("Kafka event sent:", message)
