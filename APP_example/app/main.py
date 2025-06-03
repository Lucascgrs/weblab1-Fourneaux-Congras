"""
from sqlalchemy.orm import Session

from . import models, schemas

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    # return db.query(models.User).offset(skip).limit(limit).all()
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(email=user.email,
                          name=user.name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_todos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Todo).offset(skip).limit(limit).all()

def create_user_todo(db: Session, todo: schemas.TodoCreate, user_id: int):
    db_todo = models.Todo(**todo.model_dump(), owner_id=user_id)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo
"""

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import crud, models, schema
from .database import SessionLocal, engine

from fastapi import FastAPI, Depends, HTTPException, Request, Form
from sqlalchemy.orm import Session

from . import crud, models, schema
from .database import SessionLocal, engine

from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/", response_model=schema.User)
def post_user(user: schema.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@app.get("/users/", response_model=list[schema.User])
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@app.get("/users/{user_id}", response_model=schema.User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.post("/users/{user_id}/todos/", response_model=schema.Todo)
def post_todo_for_user(user_id: int, todo: schema.TodoCreate, db: Session = Depends(get_db)):
    return crud.create_user_todo(db=db, todo=todo, user_id=user_id)

@app.get("/todos/", response_model=list[schema.Todo])
def get_todos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    todos = crud.get_todos(db, skip=skip, limit=limit)
    return todos

app.mount("/static", StaticFiles(directory="APP_example/public"), name="public")
templates = Jinja2Templates(directory="APP_example/app/templates")

@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse(request, "home.html")

@app.get("/basic")
def get_basic_form(request: Request):
    return templates.TemplateResponse("users_create.html", {"request": request})

@app.post("/basic")
async def post_basic_form(
    request: Request,
    formusername: str = Form(...),
    foremail: str = Form(...),
    db: Session = Depends(get_db)):
    print(f'username: {formusername}')
    print(f'email: {foremail}')

    db_user = crud.get_user_by_email(db, email=foremail)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = models.User(
        name=formusername, email=foremail
    )
    res = crud.create_user(db=db,user=user) 

    return templates.TemplateResponse("users_create.html", {"request": request})