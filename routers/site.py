# from main import DOMAIN
from fastapi import APIRouter, Depends, BackgroundTasks, UploadFile, File
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse
from models import User, UserDetails
from .authorization import auth
from utils import file_exists
import aiohttp
import json

# loading domain url
with open('config.json', 'r') as f:
    config = json.load(f)

DOMAIN = config["DOMAIN"]

router = APIRouter(default_response_class=HTMLResponse)
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


@router.get("/home", name="home")
async def index(request: Request, user: User = Depends(get_current_user)):
    if user is None:
    #     # return RedirectResponse(url="http://localhost:8000/login")
        return template.TemplateResponse("home.html", {"request": request, "user": None})
    else:
        return template.TemplateResponse("home.html", {"request": request, "user": {"name": user.name, "username": user.username}})


@router.get("/logout")
async def logout(request: Request):
    return template.TemplateResponse("logout_test.html", {"request": request})

@router.get("/download/{file_id}")
async def file_download(file_id: str, request: Request, user: User = Depends(get_current_user)):
    if user is None:
        return RedirectResponse(url=f"{DOMAIN}/home")

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
    

@router.get("/dashboard", name="dashboard")
async def dashboard(request: Request, user: User = Depends(get_current_user)):
    '''
    shows all user's files in a html page.
    '''
    if user is None:
        return RedirectResponse(url=f"{DOMAIN}/home")

    user_files = None
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{DOMAIN}/api/users/{user.username}/files") as resp:
            user_files = await resp.json()
    response = [{"file_name": file["file_name"], "date_added": file["date_added"], "file_id": file["file_id"]} for file in user_files]
    return template.TemplateResponse("fake.html",{"request": request, "user": user.dict(), "user_files": response})

@router.post("/upload")
async def upload(task: BackgroundTasks, user: UserDetails = Depends(get_current_user), file: UploadFile = File(...)):
    task.add_task(upload_file, file=file, username=user.username)
    return {"detail": "Uploaded Successfully"}


async def upload_file(file: UploadFile, user: UserDetails = Depends(get_current_user)):
    async with aiohttp.ClientSession() as session:
        await session.post(f"{DOMAIN}/api/files/{user.username}", data={'file': file.file})

