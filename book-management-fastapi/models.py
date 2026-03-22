from sqlalchemy import String, Integer, Float
from sqlalchemy.orm import Mapped, mapped_column
from database import Base


class Book(Base):
    __tablename__="books"

    id: Mapped[int]= mapped_column(Integer,primary_key=True,index=True)
    title:Mapped[str]=mapped_column(String(100),nullable=False)
    author:Mapped[str]=mapped_column(String(100),nullable=False)
    year:Mapped[int]=mapped_column(Integer,nullable=False)
    price:Mapped[float]=mapped_column(Float,nullable=False)