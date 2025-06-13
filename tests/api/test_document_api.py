import io, pytest
from tests.conftest import get_auth_header
pytestmark = pytest.mark.asyncio


async def test_document_upload_and_list(async_client):
    headers = await get_auth_header(async_client)

    pdf = io.BytesIO(b"%PDF-1.4 test\n%%EOF")
    files = {"file": ("ticket.pdf", pdf, "application/pdf")}
    res = await async_client.post("/documents/", headers=headers, files=files)
    assert res.status_code == 200
    doc = res.json()

    res = await async_client.get("/documents/", headers=headers)
    assert res.json()[0]["id"] == doc["id"]


async def test_document_validation_rejects_large_file(async_client):
    headers = await get_auth_header(async_client)

    big = b"x" * (6 * 1024 * 1024)  # 6 MB
    files = {"file": ("big.jpg", io.BytesIO(big), "image/jpeg")}
    res = await async_client.post("/documents/", headers=headers, files=files)
    assert res.status_code == 400
