from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    username = Column(String(255), unique=True, index=True)
    password = Column(String(255))
    gender = Column(String(50))
    connected = Column(Boolean, default=False)

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True)
    author = Column(String(255))
    category = Column(String(255), nullable=True)
    publication_year = Column(Integer, nullable=True)
