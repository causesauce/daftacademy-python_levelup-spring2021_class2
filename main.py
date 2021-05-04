from fastapi import FastAPI, Response, Cookie, HTTPException, Request, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import uvicorn

app = FastAPI()

app.secret_key_sample = 'qwerty'
app.composition_to_key = 1
app.session_token = ''

security = HTTPBasic()


@app.get("/welcome_session", status_code=401)
def welcome_session(response: Response, format: str = '', session_token: str = Cookie(None)):

    if session_token == app.session_token:

        if format == 'json':
            response_string = '{"message": "Welcome!"}'
            return Response(content=response_string, media_type='application/json', status_code=200)

        if format == 'html':
            response_string = "" \
                              "<html>" \
                              "<h1>Welcome!</h1>" \
                              "</html>"
            return Response(content=response_string, media_type='text/html', status_code=200)

        response_string = 'Welcome!'
        return Response(content=response_string, media_type='text/plain', status_code=200)


@app.get("/welcome_token", status_code=401)
def welcome_token(response: Response, token: str = '', format: str = ''):

    session_token = token

    if session_token is not None and session_token == app.session_token:
 
        if format == 'json':
            response_string = '{"message": "Welcome!"}'
            return Response(content=response_string, media_type='application/json', status_code=200)

        if format == 'html':
            response_string = "" \
                              "<html>" \
                              "<h1>Welcome!</h1>" \
                              "</html>"
            return Response(content=response_string, media_type='text/html', status_code=200)

        response_string = 'Welcome!'
        return Response(content=response_string, media_type='text/plain', status_code=200)


@app.post("/login_session", status_code=201)
def create_login_session(response: Response, credentials: HTTPBasicCredentials = Depends(security)):
    login = credentials.username
    password = credentials.password
    if login == '4dm1n' and password == 'NotSoSecurePa$$':
        session_token = app.secret_key_sample + str(app.composition_to_key)
        app.session_token = session_token
        app.composition_to_key += 1
        response.set_cookie(key='session_token', value=session_token)
    else:
        response.status_code = 401
        response.set_cookie(key='session_token', value='')
        return response


@app.post("/login_token", status_code=201)
def get_login_token(response: Response, session_token: str = Cookie(None)
                    , credentials: HTTPBasicCredentials = Depends(security)):
    login = credentials.username
    password = credentials.password
    if login == '4dm1n' and password == 'NotSoSecurePa$$':
        session_token = app.secret_key_sample + str(app.composition_to_key)
        app.session_token = session_token
        app.composition_to_key += 1
        response.set_cookie(key='session_token', value=session_token)
        return {"token": app.session_token}

    if session_token == app.session_token:
        return {"token": app.session_token}

    response.status_code = 401
    response.set_cookie(key='session_token', value='')
    return response


if __name__ == '__main__':
    uvicorn.run(app)
