from fastapi import HTTPException
from fastapi import FastAPI
from pydantic import BaseModel

book_id :int =0

class Book(BaseModel):
    id:int=0
    title:str
    author:str
    year:int
    price: float

    


books = []

def main():
    print("Hello from book-management-fastapi!")


if __name__ == "__main__":
    main()


app = FastAPI()


# root operations
@app.get("/")
async def root():
    return {"message":"Hello World"}


# check server health
@app.get('/health')
async def server_health():
    return {
        "status":"ok",
        "version":"1.0.0"
    }


# post route for the book 
@app.post("/books",status_code=201)
async def add_books(book:Book):
    global book_id
    book.id=book_id
    book_id+=1
    books.append(book)
    return {
        "message": "Book Added Success"
    }


# get books routes

@app.get("/books",status_code=200)
async def get_books():

    return {
        "message":"Booked fetched successfully",
        "Books": books
    }


# get book by {id}

@app.get("/books/{book_id}", status_code=200)
async def get_book_by_id(book_id:int):
    book = [book for book in books if book_id == book.id]

    if len(book)==0:
        raise HTTPException(status_code=404,detail="Book not found")

    return {
        "message":"found books",
        "book":book
    }

# update a book
@app.put("/books/{book_id}", status_code=200)
async def update_book_by_id(book_id:int,body:Book):

    for i,book in enumerate(books) :
        if book_id==book.id:
            body.id = book_id
            books[i]=body
            return {
        "message":"Updated book",
        "book":body
    }
      
           
    raise HTTPException(status_code=404,detail="Book not found")


# delete a book

@app.delete("/books/{book_id}", status_code=200)
async def delete_book_by_id(book_id:int):

    for i,book in enumerate(books) :
        if book_id==book.id:
            books.remove(book)
            return {
        "message":"Deleted book",
        
    }
      
           
    raise HTTPException(status_code=404,detail="Book not found")