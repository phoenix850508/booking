import random
from datetime import date, datetime, timezone, timedelta

from sqlalchemy import select

from app.auth.service import hash_password
from app.database import async_session
from app.models import Concert, TicketTier, User
from app.redis_client import redis, tier_seats_key

TZ_TPE = timezone(timedelta(hours=8))


def _dt(year: int, month: int, day: int, hour: int = 19, minute: int = 0) -> datetime:
    return datetime(year, month, day, hour, minute, tzinfo=TZ_TPE)


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

# (concert_data, [tier_data, ...])
CONCERTS_DATA = [
    # ── 高雄巨蛋 capacity ~15,000 ──────────────────────────────────────────
    (
        Concert(
            title="JOJI SOLARIS",
            artist="Joji",
            venue="高雄巨蛋",
            description="Joji 世界巡迴演唱會台灣站",
            start_at=_dt(2026, 11, 27),
            sale_start_at=_dt(2026, 6, 14, 12),
        ),
        [
            TicketTier(name="VIP", price=4800, total_seats=500, available_seats=500),
            TicketTier(name="A區", price=3200, total_seats=5000, available_seats=5000),
            TicketTier(name="B區", price=2200, total_seats=9500, available_seats=9500),
        ],
    ),
    (
        Concert(
            title="EXO PLANET #6 THE EℓyXiOn IN KAOHSIUNG - DAY 1",
            artist="EXO",
            venue="高雄巨蛋",
            description=None,
            start_at=_dt(2026, 7, 18, 18),
            sale_start_at=_dt(2026, 4, 5, 12),
        ),
        [
            TicketTier(name="VIP", price=4800, total_seats=500, available_seats=500),
            TicketTier(name="A區", price=3200, total_seats=5000, available_seats=5000),
            TicketTier(name="B區", price=2200, total_seats=9500, available_seats=9500),
        ],
    ),
    (
        Concert(
            title="EXO PLANET #6 THE EℓyXiOn IN KAOHSIUNG - DAY 2",
            artist="EXO",
            venue="高雄巨蛋",
            description=None,
            start_at=_dt(2026, 7, 19, 18),
            sale_start_at=_dt(2026, 4, 5, 12),
        ),
        [
            TicketTier(name="VIP", price=4800, total_seats=500, available_seats=500),
            TicketTier(name="A區", price=3200, total_seats=5000, available_seats=5000),
            TicketTier(name="B區", price=2200, total_seats=9500, available_seats=9500),
        ],
    ),
    # ── 高雄國家體育場 capacity ~55,000 ────────────────────────────────────
    (
        Concert(
            title="BTS WORLD TOUR 'ARIRANG' IN KAOHSIUNG - DAY 1",
            artist="BTS",
            venue="高雄國家體育場",
            description="BTS 世界巡迴演唱會高雄站",
            start_at=_dt(2026, 11, 19, 18),
            sale_start_at=_dt(2026, 7, 12, 12),
        ),
        [
            TicketTier(name="VIP", price=6800, total_seats=1000, available_seats=1000),
            TicketTier(name="A區", price=4800, total_seats=15000, available_seats=15000),
            TicketTier(name="B區", price=3200, total_seats=20000, available_seats=20000),
            TicketTier(name="C區", price=1800, total_seats=19000, available_seats=19000),
        ],
    ),
    (
        Concert(
            title="BTS WORLD TOUR 'ARIRANG' IN KAOHSIUNG - DAY 2",
            artist="BTS",
            venue="高雄國家體育場",
            description="BTS 世界巡迴演唱會高雄站",
            start_at=_dt(2026, 11, 20, 18),
            sale_start_at=_dt(2026, 7, 12, 12),
        ),
        [
            TicketTier(name="VIP", price=6800, total_seats=1000, available_seats=1000),
            TicketTier(name="A區", price=4800, total_seats=15000, available_seats=15000),
            TicketTier(name="B區", price=3200, total_seats=20000, available_seats=20000),
            TicketTier(name="C區", price=1800, total_seats=19000, available_seats=19000),
        ],
    ),
    (
        Concert(
            title="BTS WORLD TOUR 'ARIRANG' IN KAOHSIUNG - DAY 3",
            artist="BTS",
            venue="高雄國家體育場",
            description="BTS 世界巡迴演唱會高雄站",
            start_at=_dt(2026, 11, 21, 18),
            sale_start_at=_dt(2026, 7, 12, 12),
        ),
        [
            TicketTier(name="VIP", price=6800, total_seats=1000, available_seats=1000),
            TicketTier(name="A區", price=4800, total_seats=15000, available_seats=15000),
            TicketTier(name="B區", price=3200, total_seats=20000, available_seats=20000),
            TicketTier(name="C區", price=1800, total_seats=19000, available_seats=19000),
        ],
    ),
    (
        Concert(
            title="BTS WORLD TOUR 'ARIRANG' IN KAOHSIUNG - DAY 4",
            artist="BTS",
            venue="高雄國家體育場",
            description="BTS 世界巡迴演唱會高雄站",
            start_at=_dt(2026, 11, 22, 18),
            sale_start_at=_dt(2026, 7, 12, 12),
        ),
        [
            TicketTier(name="VIP", price=6800, total_seats=1000, available_seats=1000),
            TicketTier(name="A區", price=4800, total_seats=15000, available_seats=15000),
            TicketTier(name="B區", price=3200, total_seats=20000, available_seats=20000),
            TicketTier(name="C區", price=1800, total_seats=19000, available_seats=19000),
        ],
    ),
    (
        Concert(
            title="Post Malone Presents The BIG ASS Stadium World Tour",
            artist="Post Malone",
            venue="高雄國家體育場",
            description=None,
            start_at=_dt(2026, 9, 19),
            sale_start_at=_dt(2026, 5, 30, 12),
        ),
        [
            TicketTier(name="VIP", price=5800, total_seats=1000, available_seats=1000),
            TicketTier(name="A區", price=3800, total_seats=20000, available_seats=20000),
            TicketTier(name="B區", price=2800, total_seats=34000, available_seats=34000),
        ],
    ),
    # ── 台北小巨蛋 capacity ~15,000 ────────────────────────────────────────
    (
        Concert(
            title="IVE WORLD TOUR IN TAIPEI - DAY 1",
            artist="IVE",
            venue="台北小巨蛋",
            description=None,
            start_at=_dt(2026, 9, 11, 18, 30),
            sale_start_at=_dt(2026, 6, 7, 12),
        ),
        [
            TicketTier(name="VIP", price=4500, total_seats=500, available_seats=500),
            TicketTier(name="A區", price=3200, total_seats=5500, available_seats=5500),
            TicketTier(name="B區", price=2200, total_seats=9000, available_seats=9000),
        ],
    ),
    (
        Concert(
            title="IVE WORLD TOUR IN TAIPEI - DAY 2",
            artist="IVE",
            venue="台北小巨蛋",
            description=None,
            start_at=_dt(2026, 9, 12, 18, 30),
            sale_start_at=_dt(2026, 6, 7, 12),
        ),
        [
            TicketTier(name="VIP", price=4500, total_seats=500, available_seats=500),
            TicketTier(name="A區", price=3200, total_seats=5500, available_seats=5500),
            TicketTier(name="B區", price=2200, total_seats=9000, available_seats=9000),
        ],
    ),
    (
        Concert(
            title="IVE WORLD TOUR IN TAIPEI - DAY 3",
            artist="IVE",
            venue="台北小巨蛋",
            description=None,
            start_at=_dt(2026, 9, 13, 18, 30),
            sale_start_at=_dt(2026, 6, 7, 12),
        ),
        [
            TicketTier(name="VIP", price=4500, total_seats=500, available_seats=500),
            TicketTier(name="A區", price=3200, total_seats=5500, available_seats=5500),
            TicketTier(name="B區", price=2200, total_seats=9000, available_seats=9000),
        ],
    ),
    (
        Concert(
            title="LANY",
            artist="LANY",
            venue="台北小巨蛋",
            description=None,
            start_at=_dt(2026, 9, 26),
            sale_start_at=_dt(2026, 6, 21, 12),
        ),
        [
            TicketTier(name="VIP", price=3800, total_seats=300, available_seats=300),
            TicketTier(name="A區", price=2800, total_seats=5700, available_seats=5700),
            TicketTier(name="B區", price=1800, total_seats=9000, available_seats=9000),
        ],
    ),
    # ── 臺北大巨蛋 capacity ~40,000 ────────────────────────────────────────
    (
        Concert(
            title="aespa LIVE TOUR IN TAIPEI",
            artist="aespa",
            venue="臺北大巨蛋",
            description=None,
            start_at=_dt(2026, 8, 11, 18, 30),
            sale_start_at=_dt(2026, 5, 10, 12),
        ),
        [
            TicketTier(name="VIP", price=4800, total_seats=800, available_seats=800),
            TicketTier(name="A區", price=3500, total_seats=15000, available_seats=15000),
            TicketTier(name="B區", price=2500, total_seats=24200, available_seats=24200),
        ],
    ),
    # ── 台北國際會議中心 TICC capacity ~3,000 ──────────────────────────────
    (
        Concert(
            title="wave to earth - the pieces tour",
            artist="wave to earth",
            venue="台北國際會議中心 TICC",
            description=None,
            start_at=_dt(2026, 11, 24),
            sale_start_at=_dt(2026, 7, 5, 12),
        ),
        [
            TicketTier(name="前排", price=2800, total_seats=500, available_seats=500),
            TicketTier(name="一般", price=1800, total_seats=2500, available_seats=2500),
        ],
    ),
    # ── 桃園陽光劇場 capacity ~8,000 ───────────────────────────────────────
    (
        Concert(
            title="Charlie Puth - Whatever's Clever! World Tour",
            artist="Charlie Puth",
            venue="桃園陽光劇場",
            description=None,
            start_at=_dt(2026, 10, 18),
            sale_start_at=_dt(2026, 6, 28, 12),
        ),
        [
            TicketTier(name="搖滾區", price=3200, total_seats=1000, available_seats=1000),
            TicketTier(name="A區", price=2500, total_seats=3500, available_seats=3500),
            TicketTier(name="B區", price=1800, total_seats=3500, available_seats=3500),
        ],
    ),
]


async def seed():
    async with async_session() as session:
        result = await session.execute(select(User).limit(1))
        if result.scalars().first() is None:
            session.add_all(DUMMY_USERS)
            await session.flush()

            for concert, tiers in CONCERTS_DATA:
                session.add(concert)
                await session.flush()
                for tier in tiers:
                    tier.concert_id = concert.id
                    session.add(tier)

            await session.commit()
            print(f"Seeded {len(DUMMY_USERS)} users and {len(CONCERTS_DATA)} concerts.")
        else:
            print("Seed skipped: data already exists.")

        # 每次啟動都從 DB 同步 Redis，確保 Redis 重啟後座位數正確
        result = await session.execute(select(TicketTier))
        tiers = result.scalars().all()
        async with redis.pipeline() as pipe:
            for tier in tiers:
                pipe.set(tier_seats_key(tier.id), tier.available_seats)
            await pipe.execute()

        print(f"Synced {len(tiers)} ticket tier(s) to Redis.")
