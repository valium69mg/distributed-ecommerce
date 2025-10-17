from pydantic import BaseModel

class ProductRead(BaseModel):
    id: int
    name: str
    description: str
    price: float
    stock: int
    user_id: int

    class Config:
        orm_mode = True
