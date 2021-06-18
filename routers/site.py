from fastapi import APIRouter
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse



router = APIRouter()
template = Jinja2Templates(directory="templates")

@router.get("/login", response_class=HTMLResponse)
async def index(request: Request):
    return template.TemplateResponse("test_login.html", {"request": request})