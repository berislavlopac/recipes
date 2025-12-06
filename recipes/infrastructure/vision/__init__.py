import os
from crewai import LLM
from crewai.tools import BaseTool

from recipes.application.config import settings

from . import tools


def get_model() -> LLM:
    if settings.USE_LOCAL_MODELS:
        os.environ["OPENAI_API_KEY"] = "NA"
        return LLM(
            temperature=settings.VISION_TEMPERATURE,
            model=settings.VISION_LOCAL_MODEL,
            base_url=settings.VISION_LOCAL_URL,
            api_key="NA",
        )
    else:
        return LLM(
            temperature=settings.VISION_TEMPERATURE,
            model=settings.VISION_GEMINI_MODEL,
            api_key=settings.GEMINI_API_KEY,
        )


def get_tool() -> BaseTool:
    if settings.USE_LOCAL_MODELS:
        return tools.LocalVisionTool()
    else:
        return tools.Gemini3VisionTool()
