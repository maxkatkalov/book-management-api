from typing import Annotated

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from database import SessionLocal


async def get_db() -> AsyncSession:
    async with SessionLocal() as session:
        yield session


DatabaseDependancy = Annotated[AsyncSession, Depends(get_db)]
