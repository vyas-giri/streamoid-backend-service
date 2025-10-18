from fastapi import FastAPI
from .db import engine
from .model import Product, Base

app = FastAPI(title="Streamoid Product API")

Base.metadata.create_all(bind=engine)

@app.get('/')
async def root():
    return {"message": "Hello"}