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
    CompanyName: constr(max_length=40)
    ContactName: constr(max_length=40)
    ContactTitle: constr(max_length=40)
    Address: constr(max_length=40)
    City: constr(max_length=40)
    PostalCode: constr(max_length=40)
    Country: constr(max_length=40)
    Phone: constr(max_length=40)
