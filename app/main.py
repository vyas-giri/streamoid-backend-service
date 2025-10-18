from fastapi import FastAPI
from .db import engine
from .model import Product, Base
from .routes import upload, products

app = FastAPI(title="Streamoid Product API")

Base.metadata.create_all(bind=engine)

app.include_router(upload.router)
app.include_router(products.router)

@app.get('/')
async def root():
    return {"message": "Hello"}