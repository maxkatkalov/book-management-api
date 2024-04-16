import pytest
from fastapi.testclient import TestClient
from faker import Faker
from httpx import AsyncClient


from book_api.schemas import AuthorCreate
from book_api import crud
from book_api.main import app
from database import SessionLocal


client = TestClient(app)
fake = Faker()


async def create_author_instance(
    db, first_name: str = None, last_name: str = None
):
    author_data = AuthorCreate(
        first_name=fake.first_name(), last_name=fake.last_name()
    )
    if first_name:
        author_data.first_name = first_name
    if last_name:
        author_data.last_name = last_name

    new_author = await crud.create_author(db=db, author=author_data)

    db.add(new_author)
    await db.commit()
    await db.refresh(new_author)

    yield new_author

    await crud.delete_author(db=db, author_id=new_author.id)


@pytest.mark.asyncio
async def test_get_all_authors():
    async with SessionLocal() as db:
        async with AsyncClient(app=app, base_url="http://") as ac:
            response = await ac.get("/authors/")
            assert response.status_code == 200
            assert len(response.json()) == 0

        instance1 = create_author_instance(db)
        await instance1.__anext__()

        async with AsyncClient(app=app, base_url="http://") as ac:
            response = await ac.get("/authors/")
            assert response.status_code == 200
            assert len(response.json()) == 1

        try:
            await instance1.__anext__()
        except StopAsyncIteration:
            pass


@pytest.mark.asyncio
async def test_post_author():
    author_data = {
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
    }

    async with SessionLocal() as db:
        async with AsyncClient(app=app, base_url="http://") as ac:
            response = await ac.post("/authors/", json=author_data)
            response_duplicate = await ac.post("/authors/", json=author_data)
            response_json = response.json()
            response_duplicate_json = response.json()

            db_author = await crud.get_author_by_id(
                db=db, author_id=response_json.get("id")
            )

            assert response.status_code == 200
            assert len(response.json()) == 3
            assert response_json == {
                "first_name": author_data.get("first_name"),
                "last_name": author_data.get("last_name"),
                "id": response_json.get("id"),
            }
            assert db_author is not False

            assert response_duplicate.status_code == 422

            await crud.delete_author(db=db, author_id=response_json.get("id"))


@pytest.mark.asyncio
async def test_get_author_id():
    async with SessionLocal() as db:
        async with AsyncClient(app=app, base_url="http://") as ac:
            instance1 = create_author_instance(db)
            author = await instance1.__anext__()

            response_сorrect = await ac.get(f"/authors/{author.id}/")
            response_not_found = await ac.get(f"/authors/{author.id + 1}/")
            assert response_сorrect.status_code == 200
            assert response_сorrect.json() == {
                "first_name": author.first_name,
                "last_name": author.last_name,
                "id": author.id,
            }
            assert response_not_found.status_code == 404
            assert response_not_found.json() == {"detail": "Author not found"}

        try:
            await instance1.__anext__()
        except StopAsyncIteration:
            pass


@pytest.mark.parametrize(
    "first_name_to_update, last_name_to_update, first_name_after_update, last_name_after_update",
    [
        (
            "J. K.",
            None,
            "J. K.",
            "Wick",
        ),
        (
            None,
            "Rowling",
            "John",
            "Rowling",
        ),
        (
            "J. K.",
            "Rowling",
            "J. K.",
            "Rowling",
        ),
        (
            None,
            None,
            "John",
            "Wick",
        ),
    ],
    ids=[
        "Update author only with first name.",
        "Update author only with last name.",
        "Update author with new first and last name.",
        "No update for author.",
    ],
)
@pytest.mark.asyncio
async def test_update_author(
    first_name_to_update,
    last_name_to_update,
    first_name_after_update,
    last_name_after_update,
    first_name="John",
    last_name="Wick",
):
    async with SessionLocal() as db:
        async with AsyncClient(app=app, base_url="http://") as ac:
            instance1 = create_author_instance(
                db=db, first_name=first_name, last_name=last_name
            )
            author = await instance1.__anext__()

            update_data = {}
            if first_name_to_update:
                update_data["first_name"] = first_name_to_update
            if last_name:
                update_data["last_name"] = last_name_to_update

            response = await ac.put(f"/authors/{author.id}/", json=update_data)
            response_json = response.json()

            assert response.status_code == 200
            assert response_json.get("first_name") == first_name_after_update
            assert response_json.get("last_name") == last_name_after_update

            try:
                await instance1.__anext__()
            except StopAsyncIteration:
                pass


@pytest.mark.asyncio
async def test_delete_author():
    async with SessionLocal() as db:
        async with AsyncClient(app=app, base_url="http://") as ac:
            instance1 = create_author_instance(db=db)
            author = await instance1.__anext__()

            response = await ac.delete(f"/authors/{author.id}/")
            response_not_found = await ac.delete(f"/authors/{author.id + 1}/")

            db_author = await crud.get_author_by_id(db=db, author_id=author.id)

            assert response.status_code == 200
            assert response_not_found.status_code == 404
            assert db_author is None
