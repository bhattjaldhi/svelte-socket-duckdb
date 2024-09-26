from pydantic import BaseModel, Field
from typing import Optional, List


class Category(BaseModel):
    id: int
    name: str


class Product(BaseModel):
    id: int
    name: str
    amount: int
    color: str = Field(..., max_length=40)
    weight: float
    category_id: int
    brand: Optional[str] = None
    SKU: str
    country_of_origin: str = Field(..., max_length=3)


class ProductCreate(BaseModel):
    name: str
    amount: int
    color: str = Field(..., max_length=40)
    weight: float
    category_id: int
    brand: Optional[str] = None
    SKU: str
    country_of_origin: str = Field(..., max_length=3)


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    amount: Optional[int] = None
    color: Optional[str] = Field(None, max_length=40)
    weight: Optional[float] = None
    category_id: Optional[int] = None
    brand: Optional[str] = None
    SKU: Optional[str] = None
    country_of_origin: Optional[str] = Field(None, max_length=3)


class ProductResponse(BaseModel):
    data: List


class CellUpdateRequest(BaseModel):
    table_name: str = Field(..., pattern="^(product|category)$")
    row_id: int
    column: str
    new_value: str


class CellUpdateResponse(BaseModel):
    status: str
    message: str


class UpdateFailureResponse(BaseModel):
    status: str
    error: str
    row_id: int
    column: str
