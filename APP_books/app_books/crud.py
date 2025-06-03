from sqlalchemy.orm import Session
from . import models, schema
import hashlib


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


# -------- USERS --------
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_users(db: Session):
    return db.query(models.User).all()

def create_user(db: Session, user: schema.UserCreate):
    db_user = models.User(
        name=user.name,
        username=user.username,
        password=hash_password(user.password),
        gender=user.gender,
        connected=False
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def login_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)
    if user and user.password == hash_password(password):
        user.connected = True
        db.commit()
        db.refresh(user)
        return user
    return None

def disconnect_user(db: Session, username: str):
    user = get_user_by_username(db, username)
    if user and user.connected:
        user.connected = False
        db.commit()
        db.refresh(user)
        return user
    return None

def update_user(db: Session, user_id: int, updated_user: schema.UserCreate):
    db_user = get_user(db, user_id)
    if db_user:
        db_user.name = updated_user.name
        db_user.username = updated_user.username
        db_user.gender = updated_user.gender
        db_user.password = hash_password(updated_user.password)
        db.commit()
        db.refresh(db_user)
        return db_user
    return None

def delete_user(db: Session, user_id: int):
    db_user = get_user(db, user_id)
    if db_user:
        db.delete(db_user)
        db.commit()
        return True
    return False


# -------- BOOKS --------
def get_books(db: Session):
    return db.query(models.Book).all()

def get_book(db: Session, book_id: int):
    return db.query(models.Book).filter(models.Book.id == book_id).first()

def create_book(db: Session, book: schema.BookCreate):
    db_book = models.Book(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def update_book(db: Session, book_id: int, updated_book: schema.BookCreate):
    db_book = get_book(db, book_id)
    if db_book:
        for key, value in updated_book.dict().items():
            setattr(db_book, key, value)
        db.commit()
        db.refresh(db_book)
        return db_book
    return None

def delete_book(db: Session, book_id: int):
    db_book = get_book(db, book_id)
    if db_book:
        db.delete(db_book)
        db.commit()
        return True
    return False
