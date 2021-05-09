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
                                "select categoryid, categoryname "
                                "from categories "
                                "order by categoryid").fetchall()
    categories = [{'id': f'{x["categoryid"]}', 'name': f'{x["categoryname"]}'} for x in categories]
    return {"categories": categories}


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
    # customers = [{"id": f'{x["CustomerID"]}', "name": f'{x["CompanyName"]}',
    #               "full_address": f'{x["full_address"]}'} for x in customers]
    return dict(customers=customers)


#
# @app.get("/customers")
# async def get_customers():
#     cursor = app.db_connection.cursor()
#     cursor.row_factory = sqlite3.Row
#     customers = cursor.execute(
#         "SELECT CustomerID id, COALESCE(CompanyName, '') name, "
#         "COALESCE(Address, '') || ' ' || COALESCE(PostalCode, '') || ' ' || COALESCE(City, '') || ' ' || "
#         "COALESCE(Country, '') full_address "
#         "FROM Customers c ORDER BY UPPER(CustomerID);"
#     ).fetchall()
#     return dict(customers=customers)


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
