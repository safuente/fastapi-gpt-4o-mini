from fastapi import APIRouter, HTTPException
from schemas.summarize import SummaryRequest, SummaryResponse
from services import SummaryService

router = APIRouter(prefix="/summarize", tags=["Summarize"])
summary_service = SummaryService()


@router.post("/", response_model=SummaryResponse)
async def summarize_text(request: SummaryRequest):
    try:
        return await summary_service.summarize_text(
            text=request.text, max_length=request.max_length, style=request.style
        )
    except Exception as e:
        print(f"Error {e}")
        raise HTTPException(status_code=500, detail=str(e))
