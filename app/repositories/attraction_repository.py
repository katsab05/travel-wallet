from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.attraction import Attraction
from app.schemas.attraction_schema import AttractionCreate


class AttractionRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: AttractionCreate) -> Attraction:
        attraction = Attraction(**data.dict())
        self.db.add(attraction)
        await self.db.commit()
        await self.db.refresh(attraction)
        return attraction

    async def get_all(self) -> list[Attraction]:
        result = await self.db.execute(select(Attraction))
        return result.scalars().all()

    async def get_by_id(self, attraction_id: int) -> Attraction | None:
        result = await self.db.execute(
            select(Attraction).where(Attraction.id == attraction_id)
        )
        return result.scalar_one_or_none()

    async def delete_by_id(self, attraction_id: int) -> None:
        attraction = await self.get_by_id(attraction_id)
        if attraction:
            await self.db.delete(attraction)
            await self.db.commit()
