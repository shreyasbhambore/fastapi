from itertools import product

from fastapi import FastAPI, Request,HTTPException,Query
from service.products import get_all_products 
app=FastAPI()   
@app.get("/")
def root():
    return {"message": "Hello  World"} 

@app.get("/products/{item_id}")
def read_item(item_id: int):
    products = ["Laptop","Smartphone","Tablet"]
    return products[item_id]

@app.get("/students/{student_id}")
def read_student(student_id: int):
    students = ["Alice", "Bob", "Charlie"]
    return students[student_id]

#@app.get("/products")
#def list_products():
#   return get_all_products()


@app.get("/products")
def list_products(name: str = Query(default=None, min_length=1,max_length=50, description="Name of the product to search for"),
                  sort_by_price: bool = Query(default=False, description="Sort products by price"),
                  order: str = Query(default="asc",  description="Order of sorting (asc or desc)"),
                  limit: int = Query(default=5, ge=1, le=3, description="Limit the number of products returned"),
                  offset: int = Query(default=0, ge=0, description="Offset for pagination")):
    products = get_all_products()
    if name:
        needle=name.strip().lower()
        products = [p for p in products if needle in p.get("name", "").lower()]
        if not products:
            raise HTTPException(status_code=404, detail=f"No products found matching '{name}'")
        

    if sort_by_price:
        reverse=order == "desc" 
        products=sorted(products, key=lambda p: p.get("price", 0), reverse=reverse)
    total_products = len(products)
    products = products[offset:offset+limit]

    return {
        "total": total_products,
        "items": products
    }

@app.get("/products/{product_id}")
def get_product(product_id: str):
    products = get_all_products()
    for product in products:
        if product.get("id") == product_id:
            return product
        raise HTTPException(status_code=404, detail=f"Product with ID '{product_id}' not found")            
    
    

    

