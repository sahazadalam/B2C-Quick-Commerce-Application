from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from bson import ObjectId
from typing import List
import httpx
import random
import string
from datetime import datetime
from .models import CartItem, Cart, OrderCreate, Order
from .database import cart_collection, orders_collection
from config import Config

app = FastAPI(title="Cart and Order Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def get_product_details(product_id: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{Config.PRODUCT_SERVICE_URL}/products/{product_id}")
        if response.status_code == 200:
            return response.json()
    return None

def generate_order_reference():
    return 'ORD' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

@app.post("/cart/add")
async def add_to_cart(user_id: str, item: CartItem):
    # Get product details to verify and get price
    product = await get_product_details(item.product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Update item with product details
    item.name = product["name"]
    item.price = product["price"]
    
    # Find user's cart
    cart = cart_collection.find_one({"user_id": user_id})
    
    if cart:
        # Update existing cart
        items = cart.get("items", [])
        found = False
        for i, existing_item in enumerate(items):
            if existing_item["product_id"] == item.product_id:
                items[i]["quantity"] += item.quantity
                found = True
                break
        
        if not found:
            items.append(item.dict())
        
        # Calculate total
        total = sum(i["price"] * i["quantity"] for i in items)
        
        cart_collection.update_one(
            {"user_id": user_id},
            {"$set": {"items": items, "total": total}}
        )
    else:
        # Create new cart
        cart_data = {
            "user_id": user_id,
            "items": [item.dict()],
            "total": item.price * item.quantity
        }
        cart_collection.insert_one(cart_data)
    
    return {"message": "Item added to cart"}

@app.post("/cart/remove")
async def remove_from_cart(user_id: str, product_id: str):
    cart = cart_collection.find_one({"user_id": user_id})
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    
    items = cart.get("items", [])
    items = [i for i in items if i["product_id"] != product_id]
    
    total = sum(i["price"] * i["quantity"] for i in items)
    
    cart_collection.update_one(
        {"user_id": user_id},
        {"$set": {"items": items, "total": total}}
    )
    
    return {"message": "Item removed from cart"}

@app.get("/cart")
async def get_cart(user_id: str):
    cart = cart_collection.find_one({"user_id": user_id})
    if not cart:
        return {"user_id": user_id, "items": [], "total": 0}
    
    cart["_id"] = str(cart["_id"])
    return cart

@app.post("/order/create")
async def create_order(order_data: OrderCreate):
    # Create order
    order_dict = {
        "user_id": order_data.user_id,
        "items": [item.dict() for item in order_data.items],
        "total": order_data.total,
        "status": "PLACED",
        "created_at": datetime.utcnow(),
        "order_reference": generate_order_reference()
    }
    
    result = orders_collection.insert_one(order_dict)
    order_dict["id"] = str(result.inserted_id)
    
    # Clear user's cart
    cart_collection.delete_one({"user_id": order_data.user_id})
    
    return {
        "message": "Order created successfully",
        "order_id": str(result.inserted_id),
        "order_reference": order_dict["order_reference"]
    }

@app.get("/orders")
async def get_orders(user_id: str):
    orders = []
    for order in orders_collection.find({"user_id": user_id}).sort("created_at", -1):
        order["id"] = str(order["_id"])
        orders.append(order)
    return orders

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)