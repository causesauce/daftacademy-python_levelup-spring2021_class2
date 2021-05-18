import uvicorn
from fastapi import APIRouter, Depends, HTTPException, FastAPI
from pydantic import PositiveInt
from sqlalchemy.orm import Session

import crud
import schemas
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
    db_supp = crud.get_supplier(db, id)
    if db_supp is None:
        raise HTTPException(status_code=404)

    db_products = crud.get_products(db, id)
    return db_products


@app.get("/suppliers/{id}/")
async def get_supplier(id: PositiveInt, db: Session = Depends(get_db)):
    db_supps = crud.get_supplier(db, id)
    if db_supps is None:
        raise HTTPException(status_code=404)
    return db_supps


def main():
    pass


if __name__ == '__main__':
    # app.include_router(router, tags=["northwind"])
    uvicorn.run(app)
