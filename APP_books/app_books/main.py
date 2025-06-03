from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from . import crud, schema, models
from .database import SessionLocal, Base, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Fonction pour obtenir la session de base de données
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -------- USERS --------
@app.post("/users/create_user", response_model=schema.User)
def create_user(new_user: schema.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, new_user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    return crud.create_user(db=db, user=new_user)

@app.post("/users/login", response_model=schema.User)
def login(username: str, password: str, db: Session = Depends(get_db)):
    user = crud.login_user(db=db, username=username, password=password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    return user

@app.get("/users", response_model=List[schema.User])
def get_all_users(db: Session = Depends(get_db)):
    return crud.get_users(db)

@app.get("/users/{user_id}", response_model=schema.User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# -------- BOOKS --------
@app.get("/books", response_model=List[schema.Book])
def get_all_books(db: Session = Depends(get_db)):
    return crud.get_books(db)

@app.get("/books/{book_id}", response_model=schema.Book)
def get_book(book_id: int, db: Session = Depends(get_db)):
    db_book = crud.get_book(db, book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book

@app.post("/books/create_book", response_model=schema.Book)
def create_book(new_book: schema.BookCreate, db: Session = Depends(get_db)):
    return crud.create_book(db=db, book=new_book)

@app.put("/books/update_book/{book_id}", response_model=schema.Book)
def update_book(book_id: int, updated_book: schema.BookCreate, db: Session = Depends(get_db)):
    db_book = crud.update_book(db, book_id, updated_book)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book

@app.delete("/books/delete_book/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    if crud.delete_book(db, book_id):
        return {"message": f"Book with id {book_id} has been deleted"}
    raise HTTPException(status_code=404, detail="Book not found")
