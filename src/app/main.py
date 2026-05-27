from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, Path
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.router import router as auth_router
from app.bookings.router import router as bookings_router
from app.concerts.router import router as concerts_router
from app.database import get_session
from app.models import User
from app.seed import seed


@asynccontextmanager
async def lifespan(app: FastAPI):
    await seed()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(auth_router)
app.include_router(concerts_router)
app.include_router(bookings_router)


@app.get("/")
async def health_check(session: AsyncSession = Depends(get_session)):
    await session.execute(text("SELECT 1"))
    return {"status": "ok", "db": "connected"}


@app.get("/users")
async def get_users(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(User.username, User.birthday, User.avatar))
    users = [
        {
            "username": row.username,
            "birthday": row.birthday.isoformat(),
            "avatar": row.avatar,
        }
        for row in result.all()
    ]
    return users
