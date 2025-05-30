from fastapi import APIRouter, Depends, Request
from schemas import TranslationRequest, TranslationResponse
from services import TranslationService

from dependencies import get_current_user
from doc_examples import translate_200, common_401 , common_422, common_429

from routers.rate_limiter import limiter

router = APIRouter(
    prefix="/translate", tags=["Translate"], dependencies=[Depends(get_current_user)]
)
translation_service = TranslationService()


@router.post(
    "",
    response_model=TranslationResponse,
    responses=translate_200 | common_401 | common_422 | common_429,
)
@limiter.limit("1000/hour")
async def translate(
    request: Request,
    body: TranslationRequest,
):
    return await translation_service.translate_text(
        text=body.text, target_language=body.target_language
    )