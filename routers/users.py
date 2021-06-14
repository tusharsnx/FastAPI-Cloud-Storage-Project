from fastapi import APIRouter
from models import CreateUser
from fastapi import HTTPException
from database.crud import delete_user, get_files, get_user_detail, get_users, create_user

router = APIRouter(tags=["users"], prefix="/users")


@router.get("/", tags=["users"])
def users_list(limit: int = 10):
    return get_users(limit = limit)


@router.get("/{user_id}", tags=["users"])
def user_detail(user_id: str):
    return get_user_detail(user_id)


@router.get("/{user_id}/files", tags=["users"])
def get_files_list(user_id: str):
    return get_files(user_id)


@router.post("/", tags=["users"])
def add_user(user: CreateUser):
    response = create_user(user_id = user.user_id, 
        name = user.name, 
        password = user.password, 
        username = user.username
    )
    return {"user": response, "detail": "Operation successful"}


@router.delete("/{user_id}", tags=["users"])
def remove_user(user_id: str):
    response = delete_user(user_id = user_id)
    if response:
        return {"detail": "operation successful"}
    else:
        raise HTTPException(400, detail="user could not be found!!")