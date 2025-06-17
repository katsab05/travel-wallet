import pytest, uuid
pytestmark = pytest.mark.asyncio


async def test_register_and_login(async_client):
    email = f"user_{uuid.uuid4().hex}@example.com"
    reg_payload = {
        "email": email,
        "password": "SuperSecret123!",
        "full_name": "Tester",
    }

    # Register
    r = await async_client.post("/auth/register", json=reg_payload)
    assert r.status_code in (200, 201)
    token = r.json()["access_token"]

    # Login
    login_data = {"username": email, "password": reg_payload["password"]}
    r = await async_client.post("/auth/login", data=login_data)
    assert r.status_code == 200
    login_token = r.json()["access_token"]

    assert token != ""
    assert login_token != ""
