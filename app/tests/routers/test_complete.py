import pytest
from httpx import AsyncClient
from main import app
from config import get_settings

settings = get_settings()


class TestCompleteEndpoint:
    URL = f"{settings.api_prefix}{settings.api_version}/complete"

    @pytest.mark.asyncio
    async def test_complete_text(self, auth_headers):
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post(
                self.URL,
                json={
                    "prompt": "Once upon a time in a galaxy far, far away",
                    "max_tokens": 50,
                    "temperature": 0.5,
                    "top_p": 1.0,
                },
                headers=auth_headers,
            )

        assert response.status_code == 200
        data = response.json()
        assert "completion" in data
        assert isinstance(data["completion"], str)
        assert len(data["completion"]) > 0

    @pytest.mark.asyncio
    async def test_complete_text_without_token(self):
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post(
                self.URL,
                json={"prompt": "Tell me a joke", "max_tokens": 30},
            )

        assert response.status_code == 401
        assert response.json()["detail"] in ["Invalid token"]

    @pytest.mark.asyncio
    async def test_complete_text_empty_prompt(self, auth_headers):
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post(
                self.URL,
                json={"prompt": "   ", "max_tokens": 50},
                headers=auth_headers,
            )

        assert response.status_code == 422
        data = response.json()
        assert data["error_code"] == "validation_error"
        assert "Invalid request" in data["detail"]

    @pytest.mark.asyncio
    async def test_complete_text_streaming(self, auth_headers):
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post(
                f"{self.URL}?stream=true",
                json={
                    "prompt": "Continue the following poem: Roses are red",
                    "max_tokens": 20,
                    "temperature": 0.5,
                    "top_p": 1.0,
                },
                headers=auth_headers,
            )

        assert response.status_code == 200
        assert response.headers["content-type"].startswith("text/plain")
        streamed_text = b"".join(response.iter_bytes()).decode()
        assert isinstance(streamed_text, str)
        assert len(streamed_text.strip()) > 0
