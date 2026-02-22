from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class CartItem(BaseModel):
    product_id: str
    quantity: int
    name: Optional[str] = None
    price: Optional[float] = None

class Cart(BaseModel):
    user_id: str
    items: List[CartItem] = []
    total: float = 0

class OrderCreate(BaseModel):
    user_id: str
    items: List[CartItem]
    total: float

class Order(BaseModel):
    id: Optional[str] = None
    user_id: str
    items: List[CartItem]
    total: float
    status: str = "PLACED"
    created_at: datetime
    order_reference: str