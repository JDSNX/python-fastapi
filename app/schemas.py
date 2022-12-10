from pydantic import BaseModel, EmailStr, conint
from typing import Optional
from datetime import datetime


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    
class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class PostBase(BaseModel):
    title: str
    content: str
    published: bool=True

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    created_at: datetime
    user_id: int
    user: UserOut

    class Config:
        orm_mode = True

class PostOut(BaseModel):
    Posts: Post
    votes: int

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str]=None

class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)
