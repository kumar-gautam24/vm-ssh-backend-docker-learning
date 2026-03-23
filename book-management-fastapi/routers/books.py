from fastapi import APIRouter, Depends, HTTPException
from utils.crud import get_book_or_404
from sqlalchemy.orm import Session
from database import get_db
from models import Book
from schemas import BookCreate #BookResponse

router = APIRouter(prefix="/books", tags=["books"])



# post route for the book 
@router.post("/",status_code=201)
def add_books(book:BookCreate,db:Session=Depends(get_db)):
   

    new_book = Book(**book.model_dump())
    db.add(new_book)
    db.commit()
    db.refresh(new_book)

    return {
        "message": "Book Added Success",
        "Book":new_book
    }


# get books routes

@router.get("/",status_code=200)
def get_books(author:str|None=None,search:str|None=None, db:Session=Depends(get_db)):
   
    query = db.query(Book)
    if author:
        query = query.filter(Book.author.ilike(f"%{author}%"))
    if search:
        query = query.filter(Book.title.ilike(f"%{search}%"))
    result = query.all() 

    return {
        "books": result
    }


# get book by {id}

@router.get("/{book_id}", status_code=200,)
def get_book_by_id(book_id:int, db:Session=Depends(get_db)):

    book= get_book_or_404(db,book_id)
    return book

# update a book
@router.put("/{book_id}", status_code=200)
def update_book_by_id(book_id:int,body:BookCreate,db:Session=Depends(get_db)):
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
def delete_book_by_id(book_id:int,db:Session=Depends(get_db)):

    book= get_book_or_404(db,book_id)
    db.delete(book)
    db.commit()
    return {"message": "Book deleted"}



