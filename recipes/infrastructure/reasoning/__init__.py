from crewai import LLM

from recipes.application.config import settings


def get_model() -> LLM:
    if settings.USE_LOCAL_MODELS:
        return LLM(
            temperature=settings.REASONING_TEMPERATURE,
            model=settings.REASONING_LOCAL_MODEL,
            base_url=settings.REASONING_LOCAL_URL,
        )
    else:
        return LLM(
            temperature=settings.REASONING_TEMPERATURE,
            model=settings.REASONING_GEMINI_MODEL,
            api_key=settings.GEMINI_API_KEY,
        )
