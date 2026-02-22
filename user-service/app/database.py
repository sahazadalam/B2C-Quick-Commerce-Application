from pymongo import MongoClient
from config import Config

client = MongoClient(Config.MONGODB_URL)
db = client[Config.DATABASE_NAME]
users_collection = db["users"]