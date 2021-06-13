from sqlalchemy.sql.expression import null
from db import engine, Base, dbsession
from datetime import datetime
from sqlalchemy import MetaData, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

class Users(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    password = Column(String)
    username = Column(String, unique=True)
    # num_files = Column(Integer)

    files = relationship("Files", back_populates="user")

    def __repr__(self):
        return f"name: {self.name}, username: {self.username}, file: {[file.name for file in self.files]}"

class Files(Base):
    __tablename__ = "files"

    file_id = Column(Integer, primary_key=True)
    name = Column(String)
    path = Column(String)
    date_added = Column(DateTime)
    user_id = Column(ForeignKey("users.user_id"), nullable=True)
    
    user = relationship("Users", back_populates="files")

    def __repr__(self):
        return f"file_name: {self.name}, file_path: {self.path}, date_added: {self.date_added}"

Base.metadata.create_all(engine)


# user = Users(name="Tushar Singh", username="tusharvickey1999", password="1999")
# print(user)

# with dbsession() as session:
#     # session.add(user)
#     # session.commit()
#     # file1 = Files(file_name="1.txt", file_path="1.txt", date_added=datetime(1999,5,21).date())
#     # file2 = Files(file_name="2.txt", file_path="2.txt", date_added="1999-06-29")
#     # session.add_all([file1])
#     # session.commit()
#     with dbsession() as session:
#         result = session.query(Files).filter(Files.file_name=="1.txt").all()
#         list_of_files = list(result)
#         user = Users(name="Tushar Singh", password="1999", username="tusharvickey1999")
#         user.file = list_of_files
#         session.add(user)
#         session.commit()
#         # for row in result:
#         #     print(row.user_id)
#         print(user)

# with dbsession() as session:
    
    # for table in Base.metadata.sorted_tables:                                        # list of table object in the database
    #     print(table.name)                                                                          # prints name of the table
    #     print(table.columns)                                                                     # prints list of columns object of the table
    # for table in Base.metadata.tables:
    #     print(table)
    