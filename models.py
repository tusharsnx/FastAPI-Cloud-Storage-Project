from pydantic import BaseModel, Field
from uuid import UUID
import uuid
from datetime import date
from typing import Optional

class User(BaseModel):
    name: str
    username: str
    
# class AddFile(BaseModel):
# print(BlogsUpdate.schema())


