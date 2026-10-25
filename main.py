from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Book(BaseModel):
    title: str
    author: str

books = {
    1: {"title": "Harry Potter", "author": "JK Rowling"},
    2: {"title": "Physics", "author": "H.C. Verma"},
}

@app.get("/books/{book_id}")
def get_book(book_id: int):
    return books.get(book_id, {"error": "Book not found"})

@app.get("/books")
def list_books(author: str | None = None):
    if author:
        return [b for b in books.values() if author.lower() in b["author"].lower()]
    return list(books.values())

@app.post("/books")
def add_book(book: Book):
    new_id = max(books)+1
    books[new_id] = book.model_dump()
    return {"id": new_id, **books[new_id]}
