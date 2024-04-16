from sqlalchemy import (
    Column,
    Integer,
    String,
    VARCHAR,
    ForeignKey,
    Date,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

from book_api import schemas
from database import Base


class DBAuthor(Base):
    __tablename__ = "author"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(VARCHAR(56), nullable=False)
    last_name = Column(VARCHAR(128), nullable=False, unique=True)

    __table_args__ = (
        UniqueConstraint("first_name", "last_name", name="uq_author_name"),
    )


class DBBook(Base):
    __tablename__ = "book"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(length=255), nullable=False, unique=True)
    description = Column(String(length=512), nullable=False)
    publish_date = Column(Date, nullable=False)
    author_id = Column(Integer, ForeignKey("author.id", ondelete="CASCADE"))
    ISBN = Column(VARCHAR(length=13))

    author = relationship(DBAuthor)
