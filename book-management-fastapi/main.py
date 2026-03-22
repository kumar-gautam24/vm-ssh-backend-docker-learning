from database import get_db
from fastapi import Depends
from fastapi import HTTPException
from fastapi import FastAPI
from sqlalchemy.orm import Session
from database import engine
import models
from models import Book
from schemas import BookCreate,BookResponse




def main():
    print("Hello from book-management-fastapi!")


if __name__ == "__main__":
    main()


app = FastAPI()
models.Base.metadata.create_all(bind=engine)



# root operations
@app.get("/")
def root():
    return {"message":"Hello World"}


# check server health
@app.get('/health')
def server_health():
    return {
        "status":"ok",
        "version":"1.0.0"
    }


# post route for the book 
@app.post("/books",status_code=201)
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

@app.get("/books",status_code=200)
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

@app.get("/books/{book_id}", status_code=200,)
def get_book_by_id(book_id:int, db:Session=Depends(get_db)):

    book = db.query(Book).filter(Book.id==book_id).first()
    if  book :
        return book
    

    raise HTTPException(status_code=404, detail="Book not found")

# update a book
@app.put("/books/{book_id}", status_code=200)
def update_book_by_id(book_id:int,body:BookCreate,db:Session=Depends(get_db)):
    book = db.query(Book).filter(Book.id==book_id).first()
    if book:
        book.title = body.title
        book.author = body.author
        book.year = body.year
        book.price = body.price
        db.commit()
        db.refresh(book)
        return book
        
      
           
    raise HTTPException(status_code=404,detail="Book not found")


# delete a book

@app.delete("/books/{book_id}", status_code=200)
def delete_book_by_id(book_id:int,db:Session=Depends(get_db)):

    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404,detail="Book not found")
    db.delete(book)
    db.commit()
    return {"message": "Book deleted"}



