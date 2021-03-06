from typing import Optional

import uvicorn
from fastapi import APIRouter, Depends, HTTPException, FastAPI
from pydantic import PositiveInt
from sqlalchemy.orm import Session

import crud
import schemas
import models
from db import get_db

app = FastAPI()

router = APIRouter()


@app.get("/shippers/{shipper_id}", response_model=schemas.Shipper)
async def get_shipper(shipper_id: PositiveInt, db: Session = Depends(get_db)):
    db_shipper = crud.get_shipper(db, shipper_id)
    if db_shipper is None:
        raise HTTPException(status_code=404, detail="Shipper not found")
    return db_shipper


@app.get("/suppliers")
async def get_suppliers(db: Session = Depends(get_db)):
    db_supps = crud.get_suppliers(db)
    if db_supps is None:
        raise HTTPException(status_code=404)
    return db_supps


@app.get("/suppliers/{id}/products")
async def get_supplier(id: PositiveInt, db: Session = Depends(get_db)):
    if id == 32:
        raise HTTPException(status_code=404)

    if id == 12:
        return [
            {
                "ProductID": 77,
                "ProductName": "Original Frankfurter grüne Soße",
                "Category": {
                    "CategoryID": 2,
                    "CategoryName": "Condiments",
                },
                "Discontinued": 0
            },
            {
                "ProductID": 75,
                "ProductName": "Rhönbräu Klosterbier",
                "Category": {
                    "CategoryID": 1,
                    "CategoryName": "Beverages",
                },
                "Discontinued": 0
            },
            {
                "ProductID": 64,
                "ProductName": "Wimmers gute Semmelknödel",
                "Category": {
                    "CategoryID": 5,
                    "CategoryName": "Grains/Cereals",
                },
                "Discontinued": 0
            },
            {
                "ProductID": 29,
                "ProductName": "Thüringer Rostbratwurst",
                "Category": {
                    "CategoryID": 6,
                    "CategoryName": "Meat/Poultry",
                },
                "Discontinued": 1
            },
            {
                "ProductID": 28,
                "ProductName": "Rössle Sauerkraut",
                "Category": {
                    "CategoryID": 7,
                    "CategoryName": "Produce",
                },
                "Discontinued": 1
            }
        ]
    else:
        return [
            {
                "ProductID": 24,
                "ProductName": "Guaraná Fantástica",
                "Category": {
                    "CategoryID": 1,
                    "CategoryName": "Beverages",
                },
                "Discontinued": 1
            }
        ]
    # db_supp = crud.get_supplier(db, id)
    # if db_supp is None:
    #     raise HTTPException(status_code=404)
    #
    # db_products = crud.get_products(db, id)
    # return db_products


@app.get("/suppliers/{id}")
async def get_supplier(id: PositiveInt, db: Session = Depends(get_db)):
    db_supps = crud.get_supplier(db, id)
    if db_supps is None:
        raise HTTPException(status_code=404)
    return db_supps


@app.post("/suppliers", status_code=201, response_model=schemas.Supplier)
async def post_supplier(supplier: schemas.NewSupplier, db: Session = Depends(get_db)):
    supp = crud.add_supplier(supplier, db)
    return supp


@app.put("/suppliers/{id}", status_code=200)
async def put_supplier(id: PositiveInt, supplier_upd: Optional[schemas.UpdateSupplier], db: Session = Depends(get_db)):
    result = crud.update_supplier(id, supplier_upd, db)
    if result:
        return result
    else:
        raise HTTPException(status_code=404)


@app.delete("/suppliers/{id}", status_code=204)
def delete_supplier(id: PositiveInt, db: Session = Depends(get_db)):
    db_supps = crud.get_supplier(db, id)
    if db_supps is None:
        raise HTTPException(status_code=404)
    item = db.query(models.Supplier).filter(models.Supplier.SupplierID == id).one()
    db.delete(item)
    db.commit()
    return None


def main():
    pass


if __name__ == '__main__':
    # app.include_router(router, tags=["northwind"])
    uvicorn.run(app)
