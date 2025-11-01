from pydantic import BaseModel, Field
from typing import List
from enum import Enum

class UserRoles(BaseModel):
    userId: str
    roles: List[str]


class ProductRead(BaseModel):
    id: int
    name: str
    description: str
    price: float
    stock: int
    user_id: str

    class Config:
        orm_mode = True

class ProductCreate(BaseModel):
    name: str 
    description: str 
    price: float 
    stock: int 
    category_id: int

class CategoryRead(BaseModel):
    id: int
    name: str

class EventType(Enum):
    CREATE = "CREATE"
    APPROVED_STOCK = "APPROVED_STOCK"
    NO_STOCK = "NO_STOCK"

class ProductEventDTO(BaseModel):
    units: int
    productId: int

class OrderEventDTO(BaseModel):
    orderId: int
    type: EventType
    products: List[ProductEventDTO]

class PhotoExtensions(Enum):
    PNG = "png"
    JPG = "jpg"
    JPEG = "jpeg"