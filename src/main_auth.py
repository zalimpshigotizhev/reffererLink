import secrets
from datetime import datetime
from typing import Annotated, Any
from fastapi import FastAPI, Depends, status, HTTPException, Header, Cookie, Response
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from main_jwt import router as jwt_router


app = FastAPI()
security = HTTPBasic()

# app.include_router(jwt_router)


#######################################################
#######################################################
#                     AUTH-BASIC
#######################################################
#######################################################


data = {
    "adam": "sadasdasdasdasdasd",
    "zalim": "552216742",
    "eva": "sdasdasdasdasd",
    "david": "1231231"
}


async def get_auth_username(
    credential: Annotated[HTTPBasicCredentials, Depends(security)]
):
    unauthed_exc = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                 detail="Not authenticated",
                                 headers={"WWW-Authenticate": "Basic"})

    password = data.get(credential.username)
    if password is None:
        raise unauthed_exc

    if credential.password != password:
        raise unauthed_exc

    return credential.username


@app.get("/auth_basic/")
async def auth_username(
    auth_username: str = Depends(get_auth_username)
):
    return {
        "message": f"Hello {auth_username}",
        "username": auth_username
    }


#######################################################
#######################################################
#                  AUTH-TOKEN (HEADER)
#######################################################
#######################################################


users = [
    {
        "username": "adam",
        "password": "5522112233",
        "token": "sadasdasdasdasdasd"
    },
    {
        "username": "eva",
        "password": "5522112233",
        "token": "sdasdasdasdasd"
    }
]

def get_auth_header_username(
        static_token: str = Header(alias="X-Auth-Token")
):
    unauthed_exc = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                 detail="Not authenticated",
                                 headers={"WWW-Authenticate": "Basic"})
    for user in users:
        if user["token"] == static_token:
            return user
    raise unauthed_exc


@app.get("/auth_header_token/")
async def auth_username(
    user: dict = Depends(get_auth_header_username)
):

    return {
        "message": f"Hello {user.get('username')}",
        "token": user["token"],
        "password": user["password"],
    }


#######################################################
#######################################################
#                  AUTH-COOKIE
#######################################################
#######################################################


# def get_auth_cookie_username(
#         auth_cookie: Annotated[str, Header()]
# ):
#     if auth_cookie not in ["sadasdasdasdasdasd", "sdasdasdasdasd"]:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
#                             detail="Not authenticated",
#                             headers={"WWW-Authenticate": "Basic"})
#     return auth_cookie


COOKIES: dict[str, dict[str, Any]] = {
    "sadasdasdasdasdasd": {
        "username": "adam",
        "password": "5522112233",
        "token": "sadasdasdasdasdasd"
    },
    "sdasdasdasdasd": {
        "username": "eva",
        "password": "5522112233",
        "token": "sdasdasdasdasd"
    }

}

COOKIE_SESSION_ID_KEY = "web-app-session-id"


def genarate_session_id() -> str:
    return secrets.token_urlsafe()


@app.post("/login_cookie/")
async def auth_username(
    response: Response,
    auth_username: str = Depends(get_auth_username)
):
    session_id = genarate_session_id()
    COOKIES[session_id] = {
        "username": auth_username,
        "login_at": datetime.now().isoformat()
    }
    response.set_cookie(key=COOKIE_SESSION_ID_KEY, value=session_id)
    return {
        "result": "ok"
    }

def get_session_data(
        session_id: str = Cookie(alias=COOKIE_SESSION_ID_KEY)
) -> dict[str, Any]:
    if session_id not in COOKIES:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="No session id",
                            headers={"WWW-Authenticate": "Basic"})
    return COOKIES[session_id]



@app.get("/check_cookie/")
def get_auth_check_cookie(
    response: Response,
    user_session_data: dict[str, Any] = Depends(get_session_data)
):
    response.delete_cookie(key=COOKIE_SESSION_ID_KEY)
    return {
        "message": f"Nice, {user_session_data.get('username')}",
        **user_session_data
    }



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
