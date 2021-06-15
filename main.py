from fastapi import FastAPI
from database.db import Base, engine
from routers import users, files, authorization
import os
app = FastAPI()


app.include_router(users.router)
app.include_router(files.router)
app.include_router(authorization.router)

Base.metadata.create_all(engine)

# if not os.path.exists("uploaded/"):
#     os.mkdir("uploaded/")





