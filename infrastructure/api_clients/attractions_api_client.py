import os
import httpx
import logging
from typing import List
from app.schemas.attraction_schema import AttractionBase

logger = logging.getLogger(__name__)

GOOGLE_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
BASE_URL = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"


class AttractionsAPIClient:
    def __init__(self):
        self.client = httpx.AsyncClient(timeout=10.0)

    async def fetch_attractions(self, lat: float, lon: float) -> List[AttractionBase]:
        try:
            response = await self.client.get(
                BASE_URL,
                params={
                    "location": f"{lat},{lon}",
                    "radius": 1500,
                    "type": "tourist_attraction",
                    "key": GOOGLE_API_KEY,
                }
            )
            response.raise_for_status()
            results = response.json().get("results", [])

            attractions = []
            for item in results[:10]:  # Limit for demo
                attractions.append(
                    AttractionBase(
                        id=item.get("place_id", ""),
                        name=item.get("name", "Unknown"),
                        lat=item.get("geometry", {}).get("location", {}).get("lat", lat),
                        lon=item.get("geometry", {}).get("location", {}).get("lng", lon),
                        description=item.get("types", ["No description"])[0]
                    )
                )
            return attractions

        except httpx.HTTPError as e:
            logger.error(f"Google Places API request failed: {e}")
            return []
        except Exception as e:
            logger.exception("Unexpected error during attraction fetch")
            return []

    async def close(self):
        await self.client.aclose()
