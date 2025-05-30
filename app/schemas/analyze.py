import re
import uuid
from enum import Enum

from pydantic import BaseModel, Field, field_validator


from doc_examples import analysis_request


class AnalysisType(str, Enum):
    SENTIMENT = "sentiment"
    KEY_TOPICS = "key_topics"
    ENTITIES = "entities"
    READABILITY = "readability"
    TONE = "tone"


class AnalysisRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=4000, description="Text to analyze")
    type: AnalysisType = Field(..., description="Type of analysis to perform")

    model_config = {"json_schema_extra": {"example": analysis_request}}

    @field_validator("text")
    @classmethod
    def validate_text(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Text cannot be empty or whitespace only")
        return v.strip()


class AnalysisResponse(BaseModel):
    result: str = Field(..., description="Textual result of the analysis")
