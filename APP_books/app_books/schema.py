from pydantic import BaseModel, Field
from typing import Optional


# -------- BOOK --------
class BookBase(BaseModel):
    title: str
    author: str
    category: Optional[str] = None
    publication_year: Optional[int] = None

class BookCreate(BookBase):
    pass

class Book(BookBase):
    id: int

    class Config:
        orm_mode = True


# -------- USER --------
class UserBase(BaseModel):
    name: str
    username: str
    gender: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    connected: bool

    class Config:
        orm_mode = True
