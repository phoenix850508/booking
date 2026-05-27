from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_user
from app.database import get_session
from app.models import Booking, Concert, TicketTier, User
from app.redis_client import Redis, get_redis, tier_seats_key
from app.schemas import BookingCreate, BookingResponse

router = APIRouter(prefix="/concerts", tags=["bookings"])


@router.post(
    "/{concert_id}/book",
    response_model=BookingResponse,
    status_code=status.HTTP_201_CREATED,
)
async def book_concert(
    concert_id: int,
    body: BookingCreate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
    redis: Redis = Depends(get_redis),
):
    result = await session.execute(select(Concert).where(Concert.id == concert_id))
    if result.scalars().first() is None:
        raise HTTPException(status_code=404, detail="Concert not found")

    result = await session.execute(
        select(TicketTier).where(
            TicketTier.id == body.ticket_tier_id,
            TicketTier.concert_id == concert_id,
        )
    )
    tier = result.scalars().first()
    if tier is None:
        raise HTTPException(status_code=404, detail="Ticket tier not found")

    key = tier_seats_key(body.ticket_tier_id)

    # DECR 是原子操作，不需要任何 DB 鎖
    remaining = await redis.decrby(key, body.quantity)

    if remaining < 0:
        # 扣超了，rollback Redis 再回傳錯誤
        await redis.incrby(key, body.quantity)
        raise HTTPException(status_code=400, detail="Not enough seats")

    # Redis 已確保不會超賣，直接寫 DB 不需要鎖
    await session.execute(
        update(TicketTier)
        .where(TicketTier.id == body.ticket_tier_id)
        .values(available_seats=TicketTier.available_seats - body.quantity)
        .execution_options(synchronize_session=False)
    )
    booking = Booking(
        user_id=current_user.id,
        concert_id=concert_id,
        ticket_tier_id=body.ticket_tier_id,
        quantity=body.quantity,
    )
    session.add(booking)
    await session.commit()
    await session.refresh(booking)
    return booking
