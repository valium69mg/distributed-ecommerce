from fastapi import FastAPI, Depends, Request, Query, Path, UploadFile, File
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
from pydantic import ValidationError
from contextlib import asynccontextmanager
from aiokafka import AIOKafkaProducer
import kafka_client 
from fastapi.responses import FileResponse

@asynccontextmanager
async def lifespan(app: FastAPI):
    kafka_host = os.getenv("KAFKA_HOST", "localhost")
    kafka_port = os.getenv("KAFKA_PORT", "9092")
    kafka_address = f"{kafka_host}:{kafka_port}"

    # Start Kafka consumer
    kafka_client.consumer = AIOKafkaConsumer(
        "order-events",
        bootstrap_servers=kafka_address,
        group_id="products-consumer-group",
        auto_offset_reset="earliest"
    )
    await kafka_client.consumer.start()
    print("Kafka consumer started")

    # Start Kafka producer
    kafka_client.producer = AIOKafkaProducer(bootstrap_servers=kafka_address)
    await kafka_client.producer.start()
    print("Kafka producer started")

    async def consume():
        async for msg in kafka_client.consumer:
            try:
                data = json.loads(msg.value.decode())
                order_event = OrderEventDTO(**data)

                db_gen = get_db()
                db = next(db_gen)

                try:
                    print(f"Excecuting order event: {order_event}")
                    await excecuteOrderEvent(db, order_event)
                finally:
                    db_gen.close()

            except json.JSONDecodeError as e:
                print("Failed to parse JSON:", e)
            except ValidationError as ve:
                print("DTO validation failed:", ve)
            except Exception as e:
                print("Unexpected error during event processing:", e)

    asyncio.create_task(consume())

    yield

    await kafka_client.consumer.stop()
    await kafka_client.producer.stop()


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

@app.post("/products/", response_model=list[ProductRead])
async def read_products_by_ids(
    ids: list[int],
    request: Request,
    db: Session = Depends(get_db),
    user: UserRoles = Depends(verify_token),
):
    return await get_products_by_ids(db, ids)

@app.post('/products/')
async def create_product(product: ProductCreate, db: Session = Depends(get_db), user: UserRoles = Depends(verify_token)):
    user_id = user.userId
    await create_product(db, product, user_id)
    return {"message": "Product created successfully"}

@app.post("/products/uploadPhotos")
async def upload_photos_endpoint(files: List[UploadFile] = File(...), 
        product_id: int = Query(..., description="ID of the product"),
        db: Session = Depends(get_db), 
        user: UserRoles = Depends(verify_token)):
    
    await validate_photos_format(files)
    await upload_photos(db, product_id, files, os.getenv('PHOTOS_DIR'))
    
    return {"message": "Files created successfully"}

@app.get("/product/photos/{photo_id}")
def serve_photo(photo_id: int, db: Session = Depends(get_db)):
    path = get_photo_path_by_id(db, photo_id)
    if not path:
        raise HTTPException(status_code=404, detail="Photo not found")
    return FileResponse(path)

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

