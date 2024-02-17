from typing import Optional

from fastapi import FastAPI, Body
from pydantic import BaseModel, Field

app = FastAPI()


class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int

    def __init__(self, id, title, author, description, rating):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating


class BookRequest(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=-1, lt=6)

    class Config:
        json_schema_extra ={
            'example':{
            'title': 'A new book',
            'author':'codingwithroby',
            'description': 'A new description of a book',
            'rating': 5
            }
        }

BOOKS = [
      Book(1, 'Computer Science Pro', 'codingwithroby',  'A very nice book!', 5),
      Book(2, 'Be Fast with FastAPI', 'codingwithroby',  'A great book!', 5),
      Book(3, 'Master Endpoint', 'codingwithroby',  'An awesome book!', 5),
      Book(4, 'HP1', 'Author 1',  'Book description', 2),
      Book(5, 'HP2', 'Author 2',  'Book description', 3),
      Book(6, 'HP3', 'Author 3',  'Book description', 1)

]


@app.get("/books")
async def read_all_books():
    return BOOKS


@app.get("/books/{book_id}")
async def read_book(book_id: int):
    for book in BOOKS:
        if book_id == book.id:
            return book


@app.get("/books/")
async def read_book_by_rating(book_rating: int):
    books_to_return = []
    for book in BOOKS:
        if book.rating == book_rating:
            books_to_return.append(book)
    return books_to_return


@app.post("/create-book")
async def create_book(book_quest: BookRequest):
    new_book = Book(**book_quest.model_dump())
    BOOKS.append(find_book_id(new_book))


def find_book_id(book: Book):
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book


@app.put("/books/update_book")
async def update_book(book: BookRequest):
    for i in range(len(BOOKS)):
            if BOOKS[i].id == book.id:
                BOOKS[i] = book

@app.delete("/books/{book_id}")
async def delete_book(book_id: int):
        for i in range(len(BOOKS)):
            if BOOKS[i].id == book_id:
                BOOKS.pop(i)
                break