class AppException(Exception):
    def __init__(self, message: str, error_code: str = "internal_error"):
        self.message = message
        self.error_code = error_code


class LLMServiceException(AppException):
    def __init__(self, detail="Failed in LLM Service"):
        super().__init__(detail, "llm_error")
