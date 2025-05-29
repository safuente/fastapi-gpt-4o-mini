# routers/translate.py

from fastapi import APIRouter, Depends
from schemas import TranslationRequest, TranslationResponse
from services import TranslationService

router = APIRouter(prefix="/translate", tags=["Translate"])
translation_service = TranslationService()


@router.post("", response_model=TranslationResponse)
async def translate(
    request: TranslationRequest,
):
    return await translation_service.translate_text(
        text=request.text,
        target_language=request.target_language
    )
