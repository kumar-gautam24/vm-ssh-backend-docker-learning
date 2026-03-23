
from sqlalchemy.orm import Session
from models import Book
from fastapi import  HTTPException



def get_book_or_404(db: Session, book_id: int):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book
