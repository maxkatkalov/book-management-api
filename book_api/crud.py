import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, Any

from book_api import schemas
from book_api import models


async def get_all_authors_instances(db: AsyncSession):
    query = select(models.DBAuthor)
    authors = await db.execute(query)

    return authors.scalars().all()


async def get_author_by_first_last_names(
    db: AsyncSession, author: schemas.AuthorCreate
):
    query = select(models.DBAuthor).filter(
        models.DBAuthor.last_name == author.last_name
        and models.DBAuthor.first_name == author.first_name
    )
    author = await db.execute(query)

    return author.scalar_one_or_none()


async def get_author_by_id(db: AsyncSession, author_id: int):
    query = select(models.DBAuthor).filter(models.DBAuthor.id == author_id)
    author = await db.execute(query)

    return author.scalar_one_or_none()


async def create_author(db: AsyncSession, author: schemas.AuthorCreate):
    db_author = models.DBAuthor(**author.model_dump())
    db.add(db_author)

    await db.commit()
    await db.refresh(db_author)

    return db_author


async def update_author(
    db: AsyncSession, author_id: int, author_update: schemas.AuthorUpdate
):
    db_author = await get_author_by_id(db=db, author_id=author_id)
    if not db_author:
        return False

    for key, value in author_update.model_dump().items():
        if value:
            setattr(db_author, key, value)

    await db.commit()
    await db.refresh(db_author)

    return db_author


async def delete_author(db: AsyncSession, author_id: int):
    db_author = await get_author_by_id(db=db, author_id=author_id)
    if db_author:
        await db.delete(db_author)
        await db.commit()
        return True

    return False


async def get_books_list(
    db: AsyncSession,
    title: str = None,
    publish_date: datetime.date = None,
    author_id: int = None,
):
    query = select(models.DBBook)

    if title:
        query = query.filter(models.DBBook.title == title)
    if publish_date:
        query = query.filter(models.DBBook.publish_date == publish_date)
    if author_id:
        query = query.filter(models.DBBook.author_id == author_id)

    authors = await db.execute(query)

    return authors.scalars().all()


async def get_book(db: AsyncSession, book_id: int):
    query = select(models.DBBook).filter(models.DBBook.id == book_id)
    db_book = await db.execute(query)

    return db_book.scalar_one_or_none()


async def get_book_by_title(db: AsyncSession, book_title: str):
    query = select(models.DBBook).filter(models.DBBook.title == book_title)
    result = await db.execute(query)
    db_book = result.scalar_one_or_none()

    if db_book:
        return True

    return False


async def create_book(db: AsyncSession, book: schemas.BookCreate):
    db_book = models.DBBook(**book.model_dump())
    db.add(db_book)

    await db.commit()
    await db.refresh(db_book)

    return db_book


async def update_book(
    db: AsyncSession,
    book_id: int,
    book_update: schemas.BookUpdate,
):
    db_book = await get_book(db=db, book_id=book_id)
    if not db_book:
        return False

    for key, value in book_update.model_dump().items():
        if value:
            setattr(db_book, key, value)

    await db.commit()
    await db.refresh(db_book)

    return db_book


async def delete_book(db: AsyncSession, book_id: int):
    db_book = await get_book(db=db, book_id=book_id)
    if db_book:
        await db.delete(db_book)
        await db.commit()
        return True

    return False
