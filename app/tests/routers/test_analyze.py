import pytest
from httpx import AsyncClient
from main import app


@pytest.mark.asyncio
async def test_analyze_sentiment(auth_headers):
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/api/analyze",
            json={
                "text": "This is a wonderful product!",
                "type": "sentiment"
            },
            headers=auth_headers
        )

    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
    data = response.json()

    assert "result" in data, "Missing 'result' key in response"
    assert isinstance(data["result"], str)
    assert len(data["result"]) > 0


@pytest.mark.asyncio
async def test_analyze_sentiment_without_token():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/api/analyze",
            json={
                "text": "This is a wonderful product!",
                "type": "sentiment"
            }
        )

    assert response.status_code == 403 or response.status_code == 401
    assert response.json()["detail"] in ["Not authenticated", "Invalid token"]


@pytest.mark.asyncio
async def test_analyze_with_invalid_type(auth_headers):
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/api/analyze",
            json={
                "text": "This is a test input",
                "type": "unsupported_type"
            },
            headers=auth_headers
        )
    res = response.json()
    assert response.status_code == 422
    assert "Input should be" in str(res)
    assert res["error_code"] == "validation_error"
