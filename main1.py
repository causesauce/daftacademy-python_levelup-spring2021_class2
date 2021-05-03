from fastapi import FastAPI, Response, Request
import uvicorn
from pydantic import BaseModel
import datetime

app = FastAPI()


@app.get("/hello")
def get_hello_html():
    response_string = "" \
                      "<html>" \
                      "<head>" \
                      "</head>" \
                      "<body>" \
                      "<h1>Hello! Today date is 2021-05-03</h1>" \
                      "</body>" \
                      "</html>"
    return Response(content=response_string, media_type='text/html')


if __name__ == '__main__':
    uvicorn.run(app)
