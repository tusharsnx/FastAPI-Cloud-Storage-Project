from fastapi import APIRouter
from fastapi import BackgroundTasks, File, UploadFile, HTTPException
from database.crud import read_file, delete_file, create_file
import utils

router = APIRouter(tags=["files"], prefix="/files")


@router.post("/{user_id}")
def add_file(user_id: str,  task: BackgroundTasks, file: UploadFile = File(...)):
    # 'file' attributes are filename, file(file-like object)
    response = create_file(user_id = user_id, file_name = file.filename)
    if response is None:
        raise HTTPException(status_code=403, detail="user not found")
    task.add_task(utils.file_save, file = file,  path = response["file_path"])
    return response


@router.delete("/{file_id}")
def remove_file(file_id: str, tasks: BackgroundTasks):
    response = delete_file(file_id=file_id)
    if not response:
        raise HTTPException(400, detail="user's file not found!!")
    tasks.add_task(utils.file_delete, path=response)
    return {"detail": "operation successful"}


@router.get("/{file_id}")
def get_file(file_id: str):
    response = read_file(file_id = file_id)
    if response is None:
        raise HTTPException(status_code=401, detail="file not found")
    else:
        return response
