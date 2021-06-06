from fastapi import FastAPI
from typing  import Optional
from pydantic import BaseModel

app = FastAPI()

class Blogs(BaseModel):
    title: str = "10"
    body: str = "body"
    published_at: Optional[bool]

@app.get("/blogs")
@app.get('/')
def blogs(limit: int = 100, sort: Optional[str] = None):
    return {"data" : limit}

@app.post("/blogs")
def create_blogs(blog: Blogs):
    return blog.title

@app.get("/blogs/unpublished")
def blog_id(id: int):
    return {"id": id, "data": {"name": "Tushar Singh", "age": 19}}

@app.get("/blogs/{id}")
def blog_id(id: int):
    return {"id": id, "data": {"name": "Tushar Singh", "age": 19}}

@app.get("/blogs/{id}/age")
def user_age(id: int):
    return {"id": id, "age": 19}
