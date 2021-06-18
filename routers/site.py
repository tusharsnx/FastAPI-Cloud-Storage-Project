from fastapi import APIRouter, Depends
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from starlette.responses import RedirectResponse
from models import AuthUser


router = APIRouter()
template = Jinja2Templates(directory="templates")

def get_current_user(request: Request):
    token = request.cookies.get("id_token")
    if token:
        # return token
        # return jwt.decode(token, SECRET, algorithm = "HS256")
        return AuthUser(username=token)
    else:
        return None


@router.get("/profile")
def profile(user: AuthUser = Depends(get_current_user)):
    if user is None:
        return RedirectResponse(url="http://localhost:8000/login")
    else:
        return {"username": user.username}

@router.get("/login", response_class=HTMLResponse)
async def index(request: Request):
    return template.TemplateResponse("test_login.html", {"request": request})

@router.get("/logout")
async def logout(request: Request):
    return template.TemplateResponse("test_logout.html", {"request": request})