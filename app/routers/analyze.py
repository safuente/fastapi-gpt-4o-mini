from fastapi import APIRouter, Depends, Request
from schemas.analyze import AnalysisRequest, AnalysisResponse
from services import AnalysisService

from dependencies import get_current_user
from doc_examples import analyze_200, common_401 , common_422, common_429

from routers.rate_limiter import limiter

router = APIRouter(
    prefix="/analyze", tags=["Analysis"], dependencies=[Depends(get_current_user)]
)
analysis_service = AnalysisService()


@router.post("", response_model=AnalysisResponse, responses=analyze_200 | common_401 | common_422 | common_429)
@limiter.limit("1000/hour")
async def analyze_text(request: Request, body: AnalysisRequest):
    return await analysis_service.analyze_text(body.text, body.type)
