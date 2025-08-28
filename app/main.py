from fastapi import FastAPI 
from . import model
from .database import engine
from .routers import posts, user, auth, vote
from .config import setting

model.Base.metadata.create_all(bind = engine)

app = FastAPI()

app.include_router(posts.router)
app.include_router(user.router)
app.include_router(vote.router)
app.include_router(auth.router)

@app.get("/")
def root():
    return {"message" :"Hello World go go "}
