from fastapi import APIRouter
from starlette.background import BackgroundTasks
from models import CreateUser
from fastapi import HTTPException
from database.crud import delete_user, get_files, read_user, read_users, create_user
import utils

router = APIRouter(tags=["users"], prefix="/users")


@router.get("/", tags=["users"])
def users_list(limit: int = 10):
    return read_users(limit = limit)


@router.get("/{user_id}", tags=["users"])
def user_detail(user_id: str):
    response = read_user(user_id)
    if response is None:
        raise HTTPException(status_code=403, detail="user not found")
    return response


@router.get("/{user_id}/files", tags=["users"])
def get_files_list(user_id: str):
    response = get_files(user_id)
    if response is None:
        raise HTTPException(status_code = 401, detail = "user not found")
    else:
        return response


@router.post("/", tags=["users"])
def add_user(user: CreateUser):
    response = create_user(name=user.name, 
        password=user.password, 
        username=user.username
    )
    return {"user": response, "detail": "Operation successful"}


@router.delete("/{user_id}", tags=["users"])
def remove_user(user_id: str, task: BackgroundTasks):
    response = delete_user(user_id = user_id)
    if not response:
        raise HTTPException(400, detail="user not found!!")
    for path in response:
        task.add_task(utils.file_delete, path=path)
    return {"detail": "operation successful"}