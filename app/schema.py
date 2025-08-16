from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True  #optional field by default its True

class PostCreate(PostBase):  #inheriting postbase model 
    pass  #by writing this is automatically inherits all the things from base class

# Response model
class PostResponse(PostBase):  #yahan jo likhoge wahi response mein milega
    id: int 
    created_at:datetime 
    #  it tells Pydantic to work with ORM objects directly — not just plain Python dicts.
    class Config:
        orm_mode= True


class UserCreate(BaseModel):
            email: EmailStr   #this Emailstr import checks if the input email is valid
            password: str

#this is a response model -> what we want the api to send back
class UserOut(BaseModel):
      id: int
      email: EmailStr
      class Config:
        orm_mode= True

class UserLogin(BaseModel):
     email: EmailStr
     password: str        

class Token(BaseModel):
        access_token : str
        token_type : str


class TokenData(BaseModel):
     id: Optional[str] = None
