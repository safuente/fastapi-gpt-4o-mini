from fastapi import APIRouter, Query
from fastapi.responses import StreamingResponse, JSONResponse
from services import CompletionService
from schemas import CompletionRequest, CompletionResponse

router = APIRouter(prefix="/complete", tags=["Complete"])
complete_service = CompletionService()


@router.post("", response_model=CompletionResponse, response_model_exclude_unset=True)
async def complete_text(
    request: CompletionRequest,
    stream: bool = Query(
        False, description="Return the response as a streamed text/plain output"
    ),
):
    result = await complete_service.chat_completion(
        prompt=request.prompt,
        max_tokens=request.max_tokens,
        temperature=request.temperature,
        top_p=request.top_p,
        stream=stream,
    )

    if stream:

        async def stream_generator():
            async for chunk in result:
                if chunk.choices and chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content

        return StreamingResponse(stream_generator(), media_type="text/plain")

    return result
