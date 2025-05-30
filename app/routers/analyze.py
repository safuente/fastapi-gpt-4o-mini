from fastapi import APIRouter, Depends
from schemas.analyze import AnalysisRequest, AnalysisResponse
from services import AnalysisService

router = APIRouter(prefix="/analyze", tags=["Analysis"])
analysis_service = AnalysisService()


@router.post("", response_model=AnalysisResponse)
async def analyze_text(request: AnalysisRequest):
    result = await analysis_service.analyze_text(request.text, request.type)
    return AnalysisResponse(type=request.type, result=result)
