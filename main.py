import shutil
from typing import List, Optional
from uuid import uuid4

from fastapi import BackgroundTasks, Body, FastAPI, File, Query, UploadFile
from pydantic import BaseModel

from database.db import dbsession, Base, engine
from database.schema import Files, Users
from models import CreateUser
from database.crud import create_file, get_users, create_user

app = FastAPI()

def file_save(file):
    with open(f"uploaded/{file.filename}", "wb") as f:
        shutil.copyfileobj(file.file, f)


@app.get("/users")
def users_list(limit: int = 10):
    return get_users(limit = limit)

@app.post("/users")
def add_user(user: CreateUser):
    response = create_user(user_id = user.user_id, name = user.user_id, password = user.password, username = user.username)
    return {"user": response, "details": "Operation successful"}

@app.post("/{user_id}/files")
def add_file(user_id: str,  task: BackgroundTasks, file: UploadFile = File(...)):
    # 'file' attributes are filename, file(file-like object)
    task.add_task(file_save, file = file)
    response = create_file(path = f"uploaded/{file.filename}", 
        user_id = user_id, 
        name = file.filename
    )
    return response

Base.metadata.create_all(engine)
    





