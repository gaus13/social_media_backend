from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor 
import time 
from . import model, schema , utils
from .database import engine, get_db
from sqlalchemy.orm import Session
from .routers import posts, user


model.Base.metadata.create_all(bind = engine)

app = FastAPI()


while True:

  try:
    # hardcoding DB info here is a big problem 
    conn = psycopg2.connect(host= 'localhost', database = 'fastapi data',
                             user = 'postgres', password = 'Gulam@123', cursor_factory= RealDictCursor)
    cursor = conn.cursor()
    print("Database connection was successful")
    break  # exits from the infinite loop 

  except Exception as error:
    print("connection to Database failed")
    print("Error: ", error)
    time.sleep(3)

my_posts = [{"title": "title of post 1", "content": "Content of post 1", "id":1}, {"title":"Favourite food", "content":"I love pizza", "id": 2}]    

def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p

def find_index_id(id):
    for i , p in enumerate(my_posts):
        if p['id'] == id:
            return i
    return None    

app.include_router(posts.router)
app.include_router(user.router)

@app.get("/")
def root():
    return {"message" :"Hello World go go "}
