from datetime import datetime
import os
from pathlib import Path
from fastapi import FastAPI, HTTPException, Query,Depends,Request
from fastapi.responses import JSONResponse

from app.products.products import (
    add_product,
    delete_product as delete_product_from_store,
    get_all_products,
    update_product as update_product_in_store,load_products
)
from app.schema.product import Product
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent / ".env")


app = FastAPI()

#@app.middleware("http")
#async def lifecycle(request,call_next):
#    print("Before request")
 #   response=await call_next(request)
  #  #response["lifecycle"] = "Was inside the middleware"
   # print("After request")
    #return response




def common_logic():
    return "hello fastapi"

@app.get("/")
def root(dep=Depends(common_logic)):
    db_path = os.getenv("DB_PATH")
    #return {"message": "Hello World","dependency":dep,"DB_PATH":db_path}
    return JsonResponse(status_code=200,content={"message": "Hello World","dependency":dep,"DB_PATH":db_path})



@app.get("/students/{student_id}")
def read_student(student_id: int):
    students = ["Alice", "Bob", "Charlie"]
    return students[student_id]


@app.get("/products")
def list_products(dep=Depends(load_products),
    name: str = Query(default=None, min_length=1, max_length=50, description="Name of the product to search for"),
    sort_by_price: bool = Query(default=False, description="Sort products by price"),
    order: str = Query(default="asc", description="Order of sorting (asc or desc)"),
    limit: int = Query(default=5, ge=1, le=50, description="Limit the number of products returned"),
    offset: int = Query(default=0, ge=0, description="Offset for pagination"),
):
   # products = get_all_products()
    products = dep
#dependency injection

    if name:
        needle = name.strip().lower()
        products = [p for p in products if needle in p.get("name", "").lower()]
        if not products:
            raise HTTPException(status_code=404, detail=f"No products found matching '{name}'")

    if sort_by_price:
        reverse = order == "desc"
        products = sorted(products, key=lambda p: p.get("price", 0), reverse=reverse)

    total_products = len(products)
    products = products[offset : offset + limit]

    return {"total": total_products, "items": products}


@app.get("/products/{product_id}")
def get_product(product_id: int):
    products = get_all_products()
    for product in products:
        if str(product.get("id")) == str(product_id):
            return product

    raise HTTPException(status_code=404, detail=f"Product with ID '{product_id}' not found")


@app.post("/products", status_code=201)
def create_product(product: Product):
    product_dict=product.model_dump(mode="json")
    product_dict["id"] = product_dict.get("id", None)
    product_dict["created_at"] = datetime.utcnow().isoformat()+"Z"
    try:
        add_product(product_dict)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    products = get_all_products()
    return product.model_dump(mode="json")

@app.delete("/products/{product_id}", status_code=204)
def delete_product(product_id: int):
    try:
        deleted_product = delete_product_from_store(str(product_id))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    if deleted_product is None:
        raise HTTPException(status_code=404, detail=f"Product with ID '{product_id}' not found")

    return {"message": f"Product with ID '{product_id}' has been deleted."}

@app.put("/products/{product_id}")
def update_product(product_id: int, updated_product: Product):
    updated_product_dict = updated_product.model_dump(mode="json")
    try:
        updated_product_data = update_product_in_store(str(product_id), updated_product_dict)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return updated_product_data

