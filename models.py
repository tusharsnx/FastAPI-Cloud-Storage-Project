from pydantic import BaseModel, Field
from datetime import date
from uuid import UUID
from datetime import date
from typing import Optional, List


# Request models


class User(BaseModel):
    name: str
    username: str


# Response models

# for user details
class FileDetails(BaseModel):
    file_id: UUID
    file_name: str
    file_path: str
    date_added: date
    username: str

# for file details
class UserDetails(BaseModel):
    user_id: UUID
    name: str
    username: str
    files: List






