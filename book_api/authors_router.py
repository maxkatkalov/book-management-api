from __future__ import annotations

from fastapi import APIRouter, HTTPException

from . import crud
from . import schemas
from dependencies import DatabaseDependancy

router = APIRouter()


AUTHOR_NOT_FOUND = HTTPException(status_code=404, detail="Author not found")


@router.get("/authors/", response_model=list[schemas.AuthorList])
async def read_authors(db: DatabaseDependancy):
    return await crud.get_all_authors_instances(db)


@router.post("/authors/", response_model=schemas.AuthorList)
async def create_author(author: schemas.AuthorCreate, db: DatabaseDependancy):
    db_author = await crud.get_author_by_first_last_names(db=db, author=author)
    if db_author:
        raise HTTPException(
            status_code=422,
            detail="Author with such first name and last name exists",
        )
    return await crud.create_author(db=db, author=author)


@router.get("/authors/{author_id}/", response_model=schemas.AuthorList)
async def get_author(author_id: int, db: DatabaseDependancy):
    db_author = await crud.get_author_by_id(db=db, author_id=author_id)
    if not db_author:
        raise AUTHOR_NOT_FOUND

    return db_author


@router.put("/authors/{author_id}/")
async def update_author(
    author_id: int, db: DatabaseDependancy, author_update: schemas.AuthorUpdate
):
    updated_author = await crud.update_author(
        db=db,
        author_id=author_id,
        author_update=author_update,
    )
    if not updated_author:
        raise AUTHOR_NOT_FOUND

    return updated_author


@router.delete("/authors/{author_id}/")
async def delete_author(author_id: int, db: DatabaseDependancy):
    deleted_author = await crud.delete_author(db=db, author_id=author_id)
    if not deleted_author:
        raise AUTHOR_NOT_FOUND
    return {"message": "Author deleted successfully"}
