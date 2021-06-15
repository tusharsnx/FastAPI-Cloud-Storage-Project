from .db import dbsession
from .schema import Users, Files
from uuid import uuid4
from datetime import datetime
from passlib.context import CryptContext

hasher = CryptContext(schemes=["bcrypt"])


def create_file(file_name: str, user_id: str):
    if not read_user(user_id):
        return None
    file_id = str(uuid4())
    date_added = datetime.now().date()
    response = dict()
    with dbsession() as session:
        user = session.query(Users).filter(Users.user_id==user_id).first()
        file = Files(file_id=file_id, name=file_name, path=f"uploaded/{file_id}", date_added=date_added)
        file.user = user
        session.add(file)
        session.commit()
        response = file.json()
    return response


def read_users(limit: int = 10):
    users_info= list()
    with dbsession() as session:
        result = session.query(Users).all()
        for step, user in enumerate(result):
            if step<limit:
                user_detail = user.json()
                users_info.append(user_detail)
    return users_info

def create_user(name: str, password: str, username: str):
    response = dict()
    with dbsession() as session:
        user_id = str(uuid4())
        user = Users(user_id=user_id, 
            name=name,
            password=hasher.hash(password),
            username=username
        )
        session.add(user)
        session.commit()
        response = user.json()
    return response

def read_user(user_id: str):
    response =  None
    with dbsession() as session:
        user = session.query(Users).filter(Users.user_id==user_id).first()
        if user is None:
            return None
        response = user.json()
    return response

def get_files(user_id: str):
    with dbsession() as session:
        if not read_user(user_id):
            return None
        result = session.query(Files).join(Users).filter(Users.user_id == user_id).all()
        file_list = []
        for file in result:
            file_list.append(file.json())

    return file_list

def delete_file(file_id: str):
    response = None
    with dbsession() as session:
        file = session.query(Files).filter(Files.file_id==file_id).first()
        if file is None:
            return response
        response=file.path
        session.delete(file)
        session.commit()
    return response
 

def read_file(file_id: str):
    response = dict()
    with dbsession() as session:
        file = session.query(Files).filter(Files.file_id==file_id).first()
        if file is None:
            return None
        response = file.json()
    return response

def delete_user(user_id: str):
    if not read_user(user_id):
        return None 
    file_paths = []
    with dbsession() as session:
        user = session.query(Users).filter(Users.user_id==user_id).first()
        for file in user.files:
            file_paths.append(file.path)
        session.delete(user)
        session.commit()
    return file_paths

