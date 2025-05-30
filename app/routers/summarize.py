from fastapi import APIRouter, HTTPException, Depends
from schemas.summarize import SummaryRequest, SummaryResponse
from services import SummaryService

from dependencies import get_current_user

router = APIRouter(prefix="/summarize", tags=["Summarize"], dependencies=[Depends(get_current_user)])
summary_service = SummaryService()


@router.post("/", response_model=SummaryResponse)
async def summarize_text(request: SummaryRequest):
    return await summary_service.summarize_text(
        text=request.text, max_length=request.max_length, style=request.style
    )

