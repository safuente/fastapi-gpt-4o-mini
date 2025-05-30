analysis_request = {
    "text": "This product is fantastic! I'm very happy with the results.",
    "type": "sentiment"
}

complete_request = [
    {
        "prompt": "Once upon a time, in a land far away,",
        "max_tokens": 50,
        "temperature": 0.7,
        "top_p": 1.0
    }
]

summary_request = [{
    "text":
        "Artificial Intelligence is transforming industries by enabling automation "
        "and enhancing decision-making with predictive capabilities.",
    "max_length": 50,
    "style": "concise"
}]

translate_request = [{
  "text": "Artificial Intelligence is revolutionizing the tech industry.",
  "target_language": "es"
}]






common_401 = {
    401: {
        "description": "Unauthorized - Invalid or missing token",
        "content": {
            "application/json": {
                "example": {"detail": "Invalid token", "error_code": "http_error"}
            }
        },
    }
}

common_422 = {
    422: {
        "description": "Validation Error",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Invalid request",
                    "error_code": "validation_error",
                }
            }
        },
    }
}

summarize_200 = {
    200: {
        "description": "Successful summary",
        "content": {
            "application/json": {
                "example": {
                    "summary": "This product offers excellent performance with great value.",
                    "original_length": 15,
                    "summary_length": 10,
                }
            }
        },
    }
}

complete_200 = {
    200: {
        "description": "Successful text completion",
        "content": {
            "application/json": {
                "example": {
                    "completion": "This is a completed sentence based on your input."
                }
            }
        },
    }
}

translate_200 = {
    200: {
        "description": "Successful translation",
        "content": {
            "application/json": {
                "example": {
                    "translation": "Este producto ofrece un excelente rendimiento y gran valor."
                }
            }
        },
    }
}

analyze_200 = {
    200: {
        "description": "Successful analysis",
        "content": {
            "application/json": {
                "example": {
                    "result": "Sentiment: Positive\nConfidence Score: 95%"
                }
            }
        },
    }
}




