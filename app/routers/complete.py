from fastapi import APIRouter, Query, Depends, Request
from fastapi.responses import StreamingResponse, JSONResponse
from services import CompletionService
from schemas import CompletionRequest, CompletionResponse

from dependencies import get_current_user
from routers.rate_limiter import limiter
from doc_examples import complete_200, common_401 , common_422, common_429

router = APIRouter(
    prefix="/complete", tags=["Complete"], dependencies=[Depends(get_current_user)]
)
complete_service = CompletionService()


@router.post(
    "",
    response_model=CompletionResponse,
    response_model_exclude_unset=True,
    responses=complete_200 | common_401 | common_422 | common_429,
)
@limiter.limit("1000/hour")
async def complete_text(
    request: Request,
    body: CompletionRequest,
    stream: bool = Query(
        False, description="Return the response as a streamed text/plain output"
    ),
):
    result = await complete_service.chat_completion(
        prompt=body.prompt,
        max_tokens=body.max_tokens,
        temperature=body.temperature,
        top_p=body.top_p,
        stream=stream,
    )

    if stream:

        async def stream_generator():
            async for chunk in result:
                if chunk.choices and chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content

        return StreamingResponse(stream_generator(), media_type="text/plain")

    return result