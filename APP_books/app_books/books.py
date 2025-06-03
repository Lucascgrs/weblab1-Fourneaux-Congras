from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel, Field
from typing import List, Optional
import hashlib
 
 
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


class Book(BaseModel):
    id: Optional[int] = None
    title: str
    author: str
    category: Optional[str] = None
    publication_year: Optional[int] = None

class User:
    id: int
    name: str
    username: str
    password: str
    gender: str
    connected: bool = False
 
app = FastAPI()
books_db: List[Book] = []
users_db: List[User] = []
 
@app.get("/")
def read_root():
    return {"Hello": "World"}
 
@app.get("/api-endpoint")
def first_api():
    return {"message": "Hello"}
 
@app.get("/books")
async def read_all_books():
    all_books = [book for book in books_db]
    return all_books
 
@app.get("/books/{dynamic_param}")
async def read_all_books(dynamic_param):
    return {'dynamic_param': dynamic_param}
 
@app.get("books/mybook")
async def read_all_books():
    return {'book_title': 'My Favorite Book'}
 
@app.post("/books/create_book")
async def create_book(new_book: Book):
    new_book.id = len(books_db) + 1
    books_db.append(new_book)
    return {"message": "Book created successfully", "book": new_book}
 
@app.put("/books/update_book/{book_id}")
async def update_book(book_id: int, updated_book: Book):
    for i, book in enumerate(books_db):
        if book.id == book_id:
            updated_book.id = book_id
            books_db[i] = updated_book
            return{"message": f"Book with id {book_id} has been updated", "book": updated_book}
    raise HTTPException(status_code=404, detail=f"Book with id {book_id} not found")
 
@app.delete("/books/delete_book/{book_id}")
async def delete_book(book_id: int):
    for i, book in enumerate(books_db):
        if book.id == book_id:
            del books_db[i]
            return {"message": f"Book with id {book_id} has been deleted"}
    raise HTTPException(status_code=404, detail=f"Book with id {book_id} not found")
 
@app.patch("/books/patch/{book_id}")
async def patch_book(book_id: int, patch_data: Book):
    stored_book_data = None
    for book in books_db:
        if book.id == book_id:
            stored_book_data = book
            update_data = patch_data.dict(exclude_unset=True)
            updated_book = stored_book_data.copy(update=update_data)
            books_db[books_db.index(book)] = updated_book
            return {"message": f"Book with id {book_id} has been patched", "book": updated_book}
   
    if stored_book_data is None:
        raise HTTPException(status_code=404, detail=f"Book with id {book_id} not found")
    
@app.post("/users/create_user")
async def create_user(new_user: User):
    if any(user.username == new_user.username for user in users_db):
        raise HTTPException(status_code=400, detail="Username already exists")
    if len(new_user.password) < 8:
        raise HTTPException(status_code=400, detail="Password must be at least 8 characters long")
    new_user.hash_password()
    new_user.id = len(users_db) + 1
    users_db.append(new_user)
    return {"message": "User created successfully", "user": new_user}

@app.post("/users/login")
async def login(username: str, password: str):
    hashed_pw = hash_password(password)
    for user in users_db:
        if user.username == username and user.password == hashed_pw:
            user.connected = True
            return {"message": "Login successful", "user": user}
    raise HTTPException(status_code=401, detail="Invalid username or password")

@app.post("/users/disconnect")
async def disconnect(username: str):
    for user in users_db:
        if user.username == username and user.connected:
            user.connected = False
            return {"message": "Logout successful", "user": user}
    raise HTTPException(status_code=401, detail="Invalid username or already disconnected")


@app.get("/users")
async def get_all_users():
    all_users = [user for user in users_db]
    return all_users

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    for user in users_db:
        if user.id == user_id:
            return user
    raise HTTPException(status_code=404, detail=f"User with id {user_id} not found")

@app.put("/users/update_user/{user_id}")
async def update_user(user_id: int, updated_user: User):
    for i, user in enumerate(users_db):
        if user.id == user_id:
            updated_user.id = user_id
            users_db[i] = updated_user
            return {"message": f"User with id {user_id} has been updated", "user": updated_user}
    raise HTTPException(status_code=404, detail=f"User with id {user_id} not found")

@app.delete("/users/delete_user/{user_id}")
async def delete_user(user_id: int):
    for i, user in enumerate(users_db):
        if user.id == user_id:
            del users_db[i]
            return {"message": f"User with id {user_id} has been deleted"}
    raise HTTPException(status_code=404, detail=f"User with id {user_id} not found")
