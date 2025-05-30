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
    response_model=SummaryResponse,summary="Summarize text",
    description="""
Summarize a block of text using an LLM with support for different summarization styles.

**Supported styles**:
- `concise`: A brief, to-the-point summary (default)
- `detailed`: A more comprehensive summary
- `bullet_points`: Summary in bullet point format
- `executive`: High-level summary for decision makers
- `storytelling`: Narrative-style summary

**Constraints**:
- Input text must be between **50 and 10,000 characters**
- Summary length: **50 to 500 words**
- Rate limited to **1000 requests per hour per IP**
    """,
    responses=summarize_200 | common_401 | common_422 | common_429,
)
@limiter.limit("1000/hour")
async def summarize_text(request: Request, body: SummaryRequest):
    return await summary_service.summarize_text(
        text=body.text, max_length=body.max_length, style=body.style
    )