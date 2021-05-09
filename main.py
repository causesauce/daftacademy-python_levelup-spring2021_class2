import sqlite3
from fastapi import FastAPI, Response, Cookie, HTTPException, Request, Depends
import uvicorn

app = FastAPI()


@app.get("/categories", status_code=200)
def get_categories():
    with sqlite3.connect('northwind.db') as conn:
        conn.text_factory = lambda b: b.decode(errors='ignore')
        curson = conn.cursor()
        curson.row_factory = sqlite3.Row
        products = curson.execute(""
                                  "select categoryid, categoryname "
                                  "from categories "
                                  "order by categoryid").fetchall()
        categories = [{'id': f'{x["categoryid"]}', 'name': f'{x["categoryname"]}'} for x in products]
        result = {"categories": categories}
        print(result)


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
