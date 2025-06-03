from sqlalchemy.orm import Session

from . import models, schema

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    # return db.query(models.User).offset(skip).limit(limit).all()
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schema.UserCreate):
    db_user = models.User(email=user.email,
                          name=user.name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_todos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Todo).offset(skip).limit(limit).all()

def create_user_todo(db: Session, todo: schema.TodoCreate, user_id: int):
    db_todo = models.Todo(**todo.model_dump(), owner_id=user_id)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo
