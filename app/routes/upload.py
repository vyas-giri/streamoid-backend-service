from fastapi import APIRouter, File, UploadFile, Depends
import csv, io
from sqlalchemy.orm import Session
from ..model import Product
from ..db import get_db
from typing import Annotated

router = APIRouter()

@router.post("/upload")
async def uploadProducts(file: UploadFile, db: Annotated[Session, Depends(get_db)]):
    content = await file.read()
    reader = csv.DictReader(io.StringIO(content.decode()))
    stored, failed = 0, []

    for i, row in enumerate(reader, start=2):
        try:
            # --- validation ---
            if not all([row.get("sku"), row.get("name"), row.get("brand"), row.get("mrp"), row.get("price")]):
                raise ValueError("Missing required fields")
            if float(row["price"]) > float(row["mrp"]):
                raise ValueError("price > mrp")
            if int(row.get("quantity", 0)) < 0:
                raise ValueError("negative quantity")

            product = Product(
                sku=row["sku"],
                name=row["name"],
                brand=row["brand"],
                color=row.get("color"),
                size=row.get("size"),
                mrp=float(row["mrp"]),
                price=float(row["price"]),
                quantity=int(row.get("quantity", 0))
            )
            db.merge(product)  # upsert
            stored += 1
        except Exception as e:
            failed.append(f"Row {i}: {e}")

    db.commit()
    return {"stored": stored, "failed": failed}
