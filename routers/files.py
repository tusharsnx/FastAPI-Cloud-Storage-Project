from fastapi import APIRouter
from typing import List
from fastapi import BackgroundTasks, File, UploadFile, HTTPException
from database.crud import read_file, delete_file, create_file
import utils
from fastapi.security import OAuth2PasswordBearer

router = APIRouter(tags=["files"], prefix="/api/files")
auth = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/{username}")
async def add_file(username: str,  task: BackgroundTasks, file: UploadFile = File(...)):
    # 'file' attributes are filename, file(file-like object)
    response = create_file(username = username, file_name = file.filename)
    if response is None:
        raise HTTPException(status_code=403, detail="user not found")
    task.add_task(utils.file_save, file = file,  path = response["file_path"])
    return response


@router.delete("/{username}/{file_id}")
async def remove_file(file_id: str, tasks: BackgroundTasks, username: str):
    response = delete_file(file_id=file_id, username=username)
    if not response:
        raise HTTPException(400, detail="user's file not found!!")
    tasks.add_task(utils.file_delete, path=response)
    return {"detail": "operation successful"}


@router.get("/{username}/{file_id}")
async def get_file(file_id: str, username: str):
    response = read_file(file_id = file_id, username=username)
    if response is None:
        raise HTTPException(status_code=401, detail="file not found")
    else:
        return response

# @router.get("/download/{file_id}", response_model=FileResponse)
# def download_file(file_id: str):
#     response = requests.get()
