import pytest
from httpx import AsyncClient
from main import app
from config import get_settings

settings = get_settings()


class TestTranslateEndpoint:
    URL = f"{settings.api_prefix}{settings.api_version}/translate"

    @pytest.mark.asyncio
    async def test_translate_success(self, auth_headers):
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post(
                self.URL,
                json={"text": "Hello, how are you?", "target_language": "es"},
                headers=auth_headers,
            )

        assert response.status_code == 200
        data = response.json()
        assert "translation" in data
        assert isinstance(data["translation"], str)
        assert len(data["translation"].strip()) > 0

    @pytest.mark.asyncio
    async def test_translate_without_token(self):
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post(
                self.URL,
                json={"text": "Good morning", "target_language": "fr"},
            )

        assert response.status_code in (401, 403)
        assert response.json()["detail"] in ["Not authenticated", "Invalid token"]

    @pytest.mark.asyncio
    async def test_translate_invalid_language_code(self, auth_headers):
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post(
                self.URL,
                json={"text": "Hi!", "target_language": "invalid_lang"},
                headers=auth_headers,
            )

        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_translate_empty_text(self, auth_headers):
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post(
                self.URL,
                json={"text": "   ", "target_language": "es"},
                headers=auth_headers,
            )

        assert response.status_code == 422
        data = response.json()
        assert data["error_code"] == "validation_error"
