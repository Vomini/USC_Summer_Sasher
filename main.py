from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Sample inventory data
inventory = [
    {
        "id": 1,
        "Product_name": "CZero Pen Brand",
        "Variant": "Red Pen",
        "SKU": "CZPR", 
        "Price": 1.00,    
        "quantity": 5,
        "Description": "High quality pens that are carbon-neutral"
    },
    {
        "id": 2,
        "Product_name": "Red’s Pens",
        "Variant": "Black Fountain Pen",
        "SKU": "RPG", 
        "Price": 5.00,    
        "quantity": 100,
        "Description": "Fountain pens designed by Paul Red"
    },
    {
        "id": 3,
        "Product_name": "CZero Pen Brand",
        "Variant": "Blue Pen",
        "SKU": "CZPB", 
        "Price": 1.00,    
        "quantity": 5,
        "Description": "High quality pens that are carbon-neutral"
        
    },
     {
        "id": 4,
        "Product_name": "CZero Pen Brand",
        "Variant": "Green Pen",
        "SKU": "CZPG", 
        "Price": 1.00,    
        "quantity": 5,
        "Description": "High quality pens that are carbon-neutral"
        
    },
    {
        "id": 5,
        "Product_name": "Red’s Pens",
        "Variant": "Purple Fountain Pen",
        "SKU": "PRG", 
        "Price": 5.00,    
        "quantity": 100,
        "Description": "Fountain pens designed by Paul Red"    
    }
]

# Data model for product
class Product(BaseModel):
    id: int
    Product_name: str
    Variant: str
    SKU: str
    Price: float
    quantity: int
    Description: str

# Add new product
@app.post('/api/products')
def add_product(product: Product):
    inventory.append(product.dict())
    return inventory

# Add/Remove from inventory
@app.post('/api/inventory')
def update_inventory(request: dict):
    product_id = request.get("id")
    quantity = request.get("quantity")

    for item in inventory:
        if item['id'] == product_id:
            new_quantity = item['quantity'] + quantity
            if new_quantity < 0:
                return "The product quantity cannot be less than 0"
            else:
                item['quantity'] = new_quantity
                return item

    return "Product not found in inventory"

# Update product
@app.put('/api/products/{product_id}')
def update_product(product_id: int, product: Product):
    for item in inventory:
        if item['id'] == product_id:
            item.update(product.dict())
            return item

    return "Product not found"

# Remove product
@app.delete('/api/products/{product_id}')
def remove_product(product_id: int):
    for item in inventory:
        if item['id'] == product_id:
            inventory.remove(item)
            return inventory

    return "Product not found"

# Buy products (Shopping Cart)
@app.post('/api/buy')
def buy_products(cart: list[dict]):
    total = 0

    for item in cart:
        product_id = item.get("id")
        quantity = item.get("quantity")

        for product in inventory:
            if product['id'] == product_id:
                if quantity <= product['quantity']:
                    total += product['Price'] * quantity
                    product['quantity'] -= quantity
                else:
                    return "Insufficient quantity for product: {}".format(product['Product_name'])

    return "Total amount: ${}".format(total)

# Global search
@app.get('/api/search')
def search_products(keyword: str):
    results = []

    for product in inventory:
        if keyword.lower() in product['Product_name'].lower() or keyword.lower() in product['Variant'].lower() or keyword.lower() in product['Description'].lower():
            results.append(product)

    return {'results': results}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='localhost', port=8000)

