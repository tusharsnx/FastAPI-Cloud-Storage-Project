from typing import List, Optional
from fastapi import Body, FastAPI, Query
from pydantic import BaseModel

app = FastAPI()

class Blogs(BaseModel):
    title: str = "10"
    body: str = "body"
    published_at: Optional[bool]

@app.get("/blogs")
@app.get('/')
def blogs(limit: int = 100, sort: Optional[str] = None):
    return {"data" : limit, "sort": sort}

@app.post("/blogs")
def create_blogs(blog: Blogs):
    return blog.title


@app.get("/search")
# need to explicit define q as query param or else default to body param due to q not being in [str, int, bool, float](singular types)
def search_blogs(q: List[str] = Query(..., deprecated=True, title="Tushar singh", description="Description")):
    results = {"q":q}
    return results

@app.get("/blogs/unpublished")
def blog_unpublished(id: int):
    return {"id": id, "data": {"name": "Tushar Singh", "age": 19}}

@app.get("/blogs/{id}")
def blog_users(id: int):
    return {"id": id, "data": {"name": "Tushar Singh", "age": 19}}

@app.get("/blogs/{id}/age")
def user_age(id: int):
    return {"id": id, "age": 19}
