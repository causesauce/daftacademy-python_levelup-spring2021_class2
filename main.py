from fastapi import FastAPI, Response, Cookie, HTTPException, Request

import uvicorn

app = FastAPI()

app.secret_key_sample = 'qwerty'
app.composition_to_key = 1
app.session_token = ''


@app.post("/login_session", status_code=201)
def create_login_session(login: str, password: str, response: Response):
    if login == '4dm1n' and password == 'NotSoSecurePa$$':
        session_token = app.secret_key_sample + str(app.composition_to_key)
        app.session_token = session_token
        app.composition_to_key += 1
        response.set_cookie(key='session_token', value=session_token)
        return {"message": "Welcome"}
    else:
        return HTTPException(status_code=401, detail='Wrong credentials')


@app.get("/login_token", status_code=201)
def get_login_token(response: Response, request: Request):
    session_token = request.cookies['session_token']
    if session_token == app.session_token:
        return {"token": session_token}
    else:
        return HTTPException(status_code=401, detail='Unauthorized')


if __name__ == '__main__':
    uvicorn.run(app)
