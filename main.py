from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from fastapi import Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models import BookModel

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
