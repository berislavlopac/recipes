from crewai import LLM

from recipes.application.config import settings


def get_vision_model():
    return LLM(
        model="gemini/gemini-2.5-flash",
        temperature=0.1,
        api_key=settings.GEMINI_API_KEY,
    )


def get_reasoning_model():
    return LLM(
        model="gemini/gemini-3.0-pro",
        temperature=0.8,  # Higher temp for creativity
        api_key=settings.GEMINI_API_KEY,
    )
