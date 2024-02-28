from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

from typing import Annotated
from fastapi.staticfiles import StaticFiles
from fastapi import File, UploadFile

import os

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

IMAGEDIR = "./static/images/"

app.mount("/static", StaticFiles(directory="./static"), name="static")

origins = [
    "http://localhost:8080",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# functions

def get_files_name(path):
    for file in os.listdir(path):
        if os.path.isfile(os.path.join(path, file)):
            yield file


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/{user_id}/items/", response_model=schemas.Item)
def create_item_for_user(
    user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
):
    return crud.create_user_item(db=db, item=item, user_id=user_id)


@app.get("/items/", response_model=list[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items


# Upload Files to system archive
@app.post("/uploadfiles/")
async def create_upload_files(files: list[UploadFile]):
    # Read File
    for file in files:
        contents = await file.read()

        # Save File
        with open(f"{IMAGEDIR}{file.filename}", 'wb') as f:
            f.write(contents)

    #return {"filename": file.filename}
    return {"filenames": [file.filename for file in files]}

# Get Articles Title
@app.get("/Articles/")
async def get_Articles_title():
    list_titles = []
    titles = get_files_name(IMAGEDIR)
    for title in titles:
        title = title.removesuffix(".md")
        list_titles.append(title)
    
    return list_titles


# Get Article COntent

@app.get("/article")


# Upload file and store fileapth into database
@app.post("/users/{user_id}/articles/", response_model=schemas.Article)
def upload_article_for_user(
    user_id: int, article: schemas.ArticleCreate, db: Session = Depends(get_db)
):
    return crud.upload_user_articles(db=db, article=article, user_id=user_id)


    
