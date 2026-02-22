from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from bson import ObjectId
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
import httpx
from .models import DeliveryStatus, StatusUpdate
from .database import delivery_collection
from config import Config

app = FastAPI(title="Delivery Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

scheduler = BackgroundScheduler()

def simulate_delivery_updates():
    """Background task to simulate delivery updates"""
    with app.app_context():
        # Find orders in PLACED status and update to PACKED after 2 minutes
        placed_orders = delivery_collection.find({"status": "PLACED"})
        for order in placed_orders:
            # Update to PACKED
            delivery_collection.update_one(
                {"_id": order["_id"]},
                {"$set": {"status": "PACKED", "last_updated": datetime.utcnow()}}
            )
        
        # Find PACKED orders and update to OUT_FOR_DELIVERY after 2 more minutes
        packed_orders = delivery_collection.find({"status": "PACKED"})
        for order in packed_orders:
            delivery_collection.update_one(
                {"_id": order["_id"]},
                {"$set": {"status": "OUT_FOR_DELIVERY", "last_updated": datetime.utcnow()}}
            )
        
        # Find OUT_FOR_DELIVERY orders and update to DELIVERED after 2 more minutes
        out_for_delivery = delivery_collection.find({"status": "OUT_FOR_DELIVERY"})
        for order in out_for_delivery:
            delivery_collection.update_one(
                {"_id": order["_id"]},
                {"$set": {"status": "DELIVERED", "last_updated": datetime.utcnow()}}
            )

@app.on_event("startup")
async def startup_event():
    scheduler.add_job(simulate_delivery_updates, 'interval', minutes=2)
    scheduler.start()

@app.on_event("shutdown")
async def shutdown_event():
    scheduler.shutdown()

@app.post("/order/{order_id}/initiate")
async def initiate_delivery(order_id: str):
    # Check if delivery tracking already exists
    existing = delivery_collection.find_one({"order_id": order_id})
    if existing:
        return {"message": "Delivery already initiated"}
    
    # Create new delivery tracking
    delivery = {
        "order_id": order_id,
        "status": "PLACED",
        "last_updated": datetime.utcnow()
    }
    
    result = delivery_collection.insert_one(delivery)
    return {"message": "Delivery initiated", "tracking_id": str(result.inserted_id)}

@app.get("/order/{order_id}/status")
async def get_order_status(order_id: str):
    delivery = delivery_collection.find_one({"order_id": order_id})
    if not delivery:
        raise HTTPException(status_code=404, detail="Order not found in delivery system")
    
    delivery["_id"] = str(delivery["_id"])
    return delivery

@app.post("/order/{order_id}/update-status")
async def update_status(order_id: str, update: StatusUpdate):
    # Validate status
    valid_statuses = ["PLACED", "PACKED", "OUT_FOR_DELIVERY", "DELIVERED"]
    if update.status not in valid_statuses:
        raise HTTPException(status_code=400, detail="Invalid status")
    
    result = delivery_collection.update_one(
        {"order_id": order_id},
        {"$set": {"status": update.status, "last_updated": datetime.utcnow()}}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Order not found")
    
    return {"message": "Status updated successfully"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8004)