import pytest

from config import get_settings
from services.auth_service import AuthService
from services import CompletionService, AnalysisService, SummaryService, TranslationService


@pytest.fixture
def test_token():
    settings = get_settings()
    auth_service = AuthService()
    token = auth_service.create_access_token({"sub": settings.fake_username})
    return token


@pytest.fixture
def auth_headers(test_token):
    return {"Authorization": f"Bearer {test_token}"}


@pytest.fixture
def translation_service():
    return TranslationService()


@pytest.fixture
def completion_service():
    return CompletionService()


@pytest.fixture
def analysis_service():
    return AnalysisService()


@pytest.fixture
def summary_service():
    return SummaryService()


@pytest.fixture
def mock_chat(monkeypatch):
    def _patch(service, return_value="Mocked response"):
        async def mock_method(*args, **kwargs):
            return return_value
        monkeypatch.setattr(service, "chat_complete", mock_method)
    return _patch
