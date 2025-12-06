from crewai import LLM

from recipes.application.config import settings


def get_vision_model():
    return LLM(
        model=settings.VISION_GEMINI_MODEL,
        temperature=settings.VISION_TEMPERATURE,
        api_key=settings.GEMINI_API_KEY,
    )


def get_reasoning_model():
    return LLM(
        model=settings.REASONING_GEMINI_MODEL,
        temperature=settings.REASONING_TEMPERATURE,  # Higher temp for creativity
        api_key=settings.GEMINI_API_KEY,
    )
