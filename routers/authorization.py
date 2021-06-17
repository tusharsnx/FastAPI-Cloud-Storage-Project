from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends,  Cookie
from starlette.responses import HTMLResponse
from models import AuthUser
from fastapi.requests import Request
from fastapi.responses import Response, RedirectResponse
from jose import jwt
from uuid import uuid4

SECRET = "mysecret"
CLIENT_ID = "722606380137-og8ok3tuotbrclko9fufih9ecdrb01a9.apps.googleusercontent.com"
CLIENT_SECRET = "C6nN5q32iylE7SFtH5ZFNp4g"
REDIRECT_URI = "http://localhost:8000/login"
SCOPE = "openid email"
OAUTH2_Server = "https://accounts.google.com/o/oauth2/v2/auth?"
Token_Server = ""

google_auth_query_params = f"client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code&scope={SCOPE}&nonce={uuid4()}"

auth = OAuth2PasswordBearer(tokenUrl="token")
router = APIRouter()

# checks if user is logged in
def get_current_user(request: Request, response: Response):
    token = request.cookies.get("access_token")
    if token:
        # return jwt.decode(token, SECRET, algorithm = "HS256")
        return AuthUser(username="username")
    else:
        print("redirecting.....")
        return RedirectResponse(url="http://localhost:8000/login")
        
# returns username if user is logged in
@router.get("/me")
def profile(user: AuthUser = Depends(get_current_user)):
    print("inside me")
    return {"user": user.username}

# redirects to auth server if not logged in
@router.get("/login", response_class=HTMLResponse)
def login(response: Response):
    print("inside login")
    return RedirectResponse(url="http://localhost:8000/callback?code=123")
    # return response.RedirectResponse(OAUTH2_Server+google_auth_query_params)        # redirects to google auth server

# callback url which receives code
@router.post("/callback")
def callback(request: Request, response: Response):
    print("inside callback")
    # q_params = request.query_params
    # code = q_params.get("code")
    # scopes = q_params.get("scope")
    code = request.body().get("code")
    response.set_cookie("token", code)
    return RedirectResponse(url="http://localhost:8000/me")


    

