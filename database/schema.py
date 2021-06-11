from .db import engine, Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

class Users(Base):
    __tablename__ = "users"

    user_id = Column(String, primary_key=True)
    name = Column(String)
    password = Column(String)
    username = Column(String)
    num_files = Column(Integer)

    file = relationship("Files", back_populates="user")

    def __repr__(self):
        return f"name: {self.name}, username: {self.username}, num_files: {self.num_files}"

class Files(Base):
    __tablename__ = "files"

    file_id = Column(String)
    file_name = Column(String)
    file_path = Column(String)
    date_added = Column(DateTime)
    user_id = Column(ForeignKey("users.user_id"))
    
    user = relationship("Users", back_populates="file")

    def __repr__(self):
        return f"file_name: {self.file_name}, file_path: {self.file_path}, date_added: {self.date_added}"

Base.meta.create_all(engine)


    