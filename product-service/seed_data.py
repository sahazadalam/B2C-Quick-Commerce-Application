from app.database import products_collection, categories_collection

# Sample categories
categories = [
    {"name": "Vegetables", "image_url": "https://via.placeholder.com/100"},
    {"name": "Fruits", "image_url": "https://via.placeholder.com/100"},
    {"name": "Dairy", "image_url": "https://via.placeholder.com/100"},
    {"name": "Snacks", "image_url": "https://via.placeholder.com/100"},
    {"name": "Beverages", "image_url": "https://via.placeholder.com/100"},
]

# Sample products
products = [
    {
        "name": "Fresh Tomatoes",
        "description": "Farm fresh tomatoes, 500g",
        "price": 40.0,
        "category": "Vegetables",
        "image_url": "https://via.placeholder.com/200",
        "available": True
    },
    {
        "name": "Organic Apples",
        "description": "Kashmiri apples, 1kg",
        "price": 120.0,
        "category": "Fruits",
        "image_url": "https://via.placeholder.com/200",
        "available": True
    },
    {
        "name": "Milk",
        "description": "Full cream milk, 1L",
        "price": 60.0,
        "category": "Dairy",
        "image_url": "https://via.placeholder.com/200",
        "available": True
    },
    {
        "name": "Potato Chips",
        "description": "Classic salted, 100g",
        "price": 30.0,
        "category": "Snacks",
        "image_url": "https://via.placeholder.com/200",
        "available": True
    },
    {
        "name": "Cola",
        "description": "Cold drink, 750ml",
        "price": 45.0,
        "category": "Beverages",
        "image_url": "https://via.placeholder.com/200",
        "available": True
    }
]

def seed_data():
    # Clear existing data
    categories_collection.delete_many({})
    products_collection.delete_many({})
    
    # Insert categories
    categories_collection.insert_many(categories)
    
    # Insert products
    products_collection.insert_many(products)
    
    print("Database seeded successfully!")

if __name__ == "__main__":
    seed_data()