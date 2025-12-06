from pathlib import Path
from typing import Annotated

import google.generativeai as genai
import PIL.Image
from crewai.tools import BaseTool
from pydantic import BaseModel, Field

from recipes.application.config import settings


class VisionToolInput(BaseModel):
    image_path: Annotated[str, Field(description="Absolute path to the image file.")]
    query: Annotated[str, Field(description="What to look for in the image.")]


class Gemini3VisionTool(BaseTool):
    name: str = "Gemini 3 Vision"
    description: str = "Analyzes images using the latest Gemini 3 model."
    args_schema: type[BaseModel] = VisionToolInput

    def _run(self, image_path: Path | str, query: str) -> str:
        image_path = Path(image_path)
        if not image_path.exists():
            return "Error: File not found."
        img = PIL.Image.open(image_path)
        genai.configure(api_key=settings.GEMINI_API_KEY)
        model = genai.GenerativeModel(settings.VISION_MODEL)
        try:
            response = model.generate_content([query, img])
        except Exception as e:  # noqa: BLE001
            return f"Vision Error: {e}"
        else:
            return response.text
