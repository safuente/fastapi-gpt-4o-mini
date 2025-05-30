import pytest
from schemas import TranslationResponse


@pytest.mark.asyncio
async def test_translate_text_returns_response(translation_service, mock_chat):
    mock_chat(translation_service, "Hola mundo")

    result = await translation_service.translate_text("Hello world", "es")

    assert isinstance(result, TranslationResponse)
    assert "Hola mundo" in result.translation
