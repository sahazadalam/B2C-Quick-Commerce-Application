import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
    DATABASE_NAME = "delivery_db"
    ORDER_SERVICE_URL = os.getenv("ORDER_SERVICE_URL", "http://localhost:8003")