from fastapi import FastAPI,Request,Response
from playground import User



app = FastAPI()


from typing import Optional

user: Optional[User] = None 

@app.get("/")
async def root ():
    return {"HEllO World"}




@app.get("/user")
async def get_user():
    if user is None:
        return {"message": "No user created yet"}
    return user.to_dict()


@app.post("/user")
async def create_user(request:Request,body:User):
    global user
    try:
        user = body
        return {"message": "Success"}
    except Exception as e:
        return {"error": str(e)}
