from .db import dbsession
from .schema import Users, Files
from uuid import uuid4
from datetime import datetime
# from passlib.context import CryptContext

# hasher = CryptContext(schemes=["bcrypt"])

# create user's file
def create_file(file_name: str, username: str):
    if not read_user(username):
        return None
    file_id = str(uuid4())
    date_added = datetime.now().date()
    response = dict()
    with dbsession() as session:
        user = session.query(Users).filter(Users.username==username).first()
        file = Files(file_id=file_id, name=file_name, path=f"uploaded/{file_id}", date_added=date_added)
        file.user = user
        session.add(file)
        session.commit()
        response = file.json()
    return response

# returns users details upto limit
def read_users(limit: int = 10):
    users_info= list()
    with dbsession() as session:
        result = session.query(Users).all()
        for step, user in enumerate(result):
            if step<limit:
                user_detail = user.json()
                users_info.append(user_detail)
    return users_info


# creates user
def create_user(name: str, username: str):
    response = dict()
    with dbsession() as session:
        user_id = str(uuid4())
        user = Users(
            user_id=user_id, 
            name=name,
            username=username
        )
        session.add(user)
        session.commit()
        response = user.json()
    return response


# returns user details
def read_user(username: str):
    response =  None
    with dbsession() as session:
        user = session.query(Users).filter(Users.username==username).first()
        if user is None:
            return None
        response = user.json()
    return response


# returns all user's files
def get_files(username: str):
    with dbsession() as session:
        if not read_user(username):
            return None
        result = session.query(Files).join(Users).filter(Users.username == username).all()
        file_list = []
        for file in result:
            file_list.append(file.json())

    return file_list

# deletes user's file
def delete_file(file_id: str, username: str):
    with dbsession() as session:
        file = session.query(Files).join(Users).filter(Files.file_id==file_id, Users.username==username).first()
        if file is None:
            return None
        response=file
        session.delete(file)
        session.commit()
    return response
 

# returns user's file details
def read_file(file_id: str, username: str):
    response = dict()
    with dbsession() as session:
        file = session.query(Files).join(Users).filter(Files.file_id==file_id, Users.username==username).first()
        if file is None:
            return None
        response = file.json()
    return response


# deletes user
def delete_user(username: str):
    if not read_user(username):
        return None 
    file_paths = []
    with dbsession() as session:
        user = session.query(Users).filter(Users.username==username).first()
        for file in user.files:
            file_paths.append(file.path)
        session.delete(user)
        session.commit()
    return file_paths

