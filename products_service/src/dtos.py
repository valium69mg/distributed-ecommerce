from pydantic import BaseModel, Field
from typing import List

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