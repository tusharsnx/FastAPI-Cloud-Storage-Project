from fastapi import FastAPI
from typing  import Optional
app = FastAPI()

@app.get("/blogs")
@app.get('/')
def blogs(limit: int = 100, sort: Optional[str] = None):
    return {"data" : limit}

@app.get("/blogs/unpublished")
def blog_id(id: int):
    return {"id": id, "data": {"name": "Tushar Singh", "age": 19}}

@app.get("/blogs/{id}")
def blog_id(id: int):
    return {"id": id, "data": {"name": "Tushar Singh", "age": 19}}

@app.get("/blogs/{id}/age")
def user_age(id: int):
    return {"id": id, "age": 19}
