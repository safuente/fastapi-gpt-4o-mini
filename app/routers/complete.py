from fastapi import APIRouter, HTTPException
from services import CompletionService
from schemas import CompletionRequest, CompletionResponse

router = APIRouter(prefix="/complete", tags=["Complete"])
complete_service = CompletionService()


@router.post("/", response_model=CompletionResponse)
async def complete_text(request: CompletionRequest):
    try:
        return await complete_service.chat_completion(
            prompt=request.prompt,
            max_tokens=request.max_tokens,
            temperature=request.temperature,
            top_p=request.top_p,
        )
    except Exception as e:
        print(f"Error {e}")
        raise HTTPException(status_code=500, detail=str(e))
