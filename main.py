from fastapi import FastAPI, Response, Cookie, HTTPException, Request, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import uvicorn
from starlette.responses import HTMLResponse

app = FastAPI()

app.secret_key_sample = 'qwerty'

app.session_token = 'adwqdwqdqwdwdqw'

security = HTTPBasic()


@app.get("/welcome_session", status_code=401)
def welcome_session(response: Response, format: str = '', session_token: str = Cookie(None)):

    if session_token == app.session_token:
        response.status_code = 200

        if format == 'json':
            response.media_type = 'json'
            return {"message": "Welcome!"}
        else:
            if format == 'html':
                response.media_type = 'html'
                return HTMLResponse("<h1>Welcome!</h1>", status_code=200, media_type='text/html')
            else:
                response.media_type = 'plain'
                return Response("Welcome!", 200, media_type='text/plain')


@app.get("/welcome_token", status_code=401)
def welcome_token(response: Response, token: str = '', format: str = ''):

    session_token = token

    if session_token == app.session_token:
        response.status_code = 200

        if format == 'json':
            response.media_type = 'json'
            return {"message": "Welcome!"}
        else:
            if format == 'html':
                response.media_type = 'html'
                return HTMLResponse("<h1>Welcome!</h1>", status_code=200, media_type='text/html')
            else:
                response.media_type = 'plain'
                return Response("Welcome!", 200, media_type='text/plain')


@app.post("/login_session", status_code=201)
def create_login_session(response: Response, credentials: HTTPBasicCredentials = Depends(security)):
    login = credentials.username
    password = credentials.password
    if login == '4dm1n' and password == 'NotSoSecurePa$$':

        session_token = app.secret_key_sample
        app.session_token = session_token

        response.set_cookie(key='token', value=session_token)
    else:
        response.status_code = 401
        return response


@app.post("/login_token", status_code=201)
def get_login_token(response: Response, session_token: str = Cookie(None)
                    , credentials: HTTPBasicCredentials = Depends(security)):
    login = credentials.username
    password = credentials.password
    if login == '4dm1n' and password == 'NotSoSecurePa$$':
        session_token = app.secret_key_sample
        app.session_token = session_token

        response.set_cookie(key='token', value=session_token)
        return {"token": app.session_token}

    if session_token == app.session_token:
        return {"token": app.session_token}

    response.status_code = 401
    return response


if __name__ == '__main__':
    uvicorn.run(app)
