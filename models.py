from pydantic import BaseModel, Field
from uuid import UUID
import uuid
from datetime import date
from typing import Optional

class CreateUser(BaseModel):
    name: str
    username: str
    password: str

class AuthUser(BaseModel):
    username: str
    
# class AddFile(BaseModel):
# print(BlogsUpdate.schema())


