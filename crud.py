from sqlalchemy import func
from sqlalchemy.orm import Session

import models
import schemas


def get_shippers(db: Session):
    return db.query(models.Shipper).all()


def get_shipper(db: Session, shipper_id: int):
    return (
        db.query(models.Shipper).filter(models.Shipper.ShipperID == shipper_id).first()
    )


def get_suppliers(db: Session):
    return (
        db.query(models.Supplier.SupplierID, models.Supplier.CompanyName).all()
    )


def get_supplier(db: Session, supplier_id: int):
    return (
        db.query(models.Supplier).filter(models.Supplier.SupplierID == supplier_id).first()
    )


def get_products(db, id_sup):
    a = db.query(models.Product.ProductID, models.Product.ProductName, models.Category, models.Product.Discontinued) \
        .join(models.Category, models.Product.CategoryID == models.Category.CategoryID) \
        .filter(models.Product.SupplierID == id_sup).order_by(models.Product.ProductID.desc()).all()

    return a


def add_supplier(supplier: schemas.Supplier, db: Session):
    supp = models.Supplier(
        SupplierID= db.query(func.max(models.Supplier.SupplierID)).one()[0]+1,
        CompanyName=supplier.CompanyName,
        ContactName=supplier.ContactName,
        ContactTitle=supplier.ContactTitle,
        Address=supplier.Address,
        City=supplier.City,
        Region=None,
        PostalCode=supplier.PostalCode,
        Country=supplier.Country,
        Phone=supplier.Phone,
        Fax=None,
        HomePage=None
    )
    db.add(supp)
    db.commit()

    return supplier
