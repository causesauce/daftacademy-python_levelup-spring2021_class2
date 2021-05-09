import sqlite3
from fastapi import FastAPI, Response, Cookie, HTTPException, Request, Depends
import uvicorn

app = FastAPI()
app.db_connection = None


@app.on_event("startup")
async def startup():
    app.db_connection = sqlite3.connect("northwind.db")
    app.db_connection.text_factory = lambda b: b.decode(errors="ignore")  # northwind specific


@app.on_event("shutdown")
async def shutdown():
    app.db_connection.close()


@app.get("/categories", status_code=200)
async def get_categories():
    conn = app.db_connection
    cursor = conn.cursor()
    cursor.row_factory = sqlite3.Row
    categories = cursor.execute(""
                                "select categoryid id, categoryname name "
                                "from categories "
                                "order by categoryid").fetchall()
    return dict(categories=categories)


@app.get("/customers", status_code=200)
async def get_customers():
    conn = app.db_connection
    cursor = conn.cursor()
    cursor.row_factory = sqlite3.Row
    customers = cursor.execute(
        "SELECT CustomerID id, COALESCE(CompanyName, '') name, "
        "COALESCE(Address, '') || ' ' || COALESCE(PostalCode, '') || ' ' || COALESCE(City, "
        "'') || "
        "' ' || COALESCE(Country, '') full_address "
        "from customers "
        "ORDER BY UPPER(CustomerID);"
    ).fetchall()
    return dict(customers=customers)


@app.get("/products/{id_prod}", status_code=200)
async def get_products(response: Response, id_prod: int):
    conn = app.db_connection
    cursor = conn.cursor()
    cursor.row_factory = sqlite3.Row
    products = cursor.execute(
        "select ProductID id, ProductName name "
        "from Products "
        "where ProductID = ?",
        (id_prod,)
    ).fetchone()

    if products is None:
        response.status_code = 404
        return
    return products


if __name__ == '__main__':
    uvicorn.run(app)
#
# with sqlite3.connect('northwind.db') as conn:
#
#     conn.text_factory = lambda b: b.decode(errors='ignore')
#     curson = conn.cursor()
#     products = curson.execute("select productname from products").fetchall()
#     for i in products:
#         print(i)
#     # conn.close()

# a = 10
# print(f'{a=}')
