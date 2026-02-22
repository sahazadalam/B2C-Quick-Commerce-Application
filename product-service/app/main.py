from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from bson import ObjectId
from typing import List
from .models import Product, Category
from .database import products_collection, categories_collection

app = FastAPI(title="Product Catalog Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/categories", response_model=List[Category])
async def get_categories():
    categories = []
    for cat in categories_collection.find():
        cat["id"] = str(cat["_id"])
        categories.append(Category(**cat))
    return categories

@app.get("/products", response_model=List[Product])
async def get_products(category: str = None):
    query = {}
    if category:
        query["category"] = category
    
    products = []
    for prod in products_collection.find(query):
        prod["id"] = str(prod["_id"])
        products.append(Product(**prod))
    return products

@app.get("/products/{product_id}", response_model=Product)
async def get_product(product_id: str):
    try:
        product = products_collection.find_one({"_id": ObjectId(product_id)})
        if product:
            product["id"] = str(product["_id"])
            return Product(**product)
        raise HTTPException(status_code=404, detail="Product not found")
    except:
        raise HTTPException(status_code=400, detail="Invalid product ID")

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)