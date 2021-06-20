# from main import DOMAIN
from fastapi import APIRouter, Depends
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse
from models import User
from .authorization import auth
from utils import file_exists
import aiohttp
import json

# loading domain url
with open('config.json', 'r') as f:
    config = json.load(f)

DOMAIN = config["DOMAIN"]

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

@router.get("/download/{file_id}")
async def file_download(file_id: str, request: Request, user: User = Depends(get_current_user)):
    if user is None:
        return RedirectResponse(url="http://localhost:8000/login")

    file = None

    # fetches file details from the database using api call
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{DOMAIN}/api/files/{user.username}/{file_id}") as resp:
            file = await resp.json()

            # file details not available
            if resp.status!=200:
                return template.TemplateResponse("file_not_found.html", {"request": request})

        # if details exist but file does not exists in the directory
        if not file_exists(file["file_path"]):
            await session.delete(f"{DOMAIN}/api/files/{user.username}/{file_id}")
            return template.TemplateResponse("file_not_found.html", {"request": request})

    # return file, if exists
    return FileResponse(file["file_path"], filename=file["file_name"])
    

@router.get("/dashboard")
async def dashboard(request: Request, user: User = Depends(get_current_user)):
    '''
    shows all user's files in a html page.
    '''
    if user is None:
        return RedirectResponse(url="http://localhost:8000/login")

    user_files = None
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{DOMAIN}/api/users/{user.username}/files") as resp:
            user_files = await resp.json()
    response = [{"file_name": file["file_name"], "date_added": file["date_added"], "file_id": file["file_id"]} for file in user_files]
    return template.TemplateResponse("dashboard_test.html",{"request": request, "user": user.dict(), "user_files": response})
