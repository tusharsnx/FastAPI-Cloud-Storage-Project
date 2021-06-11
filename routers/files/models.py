from pydantic import BaseModel, Field
from uuid import UUID
import uuid
from typing import Optional

class UsersCreate(BaseModel):
    id: UUID = Field(factory_default=uuid.uuid4)
    name: str = Field(..., max_length=5)
    email: str = Field(None, regex="/w+@/w+./w+")
    age: Optional[int]

class UsersUpdate(BaseModel):
    name: Optional[str]
    email: Optional[str] = Field(None, regex="/w+@/w+./w+")
    age: Optional[int]

# print(UsersCreate.schema())