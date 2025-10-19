# Streamoid Backend - Product API

This repository contains a backend API for **Streamoid**, a product inventory and management platform.  
It allows uploading product data via CSV, listing products with pagination, and searching/filtering products.

Built with: **Python 3.11**, **FastAPI**, **Pydantic**, **SQLAlchemy**, and **SQLite** (can be upgraded to PostgreSQL).

---

## Features

1. **CSV Upload**
   - Upload products in bulk using a CSV file.
   - Validates required fields and reports failed rows.

2. **List Products**
   - Pagination support.
   - Returns metadata: page number, limit, total records, and an array of products.

3. **Search Products**
   - Filter products by brand, name, or SKU.

4. **Automated Tests**
   - Pytest coverage for root('/'), upload('/upload'), listing('/products'), and search('/products/search') endpoints.

6. **Dockerized**
   - Runs app as a non-root user for security.
   - Easy to deploy in any containerized environment.

---

## Quick Start - Local

1. **Clone repository**
```bash
git clone <your-repo-link>
cd streamoid-backend
python3 -m venv .venv
source .venv/bin/activate
```

2. **Create virtual environment and install dependecies**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate

   pip install -r requirements.txt
   ```

3. **Run the API**
   ```bash
   fastapi dev app/main.py
   ```

   OR

   ```bash
   uvicorn app.main:app --reload
   ```

4. **Access docs**
   After starting the server you can go to http://127.0.0.1:8000/docs or http://127.0.0.1:8000/redoc to explore different endpoints and their parameters interactively.


**Docker Setup**

1. Build docker image
   ```bash
   docker build -t streamoid-backend .
   ```
2. Run container
   ```bash
   docker run -p 8000:8000 streamoid-backend
   ```
3. Access api: http://127.0.0.1:8000/docs or http://127.0.0.1:8000/redoc


**Example get request:**
```bash
curl -X GET "http://127.0.0.1:8000/products?page=1&limit=10" -H "accept: application/json"
```

**Testing**
You can run automated test using pytest:
```bash
pytest -v
```
Expected outcome:

```
========================================================================================= test session starts platform linux -- Python 3.10.12, pytest-8.4.2, pluggy-1.6.0
collected 4 items

tests/test_api.py::test_root PASSED [ 25%]
tests/test_api.py::test_upload_csv PASSED [ 50%]
tests/test_api.py::test_get_products PASSED [ 75%]
tests/test_api.py::test_search_products PASSED [100%]

========================================================================================= 4 passed in 2.28s =========================================================================================
```

---

## API Endpoints Overview

| Endpoint               | Method | Description                                           |
|------------------------|--------|-------------------------------------------------------|
| `/`                    | GET    | Root endpoint, returns a greeting message.           |
| `/upload`              | POST   | Upload CSV file with product data. Returns stored & failed rows. |
| `/products`            | GET    | Paginated list of products (use `page` & `limit` query parameters). |
| `/products/search`     | GET    | Search products by `brand`, `name`, or `sku`.       |
