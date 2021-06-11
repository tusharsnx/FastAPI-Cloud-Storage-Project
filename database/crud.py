from .db import dbsession
from .schema import Users, Files


def create_user(**kwargs):
    with dbsession() as session:
        id = kwargs["id"]
        name = kwargs["name"]
        password = kwargs["password"]
        username = kwargs["username"]
        num_files = kwargs["num_files"]

        user = Users(id=id, name=name, 
            password=password, username=username, 
            num_files=num_files
            )
        
        
