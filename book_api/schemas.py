import datetime
from datetime import date
from typing import Optional

from pydantic import BaseModel


class AuthorBase(BaseModel):
    first_name: str
    last_name: str


class AuthorCreate(AuthorBase):
    pass


class AuthorUpdate(AuthorBase):
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class AuthorList(AuthorBase):
    id: int

    class Config:
        from_attributes = True


class BookBase(BaseModel):
    title: str
    description: str
    publish_date: datetime.date
    author_id: int
    ISBN: Optional[str]


class BookCreate(BookBase):
    pass


class BookUpdate(BookBase):
    title: Optional[str] = None
    description: Optional[str] = None
    publish_date: Optional[datetime.date] = None
    author_id: Optional[int] = None
    ISBN: Optional[str] = None


class Book(BookBase):
    id: int

    class Config:
        from_attributes = True
