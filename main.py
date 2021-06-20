from fastapi import FastAPI
from database.db import Base, engine
from routers import users, files, authorization, site
from fastapi.templating import Jinja2Templates
import os

app = FastAPI()

app.include_router(users.router)
app.include_router(files.router)
app.include_router(authorization.router)
app.include_router(site.router)

# DOMAIN = "http://localhost:8000" 

Base.metadata.create_all(engine)

# if not os.path.exists("uploaded/"):
#     os.mkdir("uploaded/")