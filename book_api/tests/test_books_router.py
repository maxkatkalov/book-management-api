import datetime

import pytest
from fastapi.testclient import TestClient
from faker import Faker
from httpx import AsyncClient


from book_api.schemas import BookCreate
from book_api import crud
from book_api.main import app
from database import SessionLocal
from .test_authors_router import create_author_instance


client: TestClient = TestClient(app)
fake: Faker = Faker()

TEST_PUBLISH_DATE: datetime.date = datetime.date(2023, 12, 1)
TEST_TITLE: str = "Titanik"
TEST_DESCRIPTION: str = "Cool film"
TEST_ISBN: str = str(range(1, 14))


async def create_book_instance(
    db,
    title: str = None,
    description: str = None,
    author_id: int = None,
    publish_date: datetime.date = None,
    ISBN: str = None,
):
    if not author_id:
        author_instance = create_author_instance(db=db)
        author_db = await author_instance.__anext__()
        author_id = author_db.id

    book_data = BookCreate(
        title=" ".join(fake.words(nb=3)),
        description="\n".join(fake.paragraphs()),
        publish_date=fake.date(),
        author_id=author_id,
        ISBN=fake.words(nb=1)[0],
    )
    if title:
        book_data.title = title
    if description:
        book_data.description = description
    if author_id:
        book_data.author_id = author_id
    if description:
        book_data.description = description
    if ISBN:
        book_data.ISBN = ISBN
    if publish_date:
        book_data.publish_date = publish_date

    new_book = await crud.create_book(db=db, book=book_data)

    db.add(new_book)
    await db.commit()
    await db.refresh(new_book)

    yield new_book

    await crud.delete_author(db=db, author_id=author_id)


@pytest.mark.asyncio
async def test_get_all_books():
    async with SessionLocal() as db:
        async with AsyncClient(app=app, base_url="http://") as ac:
            response = await ac.get("/books/")
            assert response.status_code == 200
            assert len(response.json()) == 0

        instance1 = create_book_instance(db)
        await instance1.__anext__()

        async with AsyncClient(app=app, base_url="http://") as ac:
            response = await ac.get("/books/")
            assert response.status_code == 200
            assert len(response.json()) == 1

        try:
            await instance1.__anext__()
        except StopAsyncIteration:
            pass


@pytest.mark.asyncio
async def test_post_book():
    async with SessionLocal() as db:
        instance1 = create_author_instance(db)
        author = await instance1.__anext__()
        book_data = {
            "title": " ".join(fake.words(nb=3)),
            "description": "\n".join(fake.paragraphs()),
            "publish_date": fake.date(),
            "author_id": author.id,
            "ISBN": fake.words(nb=1)[0],
        }

        async with AsyncClient(app=app, base_url="http://") as ac:
            response = await ac.post("/books/", json=book_data)
            response_duplicate = await ac.post("/books/", json=book_data)
            response_json = response.json()

            db_book = await crud.get_book(
                db=db, book_id=response_json.get("id")
            )

            assert response.status_code == 200
            assert len(response.json()) == 6
            assert response_json == {
                "title": book_data.get("title"),
                "description": book_data.get("description"),
                "publish_date": book_data.get("publish_date"),
                "author_id": response_json.get("author_id"),
                "ISBN": response_json.get("ISBN"),
                "id": db_book.id,
            }
            assert db_book is not False

            assert response_duplicate.status_code == 422

            try:
                await instance1.__anext__()
            except StopAsyncIteration:
                pass


@pytest.mark.asyncio
async def test_get_book_id():
    async with SessionLocal() as db:
        async with AsyncClient(app=app, base_url="http://") as ac:
            instance1 = create_book_instance(db)
            db_book = await instance1.__anext__()

            response_сorrect = await ac.get(f"/books/{db_book.id}/")
            response_not_found = await ac.get(f"/books/{db_book.id + 1}/")
            assert response_сorrect.status_code == 200
            assert response_сorrect.json() == {
                "title": db_book.title,
                "description": db_book.description,
                "publish_date": str(db_book.publish_date),
                "author_id": db_book.author_id,
                "ISBN": db_book.ISBN,
                "id": db_book.id,
            }
            assert response_not_found.status_code == 404
            assert response_not_found.json() == {
                "detail": "Book with such params not found."
            }

        try:
            await instance1.__anext__()
        except StopAsyncIteration:
            pass


@pytest.mark.parametrize(
    (
        "title_to_update, "
        "description_to_update, "
        "publish_date_to_update, "
        "ISBN_to_update, "
        "title_after_update, "
        "description_after_update, "
        "publish_date_after_update, "
        "ISBN_after_update, "
    ),
    [
        (
            "Terminator",
            None,
            None,
            None,
            "Terminator",
            TEST_DESCRIPTION,
            TEST_PUBLISH_DATE,
            TEST_ISBN,
        ),
        (
            None,
            "test description",
            None,
            None,
            TEST_TITLE,
            "test description",
            TEST_PUBLISH_DATE,
            TEST_ISBN,
        ),
        (
            None,
            None,
            datetime.date(2002, 2, 2),
            None,
            TEST_TITLE,
            TEST_DESCRIPTION,
            datetime.date(2002, 2, 2),
            TEST_ISBN,
        ),
        (
            None,
            None,
            None,
            "NRC1313",
            TEST_TITLE,
            TEST_DESCRIPTION,
            TEST_PUBLISH_DATE,
            "NRC1313",
        ),
        (
            "Terminator",
            "test description",
            datetime.date(2002, 2, 2),
            "NRC1313",
            "Terminator",
            "test description",
            datetime.date(2002, 2, 2),
            "NRC1313",
        ),
        (
            None,
            None,
            None,
            None,
            TEST_TITLE,
            TEST_DESCRIPTION,
            TEST_PUBLISH_DATE,
            TEST_ISBN,
        ),
    ],
    # ids=[
    #     "Update book only with first name.",
    #     "Update book only with last name.",
    #     "Update book with new first and last name.",
    #     "No update for book.",
    # ]
)
@pytest.mark.asyncio
async def test_update_author(
    title_to_update: str,
    description_to_update: str,
    ISBN_to_update: str,
    publish_date_to_update: datetime.date,
    title_after_update: str,
    description_after_update: str,
    publish_date_after_update: datetime.date,
    ISBN_after_update: str,
    title=TEST_TITLE,
    description=TEST_DESCRIPTION,
    publish_date=TEST_PUBLISH_DATE,
    ISBN=TEST_ISBN,
):
    async with SessionLocal() as db:
        instance1 = create_author_instance(db)
        author = await instance1.__anext__()
        async with AsyncClient(app=app, base_url="http://") as ac:
            instance2 = create_book_instance(
                db=db,
                title=title,
                description=description,
                publish_date=publish_date,
                ISBN=ISBN,
                author_id=author.id,
            )
            db_book = await instance2.__anext__()

            update_data = {}
            if title_to_update:
                update_data["title"] = title_to_update
            if description_to_update:
                update_data["description"] = description_to_update
            if publish_date_to_update:
                update_data["publish_date"] = str(publish_date_to_update)
            if ISBN_to_update:
                update_data["ISBN"] = ISBN_to_update

            response = await ac.put(f"/books/{db_book.id}/", json=update_data)
            response_json = response.json()

            assert response.status_code == 200
            assert response_json.get("title") == title_after_update
            assert response_json.get("description") == description_after_update
            assert response_json.get("publish_date") == str(
                publish_date_after_update
            )
            assert response_json.get("ISBN") == ISBN_after_update

            try:
                await instance1.__anext__()
            except StopAsyncIteration:
                pass


@pytest.mark.asyncio
async def test_delete_book():
    async with SessionLocal() as db:
        async with AsyncClient(app=app, base_url="http://") as ac:
            instance1 = create_book_instance(db=db)
            book = await instance1.__anext__()

            response = await ac.delete(f"/books/{book.id}/")
            response_not_found = await ac.delete(f"/books/{book.id + 1}/")

            db_author = await crud.get_book(db=db, book_id=book.id)

            assert response.status_code == 200
            assert response_not_found.status_code == 404
            assert db_author is None

        try:
            await instance1.__anext__()
        except StopAsyncIteration:
            pass
