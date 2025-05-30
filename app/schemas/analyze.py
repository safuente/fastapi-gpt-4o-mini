import re
import uuid
from enum import Enum

from pydantic import BaseModel, Field, field_validator
from typing import Optional
from typing_extensions import Annotated


class AnalysisType(str, Enum):
    SENTIMENT = "sentiment"
    KEY_TOPICS = "key_topics"
    ENTITIES = "entities"
    READABILITY = "readability"
    TONE = "tone"


class AnalysisRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=4000, description="Text to analyze")
    type: AnalysisType = Field(..., description="Type of analysis to perform")


class AnalysisResponse(BaseModel):
    type: AnalysisType = Field(..., description="Type of analysis performed")
    result: str = Field(..., description="Textual result of the analysis")
