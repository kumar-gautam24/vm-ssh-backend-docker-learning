from schemas import Common
from fastapi import APIRouter, Depends, Query,Path
from utils.crud import get_book_or_404
from sqlalchemy.orm import Session
from database import get_db
from models import Book
from schemas import BookCreate, BookResponse

from typing import Annotated

router = APIRouter(prefix="/books", tags=["books"])

BOOK_ID= Annotated[int,Path(min_length=1)]

# post route for the book 
@router.post("/",status_code=201, response_model=BookResponse)
def add_books(book:BookCreate,db:Session=Depends(get_db)):
   

    new_book = Book(**book.model_dump())
    db.add(new_book)
    db.commit()
    db.refresh(new_book)

    return new_book


# get books routes
@router.get("/",status_code=200,response_model=list[BookResponse])
def get_books(author:Annotated[str|None,Query(min_length=2)]=None,
search:Annotated[str|None,Query(min_length=2)]=None,
db:Session=Depends(get_db)
 ):
   
    query = db.query(Book)
    if author:
        query = query.filter(Book.author.ilike(f"%{author}%"))
    if search:
        query = query.filter(Book.title.ilike(f"%{search}%"))
    result = query.all() 

    return result


# get book by {id}
@router.get("/{book_id}", status_code=200,response_model=BookResponse)
def get_book_by_id(book_id:BOOK_ID, db:Session=Depends(get_db)):

    book= get_book_or_404(db,book_id)
    return book

# update a book
@router.put("/{book_id}", status_code=200,response_model=BookResponse)
def update_book_by_id(book_id:Annotated[int,Path(gt=0)],body:BookCreate,db:Session=Depends(get_db)):
    book= get_book_or_404(db,book_id)
    book.title = body.title
    book.author = body.author
    book.year = body.year
    book.price = body.price
    db.commit()
    db.refresh(book)
    return book
        
      
# delete a book
@router.delete("/{book_id}", status_code=200)
def delete_book_by_id(book_id:Annotated[int,Path(gt=0)],db:Session=Depends(get_db)):

    book= get_book_or_404(db,book_id)
    db.delete(book)
    db.commit()
    return {"message": "Book deleted"}



