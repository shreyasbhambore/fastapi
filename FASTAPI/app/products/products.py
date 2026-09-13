import json
from pathlib import Path
from typing import Dict, List


Data_file = Path(__file__).resolve().parents[2] / "data" / "dummy.json"

def load_products() -> List[Dict]:
    if not Data_file.exists():
        return []
    with open(Data_file, "r", encoding="utf-8") as file:
        return json.load(file)


def get_all_products() -> List[Dict]:
    return load_products()

def save_products(products: List[Dict]) -> None:
    with open(Data_file, "w", encoding="utf-8") as file:
        json.dump(products, file, indent=2, ensure_ascii=False)

def add_product(product:Dict)->Dict:
    products = get_all_products()
    if any(p.get("id") == product.get("id") for p in products): 
        raise ValueError(f"Product with ID '{product.get('id')}' already exists.")  
    products.append(product)
    save_products(products)
    return product

def delete_product(id: str) -> None:
    products = get_all_products()
    for index,p in enumerate(products):
        if p["id"] == str(id):
            deleted=products.pop(index)
            save_products(products)
            return deleted

def update_product(id: str, updated_product: Dict) -> Dict:
    products = get_all_products()
    for index, p in enumerate(products):
        if str(p.get("id")) == str(id):
            merged_product = {**p, **updated_product}
            merged_product["id"] = str(id)
            products[index] = merged_product
            save_products(products)
            return merged_product

    raise ValueError(f"Product with ID '{id}' not found.")
        