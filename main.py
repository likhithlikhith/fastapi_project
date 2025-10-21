from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import db

app = FastAPI()

class Product(BaseModel):
    id: int
    name: str
    desc: str
    price: float
    quantity: int

products = db.load_products()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/product")
def add_product(product: Product):
    for p in products:
        if p['id'] == product.id:
            raise HTTPException(status_code=400, detail="Product ID already exists")
    products.append(product.dict())
    db.save_products(products)
    return {"message": "Product added!", "product": product}

@app.get("/products")
def get_products():
    return products

@app.put("/product/{id}")
def update_product(id: int, updated: Product):
    for i, p in enumerate(products):
        if p['id'] == id:
            products[i] = updated.dict()
            db.save_products(products)
            return {"message": "Product updated!", "product": updated}
    raise HTTPException(status_code=404, detail="Product not found")

@app.delete("/product/{id}")
def delete_product(id: int):
    for i, p in enumerate(products):
        if p['id'] == id:
            del products[i]
            db.save_products(products)
            return {"message": "Product deleted!"}
    raise HTTPException(status_code=404, detail="Product not found")
@app.get("/product/{id}")
def get_product_by_id(id: int):
    for product in products:
        if product["id"] == id:
            return product
    raise HTTPException(status_code=404, detail="Product not found")