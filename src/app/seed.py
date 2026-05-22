import random
import string
from datetime import date

from sqlalchemy import select

from app.auth.service import hash_password
from app.database import engine, async_session
from app.models import Base, Concert, User


def _random_birthday() -> date:
    return date(
        random.randint(1980, 2005), random.randint(1, 12), random.randint(1, 28)
    )


DUMMY_USERS = [
    User(
        username=(f"user_{i}"),
        password=hash_password(f"password_{i}"),
        birthday=_random_birthday(),
    )
    for i in range(1, 101)
]


async def seed():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session() as session:
        result = await session.execute(select(User).limit(1))
        if result.scalars().first() is not None:
            print("Seed skipped: users table already has data.")
            return

        session.add_all(DUMMY_USERS)
        await session.commit()
        print(f"Seeded {len(DUMMY_USERS)} users.")
