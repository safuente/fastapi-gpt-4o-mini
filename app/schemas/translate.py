from pydantic import BaseModel, Field, field_validator
from typing import Literal

from doc_examples import translate_request


class TranslationRequest(BaseModel):
    text: str = Field(..., min_length=1, description="Text to be translated")
    target_language: Literal["en", "es", "fr", "de", "it"] = Field(
        ..., description="Target language code"
    )

    model_config = {
        "json_schema_extra": {
            "examples": translate_request
        }
    }

    @field_validator("text")
    @classmethod
    def validate_text(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Text cannot be empty or whitespace only")
        return v.strip()




class TranslationResponse(BaseModel):
    translation: str = Field(..., description="Translated text")
