from fastapi import APIRouter, Depends, Request
from schemas.analyze import AnalysisRequest, AnalysisResponse
from services import AnalysisService

from dependencies import get_current_user
from doc_examples import analyze_200, common_401, common_422, common_429

from routers.rate_limiter import limiter

router = APIRouter(
    prefix="/analyze", tags=["Analysis"], dependencies=[Depends(get_current_user)]
)
analysis_service = AnalysisService()


@router.post(
    "",
    response_model=AnalysisResponse,
    responses=analyze_200 | common_401 | common_422 | common_429,
    summary="Analyze text",
    description="""
Perform advanced analysis on the input text using an LLM.

**Supported analysis types**:
- `sentiment`: Detect sentiment (positive, negative, neutral)
- `key_topics`: Extract key topics and themes
- `entities`: Identify named entities (people, places, organizations)
- `readability`: Assess the readability level
- `tone`: Analyze the tone and writing style

**Constraints**:
- Text length must be between **1 and 4000 characters**
- Limited to **1000 requests per hour** per IP address
    """,
)
@limiter.limit("1000/hour")
async def analyze_text(request: Request, body: AnalysisRequest):
    return await analysis_service.analyze_text(body.text, body.type)
