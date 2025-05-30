import pytest
from schemas import CompletionResponse


@pytest.mark.asyncio
async def test_chat_completion_returns_response(completion_service, mock_chat):
    mock_chat(completion_service, "This is a test completion.")

    response = await completion_service.chat_completion(prompt="Test prompt")

    assert isinstance(response, CompletionResponse)
    assert response.completion.startswith("This is a test")
