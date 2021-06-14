from fastapi import APIRouter
from fastapi import BackgroundTasks, File, UploadFile, HTTPException
from sqlalchemy.sql.functions import percentile_disc
from database.crud import read_file, delete_file, create_file
import utils

router = APIRouter(tags=["files"], prefix="/files")

@router.post("/{user_id}")
def add_file(user_id: str,  task: BackgroundTasks, file: UploadFile = File(...)):
    # 'file' attributes are filename, file(file-like object)
    response = create_file(user_id = user_id, file_name = file.filename)
    task.add_task(utils.file_save, file = file,  path = response["file_path"])
    return response

@router.delete("/{file_id}")
def remove_file(file_id: str, tasks: BackgroundTasks):
    response = delete_file(file_id = file_id)
    if response:
        tasks.add_task(utils.file_delete, path=response)
        return {"detail": "operation successful"}
    else:
        raise HTTPException(400, detail="user's file could not be found!!")


@router.get("/{file_id}")
def get_file(file_id: str):
    return read_file(file_id = file_id)
