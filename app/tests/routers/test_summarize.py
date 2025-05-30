import pytest
from httpx import AsyncClient
from main import app
from config import get_settings

settings = get_settings()


@pytest.mark.asyncio
class TestSummarizeRouter:
    URL = f"{settings.api_prefix}{settings.api_version}/summarize"

    async def test_summarize_concise_style(self, auth_headers):
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post(
                self.URL,
                json={
                    "text": "Artificial Intelligence is transforming industries by automating tasks and generating insights.",
                    "max_length": 50,
                    "style": "concise",
                },
                headers=auth_headers,
            )

        assert response.status_code == 200
        res = response.json()
        assert "summary" in res
        assert isinstance(res["summary"], str)
        assert len(res["summary"]) > 0
        assert res["summary_length"] <= 50

    async def test_summarize_without_token(self):
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post(
                self.URL,
                json={
                    "text": "Artificial Intelligence is transforming industries.",
                    "max_length": 50,
                    "style": "concise",
                },
            )

        assert response.status_code in [401, 403]
        assert response.json()["detail"] in ["Not authenticated", "Invalid token"]

    async def test_summarize_invalid_style(self, auth_headers):
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post(
                self.URL,
                json={
                    "text": "AI is everywhere. AI is everywhere. AI is everywhere.",
                    "max_length": 50,
                    "style": "non_existing_style",
                },
                headers=auth_headers,
            )

        assert response.status_code == 422
        res = response.json()
        assert "style" in res["detail"]
        assert res["error_code"] == "validation_error"

    async def test_summarize_missing_text(self, auth_headers):
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post(
                self.URL,
                json={"max_length": 50, "style": "concise"},
                headers=auth_headers,
            )

        assert response.status_code == 422
        res = response.json()
        assert "text" in res["detail"]
        assert res["error_code"] == "validation_error"
