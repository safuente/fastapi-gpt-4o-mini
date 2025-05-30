from fastapi import APIRouter, Depends, Request

from schemas.summarize import SummaryRequest, SummaryResponse
from services import SummaryService
from dependencies import get_current_user
from doc_examples import summarize_200, common_401, common_422, common_429
from routers.rate_limiter import limiter

router = APIRouter(
    prefix="/summarize", tags=["Summarize"], dependencies=[Depends(get_current_user)]
)
summary_service = SummaryService()


@router.post(
    "/",
    response_model=SummaryResponse,
    responses=summarize_200 | common_401 | common_422 | common_429,
)
@limiter.limit("1000/hour")
async def summarize_text(request: Request, body: SummaryRequest):
    return await summary_service.summarize_text(
        text=body.text, max_length=body.max_length, style=body.style
    )