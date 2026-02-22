from pydantic import BaseModel
from typing import Optional, List

class Product(BaseModel):
    id: Optional[str] = None
    name: str
    description: str
    price: float
    category: str
    image_url: str
    available: bool = True

class Category(BaseModel):
    id: Optional[str] = None
    name: str
    image_url: str