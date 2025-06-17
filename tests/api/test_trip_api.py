import pytest
from tests.conftest import get_auth_header
pytestmark = pytest.mark.asyncio


async def test_create_and_list_trip(async_client):
    headers = await get_auth_header(async_client)

    payload = {
        "destination": "Cape Town",
        "start_date": "2025-07-01",
        "end_date": "2025-07-10",
        "notes": "Vacation",
    }

    res = await async_client.post("/trips/", json=payload, headers=headers)
    assert res.status_code == 201
    res = await async_client.get("/trips/", headers=headers)
    assert res.status_code == 200
    assert res.json()[0]["destination"] == "Cape Town"
