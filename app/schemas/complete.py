import uuid
from typing import Optional
from typing import Annotated
from pydantic import BaseModel, Field, field_validator

from doc_examples import complete_request


class CompletionRequest(BaseModel):
    """Request model for text completion"""

    prompt: Annotated[
        str, Field(min_length=1, max_length=4000, description="The input prompt")
    ]

    max_tokens: Annotated[
        Optional[int],
        Field(default=150, ge=1, le=2000, description="Maximum tokens to generate"),
    ]

    temperature: Annotated[
        Optional[float],
        Field(
            default=0.7,
            ge=0.0,
            le=2.0,
            description=(
                "Sampling temperature used to control the randomness of the output. "
                "Higher values (e.g., 1.5–2.0) produce more creative or diverse completions, "
                "while lower values (e.g., 0.2–0.5) make the output more focused and deterministic. "
                "A value of 0 disables sampling and makes the model deterministic if supported."
            ),
        ),
    ]

    top_p: Annotated[
        Optional[float],
        Field(
            default=1.0,
            ge=0.0,
            le=1.0,
            description=(
                "Controls the nucleus sampling strategy. The model considers only the most probable tokens "
                "whose cumulative probability is greater than or equal to `top_p`. Lower values reduce randomness; "
                "typical range is 0.8–1.0."
            ),
        ),
    ]

    model_config = {"json_schema_extra": {"examples": complete_request}}

    @field_validator("prompt")
    @classmethod
    def validate_prompt(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Prompt cannot be empty or whitespace only")
        return v.strip()


class CompletionResponse(BaseModel):
    """Response model for text completion"""

    id: str = Field(
        default_factory=lambda: f"comp-{uuid.uuid4()}",
        description="Unique completion ID",
    )
    completion: str = Field(..., description="Generated completion text")
