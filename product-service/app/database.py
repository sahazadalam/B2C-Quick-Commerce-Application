from pymongo import MongoClient
from config import Config

client = MongoClient(Config.MONGODB_URL)
db = client[Config.DATABASE_NAME]
products_collection = db["products"]
categories_collection = db["categories"]