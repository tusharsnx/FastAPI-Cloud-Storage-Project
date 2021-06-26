from fastapi import APIRouter
from typing import List
from fastapi import BackgroundTasks, File, UploadFile, HTTPException
from database.crud import read_file, delete_file, create_file
import utils
from fastapi.security import OAuth2PasswordBearer
import urllib.parse

router = APIRouter(tags=["files"], prefix="/api/files")
auth = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/{username}")
async def add_file(username: str,  task: BackgroundTasks, file: UploadFile = File(...)):

    # sometimes filename recieved are enconded in url-like format
    decoded_file_name = urllib.parse.unquote(file.filename)

    # 'file' attributes are filename, file(file-like object)
    response = create_file(username = username, file_name = decoded_file_name)
    if response is None:
        raise HTTPException(status_code=403, detail="user not found")
    
    # creating background task to save received file
    task.add_task(utils.file_save, file = file,  path = response["file_path"])
    return response


@router.delete("/{username}/{file_id}")
async def remove_file(file_id: str, tasks: BackgroundTasks, username: str):
    response = delete_file(file_id=file_id, username=username)
    if not response:
        raise HTTPException(400, detail="user's file not found!!")
    tasks.add_task(utils.file_delete, path=response.path)
    return {"detail": "operation successful"}


@router.get("/{username}/{file_id}")
async def get_file(file_id: str, username: str):
    response = read_file(file_id = file_id, username=username)
    if response is None:
        raise HTTPException(status_code=401, detail="file not found")
    else:
        return response
