from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_user
from app.database import get_session
from app.models import Booking, Concert, TicketTier, User
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
):
    result = await session.execute(select(Concert).where(Concert.id == concert_id))
    if result.scalars().first() is None:
        raise HTTPException(status_code=404, detail="Concert not found")

    result = await session.execute(
        select(TicketTier)
        .where(
            TicketTier.id == body.ticket_tier_id,
            TicketTier.concert_id == concert_id,
        )
        .with_for_update()  # 悲觀鎖：鎖住這一行直到 commit
    )
    tier = result.scalars().first()
    if tier is None:
        raise HTTPException(status_code=404, detail="Ticket tier not found")

    if tier.available_seats < body.quantity:
        raise HTTPException(status_code=400, detail="Not enough seats")

    tier.available_seats -= body.quantity
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
