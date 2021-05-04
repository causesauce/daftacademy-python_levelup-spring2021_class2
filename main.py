import secrets
from hashlib import sha256

from fastapi import FastAPI, Response, Cookie, HTTPException, Request, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.responses import RedirectResponse
import uvicorn
from starlette import status
from starlette.responses import HTMLResponse

app = FastAPI()

app.secret_key = "very constant and random secret, best 64+ characters, I love elephants and bananas"
app.key_counter = 1
app.access_tokens = []

security = HTTPBasic()


@app.get("/welcome_session")
def welcome_session(response: Response, format: str = None, token: str = Cookie(None)):
    print("token:", token)

    if (token is not None) and (token in app.access_tokens):
        response.status_code = status.HTTP_200_OK

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

    else:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return response


@app.get("/welcome_token")
def welcome_token(response: Response, token: str = None, format: str = None):
    print("token:", token)

    if (token is not None) and (token in app.access_tokens):
        response.status_code = status.HTTP_200_OK

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

    else:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return response


@app.post("/login_session")
def login_session(response: Response, credentials: HTTPBasicCredentials = Depends(security)):
    response.status_code = status.HTTP_201_CREATED

    correct_username = secrets.compare_digest(credentials.username, "4dm1n")
    correct_password = secrets.compare_digest(credentials.password, "NotSoSecurePa$$")

    if not (correct_username and correct_password):
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return response

    session_token = sha256(f"{correct_username}{correct_password}{app.secret_key}".encode()).hexdigest()
    app.access_tokens.append(session_token)
    response.set_cookie(key="token", value=session_token)

    return response


@app.post("/login_token")
def login_token(*, response: Response, credentials: HTTPBasicCredentials = Depends(security),
                session_token: str = Cookie(None)):
    correct_username = secrets.compare_digest(credentials.username, "4dm1n")
    correct_password = secrets.compare_digest(credentials.password, "NotSoSecurePa$$")

    if correct_username and correct_password:
        preparing_session_token = sha256(f"{correct_username}{correct_password}{app.secret_key}".encode()).hexdigest()
        app.access_tokens.append(preparing_session_token)
        response.set_cookie(key="token", value=preparing_session_token)

        response.status_code = status.HTTP_201_CREATED
        return {"token": preparing_session_token}

    if session_token in app.access_tokens:
        response.status_code = status.HTTP_201_CREATED
        return {"token": session_token}
    else:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return response


# 3.4

@app.delete("/logout_session")
def logout_session(response: Response, token: str = '', format: str = '',
                 credentials: HTTPBasicCredentials = Depends(security),
                 session_token: str = Cookie(None)):
    if token is None or token not in app.access_tokens:
        response.status_code = 401
        return response

    correct_username = secrets.compare_digest(credentials.username, "4dm1n")
    correct_password = secrets.compare_digest(credentials.password, "NotSoSecurePa$$")

    if not (correct_username and correct_password):
        response.status_code = 401
        return response

    app.access_tokens = []

    return RedirectResponse(
        f'/logout_token/?format={format}',
        status_code=302
    )


@app.delete("/logout_token")
def logout_token(response: Response, token: str = '', format: str = '',
                 credentials: HTTPBasicCredentials = Depends(security),
                 session_token: str = Cookie(None)):
    if token is None or token not in app.access_tokens:
        response.status_code = 401
        return response

    correct_username = secrets.compare_digest(credentials.username, "4dm1n")
    correct_password = secrets.compare_digest(credentials.password, "NotSoSecurePa$$")

    if not (correct_username and correct_password):
        response.status_code = 401
        return response

    app.access_tokens = []

    return RedirectResponse(
        f'/logout_token/?format={format}',
        status_code=302
    )


@app.get("logged_out/{format}")
def logged_out(response: Response, format: str):
    if format == 'json':
        response.media_type = 'json'
        return {"message": "Logged out!"}
    else:
        if format == 'html':
            response.media_type = 'html'
            return HTMLResponse("<h1>Logged out!</h1>", status_code=200, media_type='text/html')
        else:
            response.media_type = 'plain'
            return Response("Logged out!", 200, media_type='text/plain')


if __name__ == "__main__":
    uvicorn.run(app)

#
# app = FastAPI()
#
# app.secret_key_sample = 'qwerty'
#
# app.session_token = 'adwqdwqdqwdwdqw'
#
# security = HTTPBasic()
#
#
# @app.get("/welcome_session", status_code=401)
# def welcome_session(response: Response, format: str = '', session_token: str = Cookie(None)):
#
#     if session_token == app.session_token:
#         response.status_code = 200
#
#         if format == 'json':
#             response.media_type = 'json'
#             return {"message": "Welcome!"}
#         else:
#             if format == 'html':
#                 response.media_type = 'html'
#                 return HTMLResponse("<h1>Welcome!</h1>", status_code=200, media_type='text/html')
#             else:
#                 response.media_type = 'plain'
#                 return Response("Welcome!", 200, media_type='text/plain')
#
#
# @app.get("/welcome_token", status_code=401)
# def welcome_token(response: Response, token: str = '', format: str = ''):
#
#     session_token = token
#
#     if session_token == app.session_token:
#         response.status_code = 200
#
#         if format == 'json':
#             response.media_type = 'json'
#             return {"message": "Welcome!"}
#         else:
#             if format == 'html':
#                 response.media_type = 'html'
#                 return HTMLResponse("<h1>Welcome!</h1>", status_code=200, media_type='text/html')
#             else:
#                 response.media_type = 'plain'
#                 return Response("Welcome!", 200, media_type='text/plain')
#
#
# @app.post("/login_session", status_code=201)
# def create_login_session(response: Response, credentials: HTTPBasicCredentials = Depends(security)):
#     login = credentials.username
#     password = credentials.password
#     if login == '4dm1n' and password == 'NotSoSecurePa$$':
#
#         session_token = app.secret_key_sample
#         app.session_token = session_token
#
#         response.set_cookie(key='token', value=session_token)
#     else:
#         response.status_code = 401
#         return response
#
#
# @app.post("/login_token", status_code=201)
# def get_login_token(response: Response, session_token: str = Cookie(None)
#                     , credentials: HTTPBasicCredentials = Depends(security)):
#     login = credentials.username
#     password = credentials.password
#     if login == '4dm1n' and password == 'NotSoSecurePa$$':
#         session_token = app.secret_key_sample
#         app.session_token = session_token
#
#         response.set_cookie(key='token', value=session_token)
#         return {"token": app.session_token}
#
#     if session_token == app.session_token:
#         return {"token": app.session_token}
#
#     response.status_code = 401
#     return response
#
#
# if __name__ == '__main__':
#     uvicorn.run(app)
