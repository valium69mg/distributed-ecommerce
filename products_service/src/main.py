from fastapi import FastAPI, Depends, Request, Query, Path
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from database import SessionLocal
from product_service import *
from dtos import *
from auth_service import verify_token  
from category_service import get_all_categories
from aiokafka import AIOKafkaConsumer
import asyncio
import os, json
from contextlib import asynccontextmanager

consumer = None 

@asynccontextmanager
async def lifespan(app: FastAPI):
    global consumer
    kafka_host = os.getenv("KAFKA_HOST", "localhost")
    kafka_port = os.getenv("KAFKA_PORT", "9092")
    kafka_address = f"{kafka_host}:{kafka_port}"

    consumer = AIOKafkaConsumer(
        "order-events",
        bootstrap_servers=kafka_address,
        group_id="fastapi-consumer-group",
        auto_offset_reset="earliest"
    )
    await consumer.start()
    print("Kafka consumer started")

    async def consume():
        async for msg in consumer:
            try:
                data = json.loads(msg.value.decode())
                print("Parsed JSON:", data)
            except json.JSONDecodeError as e:
                print("Failed to parse JSON:", e)

    asyncio.create_task(consume())

    yield

    await consumer.stop()


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],           
    allow_credentials=True,
    allow_methods=["*"],           
    allow_headers=["*"],           
)
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

@app.get("/products/{id}", response_model=ProductRead)
async def read_product(
    request: Request,
    id: int = Path(..., title="The ID of the product to retrieve"),
    db: Session = Depends(get_db),
    user: UserRoles = Depends(verify_token)
):
    return await get_product_by_id(db, id)

@app.post('/products/')
async def create_product_endpoint(product: ProductCreate, db: Session = Depends(get_db), user: UserRoles = Depends(verify_token)):
    user_id = user.userId
    await create_product(db, product, user_id)
    return {"message": "Product created successfully"}

@app.get("/products/search", response_model=list[ProductRead])
async def search_products(query: str = Query(..., min_length=2), db: Session = Depends(get_db), user: UserRoles = Depends(verify_token)):
    return await search_products_by_name(db, query)

@app.get("/products/categories/", response_model=list[CategoryRead])
async def read_categories(
    request: Request,
    db: Session = Depends(get_db),
    user: UserRoles = Depends(verify_token)
    ):
    return await get_all_categories(db)

