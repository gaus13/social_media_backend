from pydantic import BaseModel, EmailStr, conint
from datetime import datetime
from typing import Optional
from enum import Enum

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True  #optional field by default its True

class PostCreate(PostBase):  #inheriting postbase model 
    pass  #by writing this is automatically inherits all the things from base class

#this is a response model -> what we want the api to send back
class UserOut(BaseModel):
      id: int
      email: EmailStr
      class Config:
        from_attributes = True


# Response model
class PostResponse(PostBase):  #yahan jo likhoge wahi response mein milega
    id: int 
    created_at:datetime 
    owner_id: int
    owner: UserOut
    #  it tells Pydantic to work with ORM objects directly — not just plain Python dicts.
    class Config:
        orm_mode= True


class UserCreate(BaseModel):
            email: EmailStr   #this Emailstr import checks if the input email is valid
            password: str


class UserLogin(BaseModel):
     email: EmailStr
     password: str        

class Token(BaseModel):
        access_token : str
        token_type : str


class TokenData(BaseModel):
     id: Optional[int] = None  #str to int correction was made here


# validation for likes
class VoteDirection(int, Enum):
    unlike = 0   # remove like / dislike
    like = 1     # add like

class Vote(BaseModel):
    post_id: int
    direction: VoteDirection