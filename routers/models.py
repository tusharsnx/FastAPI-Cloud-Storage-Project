from pydantic import BaseModel, Field
from uuid import UUID
import uuid
from datetime import date
from typing import Optional

class NewFile(BaseModel):
    id: UUID = Field(factory_default=uuid.uuid4)
    name: str = Field(...)
    date: Optional[date]

class BlogsUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=20)
    decription: Optional[str] = Field(None, max_length=120)
    published: Optional[bool]
    date: Optional[date]

# print(BlogsUpdate.schema())


