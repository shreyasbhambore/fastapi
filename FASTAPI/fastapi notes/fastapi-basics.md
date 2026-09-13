# FastAPI Notes — Basics and Practice

## 1. What is FastAPI?

FastAPI is a modern Python framework for building APIs. It uses Python type hints for validation, automatic documentation, and editor support.

Install and run:

```bash
pip install fastapi "uvicorn[standard]"
uvicorn main:app --reload
```

`main` is the file name and `app` is the FastAPI application variable.

## 2. First API

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}
```

Open these after starting the server:

- API: `http://127.0.0.1:8000/`
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## 3. HTTP Methods

```python
@app.get("/items")
def get_items(): ...

@app.post("/items")
def create_item(): ...

@app.put("/items/{item_id}")
def replace_item(item_id: int): ...

@app.patch("/items/{item_id}")
def update_item(item_id: int): ...

@app.delete("/items/{item_id}")
def delete_item(item_id: int): ...
```

## 4. Path Parameters

Values inside `{}` in a path are path parameters.

```python
@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {"user_id": user_id}
```

FastAPI converts and validates `user_id` as an integer.

## 5. Query Parameters

Parameters not included in the URL path become query parameters.

```python
@app.get("/products")
def list_products(skip: int = 0, limit: int = 10, search: str | None = None):
    return {"skip": skip, "limit": limit, "search": search}
```

Example: `/products?skip=0&limit=5&search=book`

## 6. Request Body with Pydantic

Use a Pydantic model for JSON request data.

```python
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    price: float
    in_stock: bool = True

@app.post("/items")
def create_item(item: Item):
    return item
```

FastAPI validates the input and returns a clear `422` error for invalid data.

## 7. Status Codes and Errors

```python
from fastapi import HTTPException, status

@app.get("/items/{item_id}")
def get_item(item_id: int):
    if item_id != 1:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"id": item_id, "name": "Notebook"}

@app.post("/items", status_code=status.HTTP_201_CREATED)
def create_item(item: Item):
    return item
```

Common codes: `200 OK`, `201 Created`, `204 No Content`, `400 Bad Request`, `401 Unauthorized`, `404 Not Found`, `422 Validation Error`.

## 8. Response Models

Use `response_model` to control and validate API output.

```python
class ItemResponse(BaseModel):
    name: str
    price: float

@app.post("/items", response_model=ItemResponse)
def create_item(item: Item):
    return item
```

This is useful for hiding fields such as passwords or internal IDs.

## 9. Async Endpoints

Use `async def` when the endpoint awaits asynchronous work, such as async database or HTTP calls.

```python
@app.get("/health")
async def health_check():
    return {"status": "ok"}
```

Do not use `await` inside a normal `def` function.

## 10. Practice Checklist

- [ ] Create a hello-world endpoint.
- [ ] Make CRUD endpoints for a `Task` or `Book` resource.
- [ ] Use path and query parameters.
- [ ] Validate POST/PUT bodies with Pydantic models.
- [ ] Return proper status codes and `HTTPException` errors.
- [ ] Check requests in `/docs`.
- [ ] Add a response model that excludes a private field.

## 11. Useful Project Structure

```text
app/
├── main.py          # FastAPI app and router setup
├── schemas.py       # Pydantic request/response models
├── routers/         # Endpoint modules
├── services/        # Business logic
└── database.py      # Database connection/configuration
```

## Quick Reminder

Start development server with:

```bash
uvicorn app.main:app --reload
```

Use `--reload` only for development. It automatically restarts the server after code changes.
