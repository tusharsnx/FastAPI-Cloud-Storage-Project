from fastapi import FastAPI

app = FastAPI()

@app.get("/index")
@app.get('/')
def index():
    return {"data" :"tushrh: <h1>tushar</h1>"}
