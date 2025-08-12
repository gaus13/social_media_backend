from pydantic import BaseModel 

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True  #optional field by default its True

class PostCreate(PostBase):
    pass  #by writing this is automatically inherits all the things from base class



