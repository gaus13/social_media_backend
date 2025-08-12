from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor 
import time 
from . import model, schema
from .database import engine, get_db
from sqlalchemy.orm import Session


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


@app.get("/")
def root():
    return {"message" :"Hello World go go "}

@app.get("/posts")
def get_post(db: Session = Depends(get_db)):
    
        # cursor.execute("""SELECT * FROM posts """)  # lowercase if created normally, for uppercase in table name use double quotes 
        # posts = cursor.fetchall()
        posts = db.query(model.Post).all()
        return {"data": posts}
    
    # except Exception as e:
    #     conn.rollback()  # clears aborted transaction
    #     raise HTTPException(status_code=500, detail=str(e))


@app.post("/posts", status_code= status.HTTP_201_CREATED)
# body is from fastapi lib: it extracts and converts data in dict and stores in payload var(always structure routes)
def create_posts(new_post: schema.PostCreate, db: Session = Depends(get_db)):
    # cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (new_post.title, new_post.content, new_post.published))
    # saved_post = cursor.fetchone()
    # conn.commit() #done to save this into postgres
    saved_post = model.Post(**new_post.model_dump() )
    db.add(saved_post)
    db.commit()
    db.refresh(saved_post)
    return{"data": saved_post}



# fastapi code runs from top to bottom and if we but the one with id above tha latest route it will throw error.
@app.get("/posts/latest")
def get_latest_post():
    post = my_posts[len(my_posts)-1]
    return {"detail": post}


@app.get("/posts/{id}")
def get_post(id: int, response: Response, db: Session = Depends(get_db)):
    # path param is returned as string so we typecaste/changed into int: but in fastapi we set id: int and its done
    # cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (str(id)))
    # save = cursor.fetchone()
    save = db.query(model.Post).filter(model.Post.id == id).first()
    print(save)
    # new_post = find_post(id)

    if not save:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
        # other way (hard way to throw error)
        # response.status_code= status.HTTP_404_NOT_FOUND
        # return {"message": f"post with id: {id} was not found"}
    return{"post_detail": save}


@app.delete("/posts/{id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    # find the index in array that has req id and then delete
    # cursor.execute("""DELETE FROM posts WHERE id = %s returning * """, (str(id)))
    # recently_deleted = cursor.fetchone()
    # conn.commit()
    deleted_item =  db.query(model.Post).filter(model.Post.id == id)
    if deleted_item.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exist")

    #return Response(status_code=status.HTTP_204_NO_CONTENT) {if you want to return some message u need change status code}
    #  we don't want to send back any data while deleting so used above way: return {'message': "Post was successfully deleted"}
    deleted_item.delete(synchronize_session= False)
    db.commit()
    


@app.put("/posts/{id}", )
def update_post(id: int, new_post: schema.PostCreate, db: Session = Depends(get_db)):
     
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (
    #     new_post.title, new_post.content, new_post.published, str(id,)))
    
    # updated = cursor.fetchone()
    # conn.commit()
    
    post_query = db.query(model.Post).filter(model.Post.id == id)
    existing_post = post_query.first()
    if existing_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exist")
    
    post_query.update(new_post.model_dump(), synchronize_session= False)
    db.commit()
    return post_query.first()


# this is a orm way to interacting with the database
# @app.get("/sqlalchemy")
# def test_posts(db: Session = Depends(get_db)):

#     posts = db.query(model.Post).all()
#     return{"data": posts}