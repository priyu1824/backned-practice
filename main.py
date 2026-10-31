from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from fastapi import Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from models import BookModel, UserModel
from security import hash_password, verify_password, create_access_token
from fastapi.security import OAuth2PasswordRequestForm


Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()

class Book(BaseModel):
    title: str
    author: str

class UserCreate(BaseModel):
    email: str
    password: str

books = {
    1: {"title": "Harry Potter", "author": "JK Rowling"},
    2: {"title": "Physics", "author": "H.C. Verma"},
}

@app.get("/books/{book_id}")
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(BookModel).filter(BookModel.id == book_id).first()
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@app.get("/books")
def list_books(author: str | None = None, db: Session = Depends(get_db)):
    query = db.query(BookModel)
    if author:
       query = query.filter(BookModel.author.ilike(f"%{author}%"))
    return query.all()

@app.post("/books", status_code=status.HTTP_201_CREATED)
def add_book(book: Book, db : Session = Depends(get_db)):
    new_book = BookModel(title= book.title, author= book.author)
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book

@app.put("/books/{book_id}")
def update_book(book_id: int, book: Book, db: Session = Depends(get_db)):
    existing = db.query(BookModel).filter(BookModel.id == book_id).first()
    if existing is None:
        raise HTTPException(status_code=404, detail="Book not found")
    existing.title = book.title
    existing.author = book.author
    db.commit()
    db.refresh(existing)
    return existing

@app.delete("/books/{book_id}", status_code=204)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    existing = db.query(BookModel).filter(BookModel.id == book_id).first()
    if existing is None:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(existing)
    db.commit()

@app.post("/register", status_code=status.HTTP_201_CREATED)
def user_create(user: UserCreate, db: Session= Depends(get_db)):
    existing = db.query(UserModel).filter(UserModel.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail= "User already exists")
    new_user = UserModel(email = user.email, hashed_password = hash_password(user.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"id": new_user.id, "email": new_user.email}

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.email == form_data.username).first()
    if user is None or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    return {"access_token": create_access_token(user.email), "token_type": "bearer"}


