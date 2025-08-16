from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from ..import database, schema, model, utils, oauth2

router = APIRouter(
    tags=['Authentication']
)

@router.post("/login")
def login(user_credentials: OAuth2PasswordRequestForm = Depends() , db: session = Depends(database.get_db)):
   
   user = db.query(model.User).filter(model.User.email == user_credentials.username).first()

   if not user:
      raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
   
   if not utils.verify(user_credentials.password, user.password):
      raise HTTPException(status_code=status.HTTP_403_FORBIDDEN , detail=f"Invalid Credentials")
   
# Create a Token
# Return token
   access_token = oauth2.create_access_token(data = {"user_id": user.id})   #here in data i am providing id as a payload it is upto me


   return {"access_token": access_token, "token_type": "bearer"}