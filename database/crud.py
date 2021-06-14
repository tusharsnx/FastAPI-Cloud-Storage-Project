from .db import dbsession
from .schema import Users, Files
from uuid import uuid4
from datetime import datetime

def create_file(name, path, user_id):
    file_id = str(uuid4())
    date_added = datetime.now().date()
    response = dict
    with dbsession() as session:
        user = session.query(Users).filter(Users.user_id==user_id).first()
        file = Files(file_id=file_id, name=name, path=path, date_added=date_added)
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

def create_user(name, password, username, user_id=None, ):
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




