from enum import Enum
from fastapi import Path
from fastapi import Query
from typing import Annotated
from pydantic import BaseModel, Field

class BookCreate(BaseModel):
    title:Annotated[str,Field(min_length=1,max_length=100)]
    author:Annotated[str,Field(min_length=1,max_length=100)]
    description:Annotated[str|None,Field(min_length=1,max_length=500)]=None
    tags:Annotated[list[str],Field(min_length=1,max_length=50)]=[]
    year:Annotated[int,Field(gt=1500,lt=2030)]
    price:Annotated[float,Field(ge=0)]


class BookResponse(BookCreate):
    id:int
    model_config = {"from_attributes": True}


class Common(Enum):
    book_id=Annotated[int,Path(min_length=1)]