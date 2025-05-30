from pydantic import BaseModel, Field
from typing import Literal


class TranslationRequest(BaseModel):
    text: str = Field(..., min_length=1, description="Text to be translated")
    target_language: Literal["en", "es", "fr", "de", "it"] = Field(
        ..., description="Target language code"
    )


class TranslationResponse(BaseModel):
    translation: str = Field(..., description="Translated text")
