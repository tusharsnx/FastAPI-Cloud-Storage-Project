from .db import dbsession
from .schema import Users, Files
from uuid import uuid4
from datetime import datetime

def create_file(file_name, user_id):
    file_id = str(uuid4())
    date_added = datetime.now().date()
    response = dict
    with dbsession() as session:
        user = session.query(Users).filter(Users.user_id==user_id).first()
        file = Files(file_id=file_id, name=file_name, path=f"uploaded/{file_id}", date_added=date_added)
        file.user = user
        session.add(file)
        session.commit()
        response = file.json()
    return response


def get_users(limit: int = 10):
    users_info= list()
    with dbsession() as session:
        result = session.query(Users).all()
        for step, user in enumerate(result):
            if step<limit:
                user_detail = user.json()
                users_info.append(user_detail)
    return users_info

def create_user(name, password, username, user_id=None):
    response = dict()
    with dbsession() as session:
        if user_id is None:
            user_id = str(uuid4())
        else:
            user_id = str(user_id)
        user = Users(user_id=user_id, 
            name=name,
            password=password,
            username=username
        )
        session.add(user)
        session.commit()
        response = user.json()
    return response

def get_user_detail(user_id):
    response =  dict()
    with dbsession() as session:
        user = session.query(Users).filter(Users.user_id==user_id).first()
        response = user.json()
    return response

def get_files(user_id):
    with dbsession() as session:
        result = session.query(Files).join(Users).filter(Users.user_id == user_id).all()
        file_list = []
        for file in result:
            file_list.append(file.json())

    return file_list

def delete_file(file_id):
    response = None
    with dbsession() as session:
        file = session.query(Files).filter(Files.file_id == file_id).first()
        if file is None:
            return response
        else:
            response = file.path
            session.delete(file)
            session.commit()
    return response
        # if not len(file):

def read_file(file_id):
    response = dict()
    with dbsession() as session:
        file = session.query(Files).filter(Files.file_id==file_id).first()
        response = file.json()
    return response

def delete_user(user_id):
    with dbsession() as session:
        user = session.query(Users).filter(Users.user_id==user_id).first()
        if user is None:
            return False
        session.delete(user)
        session.commit()
    return True

