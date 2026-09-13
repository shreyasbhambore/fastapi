# Streamlit frontend

Run the API:

```powershell
uvicorn app.main:app --port 8001
```

Install and start the frontend:

```powershell
pip install -r frontend/requirements.txt
streamlit run frontend/app.py
```

The dashboard supports the root/health check, list products, get product by ID, create (POST), update (PUT), and delete routes.