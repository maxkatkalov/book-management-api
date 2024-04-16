from __future__ import annotations

from fastapi import FastAPI

from .books_router import router as books_router
from .authors_router import router as authors_router


app = FastAPI()


app.include_router(books_router)
app.include_router(authors_router)

# TODO: implement default page for root /
# TODO: implement routes
# TODO: implement status codes for wrong data
