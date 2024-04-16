from __future__ import annotations

import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from . import crud
from . import schemas
from dependencies import DatabaseDependancy


router = APIRouter()


@router.get("/books/", response_model=list[schemas.Book])
async def read_books(
    db: DatabaseDependancy,
    title: str | None = None,
    publish_date: datetime.date | None = None,
    author_id: int | None = None,
):
    return await crud.get_books_list(
        db=db,
        title=title,
        publish_date=publish_date,
        author_id=author_id,
    )


@router.post("/books/", response_model=schemas.Book)
async def create_book(book: schemas.BookCreate, db: DatabaseDependancy):
    db_book = await crud.get_book_by_title(db=db, book_title=book.title)
    if db_book:
        raise HTTPException(
            status_code=422, detail="Book with such title exists."
        )
    return await crud.create_book(db=db, book=book)


@router.get("/books/{book_id}/", response_model=schemas.Book)
async def read_single_book(book_id: int, db: DatabaseDependancy):
    db_book = await crud.get_book(db=db, book_id=book_id)

    if not db_book:
        raise HTTPException(
            status_code=404, detail="Book with such params not found."
        )

    return db_book


@router.put("/books/{book_id}/", response_model=schemas.Book)
async def update_book_instance(
    book_id: int,
    book_update: schemas.BookUpdate,
    db: DatabaseDependancy,
) -> schemas.Book:
    updated_book = await crud.update_book(
        db=db, book_id=book_id, book_update=book_update
    )
    if not updated_book:
        raise HTTPException(
            status_code=404,
            detail="Book not found",
        )

    return updated_book


@router.delete("/books/{book_id}/")
async def delete_book(book_id: int, db: DatabaseDependancy):
    deleted = await crud.delete_book(db=db, book_id=book_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Book not found")

    return {"message": "Book deleted successfully"}
