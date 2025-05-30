import pytest
from httpx import AsyncClient
from main import app


@pytest.mark.asyncio
async def test_summarize_concise_style(auth_headers):
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/api/summarize/",
            json={
                "text": "Artificial Intelligence is transforming industries by automating tasks and generating insights.",
                "max_length": 50,
                "style": "concise"
            },
            headers=auth_headers
        )

    assert response.status_code == 200
    res = response.json()
    assert "summary" in res
    assert isinstance(res["summary"], str)
    assert len(res["summary"]) > 0
    assert res["summary_length"] <= 50


@pytest.mark.asyncio
async def test_summarize_without_token():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/api/summarize/",
            json={
                "text": "Artificial Intelligence is transforming industries.",
                "max_length": 50,
                "style": "concise"
            }
        )

    assert response.status_code in [401, 403]
    assert response.json()["detail"] in ["Not authenticated", "Invalid token"]


@pytest.mark.asyncio
async def test_summarize_invalid_style(auth_headers):
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/api/summarize/",
            json={
                "text": "AI is everywhere.AI is everywhere.AI is everywhere.",
                "max_length": 50,
                "style": "non_existing_style"
            },
            headers=auth_headers
        )

    assert response.status_code == 422
    res = response.json()
    assert "style" in res['detail']
    assert res["error_code"] == "validation_error"


@pytest.mark.asyncio
async def test_summarize_missing_text(auth_headers):
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/api/summarize/",
            json={
                "max_length": 50,
                "style": "concise"
            },
            headers=auth_headers
        )

    assert response.status_code == 422
    res = response.json()
    assert "text" in res['detail']
    assert res["error_code"] == "validation_error"
