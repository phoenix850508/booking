from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.models import Concert
from app.schemas import ConcertCreate, ConcertResponse

router = APIRouter(prefix="/concerts", tags=["concerts"])


@router.post("", response_model=ConcertResponse, status_code=status.HTTP_201_CREATED)
async def create_concert(body: ConcertCreate, session: AsyncSession = Depends(get_session)):
    concert = Concert(
        **body.model_dump(),
        available_seats=body.total_seats,
    )
    session.add(concert)
    await session.commit()
    await session.refresh(concert)
    return concert


@router.get("", response_model=list[ConcertResponse])
async def list_concerts(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Concert).order_by(Concert.start_at))
    return result.scalars().all()


@router.get("/{concert_id}", response_model=ConcertResponse)
async def get_concert(concert_id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Concert).where(Concert.id == concert_id))
    concert = result.scalars().first()
    if concert is None:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Concert not found")
    return concert
