from main import DOMAIN
from fastapi import APIRouter, Depends
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from models import User
from .authorization import auth
import aiohttp
# from ..main import DOMAIN

DOMAIN = "http://localhost:8000"

router = APIRouter()
template = Jinja2Templates(directory="templates")

async def get_current_user(request: Request):
    token = request.cookies.get("token")

    # cookie contains token
    if token:
        data = await auth.decode_token(token)
        
        # token is still valid
        if data:
            return User(name=data["name"], username=data["email"])
        
        else:
            return None
    
    else:
        return None


@router.get("/profile")
async def profile(request: Request, user: User = Depends(get_current_user)):
    if user is None:
        return RedirectResponse(url="http://localhost:8000/login")
    else:
        return template.TemplateResponse("profile_test.html", {"request": request, "name": user.name, "username": user.username})

@router.get("/login", response_class=HTMLResponse)
async def index(request: Request):
    return template.TemplateResponse("login_test.html", {"request": request})

@router.get("/logout")
async def logout(request: Request):
    return template.TemplateResponse("logout_test.html", {"request": request})

@router.get("/download")
def file_download(file_id: int):
    pass
    # file_details = await 

@router.get("/dashboard")
async def dashboard(request: Request, user: User = Depends(get_current_user)):
    user_files = None
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{DOMAIN}/api/users/{user.username}/files") as resp:
            pass
    return template.TemplateResponse("dashboard_test.html",{"request": request, "user": user.dict()})
