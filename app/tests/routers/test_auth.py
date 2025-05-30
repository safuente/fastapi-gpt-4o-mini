import pytest
from httpx import AsyncClient
from main import app
from config import get_settings

settings = get_settings()


class TestAuthLogin:
    URL = f"{settings.api_prefix}{settings.api_version}/auth/login"

    @pytest.mark.asyncio
    async def test_login_success(self):
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post(
                self.URL,
                json={
                    "username": settings.fake_username,
                    "password": settings.fake_password,
                },
            )

        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert isinstance(data["access_token"], str)
        assert data["access_token"] != ""

    @pytest.mark.asyncio
    async def test_login_wrong_password(self):
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post(
                self.URL,
                json={
                    "username": settings.fake_username,
                    "password": "wrong-password",
                },
            )

        assert response.status_code == 401
        assert response.json()["detail"] == "Invalid credentials"

    @pytest.mark.asyncio
    async def test_login_unknown_user(self):
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post(
                self.URL,
                json={
                    "username": "notarealuser",
                    "password": "1234",
                },
            )

        assert response.status_code == 401
        assert response.json()["detail"] == "Invalid credentials"

    @pytest.mark.asyncio
    async def test_login_missing_fields(self):
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post(
                self.URL,
                json={
                    "username": settings.fake_username,
                },
            )

        assert response.status_code == 422
        assert response.json()["error_code"] == "validation_error"

    @pytest.mark.asyncio
    async def test_rate_limit_exceeded(self):
        async with AsyncClient(app=app, base_url="http://test") as client:
            for i in range(6):
                response = await client.post(
                    self.URL,
                    json={
                        "username": settings.fake_username,
                        "password": settings.fake_password,
                    },
                )

            assert response.status_code == 429
            body = response.json()
            assert body["detail"] == "Rate limit exceeded. Try again later"
            assert body["error_code"] == "rate_limit_error"
