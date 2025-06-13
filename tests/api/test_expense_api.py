import pytest
from tests.conftest import get_auth_header
pytestmark = pytest.mark.asyncio


async def test_expense_crud(async_client):
    headers = await get_auth_header(async_client)

    trip = (
        await async_client.post(
            "/trips/",
            json={
                "destination": "Joburg",
                "start_date": "2025-01-01",
                "end_date": "2025-01-05",
            },
            headers=headers,
        )
    ).json()

    exp_payload = {
        "trip_id": trip["id"],
        "amount": 100.0,
        "currency": "USD",
        "category": "Food",
    }
    res = await async_client.post("/expenses/", json=exp_payload, headers=headers)
    assert res.status_code == 201
    expense_id = res.json()["id"]

    res = await async_client.get(f"/expenses?trip_id={trip['id']}", headers=headers)
    assert res.json()[0]["id"] == expense_id

    res = await async_client.delete(f"/expenses/{expense_id}", headers=headers)
    assert res.status_code == 200
