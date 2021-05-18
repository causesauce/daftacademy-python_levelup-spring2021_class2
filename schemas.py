from typing import Optional

from pydantic import BaseModel, PositiveInt, constr


class Shipper(BaseModel):
    ShipperID: PositiveInt
    CompanyName: constr(max_length=40)
    Phone: constr(max_length=24)

    class Config:
        orm_mode = True


class SuppliersShort(BaseModel):
    SupplierID: PositiveInt
    CompanyName: constr(max_length=40)

    class Config:
        orm_mode = True


class Category(BaseModel):
    CategoryID: PositiveInt
    CategoryName: constr(max_length=40)

    class Config:
        orm_mode = True


class Supplier(BaseModel):
    CompanyName: Optional[(constr(max_length=40))]
    ContactName: Optional[constr(max_length=40)]
    ContactTitle: Optional[constr(max_length=40)]
    Address: Optional[constr(max_length=40)]
    City: Optional[constr(max_length=40)]
    PostalCode: Optional[constr(max_length=40)]
    Country: Optional[constr(max_length=40)]
    Phone: Optional[constr(max_length=40)]
