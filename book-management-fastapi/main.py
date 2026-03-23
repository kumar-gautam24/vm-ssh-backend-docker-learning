from routers.books import router as books_router
from fastapi import FastAPI

from database import engine
import models


app = FastAPI()
models.Base.metadata.create_all(bind=engine)
app.include_router(books_router)



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


