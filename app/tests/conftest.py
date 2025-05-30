import pytest
from services import CompletionService, AnalysisService, SummaryService, TranslationService


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
