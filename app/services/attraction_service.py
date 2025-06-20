from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.schemas.attraction_schema import AttractionCreate, AttractionOut, AttractionBase
from app.repositories.attraction_repository import AttractionRepository
from infrastructure.api_clients.attractions_api_client import AttractionsAPIClient


class AttractionService:
    def __init__(self, db: AsyncSession):
        self.repo = AttractionRepository(db)
        self.client = AttractionsAPIClient()

    async def fetch_and_store_nearby_attractions(
        self, lat: float, lon: float
    ) -> List[AttractionOut]:
        api_results: List[AttractionBase] = await self.client.fetch_attractions(lat, lon)
        stored = []

        for attr in api_results:
            create_schema = AttractionCreate(
                name=attr.name,
                lat=attr.lat,
                lon=attr.lon,
                description=attr.description,
                external_id=attr.id
            )
            attraction = await self.repo.create(create_schema)
            stored.append(AttractionOut.from_orm(attraction))

        return stored

    async def list_local_attractions(self) -> List[AttractionOut]:
        results = await self.repo.get_all()
        return [AttractionOut.from_orm(r) for r in results]
