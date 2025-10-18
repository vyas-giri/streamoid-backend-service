import io, csv
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def sample_csv() -> bytes:
    data = io.StringIO()
    writer = csv.writer(data)
    writer.writerow(["sku", "name", "brand", "color", "size", "mrp", "price", "quantity"])
    writer.writerow(["SKU-1", "Test Shirt", "BrandX", "Red", "M", 500, 400, 10])
    return data.getvalue().encode()


def test_root():
    r = client.get("/")
    assert r.status_code == 200
    assert "Hello" in r.json()["message"]

def test_upload_csv():
    files = {"file": ("products.csv", sample_csv(), "text/csv")}
    r = client.post("/upload", files=files)
    js = r.json()
    assert r.status_code == 200
    assert js["stored"] == 1
    assert js["failed"] == []

def test_get_products():
    r = client.get("/products/?page=1&limit=10")
    js = r.json()
    assert r.status_code == 200
    assert "data" in js
    assert isinstance(js["data"], list)

def test_search_products():
    r = client.get("/products/search?brand=BrandX")
    assert r.status_code == 200
    data = r.json()
    assert any("BrandX" in p["brand"] for p in data)
