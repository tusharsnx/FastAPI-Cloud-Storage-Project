from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends,  Cookie
from starlette.datastructures import URL
from starlette.responses import HTMLResponse
from models import AuthUser
from fastapi.requests import Request
from fastapi.responses import Response, RedirectResponse
from jose import jwt
from uuid import uuid4
import aiohttp
import asyncio


SECRET = "mysecret"
CLIENT_ID = "722606380137-og8ok3tuotbrclko9fufih9ecdrb01a9.apps.googleusercontent.com"
CLIENT_SECRET = "C6nN5q32iylE7SFtH5ZFNp4g"
REDIRECT_URI = "http://localhost:8000/auth/callback"
SCOPE = "openid email"
AUTH_Server = "https://accounts.google.com/o/oauth2/v2/auth?"
Token_Server = "https://oauth2.googleapis.com/token?"

google_query_params = f"client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code&scope={SCOPE}&nonce={uuid4()}"

auth = OAuth2PasswordBearer(tokenUrl="token")
router = APIRouter(prefix="/auth")

# checks if user is logged in
def get_current_user(request: Request, response: Response):
    token = request.cookies.get("token")
    if token:
        # return jwt.decode(token, SECRET, algorithm = "HS256")
        return AuthUser(username="username")
    else:
        print("redirecting.....")
        return None
        
# returns username if user is logged in
# @router.get("/profile")
# def profile(user: AuthUser = Depends(get_current_user)):
#     print("inside me")
#     if not user:
#         return RedirectResponse(url="http://localhost:8000/login")
#     else:
#         return {"user": user.username}

# redirects to auth server if not logged in
@router.get("/login", response_class=HTMLResponse)
def login(response: Response):
    # print("inside login")
    # return RedirectResponse(url="http://localhost:8000/api/auth/callback?code=123")
    return RedirectResponse(url=AUTH_Server+google_query_params)      # redirects to google auth server

# callback url which receives code
@router.get("/callback")
async def callback(request: Request, response: Response):
    print("inside callback")
    code = request.query_params.get("code")

    # aiohttp for async access_token request
    payload = {
        "grant_type": "authorization_code",
        "code": code,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI
    }
    token = None
    async with aiohttp.ClientSession() as session:
        async with session.post(Token_Server, data=payload) as response:
            data = await response.json()
            print(data)
            token = data.get("id_token")

    response = RedirectResponse(url="http://localhost:8000/me")
    response.set_cookie(key="token", value=token, httponly=True)
    # return "done with cookie"
    return response

@router.get("/logout")
def logout(response: Response):
    response = RedirectResponse(url="http://localhost:8000/me")
    response.delete_cookie("token")
    return response



    

