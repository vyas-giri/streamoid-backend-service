from sqlalchemy import String, Float, Integer
from typing import Optional
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

class Product (Base):
    __tablename__ = "products"

    sku: Mapped[str] = mapped_column(String, primary_key=True, index=True, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    brand: Mapped[str] = mapped_column(String, nullable=False)
    color: Mapped[Optional[str]] = mapped_column(String)
    size: Mapped[Optional[str]] = mapped_column(String)
    mrp: Mapped[float] = mapped_column(Float, nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, default=0)