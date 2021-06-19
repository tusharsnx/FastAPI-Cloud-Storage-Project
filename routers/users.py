from fastapi import APIRouter, Depends
from starlette.background import BackgroundTasks
from models import User
from fastapi import HTTPException, Request
from database.crud import delete_user, get_files, read_user, read_users, create_user
import utils
from fastapi.security import OAuth2PasswordBearer

router = APIRouter(tags=["users"], prefix="/api/users")

scopes = {"user":"scopes"}

auth = OAuth2PasswordBearer(tokenUrl="token")

@router.get("/")
async def users_list(request: Request, limit: int = 10):
    # return request.headers["Authorization"]
    return read_users(limit = limit)


@router.get("/{username}")
async def user_detail(username: str):
    user_detail = read_user(username)
    if user_detail is None:
        raise HTTPException(status_code=404, detail="user not found")
    return user_detail


@router.get("/{username}/files")
async def get_files_list(username: str):
    response = get_files(username)
    if response is None:
        raise HTTPException(status_code=404, detail = "user not found")
    else:
        return response


@router.post("/")
async def add_user(user: User):
    user_detail = create_user(name=user.name, username=user.username)
    return {"user": user_detail, "detail": "Operation successful"}


@router.delete("/{username}")
async def remove_user(username: str, task: BackgroundTasks):
    response = delete_user(username = username)
    if not response:
        raise HTTPException(400, detail="user not found!!")
    for path in response:
        task.add_task(utils.file_delete, path=path)
    return {"detail": "operation successful"}