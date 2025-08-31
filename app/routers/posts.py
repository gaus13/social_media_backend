from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy.orm import Session
from sqlalchemy import func
from .. import model, schema, oauth2
from ..database import get_db
from typing import List, Optional

router = APIRouter(
    prefix="/posts", #reduces repetition of writing post in endpoint url
    tags=['Posts']
)

@router.get("/", response_model= List[schema.PostOutVote])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),
               limit: int = 10, skip: int = 0, search: Optional[str]= ""):  #if you want to add space in qparam add %20
    
        # cursor.execute("""SELECT * FROM posts """)  # lowercase if created normally, for uppercase in table name use double quotes 
        # posts = cursor.fetchall()
        # posts = db.query(model.Post).filter(model.Post.title.contains(search)).limit(limit).offset(skip).all()  #this was before we added votes feature

       posts = db.query(model.Post, func.count(model.Vote.post_id).label("votes")).join(
            model.Vote, model.Vote.post_id == model.Post.id, isouter = True).group_by(model.Post.id).filter(model.Post.title.contains(search)).limit(limit).offset(skip).all()
       return posts

    # except Exception as e:
    #     conn.rollback()  # clears aborted transaction
    #     raise HTTPException(status_code=500, detail=str(e))


@router.post("/", status_code= status.HTTP_201_CREATED, response_model=schema.PostResponse)
# body is from fastapi lib: it extracts and converts data in dict and stores in payload var(always structure routes)
def create_posts(new_post: schema.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (new_post.title, new_post.content, new_post.published))
    # saved_post = cursor.fetchone()
    # conn.commit() #done to save this into postgres
    saved_post = model.Post(owner_id = current_user.id, **new_post.model_dump() )
    db.add(saved_post)
    db.commit()
    db.refresh(saved_post)
    return  saved_post



# fastapi code runs from top to bottom and if we but the one with id above tha latest route it will throw error.
@router.get("/latest", response_model=schema.PostResponse)
def get_latest_post(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    latest_post = db.query(model.Post).order_by(model.Post.id.desc()).first()
    if not latest_post:
        raise HTTPException(status_code=404, detail="No posts found")
    return latest_post


@router.get("/{id}", response_model=schema.PostOutVote)
def get_post(id: int, response: Response, db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    # path param is returned as string so we typecaste/changed into int: but in fastapi we set id: int and its done
    # cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (str(id)))
    # save = cursor.fetchone()
    # save = db.query(model.Post).filter(model.Post.id == id).first()
    
    save = db.query(model.Post, func.count(model.Vote.post_id).label("votes")).join(
            model.Vote, model.Vote.post_id == model.Post.id, isouter = True).group_by(model.Post.id).filter(model.Post.id == id).first()


    # new_post = find_post(id)
    if not save:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
        # other way (hard way to throw error)
        # response.status_code= status.HTTP_404_NOT_FOUND
        # return {"message": f"post with id: {id} was not found"}
    return save


@router.delete("/{id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):
    # find the index in array that has req id and then delete
    # cursor.execute("""DELETE FROM posts WHERE id = %s returning * """, (str(id)))
    # recently_deleted = cursor.fetchone()
    # conn.commit()
    deleted_item =  db.query(model.Post).filter(model.Post.id == id)
    
    delete = deleted_item.first()

    if delete == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exist")
    
    if delete.owner_id != current_user.id:
       raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform this action ")

    #return Response(status_code=status.HTTP_204_NO_CONTENT) {if you want to return some message u need change status code}
    #  we don't want to send back any data while deleting so used above way: return {'message': "Post was successfully deleted"}
    deleted_item.delete(synchronize_session= False)
    db.commit()
    


@router.put("/{id}", response_model= schema.PostResponse )
def update_post(id: int, new_post: schema.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
     
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (
    #     new_post.title, new_post.content, new_post.published, str(id,)))
    
    # updated = cursor.fetchone()
    # conn.commit()
    
    post_query = db.query(model.Post).filter(model.Post.id == id)
    existing_post = post_query.first()

    if existing_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exist")
    
    if existing_post.owner_id != current_user.id:
       raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform this action ")


    post_query.update(new_post.model_dump(), synchronize_session= False)
    db.commit()
    return post_query.first()


# this is a orm way to interacting with the database
# @app.get("/sqlalchemy")
# def test_posts(db: Session = Depends(get_db)):

#     posts = db.query(model.Post).all()
#     return{"data": posts} 
