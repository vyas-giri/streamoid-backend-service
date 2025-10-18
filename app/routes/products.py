from fastapi import APIRouter, Depends, Query
from typing import Optional, Annotated
from sqlalchemy.orm import Session
from ..db import get_db
from ..model import Product
from pydantic import BaseModel

router = APIRouter(prefix="/products", tags=["Products"])

class ProductOut(BaseModel):
    sku: str
    name: str
    brand: str
    color: Optional[str] = None
    size: Optional[str] = None
    mrp: float
    price: float
    quantity: int

    model_config = {"from_attributes": True}


class PaginatedResults(BaseModel):
    page: int
    limit: int
    total: int
    data: list[ProductOut]


@router.get("", response_model=PaginatedResults)
def getProducts(
    db: Annotated[Session, Depends(get_db)],
    page: Annotated[int, Query(ge=1)] = 1,
    limit: Annotated[int, Query(ge=1, le=100)] = 10
):

    offset = (page - 1) * limit
    products = db.query(Product).offset(offset).limit(limit).all()
    count = db.query(Product).count()
    return {
        "page": page,
        "limit": limit,
        "total": count,
        "data": products
    }

@router.get("/search", response_model=list[ProductOut])
def search_products(
    db: Annotated[Session, Depends(get_db)],
    brand: Annotated[Optional[str], Query()] = None,
    color: Annotated[Optional[str], Query()] = None,
    minPrice: Annotated[Optional[float], Query()] = None,
    maxPrice: Annotated[Optional[float], Query()] = None,
):
    query = db.query(Product)
    if brand:
        query = query.filter(Product.brand.ilike(f"%{brand}%"))
    if color:
        query = query.filter(Product.color.ilike(f"%{color}%"))
    if minPrice is not None:
        query = query.filter(Product.price >= minPrice)
    if maxPrice is not None:
        query = query.filter(Product.price <= maxPrice)
    return query.all()