from fastapi import FastAPI, HTTPException, status
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
    if book_id not in books:
        raise HTTPException(status_code=404, detail="Book not found")
    return books[book_id]

@app.get("/books")
def list_books(author: str | None = None):
    if author:
        return [b for b in books.values() if author.lower() in b["author"].lower()]
    return list(books.values())

@app.post("/books", status_code=status.HTTP_201_CREATED)
def add_book(book: Book):
    new_id = max(books, default=0)+1
    books[new_id] = book.model_dump()
    return {"id": new_id, **books[new_id]}

@app.put("/books/{book_id}")
def update_book(book_id: int, book: Book):
    if book_id not in books:
        raise HTTPException(status_code=404, detail="Book not found")
    books[book_id] = book.model_dump()
    return {"id":book_id, **books[book_id]}

@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int):
    if book_id not in books:
        raise HTTPException(status_code= 404, detail="Book not found")
    del books[book_id]
