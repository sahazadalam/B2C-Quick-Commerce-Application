from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class DeliveryStatus(BaseModel):
    order_id: str
    status: str  # PLACED, PACKED, OUT_FOR_DELIVERY, DELIVERED
    last_updated: datetime

class StatusUpdate(BaseModel):
    status: str