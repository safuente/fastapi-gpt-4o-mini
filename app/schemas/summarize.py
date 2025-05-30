import re
import uuid
from enum import Enum

from pydantic import BaseModel, Field, field_validator
from typing import Optional
from typing_extensions import Annotated

from doc_examples import summary_request


class SummaryStyle(str, Enum):
    CONCISE = "concise"
    DETAILED = "detailed"
    BULLET_POINTS = "bullet_points"
    EXECUTIVE = "executive"
    STORYTELLING = "storytelling"


class SummaryRequest(BaseModel):
    """Request model for text summarization"""

    text: Annotated[
        str, Field(min_length=50, max_length=10000, description="Text to summarize")
    ]
    max_length: Annotated[
        Optional[int],
        Field(ge=50, le=500, description="Maximum summary length in words"),
    ] = 150
    style: Optional[SummaryStyle] = Field(
        default=SummaryStyle.CONCISE, description="Summary style"
    )

    model_config = {"json_schema_extra": {"examples": summary_request}}

    @field_validator("text")
    @classmethod
    def validate_text(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Text cannot be empty or whitespace only")
        return v.strip()


class SummaryResponse(BaseModel):
    """Response model for text summarization"""

    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()), description="Unique completion ID"
    )
    summary: str = Field(..., description="Generated summary")
    original_length: int = Field(..., description="Original text length in characters")
    summary_length: int = Field(..., description="Summary length in characters")
