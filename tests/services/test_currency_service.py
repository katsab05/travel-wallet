import pytest
import respx
from httpx import Response
from app.services.currency_service import convert_currency

pytestmark = pytest.mark.asyncio

@respx.mock
async def test_conversion_with_external_api(monkeypatch, db_session):
    # Mock remote API
    fake_json = {"base": "USD", "rates": {"ZAR": 20.0}}
    respx.get("https://api.exchangerate-api.com/v4/latest/USD").mock(
        return_value=Response(200, json=fake_json)
    )

    amount = await convert_currency(10, "USD", "ZAR", db=db_session)
    assert amount == 200.0  # 10 × 20

    # second call → should hit DB cache, so mock not triggered
    amount2 = await convert_currency(5, "USD", "ZAR", db=db_session)
    assert amount2 == 100.0
