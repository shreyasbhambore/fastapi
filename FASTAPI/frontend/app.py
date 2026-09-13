"""Streamlit UI for the FastAPI product API."""

import os

import requests
import streamlit as st

DEFAULT_API_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8001")


def api_request(method: str, path: str, **kwargs):
    """Call the FastAPI API and return JSON data or an error message."""
    try:
        response = requests.request(method, f"{st.session_state.api_url}{path}", timeout=10, **kwargs)
        response.raise_for_status()
        return response.json() if response.content else {"message": "Request completed."}, None
    except requests.RequestException as error:
        detail = error.response.text if getattr(error, "response", None) is not None else str(error)
        return None, detail


def show_result(data, error):
    if error:
        st.error(error)
    else:
        st.json(data)


st.set_page_config(page_title="FastAPI Products", page_icon="Products")
st.title("FastAPI Product Dashboard")

if "api_url" not in st.session_state:
    st.session_state.api_url = DEFAULT_API_URL
st.session_state.api_url = st.sidebar.text_input("API base URL", st.session_state.api_url).rstrip("/")
st.sidebar.caption("Start API: uvicorn app.main:app --port 8001")

tab_health, tab_list, tab_get, tab_create, tab_update, tab_delete = st.tabs(
    ["Health", "All products", "Get by ID", "Create", "Update", "Delete"]
)

with tab_health:
    st.write("Checks `GET /`.")
    if st.button("Check API", key="health"):
        show_result(*api_request("GET", "/"))

with tab_list:
    st.write("Gets products with `GET /products`.")
    if st.button("Load products", key="list"):
        show_result(*api_request("GET", "/products", params={"limit": 50}))

with tab_get:
    product_id = st.number_input("Product ID", min_value=1, step=1, key="get_id")
    if st.button("Get product", key="get"):
        show_result(*api_request("GET", f"/products/{product_id}"))

with tab_create:
    st.write("Creates a product with `POST /products`.")
    with st.form("create_product"):
        name = st.text_input("Name", key="create_name")
        price = st.number_input("Price", min_value=0.01, step=0.01, key="create_price")
        description = st.text_area("Description (at least 10 characters)", key="create_description")
        image_urls = st.text_area("Image URLs (one per line)", key="create_images")
        submitted = st.form_submit_button("Create product")
    if submitted:
        payload = {"name": name, "price": price, "description": description or None, "image_urls": [url.strip() for url in image_urls.splitlines() if url.strip()]}
        show_result(*api_request("POST", "/products", json=payload))

with tab_update:
    st.write("Updates a product with `PUT /products/{product_id}`.")
    with st.form("update_product"):
        product_id = st.number_input("Product ID", min_value=1, step=1, key="update_id")
        name = st.text_input("Name", key="update_name")
        price = st.number_input("Price", min_value=0.01, step=0.01, key="update_price")
        description = st.text_area("Description (at least 10 characters)", key="update_description")
        image_urls = st.text_area("Image URLs (one per line)", key="update_images")
        submitted = st.form_submit_button("Update product")
    if submitted:
        payload = {"name": name, "price": price, "description": description or None, "image_urls": [url.strip() for url in image_urls.splitlines() if url.strip()]}
        show_result(*api_request("PUT", f"/products/{product_id}", json=payload))

with tab_delete:
    st.write("Deletes a product with `DELETE /products/{product_id}`.")
    product_id = st.number_input("Product ID", min_value=1, step=1, key="delete_id")
    if st.button("Delete product", type="primary", key="delete"):
        show_result(*api_request("DELETE", f"/products/{product_id}"))